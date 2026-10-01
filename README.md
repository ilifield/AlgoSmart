# AlgoSmart 🧠

Paste two Python algorithm implementations, run them through an AI-powered analyzer, and instantly find out:

1. **What is their exact Big-O complexity?** — Time and Space analysis without manual mathematical proofs.
2. **Which one is faster and lighter?** — A definitive verdict on Speed and Memory efficiency based on structural code analysis.

> *AlgoSmart leverages Google's advanced Generative AI to parse, understand, and compare algorithmic logic natively. It doesn't just run the code; it understands the underlying data structures to provide competitive programming-grade verdicts.*

---

## Quick Start

Ensure you have Python 3.8+ installed. Clone the repository and set up your environment:

```bash
git clone https://github.com/ilifield/AlgoSmart.git
cd AlgoSmart
python -m venv .venv
```

Activate the virtual environment:
* **Windows:** `.venv\Scripts\activate`
* **macOS/Linux:** `source .venv/bin/activate`

Install dependencies and run the server:

```bash
pip install Flask google-generativeai
python app.py
```
Then open <http://localhost:5000> in your browser.

---

## Configuration & Security

To run the AI engine, you need a Google Gemini API Key. 
1. Get a free API key from [Google AI Studio](https://aistudio.google.com/).
2. Open `app.py` and replace the placeholder in `genai.configure(api_key="YOUR_API_KEY_HERE")` with your actual key.

**🚨 Security Warning:** Never commit your real API key to GitHub. The repository is configured to ignore `.env` files for future environment variable implementations. The current remote branch is scrubbed of any GCP API Key secrets.

---

## How it works

```text
   Browser  ──POST /api/compare_codes──▶  Flask (app.py)
      ▲                                        │
      │                                        ▼
      │                                Strict Prompt Engineering
      │                                        │
      └────── JSON (Complexity & Verdict) ─────┼──▶ Gemini 3.6 Flash
                                               │    (Google AI Engine)
                                               ▼
                                        Static Analysis
                                  (Time/Space O-notation eval)
```

### The AI Pipeline
Instead of sandboxing and brute-force benchmarking (which suffers from machine load noise and infinite-loop risks), AlgoSmart uses **Gemini 3.6 Flash** for deep static analysis. 

The backend sends both code snippets wrapped in a strict instructional prompt. The AI evaluates:
* **Time Complexity:** Identifies nested loops, recursive depths, and standard library internal complexities.
* **Space Complexity:** Analyzes auxiliary data structures (e.g., creating arrays vs. in-place modifications).
* **Verdict:** Compares the Big-O notations to declare a definitive Speed Winner and Memory Winner.

### Frontend Architecture
The UI is lightweight and strictly dependency-free:
* Pure HTML/CSS with a modern, dark-themed developer aesthetic.
* Vanilla JavaScript for asynchronous API polling.
* Real-time loading states and smooth DOM updates without page reloads.

---

## Output Format

The comparison engine is heavily constrained to output purely technical, AI-agnostic results. Example output:

* **Code A Complexity:** Time O(N^2), Space O(1)
* **Code B Complexity:** Time O(N log log N), Space O(N)
* **Speed Winner:** Code B (Sieve of Eratosthenes algorithm avoids redundant division checks)
* **Memory Winner:** Code A (Uses O(1) auxiliary space, whereas Code B allocates an extra array of size N)

---

## Project Layout

```text
AlgoSmart/
  app.py                 Flask application, routing, and Gemini API integration
  templates/
    index.html           Main UI, vanilla JS handlers, and CSS styling
  .gitignore             Security guardrails against committing keys/pycache
  README.md              Project documentation
```

---

## Future Roadmap

* **.env Integration:** Moving the API key to a secure environment variable pipeline.
* **Multi-Language Support:** Extending the prompt logic to analyze C++, Java, and Go implementations.
* **Historical Tracking:** Saving previous comparisons in a local SQLite database for quick reference.