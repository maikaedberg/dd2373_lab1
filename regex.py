
from parser import parse_regexp
from nfa import regex_to_nfa
from dfa import nfa_to_dfa 
from typing import List, Dict
from dfa import DFA
from graph import nfa_to_graph, dfa_to_graph

def build_minimal_dfa(regexstr:str, alphabet:List[str], graph:bool=False, timing:bool=False) -> DFA:

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

def match_substrings(regexstr_input:str, alphabet:List[str], graph:bool=False, test_strings:List[str]=[]):

    regexpstr = "(.*)({R})".format(R=regexstr_input) # allow matching anywhere in the string
    dfa = build_minimal_dfa(regexpstr, alphabet, graph)

    for s in test_strings:
        match = dfa.partial_match(s)
        if match:
            print(s)

def get_match_complete_strings(regexstr_input:str, alphabet:List[str], graph:bool=False, test_strings:List[str]=[]) -> Dict[str, bool]:
    
    dfa = build_minimal_dfa(regexstr_input, alphabet, graph)
    matched_strings = {
        s: dfa.complete_match(s) for s in test_strings
    }
    return matched_strings