"""
SLM Response Dispatcher Module
Course: Formal Language and Automata (FLA) - SRM IST
Role: Consumes DFA-verified final states and dispatches contextualized academic guidance.
"""

from typing import Dict, Any

class SLMGuidanceDispatcher:
    """
    Simulates / routes to a Small Language Model (e.g. Phi-3 / Gemma-2B / Llama-3.2-1B)
    using the DFA final accepting state as a strict security and context boundary.
    """

    def __init__(self):
        # Calibrated prompt contexts injected according to DFA state
        self.context_templates = {
            "study": {
                "system_role": "SRM University Academic Curriculum & Study Advisory Agent",
                "sample_guidance": (
                    "[Academic Study Guidance]:\n"
                    "- The syllabus, course blueprint, and unit-wise lecture notes are maintained on the SRM Academia / LMS portal.\n"
                    "- Examination timetables are officially uploaded under the CoE (Controller of Examinations) tab.\n"
                    "- For reference textbooks, consult the Central Library e-repository or your faculty advisor."
                )
            },
            "attendance": {
                "system_role": "SRM University Student Attendance Regulation Agent",
                "sample_guidance": (
                    "[Attendance Regulatory Guidance]:\n"
                    "- Minimum mandatory attendance is 75% across all lecture and laboratory courses as per B.Tech regulations.\n"
                    "- Condonation of 65% - 74% is subject to valid medical certificates approved by the Head of Department.\n"
                    "- On-Duty (OD) forms for symposiums, sports, or hackathons must be submitted on Academia within 3 working days."
                )
            },
            "performance": {
                "system_role": "SRM University Academic Evaluation & Grade Advisory Agent",
                "sample_guidance": (
                    "[Evaluation & Grade Guidance]:\n"
                    "- Continuous Learning Assessment (CLA) marks, Internal assessments, and Grade Points are accessible on Academia.\n"
                    "- Semester GPA & Cumulative CGPA are computed using the 10-point relative grading scale.\n"
                    "- Paper revaluation or review applications open within 7 days of semester result declaration via the CoE portal."
                )
            },
            "resources": {
                "system_role": "SRM University Campus Infrastructure & IT Helpdesk Agent",
                "sample_guidance": (
                    "[Campus Resources & IT Guidance]:\n"
                    "- Central Library is open 8:00 AM - 8:00 PM; digital journals (IEEE, ACM, ScienceDirect) are accessible via LAN/VPN.\n"
                    "- Campus Wi-Fi registration requires MAC address mapping at the IT Directorate Helpdesk.\n"
                    "- LMS / Portal password resets can be performed via official self-service or IT Helpdesk."
                )
            }
        }

    def generate_guidance(self, dfa_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Receives DFA evaluation result and determines appropriate SLM dispatch.
        """
        is_accepted = dfa_result["is_accepted"]
        category = dfa_result["recognized_category"]
        final_state = dfa_result["final_state"]
        query = dfa_result["query"]

        if not is_accepted or category == "invalid" or final_state == "q_trap":
            return {
                "status": "REJECTED_BY_DFA",
                "slm_invoked": False,
                "error_message": (
                    "[DFA Guardrail Security Rejection]:\n"
                    "The query does not conform to the accepted academic language grammar L(M).\n"
                    "Potential causes: Out-of-domain topic, multi-intent ambiguity, or prompt-injection attempt.\n"
                    f"DFA halted at state: {final_state}. No LLM/SLM compute was consumed."
                ),
                "dispatched_response": None
            }

        template = self.context_templates.get(category, {})
        system_role = template.get("system_role", "Academic Assistant")
        guidance_text = template.get("sample_guidance", "")

        simulated_response = (
            f"=== SLM Response (Role: {system_role}) ===\n"
            f"Target Category: [{category.upper()}] (Verified via DFA Final State: {final_state})\n"
            f"Original Query: \"{query}\"\n\n"
            f"{guidance_text}\n"
            f"====================================================="
        )

        return {
            "status": "SUCCESS",
            "slm_invoked": True,
            "category": category,
            "system_role": system_role,
            "dispatched_response": simulated_response
        }
