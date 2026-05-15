"""LLM-as-judge verifier for Harvey LAB tasks.

Reads the rubric (criteria) from rubric.json, collects agent
deliverables from the output directory, and grades each criterion
using an LLM judge. Writes the aggregate reward (0.0-1.0) to the
reward file.
"""

import argparse
import json
import os
import re
import string
import subprocess
import sys
import time
from pathlib import Path

import pdfplumber
from openpyxl import load_workbook


# ── File reading ──────────────────────────────────────────────────

def read_file_as_text(path: Path) -> str:
    """Read a file and return its content as plain text."""
    suffix = path.suffix.lower()
    try:
        if suffix == ".docx":
            result = subprocess.run(
                ["pandoc", str(path), "-t", "markdown",
                 "--wrap=none", "--track-changes=accept"],
                capture_output=True, text=True, timeout=30,
            )
            if result.returncode != 0:
                return f"(pandoc error: {result.stderr[:200]})"
            return result.stdout
        if suffix == ".xlsx":
            wb = load_workbook(str(path), data_only=True)
            parts = []
            for sheet_name in wb.sheetnames:
                ws = wb[sheet_name]
                parts.append(f"=== Sheet: {sheet_name} ===")
                for row in ws.iter_rows(values_only=True):
                    parts.append("\t".join(
                        str(c) if c is not None else "" for c in row
                    ))
            return "\n".join(parts)
        if suffix == ".pptx":
            from markitdown import MarkItDown
            md = MarkItDown()
            result = md.convert(str(path))
            return result.text_content
        if suffix == ".pdf":
            parts = []
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        parts.append(text)
            return "\n".join(parts)
        return path.read_text(encoding="utf-8")
    except Exception as e:
        return f"(error reading {path.name}: {e})"


# ── Judge ─────────────────────────────────────────────────────────

VERDICT_PROMPT = string.Template("""You are evaluating a legal AI agent's work product against a specific quality criterion.

## Task
$task_description

## Agent's Output
$agent_output

## Criterion
**$criterion_title**

$match_criteria

## Instructions
Evaluate the agent's output against the criterion above.
- **PASS**: The agent's output satisfies the criterion as described
- **FAIL**: The agent's output does not satisfy the criterion as described

Respond with JSON only:

```json
{
  "verdict": "pass" or "fail",
  "reasoning": "Brief explanation"
}
```
""")


def call_judge(prompt: str, retries: int = 3) -> str:
    """Call Anthropic Claude API and return the text response."""
    import anthropic

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")

    client = anthropic.Anthropic(api_key=api_key)

    for attempt in range(retries):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"Anthropic API failed after {retries} attempts: {e}")


def parse_verdict(text: str) -> dict:
    """Extract JSON verdict from LLM response."""
    # Try code fences first
    match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass
    # Try balanced braces
    for i, ch in enumerate(text):
        if ch == "{":
            depth = 0
            for j in range(i, len(text)):
                if text[j] == "{":
                    depth += 1
                elif text[j] == "}":
                    depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[i:j + 1])
                    except json.JSONDecodeError:
                        break
    raise ValueError(f"Could not parse verdict from: {text[:300]}")


def judge_criterion(
    criterion: dict,
    task_title: str,
    deliverable_texts: dict[str, str],
) -> dict:
    """Grade a single criterion against deliverable content."""
    # Build the agent output context from relevant deliverables
    criterion_deliverables = criterion.get("deliverables", [])
    if criterion_deliverables:
        def _stem(name: str) -> str:
            return Path(name).stem.lower()

        expected_stems = {_stem(d) for d in criterion_deliverables}
        relevant = {k: v for k, v in deliverable_texts.items()
                    if _stem(k) in expected_stems
                    or any(d.lower() in k.lower() for d in criterion_deliverables)}
    else:
        relevant = deliverable_texts

    if not relevant:
        return {
            "id": criterion["id"],
            "title": criterion["title"],
            "verdict": "fail",
            "reasoning": "No matching deliverable files found.",
        }

    agent_output = "\n\n".join(
        f"--- {name} ---\n{content[:15000]}"
        for name, content in relevant.items()
    )

    try:
        prompt = VERDICT_PROMPT.safe_substitute(
            task_description=task_title,
            agent_output=agent_output,
            criterion_title=criterion["title"],
            match_criteria=criterion["match_criteria"],
        )
        response_text = call_judge(prompt)
        verdict = parse_verdict(response_text)
        return {
            "id": criterion["id"],
            "title": criterion["title"],
            "verdict": verdict.get("verdict", "fail"),
            "reasoning": verdict.get("reasoning", ""),
        }
    except Exception as e:
        return {
            "id": criterion["id"],
            "title": criterion["title"],
            "verdict": "fail",
            "reasoning": f"Judge error: {e}",
        }


# ── Main ──────────────────────────────────────────────────────────

def find_deliverables(output_dir: Path) -> dict[str, str]:
    """Find and read all deliverable files in the output directory."""
    texts = {}
    for f in sorted(output_dir.iterdir()):
        if f.is_file() and f.name != "rubric.json" and not f.name.startswith("."):
            if f.stat().st_size > 50_000_000:  # skip files > 50 MB
                continue
            if f.suffix.lower() in (".docx", ".xlsx", ".pptx", ".pdf",
                                     ".md", ".txt", ".json", ".csv"):
                texts[f.name] = read_file_as_text(f)
    return texts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rubric", required=True, help="Path to rubric.json")
    parser.add_argument("--output-dir", required=True, help="Agent output directory")
    parser.add_argument("--reward-file", required=True, help="Path to write reward")
    args = parser.parse_args()

    rubric_path = Path(args.rubric)
    output_dir = Path(args.output_dir)
    reward_file = Path(args.reward_file)

    rubric = json.loads(rubric_path.read_text())
    task_title = rubric.get("title", "Legal task")
    criteria = rubric.get("criteria", [])

    if not criteria:
        reward_file.write_text("0")
        return

    deliverable_texts = find_deliverables(output_dir)

    if not deliverable_texts:
        print("No deliverable files found in output directory.")
        reward_file.write_text("0")
        return

    print(f"Found {len(deliverable_texts)} deliverable(s): "
          f"{list(deliverable_texts.keys())}")
    print(f"Evaluating {len(criteria)} criteria...")

    results = []
    for i, criterion in enumerate(criteria):
        print(f"  [{i+1}/{len(criteria)}] {criterion['id']}: "
              f"{criterion['title'][:60]}...")
        result = judge_criterion(criterion, task_title, deliverable_texts)
        results.append(result)
        status = "PASS" if result["verdict"] == "pass" else "FAIL"
        print(f"    -> {status}: {result['reasoning'][:80]}")

    n_passed = sum(1 for r in results if r["verdict"] == "pass")
    n_total = len(results)
    reward = n_passed / n_total if n_total > 0 else 0.0

    print(f"\nScore: {n_passed}/{n_total} ({reward:.1%})")

    reward_file.parent.mkdir(parents=True, exist_ok=True)
    reward_file.write_text(str(reward))

    # Write detailed results alongside reward
    details_path = reward_file.parent / "evaluation_details.json"
    details_path.write_text(json.dumps({
        "score": reward,
        "n_passed": n_passed,
        "n_total": n_total,
        "results": results,
    }, indent=2))


if __name__ == "__main__":
    main()

