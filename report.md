# Project 1 Report: Intelligent Search Visualizer

> [!IMPORTANT]
> **AUTOGRADER COMPLIANCE INSTRUCTIONS:**
> This report is parsed automatically by the autograder. To ensure you receive full credit for your work:
> 1. **Do not modify** the section headers (`## ...`) or bold field keys (e.g., `**Name:**`, `**Selected Region:**`, `**Live Deployment URL:**`, etc.).
> 2. **Write your answers directly after** the colon `:` of each field, replacing the placeholder text completely (including the outer brackets `[` and `]`).
> 3. **Maintain the file structure**. Changing headers, bold titles, or deleting lines can cause the autograder to miss your responses and award 0 marks.

---

## Student Information 
- **Name:** Shlok Zala
- **UID (netID):** szala
- **UIN:** 659741534

---

## Section 1: Selected City Region
- **Selected Region:** Illinois, USA

---

## Section 2: Map Graph Configuration
- **Total Cities Configured:** 22
- **Total Connection Edges:** 29
- **Graph Fully Connected:** Yes

---

## Section 3: Local Verification & Search Algorithms
*Check the algorithms you successfully ran and verified on your local development server by placing an `x` in the brackets (e.g., `[x]`):*
- [x] Breadth-First Search (BFS)
- [x] Depth-First Search (DFS)
- [x] Uniform Cost Search (UCS)
- [x] Iterative Deepening Search (IDS)
- [x] Greedy Best-First Search (Greedy)
- [x] A* Search (A*)

---

## Section 4: Deployed and Presentation Information
- **Deployment Platform:** Render
- **Live Deployment URL:** https://cs-411-project1.onrender.com/
- **Video Presentation Link:** [Provide an accessible link to your 5–7 minute video presentation]

---

## Section 5: Discussion
- **Which search algorithm is best for this route finding problem?** 
    A* is the best one for this project. Because the road network has varying driving distances and known geographic coordinates, A* calculates the optimal route by using the far-fetched path costs and a straight-line heuristic. UCS correctly calculates the most optimal path cost, but it expands many nodes in the process. Greedy can get lucky sometimes as it aggressively follows the straight-line heuristic, but only sees the initial path cost.
- **Search Efficiency (Nodes expanded/time taken comparison):** 
- **Link the idea of search algorithm to today Generative AI.** 
    The state space graph represents cities, and the task is to produce a sequence of nodes forming the optimal path. In Generative AI (LLMs), the state space is a massive probabilistic web of vocabulary. When a language model produces a sentence, it is in a sense conducting a search algorithm in order to select the optimal path of words (tokens). Actually, LLMs often use Beam Search, which is basically a more evolved version of the search algorithms that we have implemented.

