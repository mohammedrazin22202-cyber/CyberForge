# CYBERFORGE AI CHATBOT

## Project Structure

```
cyberforge_chatbot/
│
├── app.py              ← Flask backend (run this)
├── dataset.json        ← Auto-generated from DataSet.xlsx
├── requirements.txt    ← Python dependencies
│
├── responses/          ← ⚡ PUT YOUR .txt RESPONSE FILES HERE
│   ├── 1.1.Who are you.txt
│   ├── 1.2.What is CyberForge.txt
│   ├── ... (all 150 response files)
│   └── fallback.txt    ← shown when no match is found
│
└── static/
    └── index.html      ← Matrix-style UI (auto-served)
```

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Place all your response `.txt` files inside the `responses/` folder.
   File names must exactly match those in `dataset.json` (column: File Name).

3. Run the chatbot:
   ```
   python app.py
   ```

   The browser will open automatically at http://localhost:5000

## How the Scoring Works

For every user message, each of the 150 entries is scored:

| Match Type       | Points |
|------------------|--------|
| Key sentence     | +5 pts |
| Single keyword   | +1 pt  |

Key sentences include: Core Intent, Response triggers (Recruiter/Casual/Technical),
Short Triggers, Typos, and Fuzzy matches.

Keywords include: all Technical, Casual, Fuzzy, and Typo keyword columns.

The entry with the **highest total score** wins and its response file is served.

## Regenerating dataset.json

If you update DataSet.xlsx, re-run:
```
python build_dataset.py
```
