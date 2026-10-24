"""
Generates a 100% self-contained Google Colab notebook (.ipynb)
with the entire 100-query dataset embedded directly inside.
"""

import json
import os

with open("dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

test_queries = data["test_queries"]

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# SRM INSTITUTE OF SCIENCE AND TECHNOLOGY, TIRUCHIRAPPALLI\n",
    "## Department of Information Technology | 21ITC203J - Formal Language and Automata (FLA)\n",
    "### Continuous Learning Assessment – 2 (CLA-2)\n",
    "---\n",
    "**Project Title:** Design and Implementation of a Deterministic Finite Automaton (DFA) for Academic Query Lexical Analysis and Intent Classification with Downstream SLM Guidance Dispatch  \n",
    "**Team Number:** 18  \n",
    "**Team Members:**  \n",
    "- Sathyabhama P S (RA2411008050023)  \n",
    "- Hrishita Choudhury (RA2411008050013)  \n",
    "**Faculty In-Charge:** Dr. P. Nagaraj  \n",
    "**Target SDG:** SDG 4 – Quality Education  \n",
    "**Dataset Reference:** [University Chatbot Dataset (Kaggle)](https://www.kaggle.com/datasets/kunalgupta2616/university-chatbot-dataset)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Formal Computational Model (5-Tuple DFA)\n",
    "$$\\mathcal{M} = (Q, \\Sigma, \\delta, q_0, F)$$\n",
    "- **Alphabet ($\\Sigma$):** $\\{s, a, p, r, x, \\#\\}$ (Study, Attendance, Performance, Resources, Neutral, EOF)\n",
    "- **State Space ($Q$):** $\\{q_0, q_S, q_A, q_P, q_R, q_{\\text{fin-}S}, q_{\\text{fin-}A}, q_{\\text{fin-}P}, q_{\\text{fin-}R}, q_{\\text{trap}}\\}$\n",
    "- **Accepting States ($F$):** $\\{q_{\\text{fin-}S}, q_{\\text{fin-}A}, q_{\\text{fin-}P}, q_{\\text{fin-}R}\\}$"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import re\n",
    "import time\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "from typing import List, Tuple, Dict, Any\n",
    "\n",
    "class AcademicQueryDFA:\n",
    "    def __init__(self):\n",
    "        self.Q = {\"q0\", \"qS\", \"qA\", \"qP\", \"qR\", \"q_finS\", \"q_finA\", \"q_finP\", \"q_finR\", \"q_trap\"}\n",
    "        self.Sigma = {\"s\", \"a\", \"p\", \"r\", \"x\", \"#\"}\n",
    "        self.q0 = \"q0\"\n",
    "        self.F = {\"q_finS\", \"q_finA\", \"q_finP\", \"q_finR\"}\n",
    "\n",
    "        self.lexicon = {\n",
    "            \"s\": {\"syllabus\", \"unit\", \"notes\", \"timetable\", \"exam\", \"exams\", \"examination\", \"textbook\", \"revision\", \"theory\", \"module\", \"slides\", \"question\", \"questions\", \"chapter\", \"curriculum\", \"paper\", \"papers\", \"blueprint\", \"study\", \"materials\", \"weightage\"},\n",
    "            \"a\": {\"attendance\", \"absent\", \"leave\", \"percentage\", \"od\", \"onduty\", \"medical\", \"condonation\", \"shortage\", \"detention\", \"biometric\", \"compensatory\", \"duty\", \"absences\"},\n",
    "            \"p\": {\"marks\", \"gpa\", \"cgpa\", \"grade\", \"grades\", \"results\", \"result\", \"internal\", \"internals\", \"revaluation\", \"backlog\", \"backlogs\", \"score\", \"scores\", \"grading\", \"transcript\", \"assessment\", \"evaluation\", \"supplementary\", \"credit\"},\n",
    "            \"r\": {\"library\", \"lab\", \"laboratory\", \"wifi\", \"portal\", \"lms\", \"classroom\", \"books\", \"book\", \"borrow\", \"hostel\", \"hardware\", \"network\", \"datacenter\", \"journals\", \"facility\", \"facilities\", \"locker\"}\n",
    "        }\n",
    "\n",
    "        self.delta = {\n",
    "            (\"q0\", \"x\"): \"q0\", (\"q0\", \"s\"): \"qS\", (\"q0\", \"a\"): \"qA\", (\"q0\", \"p\"): \"qP\", (\"q0\", \"r\"): \"qR\", (\"q0\", \"#\"): \"q_trap\",\n",
    "            (\"qS\", \"x\"): \"qS\", (\"qS\", \"s\"): \"qS\", (\"qS\", \"a\"): \"q_trap\", (\"qS\", \"p\"): \"q_trap\", (\"qS\", \"r\"): \"q_trap\", (\"qS\", \"#\"): \"q_finS\",\n",
    "            (\"qA\", \"x\"): \"qA\", (\"qA\", \"a\"): \"qA\", (\"qA\", \"s\"): \"q_trap\", (\"qA\", \"p\"): \"q_trap\", (\"qA\", \"r\"): \"q_trap\", (\"qA\", \"#\"): \"q_finA\",\n",
    "            (\"qP\", \"x\"): \"qP\", (\"qP\", \"p\"): \"qP\", (\"qP\", \"s\"): \"q_trap\", (\"qP\", \"a\"): \"q_trap\", (\"qP\", \"r\"): \"q_trap\", (\"qP\", \"#\"): \"q_finP\",\n",
    "            (\"qR\", \"x\"): \"qR\", (\"qR\", \"r\"): \"qR\", (\"qR\", \"s\"): \"q_trap\", (\"qR\", \"a\"): \"q_trap\", (\"qR\", \"p\"): \"q_trap\", (\"qR\", \"#\"): \"q_finR\",\n",
    "            (\"q_trap\", \"x\"): \"q_trap\", (\"q_trap\", \"s\"): \"q_trap\", (\"q_trap\", \"a\"): \"q_trap\", (\"q_trap\", \"p\"): \"q_trap\", (\"q_trap\", \"r\"): \"q_trap\", (\"q_trap\", \"#\"): \"q_trap\"\n",
    "        }\n",
    "\n",
    "    def tokenize(self, text: str) -> List[Tuple[str, str]]:\n",
    "        words = re.findall(r\"\\b[A-Za-z0-9\\-_]+\\b\", text.lower())\n",
    "        tokens = []\n",
    "        for word in words:\n",
    "            sym = \"x\"\n",
    "            for category_sym, terms in self.lexicon.items():\n",
    "                if word in terms:\n",
    "                    sym = category_sym\n",
    "                    break\n",
    "            tokens.append((word, sym))\n",
    "        tokens.append((\"<EOF>\", \"#\"))\n",
    "        return tokens\n",
    "\n",
    "    def evaluate(self, query: str) -> Dict[str, Any]:\n",
    "        tokens = self.tokenize(query)\n",
    "        state = self.q0\n",
    "        history = [state]\n",
    "        for _, sym in tokens:\n",
    "            state = self.delta.get((state, sym), \"q_trap\")\n",
    "            history.append(state)\n",
    "        \n",
    "        cat_map = {\"q_finS\": \"study\", \"q_finA\": \"attendance\", \"q_finP\": \"performance\", \"q_finR\": \"resources\"}\n",
    "        cat = cat_map.get(state, \"invalid\")\n",
    "        return {\"query\": query, \"tokens\": tokens, \"state_history\": history, \"final_state\": state, \"is_accepted\": state in self.F, \"category\": cat}\n",
    "\n",
    "dfa = AcademicQueryDFA()\n",
    "print(\"DFA Engine initialized successfully!\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Downstream Small Language Model (SLM) Guidance Dispatcher"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "class SLMGuidanceDispatcher:\n",
    "    def __init__(self):\n",
    "        self.guidance = {\n",
    "            \"study\": \"[Academic Study Guidance]:\\n- Access official syllabus and course blueprint on Academia / LMS.\\n- Examination timetables are released under CoE tab.\\n- Reference textbooks available in Central Library digital repository.\",\n",
    "            \"attendance\": \"[Attendance Guidance]:\\n- Mandatory minimum attendance is 75% as per B.Tech regulations.\\n- Submit OD forms within 3 working days on Academia.\\n- Condonation for 65%-74% requires HoD approval with medical certificate.\",\n",
    "            \"performance\": \"[Performance Guidance]:\\n- Check Continuous Learning Assessment (CLA) and internal marks on portal.\\n- GPA/CGPA computed on 10-point relative grading scale.\\n- Revaluation opens within 7 days of result declaration.\",\n",
    "            \"resources\": \"[Campus Resources Guidance]:\\n- Central Library hours: 8:00 AM - 8:00 PM.\\n- Student Wi-Fi MAC registration at IT Directorate Helpdesk.\\n- Digital library accessible via LAN/VPN.\"\n",
    "        }\n",
    "\n",
    "    def dispatch(self, dfa_result: Dict[str, Any]) -> str:\n",
    "        if not dfa_result[\"is_accepted\"]:\n",
    "            return f\"[DFA Guardrail Security Rejection]: Query rejected into state [{dfa_result['final_state']}]. 0% SLM compute consumed.\"\n",
    "        cat = dfa_result[\"category\"]\n",
    "        return f\"=== SLM Guidance (Verified via DFA Final State: {dfa_result['final_state']}) ===\\nCategory: [{cat.upper()}]\\n{self.guidance[cat]}\"\n",
    "\n",
    "dispatcher = SLMGuidanceDispatcher()\n",
    "print(\"SLM Guidance Dispatcher initialized!\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Benchmark Dataset (100 Real Student Queries from Kaggle University Chatbot Dataset)\n",
    "The dataset is embedded directly into this notebook so it runs completely self-contained without needing any external file uploads."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    f"benchmark_dataset = {json.dumps(test_queries, indent=2)}\n\n",
    "print(f'Total benchmark queries embedded: {len(benchmark_dataset)}')\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. Empirical Evaluation Across All 100 Queries (Accuracy, Latency & Plots)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "categories = [\"study\", \"attendance\", \"performance\", \"resources\", \"invalid\"]\n",
    "cat_to_idx = {cat: i for i, cat in enumerate(categories)}\n",
    "confusion_mat = np.zeros((len(categories), len(categories)), dtype=int)\n",
    "\n",
    "correct = 0\n",
    "total = len(benchmark_dataset)\n",
    "latencies = []\n",
    "\n",
    "for item in benchmark_dataset:\n",
    "    q = item[\"query\"]\n",
    "    expected = item[\"category\"]\n",
    "    \n",
    "    t0 = time.perf_counter()\n",
    "    res = dfa.evaluate(q)\n",
    "    t1 = time.perf_counter()\n",
    "    \n",
    "    latencies.append((t1 - t0) * 1000)\n",
    "    pred = res[\"category\"]\n",
    "    \n",
    "    confusion_mat[cat_to_idx[expected]][cat_to_idx[pred]] += 1\n",
    "    if expected == pred:\n",
    "        correct += 1\n",
    "\n",
    "accuracy = (correct / total) * 100\n",
    "avg_lat = np.mean(latencies)\n",
    "\n",
    "print('='*70)\n",
    "print(f'Benchmark Test Accuracy: {accuracy:.2f}% ({correct}/{total} passed)')\n",
    "print(f'Average DFA Transition Latency: {avg_lat:.4f} ms per query (O(N) linear time)')\n",
    "print(f'Traditional LLM Latency: ~250.00 ms (Speedup: {250.0 / avg_lat:.0f}x faster)')\n",
    "print('='*70)\n",
    "\n",
    "# Plot Confusion Matrix\n",
    "fig, ax = plt.subplots(figsize=(7, 5))\n",
    "im = ax.imshow(confusion_mat, cmap='Blues')\n",
    "ax.figure.colorbar(im, ax=ax)\n",
    "ax.set(xticks=np.arange(5), yticks=np.arange(5),\n",
    "       xticklabels=[c.capitalize() for c in categories],\n",
    "       yticklabels=[c.capitalize() for c in categories],\n",
    "       title=f'DFA Confusion Matrix (Accuracy: {accuracy:.1f}%)',\n",
    "       ylabel='Actual Category', xlabel='DFA Recognized Category')\n",
    "for i in range(5):\n",
    "    for j in range(5):\n",
    "        val = confusion_mat[i, j]\n",
    "        ax.text(j, i, str(val), ha='center', va='center', color='white' if val > 10 else 'black', fontweight='bold')\n",
    "plt.tight_layout()\n",
    "plt.show()\n",
    "\n",
    "# Plot Latency Comparison\n",
    "fig, ax = plt.subplots(figsize=(6, 4))\n",
    "bars = ax.bar(['Standard LLM', 'Proposed DFA'], [250.0, avg_lat], color=['#e74c3c', '#2ecc71'])\n",
    "ax.set_yscale('log')\n",
    "ax.set_ylabel('Latency in ms (Log Scale)')\n",
    "ax.set_title('Inference Latency: LLM vs DFA Front-End')\n",
    "for b in bars:\n",
    "    y = b.get_height()\n",
    "    ax.text(b.get_x() + b.get_width()/2, y * 1.3, f'{y:.4f} ms', ha='center', va='bottom', fontweight='bold')\n",
    "plt.tight_layout()\n",
    "plt.show()\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5. Live Interactive Query Tester\n",
    "Enter any student query or test prompt to see the token translation, state path, and SLM output!"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "custom_query = \"Where can I find the syllabus for unit 2 FLA exam?\"\n",
    "res = dfa.evaluate(custom_query)\n",
    "\n",
    "print(f'Input Query: \"{custom_query}\"')\n",
    "print(f'Symbol Tape: {\" \".join([s for _, s in res[\"tokens\"]])}')\n",
    "print(f'State Path:  {\" -> \".join(res[\"state_history\"])}')\n",
    "print(f'Final State: [{res[\"final_state\"]}] (Accepted: {res[\"is_accepted\"]})')\n",
    "print(dispatcher.dispatch(res))\n"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

with open("DFA_Academic_Query_Classifier.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=1)

print("Successfully updated DFA_Academic_Query_Classifier.ipynb with all 100 benchmark queries embedded!")
