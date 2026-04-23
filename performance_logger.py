from random import random
from typing import List
import time
from parser import parse_regexp
from nfa import regex_to_nfa
from dfa import nfa_to_dfa, DFA
import pandas as pd
import random
from regex import build_minimal_dfa

# How many states do the intermediate automata have in your test cases?
def run_state_count_tests():

    regexp_inputs = [
        "abab", "ab|cde", "a*bc*(ab)+", "a+.+b?a+.+b+", 
        "abcd*|cba(abc)+|(abc)+(bdb)(abc)?|a.b.c.d|(((abc)+)+)+",
        "(a|b)*c(a|b)*d(a|b)*e(a|b)*"
    ]
    alphabet = ["a", "b", "c", "d", "e"]

    rows = []

    for regexp_input in regexp_inputs:
        regexpstr = "(.*)({R})".format(R=regexp_input)
        regexp = parse_regexp(regexpstr)

        nfa = regex_to_nfa(regexp, alphabet)
        num_nfa_states = len(nfa.states)

        dfa = nfa_to_dfa(nfa)
        num_dfa_states = len(dfa.states)

        dfa.minimize()
        num_min_dfa_states = len(dfa.states)
 
        # percentage improvement of min dfa vs nfa
        min_dfa_vs_nfa = (num_nfa_states - num_min_dfa_states) / num_nfa_states * 100 if num_nfa_states > 0 else 0

        rows.append({
            "Regex": "\\text{" +regexp_input + "}",
            "NFA": num_nfa_states,
            "DFA": num_dfa_states,
            "Min DFA": num_min_dfa_states,
            "Improvement": f"{min_dfa_vs_nfa:.2f}\\%"
        })


    df = pd.DataFrame(rows)

    return df.to_latex(
        index=False,
        escape=False,      # important for regex symbols!
        caption="State counts for automata",
        label="tab:state-counts"
    )

# Does the size of the regex affect the time it takes to build the NFA, DFA, and minimize the DFA?
def performance_build_time():
    regexp_inputs = [
        "abcde"*i for i in range(1,51, 9)
    ]
    alphabet = ["a", "b", "c", "d", "e"]
    rows = []
    for regexp_input in regexp_inputs:
            
        t = time.time()
        regexp = parse_regexp(regexp_input)

        nfa = regex_to_nfa(regexp, alphabet)
        nfa_build_time_ms = (time.time() - t) * 1000

        t = time.time()
        dfa = nfa_to_dfa(nfa)
        dfa_build_time_ms = (time.time() - t) * 1000

        t = time.time()
        dfa.minimize()
        minimization_time_ms = (time.time() - t) * 1000

        rows.append({
            "Size:": len(regexp_input),
            "NFA (ms)": f"{nfa_build_time_ms:.2f}",
            "DFA (ms)": f"{dfa_build_time_ms:.2f}",
            "Min. (ms)": f"{minimization_time_ms:.2f}",
            "Total (ms)": f"{nfa_build_time_ms + dfa_build_time_ms + minimization_time_ms:.2f}"
        })
    
    df = pd.DataFrame(rows)

    return df.to_latex(
        index=False,
        escape=False,      # important for regex symbols!
        caption="Performance of building automata",
        label="tab:build-performance"
    )


def performance_matching_time():
    regexp_input = "(abbc|bcab)+c(abc|aaaa)"
    alphabet = ["a", "b", "c"]

    # run with random strings of length from 100000 to 1000000 with step 100000
    test_strings = []
    for i in range(100000, 1000001, 100000):
        s = "".join(random.choice(alphabet) for _ in range(i))
        test_strings.append(s)  
    
    regex = "(.*)({R})".format(R=regexp_input)
    dfa = build_minimal_dfa(regex, alphabet)

    rows = []   
    for s in test_strings:
        t = time.time()
        dfa.partial_match(s)
        matching_time_ms = (time.time() - t) * 1000

        rows.append({
            "Length": len(s),
            "Match (ms)": f"{matching_time_ms:.2f}"
        })

    df = pd.DataFrame(rows)

    return df.to_latex(
        index=False,
        escape=False,      # important for regex symbols!
        caption="Performance of DFA matching for random strings with \\text{" + regexp_input + "} regex",
        label="tab:dfa-matching-performance"
    )

def performance_matching_nfa_vs_dfa():
    regexp_input = "(abbc|bcab)+c(abc|aaaa)"
    alphabet = ["a", "b", "c"]

    regex_str = "(.*)({R})".format(R=regexp_input)
    nfa = regex_to_nfa(parse_regexp(regex_str), alphabet)
    dfa = build_minimal_dfa(regex_str, alphabet)

    # run with random strings of length from 100000 to 1000000 with step 10000
    test_strings = []
    for i in range(10000, 100001, 10000):
        s = "".join(random.choice(alphabet) for _ in range(i))
        test_strings.append(s)  
    
    
    rows = []   
    for s in test_strings:
        t = time.time()
        nfa.partial_match(s)
        nfa_matching_time_ms = (time.time() - t) * 1000

        t = time.time()
        dfa.partial_match(s)
        dfa_matching_time_ms = (time.time() - t) * 1000

        rows.append({
            "Length": len(s),
            "NFA Match (ms)": f"{nfa_matching_time_ms:.2f}",
            "DFA Match (ms)": f"{dfa_matching_time_ms:.2f}"
        })

    df = pd.DataFrame(rows)

    return df.to_latex(
        index=False,
        escape=False,
        caption="Performance of NFA vs DFA matching for random strings with \\text{" + regexp_input + "} regex",
        label="tab:nfa-vs-dfa-matching-performance"
    )


def run_performance_tests(regexp_input: str, alphabet: List[str], test_strings: List[str]):
    
    log = dict()
    regexpstr = "(.*)({R})".format(R=regexp_input) # allow matching anywhere in the string
    regexp = parse_regexp(regexpstr)

    # measure time of building NFA, DFA, and minimizing DFA
    t = time.time()
    nfa = regex_to_nfa(regexp, alphabet)
    log['nfa_build_time_ms'] = (time.time() - t) * 1000
    log['num_of_nfa_states'] = len(nfa.states)
    
    t = time.time()
    dfa = nfa_to_dfa(nfa)
    log['dfa_build_time_ms'] = (time.time() - t) * 1000
    log['num_of_dfa_states'] = len(dfa.states)

    t = time.time()
    dfa.minimize()
    log['minimization_time_ms'] = (time.time() - t) * 1000
    log['num_of_minimized_dfa_states'] = len(dfa.states)

    log['total_build_time_ms'] = log['nfa_build_time_ms'] + log['dfa_build_time_ms'] + log['minimization_time_ms']

    # measure time of matching test strings with NFA and DFA
    matching_times = []
    for s in test_strings:
        t = time.time()
        dfa.partial_match(s)
        matching_times.append((time.time() - t) * 1000)
    
    log['avg_dfa_matching_time_ms'] = sum(matching_times) / len(matching_times) if matching_times else 0

    return dfa     
    
    
if __name__ == "__main__":

    print("-- Performance Tests ---")
    res = performance_build_time()
    print("Build time performance:")
    print(res)
    res = performance_matching_time()
    print("Matching time performance:")
    print(res)
    res = performance_matching_nfa_vs_dfa()
    print("NFA vs DFA matching performance:")   
    print(res)
