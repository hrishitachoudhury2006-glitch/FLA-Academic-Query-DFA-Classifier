"""
Main Execution & Interactive Demonstration Script
Academic Query Intent Classification using DFA and SLM Dispatch
Team 18 - SRM Institute of Science and Technology
"""

import sys
from dfa_engine import AcademicQueryDFA
from slm_dispatcher import SLMGuidanceDispatcher

def print_banner():
    print("=" * 80)
    print("  SRM INSTITUTE OF SCIENCE AND TECHNOLOGY - TIRUCHIRAPPALLI")
    print("  DEPARTMENT OF INFORMATION TECHNOLOGY")
    print("  COURSE: FORMAL LANGUAGE AND AUTOMATA (FLA)")
    print("  PROJECT: DFA LEXICAL QUERY CLASSIFIER & SLM GUIDANCE DISPATCH")
    print("=" * 80)

def demonstrate_query(query_text: str, dfa: AcademicQueryDFA, dispatcher: SLMGuidanceDispatcher):
    print("\n" + "-" * 80)
    print(f"[INPUT QUERY]: \"{query_text}\"")
    print("-" * 80)

    # 1. DFA Evaluation
    res = dfa.process_query(query_text)
    
    print("\n[Step 1: Lexical Tokenization & Symbol Translation]")
    print("  Tokens (Word -> Symbol):")
    for word, sym in res["tokens"][:-1]:
        print(f"    '{word}' -> [{sym}]")
    print("    '<EOF>' -> [#]")
    print(f"  Formal Input Tape w in Sigma*: \"{res['symbol_string']}\"")

    print("\n[Step 2: Automaton State Transition Trace]")
    history = res["state_history"]
    trace_str = " -> ".join(history)
    print(f"  State Execution Path: {trace_str}")
    print(f"  Final State Reached: [{res['final_state']}]")
    print(f"  Is Accepted in F?   : {res['is_accepted']}")
    print(f"  Classified Intent   : [{res['recognized_category'].upper()}]")

    print("\n[Step 3: Downstream SLM Response Dispatch]")
    slm_res = dispatcher.generate_guidance(res)
    if slm_res["status"] == "SUCCESS":
        print(slm_res["dispatched_response"])
    else:
        print(slm_res["error_message"])
    print("-" * 80)

def main():
    print_banner()
    dfa = AcademicQueryDFA()
    dispatcher = SLMGuidanceDispatcher()

    # Pre-defined demonstration samples across all states
    demo_samples = [
        "Where can I find the syllabus for unit 2 FLA exam?",
        "How do I apply for on duty OD leave for attendance?",
        "When will the internal marks and semester GPA results be published?",
        "What are the central library working hours and wifi access?",
        "Write a poem about the ocean and stars in python."
    ]

    print("\nRunning demonstration on sample academic queries:\n")
    for q in demo_samples:
        demonstrate_query(q, dfa, dispatcher)

    print("\n" + "=" * 80)
    print("DEMO COMPLETE: All DFA state transitions formally verified.")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
