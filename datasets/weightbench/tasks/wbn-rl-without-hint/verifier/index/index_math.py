"""Pure arithmetic for a prospectively fixed bounded benchmark index."""
import math
from fractions import Fraction

def normalized(value, metric):
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError('invalid estimate')
    b, a = metric['baseline'], metric['anchor']
    if b == a:
        raise ValueError('degenerate anchor')
    return max(0.0, min(1.0, (value-b)/(a-b)))

def aggregate(spec, allocated):
    """allocated[target] is a nonempty fixed-length list of metric->estimate dicts.

    Empty dict means allocated missing outcome. Caller validates provenance/validity
    before populating verified estimates. No caller may drop failed/missing draws.
    """
    if set(allocated) != set(spec['target_weights_fraction']):
        raise ValueError('all target allocations required')
    lo = hi = coverage = 0.0
    for target, tw in spec['target_weights_fraction'].items():
        rows = allocated[target]
        if not rows:
            raise ValueError('nonempty fixed allocation required')
        target_metrics = [m for m in spec['metrics'] if m['target']==target]
        if sum((Fraction(*m['within_target_weight_fraction']) for m in target_metrics), Fraction(0)) != 1:
            raise ValueError('within-target weights must sum to one')
        allowed = {m['id'] for m in target_metrics}
        for row in rows:
            if set(row)-allowed:
                raise ValueError('unknown or diagnostic metric in primary index')
            for m in target_metrics:
                weight = float(Fraction(*tw)*Fraction(*m['within_target_weight_fraction'])) / len(rows)
                value = normalized(row.get(m['id']), m)
                if value is None:
                    hi += weight
                else:
                    lo += weight*value
                    hi += weight*value
                    coverage += weight
    if sum((Fraction(*v) for v in spec['target_weights_fraction'].values()), Fraction(0)) != 1:
        raise ValueError('target weights must sum to one')
    return {'lower':100*lo,'upper':100*hi,'verified_weight_fraction':coverage,
            'complete':math.isclose(coverage,1.0,abs_tol=1e-12),'bounds_type':'logical, not CI'}

def gain(without, with_hint):
    return {'lower':with_hint['lower']-without['upper'],
            'upper':with_hint['upper']-without['lower'],
            'complete':without['complete'] and with_hint['complete'],
            'unit':'index points','bounds_type':'logical, not CI'}
