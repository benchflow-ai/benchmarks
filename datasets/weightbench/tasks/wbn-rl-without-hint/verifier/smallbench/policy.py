"""Evaluator implementations. Never shipped into writer input mounts."""
import numpy as np
from .spec import ENVS

def numpy_action(w,env,obs):
    x=np.asarray(obs,dtype=np.float32)
    for i in range(3):
        x=w[f'{env}.{i}.weight'] @ x + w[f'{env}.{i}.bias']
        if i<2:x=np.tanh(x)
    return np.clip(2*np.tanh(x),-2,2).astype(np.float32) if env=='Pendulum-v1' else int(np.argmax(x))

def torch_policy(w,env):
    import torch
    n,a,_=ENVS[env]
    m=torch.nn.Sequential(torch.nn.Linear(n,64),torch.nn.Tanh(),torch.nn.Linear(64,64),torch.nn.Tanh(),torch.nn.Linear(64,a)).eval()
    with torch.no_grad():
        for i,j in enumerate((0,2,4)):
            m[j].weight.copy_(torch.from_numpy(w[f'{env}.{i}.weight']))
            m[j].bias.copy_(torch.from_numpy(w[f'{env}.{i}.bias']))
    def action(obs):
        with torch.inference_mode():x=m(torch.as_tensor(obs,dtype=torch.float32))
        return torch.clamp(2*torch.tanh(x),-2,2).numpy() if env=='Pendulum-v1' else int(torch.argmax(x))
    return action
