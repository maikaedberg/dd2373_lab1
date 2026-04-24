from nfa import NFA
from typing import Dict, List, Set

State = int
Symbol = str

Transition = Dict[State, Dict[Symbol, State]]

class DFA:
    def __init__(
        self,
        alphabet: list[Symbol],
        states: Set[State],
        trans: Transition,
        start_state: State,
        acc_states: Set[State]
    ) -> None:
        self.alphabet : list[Symbol] = alphabet
        self.states : Set[State] = states
        self.transitions : Transition = trans
        self.start_state : State = start_state
        self.acc_states : Set[State] = acc_states

    def is_accepting_state(self, q:State):
        return q in self.acc_states
    
    def is_dfa(self):
        # sanity check if every arrow points to one states
        for q in self.states:
            assert q in self.transitions
            for a in self.alphabet:
                assert a in self.transitions[q]
    
    def minimize(self):
        # creates pair of all states, mark distinguishable or indistinguishable
        distinguishable = {
            (q1, q2) : False 
            for q1 in self.states
            for q2 in self.states
            if q1 > q2
        }

        for (q1, q2) in distinguishable.keys():
            if self.is_accepting_state(q1) != self.is_accepting_state(q2):
                distinguishable[(q1,q2)] = True

        while True:
            new_markings = False
            for ((q1, q2), mark) in distinguishable.items():
                if mark:
                    continue
                for a in self.alphabet:
                    dst1 = self.transitions[q1][a]
                    dst2 =  self.transitions[q2][a]
                    # if dst1 and dst2 are equal, they are indistinguishable
                    if dst1 == dst2:
                        continue

                    if distinguishable[(max(dst1, dst2), min(dst1,dst2))]:
                        distinguishable[(q1, q2)] = True
                        new_markings = True
            if not new_markings:
                break

        for ((q1, q2), mark) in distinguishable.items():
            if not mark:
                self.collapse(q1, q2)

    def collapse(self, q1:State, q2:State):
        # collapses two states, q1 and q2 together
        # replaces all mentions of q2 with q1

        if q2 in self.states:
            self.states.remove(q2)

        collapsed_transition: Transition = dict()
        for src, mapping in self.transitions.items():
            if src == q2: src = q1
            collapsed_transition[src] = dict()
            for symbol, dst in mapping.items():
                if dst == q2: dst = q1
                collapsed_transition[src][symbol] = dst
        self.transitions = collapsed_transition

        if self.start_state == q2:
            self.start_state = q1
        if q2 in self.acc_states:
            self.acc_states.remove(q2)
    
    def complete_match(self, input_str:str) -> bool:
        q = self.start_state
        for s in input_str:
            q = self.transitions[q][s]
        if q in self.acc_states:
            return True
        return False
    
    def partial_match(self, input_str:str) -> bool:
        q = self.start_state
        if q in self.acc_states:
            return True
        for s in input_str:
            q = self.transitions[q][s]
            if q in self.acc_states:
                return True
        return False

def nfa_to_dfa(nfa:NFA) -> DFA:
    
    start_states = nfa.get_eps_closure({nfa.start_state}) # df
    subsets_formed = [start_states]

    queue = [start_states]
    transitions: Transition = dict()

    while queue:
        srcs = queue.pop()
        for a in nfa.alphabet:
            dsts = nfa.reached_by_a(srcs, a)
            if dsts not in subsets_formed:
                subsets_formed.append(dsts)
                queue.append(dsts)

            srcs_q = get_subset_index(srcs, subsets_formed)
            dsts_q = get_subset_index(dsts, subsets_formed)
            if srcs_q not in transitions:
                transitions[srcs_q] = dict()
            if a in transitions[srcs_q]:
                assert transitions[srcs_q][a] == dsts_q
            else:
                transitions[srcs_q][a] = dsts_q

    nfa_start_state = get_subset_index(start_states, subsets_formed)
    dfa_acc_states = get_dfa_accepting_states(nfa, subsets_formed)
    dfa = DFA(
        nfa.alphabet,
        {i for i in range(len(subsets_formed))},
        transitions,
        nfa_start_state,
        dfa_acc_states
    )

    return dfa

def get_subset_index(subset:Set, subsets_formed:List[Set[State]]):
    return subsets_formed.index(subset)

def get_dfa_accepting_states(nfa:NFA, subsets_formed:List[Set[State]]):
    dfa_acc_states = set()
    for (i, subset) in enumerate(subsets_formed):
        subset_acc = False
        for nfa_acc_state in nfa.acc_states:
            if nfa_acc_state in subset:
                subset_acc = True
                break
        if subset_acc:
            dfa_acc_states.add(i)
    return dfa_acc_states
