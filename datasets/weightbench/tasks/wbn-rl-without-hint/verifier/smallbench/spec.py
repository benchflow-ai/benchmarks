"""Pre-subject task definition. No examples, seeds or control coefficients."""
BERT_REV = '30b0a37ccaaa32f332884b96992754e246e48c5f'
GLUE_REV = 'bcdcba79d07bc864c1c254ccfcedcce55bcc9a8c'
GYM_REV = 'a923da5d4415a1aa5195d99341069da5e16deed7'
ENVS = {'CartPole-v1': (4, 2, 500), 'Acrobot-v1': (6, 3, 500), 'Pendulum-v1': (3, 1, 200)}
COUNTS = {'sst2': 872, 'mrpc': 408, 'cola': 1043}
COMMON = '''You are an LLM WRITER, distinct from the network you are writing. Track K: use your own knowledge only. All learned tensors start at zero. Construct numerical parameters; no training, optimizer, fitting, search, simulation, rollouts, forward calls, pretrained weights, corpora, examples, lookup bypass, executable scoring hooks or evaluation feedback. No post-construction training. Only tensor checkpoint artifacts are scored. You have no native tools. Return strict JSON {"action":"code" or "submit", "design":string, "code":string}; submit code must be empty. Code runs in a restricted CPU/no-network constructor. Inspect the supplied schema and tokenizer only. Use numpy as np, weights dict of float32 arrays, schema dict, and save_tensor(name,array). Imports, private attributes, arbitrary file access and model execution are forbidden. Tensor construction may use loops and numerical arithmetic. The full method is audited before scores are valid. Intermediate feedback is limited to construction errors and tensor schema. Submission seals the exact tensor inventory; no replacements or score-based adaptations.'''
BERT_TEXT = '''Google bert_uncased_L-2_H-128_A-2: 2 encoder layers, hidden128, intermediate512, 2 attention heads, GELU, vocabulary30522, positions512, type vocabulary2, LayerNorm epsilon1e-12. One shared encoder, learned pooler dense128+tanh applied to final CLS (position0), and three independent linear 128->2 heads (bias included). Full GLUE validation subsets only: SST-2 sentiment (0 negative,1 positive), MRPC sentence-pair paraphrase (0 not equivalent,1 equivalent), CoLA linguistic acceptability (0 unacceptable,1 acceptable). Metrics: SST-2 accuracy; MRPC accuracy and binary F1 positive1 (zero denominator=0); CoLA Matthews correlation (zero denominator=0). No full GLUE score. Google uncased WordPiece tokenizer: lowercase/basic tokenize, add CLS and SEP, MRPC [CLS]A[SEP]B[SEP] with segment0/1; single sentence segment0. Right padding to128, longest-first truncation including special tokens; pad id0, attention mask excludes pad. Float32 CPU evaluation, model.eval() dropout disabled. Lowest-index argmax resolves ties. Every embedding, encoder, LayerNorm gamma/beta, pooler and head starts zero. No learned tensor is loaded from Google. 90min/150 code actions, at most120s each.'''
RL_TEXT = '''Classic-control Gymnasium1.2.2, default TimeLimit(OrderEnforcing(PassiveEnvChecker(env))) wrappers. Each independent policy is Linear(input,64)->tanh->Linear(64,64)->tanh->Linear(64,output), biases in every layer. Float32 CPU evaluation, raw observations, no normalization/scaling. Discrete actions use lowest-index argmax; Pendulum action float32 clip(2*tanh(logit),-2,2). All weights/biases initially zero. CartPole-v1 obs=(x,x_velocity,theta,theta_velocity), actions0 push left/1 right with force10, dt0.02, gravity9.8, cart mass1/pole mass0.1/half-length0.5; Euler dynamics. Reward+1 including terminal step; termination x outside+-2.4 or theta outside+-12degrees; truncation500 steps. Acrobot-v1 obs=(cos(theta1),sin(theta1),cos(theta2),sin(theta2),velocity1,velocity2), torque actions=(-1,0,+1), dt0.2 RK4, gravity9.8, unit link masses/lengths/inertias, centers0.5; default book dynamics. Velocities clip+-4pi/+-9pi, angles wrap+-pi. Reward-1 per nonterminal step,0 on terminal; terminal when -cos(theta1)-cos(theta1+theta2)>1; truncation500. Pendulum-v1 obs=(cos(theta),sin(theta),theta_velocity), torque[-2,2], dt0.05, gravity10,mass1,length1,max speed8. Acceleration3*g/(2*l)*sin(theta)+3*u/(m*l*l), update clipped velocity then angle. Reward negative(wrapped theta squared+0.1*velocity squared+0.001*torque squared) at pre-transition state. No natural termination; truncation200. Seeds and trajectories private. Report each return distribution separately; no grand score or Atari/MuJoCo claim. Shared budget for all THREE policies45min/100 code actions,120s each.'''

def rl_schema():
    out = {}
    for env, (n, a, _) in ENVS.items():
        for layer, shape in enumerate(((64,n),(64,64),(a,64))):
            out[f'{env}.{layer}.weight'] = list(shape)
            out[f'{env}.{layer}.bias'] = [shape[0]]
    return out

def bert_schema():
    out = {'embeddings.word_embeddings.weight':[30522,128],
           'embeddings.position_embeddings.weight':[512,128],
           'embeddings.token_type_embeddings.weight':[2,128],
           'embeddings.LayerNorm.weight':[128], 'embeddings.LayerNorm.bias':[128],
           'pooler.dense.weight':[128,128], 'pooler.dense.bias':[128]}
    for i in range(2):
        p=f'encoder.layer.{i}.'
        for q in ('query','key','value'):
            out[p+'attention.self.'+q+'.weight']=[128,128]
            out[p+'attention.self.'+q+'.bias']=[128]
        for q,shape in [('attention.output.dense',[128,128]),('intermediate.dense',[512,128]),('output.dense',[128,512])]:
            out[p+q+'.weight']=shape; out[p+q+'.bias']=[shape[0]]
        for q in ('attention.output.LayerNorm','output.LayerNorm'):
            out[p+q+'.weight']=[128]; out[p+q+'.bias']=[128]
    for task in COUNTS:
        out['heads.'+task+'.weight']=[2,128];out['heads.'+task+'.bias']=[2]
    return out
