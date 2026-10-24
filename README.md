# Academic Query Intent Classification using Deterministic Finite Automata (DFA) and SLM

### SRM Institute of Science and Technology, Tiruchirappalli
**Department of Information Technology**  
**Course:** 21ITC203J – Formal Language and Automata (FLA) | CLA-2  
**Faculty In-Charge:** Dr. P. Nagaraj  

---

### Team 18 Details
* **Sathyabhama P S** (Register No: `RA2411008050023`)
* **Hrishita Choudhury** (Register No: `RA2411008050013`)
* **Sustainable Development Goal (SDG):** SDG 4 – Quality Education
* **Case Study Area:** Compiler Lexical Analysis / Intent Tokenizer & Pattern Recognizer

---

## 1. Project Overview
In automated academic advisory systems, sending raw student queries directly to Large Language Models (LLMs) leads to:
1. High computational overhead ($>250\text{ ms}$ latency).
2. Hallucinations on official university policies.
3. Vulnerabilities to prompt-injection jailbreaks.

This project implements a **two-stage hybrid architecture**:
1. **Front-End DFA (Deterministic Finite Automaton):** Scans tokenized student queries in $O(n)$ linear time ($0.0278\text{ ms}$) to classify or reject inputs across four primary academic intents: **Study ($L_S$)**, **Attendance ($L_A$)**, **Performance ($L_P$)**, and **Resources ($L_R$)**.
2. **Back-End SLM (Small Language Model):** Dispatches verified academic guidance for accepted states ($q \in F$) while trapping malicious or off-topic inputs in $q_{\text{trap}}$ ($0\%$ SLM compute consumed).

---

## 2. Formal Computational Model (5-Tuple Definition)
$$\mathcal{M} = (Q, \Sigma, \delta, q_0, F)$$

* **Input Alphabet ($\Sigma$):** $\{s, a, p, r, x, \#\}$
  - `s`: Study keywords (`syllabus`, `exam`, `unit`, `notes`, `timetable`)
  - `a`: Attendance keywords (`attendance`, `leave`, `absent`, `od`, `percentage`)
  - `p`: Performance keywords (`marks`, `gpa`, `cgpa`, `grade`, `results`)
  - `r`: Resources keywords (`library`, `lab`, `wifi`, `portal`, `lms`)
  - `x`: Neutral filler words (`what`, `is`, `how`, `please`, `can`)
  - `#`: End-of-input string delimiter
* **State Space ($Q$):** $\{q_0, q_S, q_A, q_P, q_R, q_{\text{fin-}S}, q_{\text{fin-}A}, q_{\text{fin-}P}, q_{\text{fin-}R}, q_{\text{trap}}\}$
* **Initial State:** $q_0$
* **Accepting States ($F$):** $\{q_{\text{fin-}S}, q_{\text{fin-}A}, q_{\text{fin-}P}, q_{\text{fin-}R}\}$
* **Dead / Sink State:** $q_{\text{trap}}$

---

## 3. Empirical Results
Validated on **100 real student queries** from the **Kaggle University Chatbot Dataset**:
* **Classification Accuracy:** **$82.00\%$** (Strict deterministic zero-collision rule).
* **Adversarial / Malicious Catch Rate:** **$95.00\%$** (Intercepted into $q_{\text{trap}}$).
* **Average DFA Transition Latency:** **$0.0278\text{ ms}$** per query ($O(n)$ speed).
* **Speedup vs LLM Inference:** **$8,992\times$ faster** execution on the front-end.

---

## 4. Repository Structure
```text
├── dfa_engine.py                                # Formal 5-tuple DFA implementation
├── slm_dispatcher.py                            # Context-injected guidance dispatcher
├── evaluate.py                                  # Empirical benchmark test runner
├── main.py                                      # Live interactive demo script
├── dataset.json                                 # 100 benchmark student queries
├── dfa_automaton.jff                            # JFLAP Model file (XML)
├── DFA_Academic_Query_Classifier.ipynb          # Google Colab Notebook
├── DFA_Academic_Query_Classifier_Presentation.pptx # 10-slide PowerPoint presentation
├── CLA2_Case_Study_Report.docx                  # Full Word report with embedded figures
├── CLA2_Case_Study_Report.html                  # HTML report openable in browser
├── confusion_matrix.png                         # Empirical Confusion Matrix plot
├── latency_comparison.png                       # Latency comparison benchmark plot
├── system_architecture.png                      # Architecture flowchart diagram
└── dfa_state_diagram.png                        # State Transition Diagram image
```

---

## 5. How to Run Locally

### Run Interactive Demonstration:
```bash
python main.py
```

### Run Benchmark Evaluation & Regenerate Plots:
```bash
python evaluate.py
```

### Run on Google Colab:
Open `DFA_Academic_Query_Classifier.ipynb` in [Google Colab](https://colab.research.google.com/) and click **Runtime > Run all**.

### Open Automaton in JFLAP:
Open JFLAP $\rightarrow$ `File` $\rightarrow$ `Open` $\rightarrow$ Select `dfa_automaton.jff`.
