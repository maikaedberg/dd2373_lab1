
from parser import parse_regexp
from nfa import regex_to_nfa
from dfa import nfa_to_dfa 
from typing import List
from dfa import DFA
from graph import nfa_to_graph, dfa_to_graph

def build_minimal_dfa(regexstr:str, alphabet:List[str], graph:bool=False) -> DFA:
    regexp = parse_regexp(regexstr)
    nfa = regex_to_nfa(regexp, alphabet)
    if graph:
        nfa_to_graph(nfa, "graphs/nfa.png")
    dfa = nfa_to_dfa(nfa)
    dfa.is_dfa() # check each step is a dfa
    if graph:
        dfa_to_graph(dfa, "graphs/subset_dfa.png")
    dfa.minimize()
    dfa.is_dfa() # check each step is a dfa
    if graph:
        dfa_to_graph(dfa, "graphs/min_dfa.png")

    return dfa 


def match_string(regexstr:str, test_string:str, alphabet:List[str]):

    dfa = build_minimal_dfa(regexstr, alphabet)

    return dfa.complete_match(test_string)