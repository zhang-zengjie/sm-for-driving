import json
from tulip import transys, spec, synth

def act2out(action):

    for key, value in action.items():
        if value:
            return key


if __name__ == '__main__':

    sys_c = transys.FTS()
    sys_c.states.add_from(['X0', 'X1', 'X2'])
    sys_c.states.initial.add('X0')

    sys_c.transitions.add_comb({'X0'}, {'X0', 'X1'})
    sys_c.transitions.add_comb({'X1'}, {'X0', 'X1', 'X2'})
    sys_c.transitions.add_comb({'X2'}, {'X0', 'X1', 'X2'})

    sys_c.atomic_propositions.add_from({'STOP', 'MOVE', 'DECEL'})
    sys_c.states.add('X0', ap={'STOP'})
    sys_c.states.add('X1', ap={'MOVE'})
    sys_c.states.add('X2', ap={'DECEL'})

    env_vars = {'URGENT', 'WARNING'}
    
    env_init = set()
    env_prog = {'!URGENT'}
    env_prog |= {'!WARNING'}
    env_safe = set()

    sys_vars = set()
    sys_init = set()
    
    sys_prog = {'MOVE'}

    sys_safe = {'(URGENT && !WARNING) -> X(STOP)'}
    sys_safe |= {'(WARNING && !URGENT && (MOVE || DECEL)) -> X(DECEL)'}
    sys_safe |= {'(!URGENT && !WARNING) -> X(MOVE)'}

    specs = spec.GRSpec(env_vars, sys_vars, env_init, sys_init,
                        env_safe, sys_safe, env_prog, sys_prog)

    specs.moore = True
    specs.qinit = r'\E \A'
    ctrl = synth.synthesize(specs, sys=sys_c)

    assert ctrl is not None, 'The controller is unrealizable!'

    nodes = ctrl.nodes(data=False)

    states = [node for node in nodes]

    transition_table = {}
    output_table = {}

    for state in states:

        target_dict = {}

        for source, target, attribute in ctrl.edges(nbunch=state, data=True):
            
            env_act = {'WARNING': attribute['WARNING'], 'URGENT': attribute['URGENT']}

            if env_act['WARNING'] & env_act['URGENT']:
                action = 'X'
            elif env_act['WARNING'] & (not env_act['URGENT']):
                action = 'W'
            elif (not env_act['WARNING']) & env_act['URGENT']:
                action = 'U'
            else:
                action = 'O'

            target_dict[action] = target

            sys_act = {'MOVE': attribute['MOVE'], 'DECEL': attribute['DECEL'], 'STOP': attribute['STOP']}
            output_table[target] = act2out(sys_act)
        output_table['Sinit'] = 'STOP'

        transition_table[state] = target_dict

    file_path = 'sm_tables.json'

    with open(file_path, 'w') as file:
        json.dump({'transition': transition_table, 'output': output_table, 'states': states}, file, indent=4)
