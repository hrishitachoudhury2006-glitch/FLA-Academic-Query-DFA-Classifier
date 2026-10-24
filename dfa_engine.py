"""
Deterministic Finite Automaton (DFA) Engine for Academic Query Intent Classification
Course: Formal Language and Automata (FLA) - SRM IST
Mathematical Formulation: M = (Q, Sigma, delta, q0, F)
"""

import re
from typing import List, Tuple, Dict, Any

class AcademicQueryDFA:
    """
    Formal 5-tuple implementation:
    M = (Q, Sigma, delta, q0, F)
    """

    def __init__(self):
        # 1. State Space Q
        self.Q = {
            "q0",          # Initial listening state
            "qS",          # Active Study intent parsing state
            "qA",          # Active Attendance intent parsing state
            "qP",          # Active Performance intent parsing state
            "qR",          # Active Resource intent parsing state
            "q_finS",      # Final Accepting State: Study
            "q_finA",      # Final Accepting State: Attendance
            "q_finP",      # Final Accepting State: Performance
            "q_finR",      # Final Accepting State: Resources
            "q_trap"       # Non-accepting dead/trap state
        }

        # 2. Input Alphabet Sigma
        # s = Study, a = Attendance, p = Performance, r = Resources, x = Neutral/Filler, # = End-marker
        self.Sigma = {"s", "a", "p", "r", "x", "#"}

        # 3. Initial State q0
        self.q0 = "q0"

        # 4. Set of Final (Accepting) States F
        self.F = {"q_finS", "q_finA", "q_finP", "q_finR"}

        # 5. Domain Lexicon Dictionary (Term mapping to formal alphabet tokens)
        self.lexicon = {
            "s": {
                "syllabus", "unit", "notes", "timetable", "exam", "exams", "examination",
                "textbook", "revision", "theory", "module", "slides", "question", "questions",
                "chapter", "curriculum", "paper", "papers", "blueprint", "study", "materials",
                "weightage", "curricula"
            },
            "a": {
                "attendance", "absent", "leave", "percentage", "od", "onduty", "medical",
                "condonation", "shortage", "detention", "biometric", "compensatory", "duty",
                "absences", "detained"
            },
            "p": {
                "marks", "gpa", "cgpa", "grade", "grades", "results", "result", "internal",
                "internals", "revaluation", "backlog", "backlogs", "score", "scores",
                "grading", "transcript", "assessment", "evaluation", "supplementary", "credit"
            },
            "r": {
                "library", "lab", "laboratory", "wifi", "portal", "lms", "classroom",
                "books", "book", "borrow", "hostel", "hardware", "network", "datacenter",
                "journals", "facility", "facilities", "locker", "lockers", "it"
            }
        }

        # 6. Formal Transition Function delta: Q x Sigma -> Q
        self.delta: Dict[Tuple[str, str], str] = {
            # Transitions from Initial State q0
            ("q0", "x"): "q0",
            ("q0", "s"): "qS",
            ("q0", "a"): "qA",
            ("q0", "p"): "qP",
            ("q0", "r"): "qR",
            ("q0", "#"): "q_trap",

            # Transitions from Active Study State qS
            ("qS", "x"): "qS",
            ("qS", "s"): "qS",
            ("qS", "a"): "q_trap",  # Collision / ambiguous intent triggers trap
            ("qS", "p"): "q_trap",
            ("qS", "r"): "q_trap",
            ("qS", "#"): "q_finS",

            # Transitions from Active Attendance State qA
            ("qA", "x"): "qA",
            ("qA", "a"): "qA",
            ("qA", "s"): "q_trap",
            ("qA", "p"): "q_trap",
            ("qA", "r"): "q_trap",
            ("qA", "#"): "q_finA",

            # Transitions from Active Performance State qP
            ("qP", "x"): "qP",
            ("qP", "p"): "qP",
            ("qP", "s"): "q_trap",
            ("qP", "a"): "q_trap",
            ("qP", "r"): "q_trap",
            ("qP", "#"): "q_finP",

            # Transitions from Active Resource State qR
            ("qR", "x"): "qR",
            ("qR", "r"): "qR",
            ("qR", "s"): "q_trap",
            ("qR", "a"): "q_trap",
            ("qR", "p"): "q_trap",
            ("qR", "#"): "q_finR",

            # Transitions from Final Accepting States (Any further input halts or traps)
            ("q_finS", "x"): "q_trap", ("q_finS", "s"): "q_trap", ("q_finS", "a"): "q_trap", ("q_finS", "p"): "q_trap", ("q_finS", "r"): "q_trap", ("q_finS", "#"): "q_trap",
            ("q_finA", "x"): "q_trap", ("q_finA", "s"): "q_trap", ("q_finA", "a"): "q_trap", ("q_finA", "p"): "q_trap", ("q_finA", "r"): "q_trap", ("q_finA", "#"): "q_trap",
            ("q_finP", "x"): "q_trap", ("q_finP", "s"): "q_trap", ("q_finP", "a"): "q_trap", ("q_finP", "p"): "q_trap", ("q_finP", "r"): "q_trap", ("q_finP", "#"): "q_trap",
            ("q_finR", "x"): "q_trap", ("q_finR", "s"): "q_trap", ("q_finR", "a"): "q_trap", ("q_finR", "p"): "q_trap", ("q_finR", "r"): "q_trap", ("q_finR", "#"): "q_trap",

            # Transitions from Trap State (Total absorbing sink state)
            ("q_trap", "x"): "q_trap",
            ("q_trap", "s"): "q_trap",
            ("q_trap", "a"): "q_trap",
            ("q_trap", "p"): "q_trap",
            ("q_trap", "r"): "q_trap",
            ("q_trap", "#"): "q_trap",
        }

    def tokenize_query(self, raw_query: str) -> List[Tuple[str, str]]:
        """
        Lexical tokenization of raw text into formal alphabet Sigma.
        Returns list of (word, symbol).
        """
        # Clean punctuation and split to words
        words = re.findall(r"\b[A-Za-z0-9\-_]+\b", raw_query.lower())
        tokens = []

        for word in words:
            symbol = "x"  # Default filler symbol
            for sym, term_set in self.lexicon.items():
                if word in term_set:
                    symbol = sym
                    break
            tokens.append((word, symbol))

        # Append end-of-string marker #
        tokens.append(("#", "#"))
        return tokens

    def process_query(self, query_text: str) -> Dict[str, Any]:
        """
        Evaluates the input query string on the DFA M.
        Tracks state path step-by-step.
        """
        tokens = self.tokenize_query(query_text)
        current_state = self.q0
        state_history = [current_state]
        transition_steps = []

        for word, symbol in tokens:
            next_state = self.delta.get((current_state, symbol), "q_trap")
            transition_steps.append({
                "word": word,
                "symbol": symbol,
                "from_state": current_state,
                "to_state": next_state
            })
            current_state = next_state
            state_history.append(current_state)

        is_accepted = current_state in self.F
        recognized_category = "invalid"

        if current_state == "q_finS":
            recognized_category = "study"
        elif current_state == "q_finA":
            recognized_category = "attendance"
        elif current_state == "q_finP":
            recognized_category = "performance"
        elif current_state == "q_finR":
            recognized_category = "resources"

        symbol_string = " ".join([sym for _, sym in tokens])

        return {
            "query": query_text,
            "tokens": tokens,
            "symbol_string": symbol_string,
            "final_state": current_state,
            "state_history": state_history,
            "transition_steps": transition_steps,
            "is_accepted": is_accepted,
            "recognized_category": recognized_category
        }
