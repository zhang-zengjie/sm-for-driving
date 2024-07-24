import json
import numpy as np
import matplotlib.pyplot as plt


def draw_temporal(IN, OUT):

    TT = np.arange(0, len(IN))
    fig, ax = plt.subplots(figsize=(5, 2))

    stop = [0.8 if x == 'STOP' else 0 for x in OUT]
    move = [0.2 if x == 'MOVE' else 0 for x in OUT]
    decel = [0.5 if x == 'DECEL' else 0 for x in OUT]

    # Plot line
    ax.plot(TT, IN, label='EMG level', linewidth=1.5, color='blue')

    # Plot bars
    ax.bar(TT, move, width=0.6, label='MOVE', color='green', alpha=0.6)
    ax.bar(TT, decel, width=0.6, label='DECEL', color='orange', alpha=0.4)
    ax.bar(TT, stop, width=0.6, label='STOP', color='red', alpha=0.9)

    ax.legend(loc='upper left', bbox_to_anchor=(0.06, 0.95), fontsize='small', ncol=2)
    ax.grid(True, linestyle='-.', linewidth=0.5)
    ax.set_yticks([0, 0.5, 1])
    ax.set_yticklabels(['', 'WRN', 'URN'])

    plt.savefig('seq.svg', bbox_inches='tight', pad_inches=0.1, transparent=True)
    plt.show()

    return None


class MooreStateMachine:
    def __init__(self):

        with open('sm_tables.json', 'r') as file:
            info = json.load(file)

        self.states = info['states']
        self.current_state = 'Sinit'

        self.transition_table = info['transition']
        self.output_table = info['output']


    def reaction(self, warning, urgent):

        if warning & urgent:
            input = 'X'
        elif warning & (not urgent):
            input = 'W'
        elif (not warning) & urgent:
            input = 'U'
        else:
            input = 'O'

        self.current_state = self.transition_table[str(self.current_state)][input]


    def get_output(self):
        return self.output_table[str(self.current_state)]

    def process_inputs(self, inputs):
        for input in inputs:
            self.transition(input)
            print("Current state:", self.current_state, "Output:", self.get_output())


# Example usage
if __name__ == "__main__":
    sm = MooreStateMachine()

    N = 50
    WRN, URG = np.zeros(N, ), np.zeros(N, )
    WRN[10:20] = 1
    URG[30:40] = 1
    OUT = []

    for n in range(N):

        # print("URGENT is " + str(URG[n]==1) + " and WARNING is " + str(WRN[n]==1) + " at time " + str(n))
        sm.reaction(WRN[n]==1, URG[n]==1)
        OUT.append(sm.get_output())

    print(OUT)
    draw_temporal(0.5 * WRN + URG, OUT)