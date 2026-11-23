"""Sealed artifact grader. Invoked in original immutable image, no network/credentials."""
import argparse,json,time
from pathlib import Path
import numpy as np
from .spec import *
from .tensors import validate,sha,write
from .metrics import score
from .policy import torch_policy,numpy_action

def episode(env,seed,action):
    obs,_=env.reset(seed=int(seed));steps=[];total=0.
    while True:
        a=action(obs);nxt,r,term,trunc,_=env.step(a)
        steps.append({'observation':obs.tolist(),'action':a.tolist() if hasattr(a,'tolist') else a,'reward':float(r),'terminated':bool(term),'truncated':bool(trunc),'next_observation':nxt.tolist()})
        total+=r;obs=nxt
        if term or trunc:break
    return {'seed':int(seed),'return':float(total),'steps':steps}

def rl(weights,private,out):
    import gymnasium as gym
    assert gym.__version__=='1.2.2'
    seeds=json.loads((private/'seeds.json').read_text());summary={};inventory={}
    for name,(n,a,limit) in ENVS.items():
        env=gym.make(name);assert env.spec.max_episode_steps==limit
        wrappers=[];e=env
        while hasattr(e,'env'):wrappers.append(type(e).__name__);e=e.env
        assert wrappers==['TimeLimit','OrderEnforcing','PassiveEnvChecker']
        assert env.observation_space.shape==(n,)
        if name=='Pendulum-v1':assert env.action_space.shape==(1,) and (env.action_space.low==-2).all() and (env.action_space.high==2).all()
        else:assert env.action_space.n==a
        inventory[name]={'wrappers':wrappers,'time_limit':limit,'observation_space':str(env.observation_space),'action_space':str(env.action_space),'default_kwargs':env.spec.kwargs}
        act=torch_policy(weights,name);returns=[];parity=[]
        with (out/(name+'.jsonl')).open('x') as log:
            for i,seed in enumerate(seeds[name]):
                row=episode(env,seed,act);returns.append(row['return']);log.write(json.dumps(row,allow_nan=False)+'\n')
                if i<3: # Predeclared bounded independent NumPy policy/environment replay.
                    other=episode(env,seed,lambda obs:numpy_action(weights,name,obs))
                    exact=other==row
                    delta=abs(row['return']-other['return'])
                    parity.append({'episode_index':i,'exact_trajectory':exact,'return_abs_difference':delta,'numpy_return':other['return']})
                    (out/(name+f'.numpy-{i}.json')).write_text(json.dumps(other,allow_nan=False))
        # Also compare both policy implementations on a frozen, non-adaptive fixture set.
        fixtures=np.random.default_rng(20261106).normal(size=(100,n)).astype(np.float32)
        gate_failed=0;gate_max_diff=0.0  # v1.3 (native-001 amendment A1, 2026-11-09): torch/NumPy fixture parity is recorded, not fatal
        for obs in fixtures:
            x,y=act(obs),numpy_action(weights,name,obs)
            if name=='Pendulum-v1':ok=bool(np.allclose(x,y,atol=2e-6,rtol=2e-6));gate_max_diff=max(gate_max_diff,float(np.max(np.abs(np.asarray(x,dtype=np.float64)-np.asarray(y,dtype=np.float64)))))
            else:ok=bool(x==y);gate_max_diff=max(gate_max_diff,0.0 if ok else 1.0)
            gate_failed+=0 if ok else 1
        rng=np.random.default_rng(1106);r=np.asarray(returns)
        boot=np.mean(r[rng.integers(0,len(r),size=(10000,len(r)))],axis=1)
        summary[name]={'n':len(r),'mean_return':float(r.mean()),'std_return':float(r.std(ddof=1)),'min':float(r.min()),'max':float(r.max()),'quantiles':np.quantile(r,[0,.25,.5,.75,1]).tolist(),'mean_bootstrap95_percentile':np.quantile(boot,[.025,.975]).tolist(),'bootstrap_replicates':10000,'numpy_replay':parity,'fixture_gate':{'fixtures':len(fixtures),'failed':gate_failed,'max_abs_diff':gate_max_diff},'success_rate':None,'success_definition':'No episode success threshold registered; report raw returns only.'}
        assert len(r)==256;env.close()
    write(out/'environment-inventory.json',inventory)
    return summary

def bert(weights,private,inputs,out):
    import torch
    from transformers import BertConfig,BertModel,BertTokenizer
    torch.set_num_threads(1)
    config=BertConfig.from_json_file(str(inputs/'config.json'));config._attn_implementation='eager'
    model=BertModel(config).eval()
    state={k:torch.from_numpy(v) for k,v in weights.items() if not k.startswith('heads.')}
    assert set(model.state_dict())==set(state)
    model.load_state_dict(state,strict=True)
    tok=BertTokenizer(vocab_file=str(inputs/'vocab.txt'),do_lower_case=True,padding_side='right',truncation_side='right')
    assert len(tok)==30522 and tok.pad_token_id==0
    inventory=json.loads((private/'inventory.json').read_text());summary={}
    for task in COUNTS:
        path=private/(task+'.json');assert sha(path)==inventory[task]['rows_sha256']
        rows=json.loads(path.read_text());pred=[]
        for start in range(0,len(rows),32):
            chunk=rows[start:start+32]
            texts=[r['sentence1'] if task=='mrpc' else r['sentence'] for r in chunk]
            pairs=[r['sentence2'] for r in chunk] if task=='mrpc' else None
            batch=tok(texts,text_pair=pairs,padding='max_length',truncation='longest_first',max_length=128,return_tensors='pt')
            with torch.inference_mode():
                pooled=model(**batch).pooler_output
                logits=pooled@torch.from_numpy(weights[f'heads.{task}.weight']).T+torch.from_numpy(weights[f'heads.{task}.bias'])
            assert torch.isfinite(logits).all()
            for row,logit in zip(chunk,logits):pred.append({'idx':row['idx'],'label':row['label'],'prediction':int(logit.argmax()),'logits':logit.tolist()})
        write(out/(task+'.predictions.json'),pred)
        summary[task]=score(task,pred,inventory[task]['ids'])
    return summary

def main():
    p=argparse.ArgumentParser();p.add_argument('--target',choices=['bert','rl'],required=True);p.add_argument('--artifact',type=Path,required=True);p.add_argument('--sha256',required=True);p.add_argument('--root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    assert sha(a.artifact)==a.sha256,'seal mismatch'
    a.out.mkdir(exist_ok=False);start=time.monotonic()
    w=validate(a.artifact,bert_schema() if a.target=='bert' else rl_schema())
    result=bert(w,a.root/'private',a.root/'inputs/bert',a.out) if a.target=='bert' else rl(w,a.root/'private',a.out)
    write(a.out/'results.json',{'target':a.target,'artifact_sha256':a.sha256,'scores':result,'seconds':time.monotonic()-start,'execution_kind':'sealed-artifact evaluation; not fresh writer execution'})
    write(a.out/'manifest.json',{p.name:sha(p) for p in a.out.iterdir() if p.is_file()})
if __name__=='__main__':main()
