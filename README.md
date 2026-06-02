# CYBERFORGE AI CHATBOT

CyberForge is a portfolio chatbot built around a curated response dataset. It serves the main portfolio at `/` and the standalone chatbot at `/chatbot`.

## Project Structure

```text
CyberForge/
├── app.py              Flask backend and matching engine
├── dataset.json        Generated from DataSet.xlsx
├── DataSet.xlsx        Source response trigger sheet
├── build_dataset.py    Regenerates dataset.json
├── requirements.txt    Python dependencies
├── responses/          Curated response text files
├── static/index.html   Chatbot UI
└── portfolio/          Portfolio page, resume, and assets
```

## Setup

```bash
pip install -r requirements.txt
python app.py
```

Then open:

```text
http://localhost:5000/
http://localhost:5000/chatbot
```

## Matching Engine

The chatbot now uses a hybrid intent matcher:

| Layer | Purpose |
| --- | --- |
| Exact sentence match | Preserves curated answers for known questions |
| Intent shortcuts | Handles actions like resume, GitHub, LinkedIn, contact, projects, and skills |
| Token overlap | Matches natural wording such as "show me your skills" |
| Fuzzy similarity | Catches small typos and phrasing differences |
| Fallback response | Guides the user when no confident match is found |

Responses may include action metadata, so the UI can show buttons like `Download Resume`, `Open GitHub`, or `Email`.

## API Routes

```text
GET  /status       Dataset and response health
GET  /suggestions  Autocomplete suggestions from dataset.json
POST /chat         Chat response endpoint
```

## Regenerating Dataset

If you update `DataSet.xlsx`, run:

```bash
python build_dataset.py
```

Make sure every `File Name` value in the sheet has a matching file in `responses/`.
