import os
from nfa import NFA
from dfa import DFA


def to_dot(states, start_state, accept_states, transitions):
    lines = []
    lines.append("digraph finite_state_machine {")
    lines.append("    rankdir=LR;")
    lines.append('    size="10,10";')

    # Accept states
    if accept_states:
        lines.append("    node [shape = doublecircle]; " + " ".join(accept_states) + ";")

    # Normal states
    lines.append("    node [shape = circle];")

    # Transitions
    for src, dst, label in transitions:
        lines.append(f'    {src} -> {dst} [ label = "{label}" ];')

    lines.append("}")
    return "\n".join(lines)

def dfa_to_graph(dfa:DFA, fname:str):
    
    states = {f"q{i}" if i != dfa.start_state else "s" for i in dfa.states }
    start_state = f"s"
    accept_states = {f"q{i}" if i!= dfa.start_state else "s" for i in dfa.acc_states}
    transitions = []
    for src, mapping in dfa.transitions.items():
        for symbol, dst in mapping.items():
            q_src = f"q{src}" if src != dfa.start_state else "s"
            q_dst = f"q{dst}" if dst != dfa.start_state else "s"
            transitions.append((q_src, q_dst, symbol))

    dot_text = to_dot(states, start_state, accept_states, transitions)
    
    # Create dot filename from png filename
    dot_fname = fname.replace(".png", ".dot")
    with open(dot_fname, "w") as f:
        f.write(dot_text)

    os.system(f"dot -Tpng {dot_fname} -o {fname}")
    print(f"Graph saved to {fname}")
    os.remove(dot_fname)

def nfa_to_graph(nfa:NFA, fname:str):

    states = {f"q{i}" if i != nfa.start_state else "s" for i in nfa.states }
    start_state = "s"
    accept_states = {f"q{i}" if i!= nfa.start_state else "s"  for i in nfa.acc_states}
    transitions = []
    for src, mapping in nfa.transitions.items():
        for symbol, dsts in mapping.items():
            for dst in dsts:
                q_src = f"q{src}" if src != nfa.start_state else "s"
                q_dst = f"q{dst}" if dst != nfa.start_state else "s"
        transitions.append((q_src, q_dst, symbol))
    eps_transitions = []
    for src, dsts in nfa.eps_transitions.items():
        for dst in dsts:
            q_src = f"q{src}" if src != nfa.start_state else "s"
            q_dst = f"q{dst}" if dst != nfa.start_state else "s"
            eps_transitions.append((q_src, q_dst, "ε"))

    dot_text = to_dot(states, start_state, accept_states, transitions + eps_transitions)
  
    # Create dot filename from png filename
    dot_fname = fname.replace(".png", ".dot")
    with open(dot_fname, "w") as f:
        f.write(dot_text)

    os.system(f"dot -Tpng {dot_fname} -o {fname}")
    print(f"Graph saved to {fname}")

    os.remove(dot_fname)