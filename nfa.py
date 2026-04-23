from typing import Dict, List, Set, Tuple
import copy 
from itertools import count

from parser import (RegExp, Dot, Literal, Closure, OneOrMore, ZeroOrOne, Concatenation, Union)

State = int
Symbol = str

# Transition: state -> (symbol -> set of states)
Transition = Dict[State, Dict[Symbol, Set[State]]]
EpsilonTransition = Dict[State, Set[State]]

class NFA:
    def __init__(
        self,
        alphabet: list[Symbol],
        states: Set[State],
        trans: Transition,
        epstrans: EpsilonTransition,
        start_state: State,
        acc_states: Set[State]
    ) -> None:
        self.alphabet = alphabet
        self.states = states
        self.transitions = trans
        self.eps_transitions = epstrans
        self.start_state = start_state
        self.acc_states = acc_states

    def get_transition(self, q:State, a:Symbol) -> Set:
        dst = self.transitions.get(q, dict()).get(a, set())
        return dst

    def get_eps_transitions(self, q:State) -> Set:
        return self.eps_transitions.get(q, set())
    
    def get_eps_closure_state(self, state:State):
        
        stack = [state]
        closure = {state}

        while stack:
            q = stack.pop()
            for q_eps in self.get_eps_transitions(q):
                if q_eps not in closure:
                    closure.add(q_eps)
                    stack.append(q_eps)

        return closure

    def get_eps_closure(self, states:Set[State]):
        closure = set()
        for q in states:
            closure |= self.get_eps_closure_state(q)
        return closure

    def reached_by_a_symbol(self, srcs:Set[State], a:Symbol):
        # sets reached from moving from state with a
        dsts = set()
        for src in srcs:
            dsts |= self.get_transition(src, a)
        return dsts

    def reached_by_a(self, srcs:Set[State], a:Symbol):
        dsts = self.reached_by_a_symbol(srcs, a)
        dsts = self.get_eps_closure(dsts)
        return dsts
        


def regex_to_nfa(expr:RegExp, alphabet:List[Symbol]) -> NFA:

    counter = count()
    next_s = lambda: next(counter)

    def build(expr:RegExp) -> NFA:

        if isinstance(expr, Literal):
            s0, s1 = next_s(), next_s()
            return NFA(alphabet, {s0,s1}, {s0 : {expr.char : {s1}}}, dict(), s0, {s1})
        
        elif isinstance(expr, Dot):
            s0, s1 = next_s(), next_s()
            return NFA(alphabet, {s0,s1}, {s0 : {a: {s1} for a in alphabet }}, {}, s0, {s1})

        elif isinstance(expr, Union):
            nfa_left, nfa_right = build(expr.left), build(expr.right)

            s0, s1 = next_s(), next_s()

            new_eps_trans = {}
            new_eps_trans[s0] =  {nfa_left.start_state, nfa_right.start_state}
            for s in nfa_left.acc_states | nfa_right.acc_states:
                new_eps_trans[s] = {s1}

            states, trans, eps = merge([nfa_left, nfa_right], new_eps_trans)

            return NFA(alphabet, states | {s0, s1}, trans, eps, s0, {s1})
        
        elif isinstance(expr, Concatenation):
            nfa_left, nfa_right = build(expr.left), build(expr.right)

            new_eps_trans : EpsilonTransition = {}

            for s in nfa_left.acc_states:
                new_eps_trans[s] = {nfa_right.start_state}

            states, trans, eps = merge([nfa_left, nfa_right], new_eps_trans)

            return NFA(alphabet, states, trans, eps, nfa_left.start_state, nfa_right.acc_states)
        
        elif isinstance(expr, Closure):
            # create two new states and add epsilon transitions
            # s0 to start of expr_nfa and s1
            # each accepting of expr_nfa to start of expr_nfa and s1
            expr_nfa = build(expr.expr)
            s0, s1 = next_s(), next_s()

            new_eps_trans: EpsilonTransition = dict()
            new_eps_trans[s0] = {expr_nfa.start_state, s1}
            for s in expr_nfa.acc_states:
                new_eps_trans[s] = {expr_nfa.start_state, s1}
            eps = merge_eps_transition(new_eps_trans, expr_nfa.eps_transitions)
            trans = expr_nfa.transitions.copy()

            return NFA(alphabet, expr_nfa.states | {s0, s1}, trans, eps, s0, {s1})

        elif isinstance(expr, OneOrMore):
            # create two new states and add epsilon transitions
            # s0 to start of expr_nfa
            # each accepting of expr_nfa to start of expr_nfa and s1

            expr_nfa = build(expr.expr)
            s0, s1 = next_s(), next_s()

            new_eps_trans : EpsilonTransition = {}
            new_eps_trans[s0] = {expr_nfa.start_state}
            for s in expr_nfa.acc_states:
                new_eps_trans[s] = {expr_nfa.start_state, s1}

            trans = expr_nfa.transitions.copy()
            eps = merge_eps_transition(new_eps_trans, expr_nfa.eps_transitions)

            return NFA(alphabet, expr_nfa.states | {s0, s1}, trans, eps, s0, {s1})
    
        elif isinstance(expr, ZeroOrOne):
            # create two new states and add epsilon transitions
            # s0 to start of expr_nfa and s1
            # each accepting of expr_nfa to s1

            expr_nfa = build(expr.expr)
            s0, s1 = next_s(), next_s()

            new_eps_trans : EpsilonTransition = {}
            new_eps_trans[s0] = {expr_nfa.start_state, s1}
            for s in expr_nfa.acc_states:
                new_eps_trans[s] = {s1}

            trans = expr_nfa.transitions.copy()
            eps = merge_eps_transition(new_eps_trans, expr_nfa.eps_transitions)

            return NFA(alphabet, expr_nfa.states | {s0, s1}, trans, eps, s0, {s1})  
    
    return build(expr)

def merge(nfas: List[NFA], extra_eps: EpsilonTransition) -> Tuple[Set[State], Transition, EpsilonTransition]:
    new_states = set()
    new_trans = dict()
    new_eps = extra_eps.copy()
    
    for nfa in nfas:
        new_states |= nfa.states
        new_trans = merge_transition(new_trans, nfa.transitions)
        new_eps = merge_eps_transition(new_eps, nfa.eps_transitions)

    return new_states, new_trans, new_eps
        
def merge_transition(t1: Transition, t2: Transition) -> Transition:
    combined = copy.deepcopy(t1)

    for src, mapping in t2.items():
        if src not in combined:
            combined[src] = {}

        for symbol, dsts in mapping.items():
            if symbol not in combined[src]:
                combined[src][symbol] = set()

            combined[src][symbol] |= dsts 

    return combined

def merge_eps_transition(t1: EpsilonTransition, t2:EpsilonTransition) -> EpsilonTransition:
    new_eps = t1.copy() 
    for src, dsts in t2.items():
        if src not in new_eps:
            new_eps[src] = set()
        new_eps[src] |= dsts
    return new_eps