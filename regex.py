
import time
from parser import parse_regexp
from nfa import regex_to_nfa, NFA
from dfa import nfa_to_dfa 
from typing import List, Tuple
from dfa import DFA
from graph import nfa_to_graph, dfa_to_graph
from performance_logger import PerformanceMetrics, get_logger


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


def build_minimal_dfa_with_timing(regexstr:str, alphabet:List[str], graph:bool=False) -> Tuple[NFA, DFA, dict]:

    timing = {}
    
    # Build NFA
    start = time.time()
    regexp = parse_regexp(regexstr)
    nfa = regex_to_nfa(regexp, alphabet)
    timing['nfa_time_ms'] = (time.time() - start) * 1000
    if graph:
        nfa_to_graph(nfa, "graphs/nfa.png")
    
    # Build DFA
    start = time.time()
    dfa = nfa_to_dfa(nfa)
    dfa.is_dfa()
    dfa_states_before_min = len(dfa.states)
    timing['dfa_time_ms'] = (time.time() - start) * 1000
    if graph:
        dfa_to_graph(dfa, "graphs/subset_dfa.png")
    
    # Minimize DFA
    start = time.time()
    dfa.minimize()
    dfa.is_dfa()
    timing['minimization_time_ms'] = (time.time() - start) * 1000
    if graph:
        dfa_to_graph(dfa, "graphs/min_dfa.png")
    
    timing['total_time_ms'] = timing['nfa_time_ms'] + timing['dfa_time_ms'] + timing['minimization_time_ms']
    timing['dfa_states_before_min'] = dfa_states_before_min
    
    return nfa, dfa, timing


def match_substring(regexstr:str, input_str:str, alphabet:List[str], graph:bool=False, track_performance:bool=False):

    match_substr_regexstr = "(.*)({R})".format(R=regexstr)

    if track_performance:
        nfa, dfa, timing = build_minimal_dfa_with_timing(match_substr_regexstr, alphabet, graph)
        
        # Match with DFA
        start = time.time()
        dfa_result = dfa.partial_match(input_str)
        dfa_time_ms = (time.time() - start) * 1000
        
        # Log metrics (without NFA simulation - it's too slow)
        metrics = PerformanceMetrics(
            regex=regexstr,
            alphabet_size=len(alphabet),
            nfa_states=len(nfa.states),
            dfa_states=timing['dfa_states_before_min'],
            minimized_dfa_states=len(dfa.states),
            nfa_build_time_ms=timing['nfa_time_ms'],
            dfa_build_time_ms=timing['dfa_time_ms'],
            minimization_time_ms=timing['minimization_time_ms'],
            total_build_time_ms=timing['total_time_ms'],
            num_test_strings=1,
            dfa_matching_time_ms=dfa_time_ms,
            nfa_matching_time_ms=0.0  # Not measured to save time
        )
        get_logger().add_metrics(metrics)
        
        return dfa_result
    else:
        dfa = build_minimal_dfa(match_substr_regexstr, alphabet, graph)
        return dfa.partial_match(input_str)


def match_string(regexstr:str, test_string:str, alphabet:List[str]):

    dfa = build_minimal_dfa(regexstr, alphabet)

    return dfa.complete_match(test_string)