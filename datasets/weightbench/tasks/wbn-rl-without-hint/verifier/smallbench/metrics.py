"""Raw prediction scorer independent of Torch and Transformers."""
import math
from .spec import COUNTS

def score(task, rows, expected_ids):
    if task not in COUNTS or len(rows)!=COUNTS[task] or len(expected_ids)!=COUNTS[task]:
        raise ValueError('incorrect validation denominator')
    ids=[r['idx'] for r in rows]
    if ids!=expected_ids or len(set(ids))!=len(ids):raise ValueError('inventory mismatch')
    if any(type(r[k]) is not int or r[k] not in (0,1) for r in rows for k in ('label','prediction')):
        raise ValueError('invalid binary label/prediction')
    tp=sum(r['label']==r['prediction']==1 for r in rows)
    tn=sum(r['label']==r['prediction']==0 for r in rows)
    fp=sum(r['label']==0 and r['prediction']==1 for r in rows)
    fn=len(rows)-tp-tn-fp
    out={'n':len(rows),'tp':tp,'tn':tn,'fp':fp,'fn':fn}
    if task in ('sst2','mrpc'):out['accuracy']=(tp+tn)/len(rows)
    if task=='mrpc':out['f1']=2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0.
    if task=='cola':
        den=math.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))
        out['matthews_correlation']=(tp*tn-fp*fn)/den if den else 0.
    return out
