separator = "_"

states = [
    '1',
    '2',
    '3',
    '4'
]

alphabet = [
    'a',
    'b'
]

transitions = {
    #Откуда, по какому символу, куда
    '1' : {
        'a': ['1', '2'],
        'b': ['1'],
    },
    '2' : {
        'a': ['3'],
        'b': ['3'],
    },
    '3': {
        'a': ['4'],
        'b': ['4']
    }
}

# transitions = {
#     #Откуда, по какому символу, куда
#     '1' : {
#         'a': ['1', '2'],
#         'b': ['3'],
#     },
#     '2' : {
#         'a': ['2'],
#         'b': ['1', '3'],
#     },
#     '3': {
#         'a': ['3'],
#         'b': ['3']
#     }
# }

def combineArrays(a1: list, a2: list):
    return list(sorted(set([*a1, *a2])))

def combineDicts(d1: dict, d2: dict, d3: dict):
    for key in d1.keys():
        if key in d2.keys():
            d3[key] = combineArrays(d1[key], d2[key])
        else:
            d3[key] = d1[key]

    for key in d2.keys():
        if key not in d3.keys():
            if key in d1.keys():
                d3[key] = combineArrays(d1[key], d2[key])
            else:
                d3[key] = d2[key]

initial_state = [
    '1'
]

final_states = [
    '4'
]

# final_states = [
#     '3'
# ]

def determine():

    queue = ['1']
    i = 0
    while i < len(queue):
        state = queue[i]
        for symbol in alphabet:
            local_transitions = transitions.get(state, None)
            if local_transitions is None:
                new_transitions = {}
                for s in state.split(separator):
                    if transitions.get(s) is not None:
                        combineDicts(new_transitions, transitions[s], new_transitions)
                transitions[state] = new_transitions

            #if len(transitions[state][symbol]) > 1:
            new_state = separator.join(transitions[state][symbol])
            if new_state not in queue:
                queue.append(new_state)
        i += 1

    for state in transitions.keys():
        for symbol in transitions[state]:
            transitions[state][symbol] = separator.join(transitions[state][symbol])

    for state in states:
        if state not in queue:
            if transitions.get(state, None) is not None:
                transitions.pop(state)

def included(combined_state: str):
    for s in combined_state.split(separator):
        if s in final_states:
            return True
    return False

def printStateMachine():
    print(f"States: [{', '.join(transitions.keys())}]")
    print(f"Alphabet: [{', '.join(alphabet)}]")
    print(f"Transitions:")
    for state in transitions.keys():
        for symbol in transitions[state]:
            print(f"{state} ({symbol}) -> {transitions[state][symbol]}")
    print(f"InitialState: {initial_state[0]}")
    print(f"FinalStates: {', '.join([i for i in transitions.keys() if included(i)])}")

if __name__ == "__main__":
    determine()
    from pprint import pprint
    pprint(transitions)
    printStateMachine()
