# Google Map Scrapper and Insta Automation Site

A Python automation project that helps collect business intelligence from two sources:

1. Google Maps scraping workflow for business/store discovery and metadata extraction.
2. Instagram automation workflow for post engagement scraping and AI-based feedback summarization.

## Project Structure

```text
Scammer_detection/
├── insta.py
├── instagram_scraped_data.json
├── feedback.txt
├── requirements.txt
├── README.md
└── google_map_scrapper/
    ├── map.py
    └── output.txt
```

## Prerequisites

Install the following on any computer:

- Git
- Python 3.10+ (recommended 3.11)
- A terminal (PowerShell, CMD, Bash, or zsh)

## Quick Start (From Git Clone)

### 1) Clone the repository

```bash
git clone <REPOSITORY_URL>
cd Google_Map_Scrapper
```

### 2) Create and activate a virtual environment

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows (CMD):

```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install langchain-google-genai
python -m playwright install
```

## Environment Configuration

Create a `.env` file in the project root for Instagram automation:

```env
IG_USERNAME=your_instagram_username
IG_PASSWORD=your_instagram_password
gemini_api_key=your_gemini_api_key
```

Notes:

- `IG_USERNAME` and `IG_PASSWORD` are used to log in to Instagram.
- `gemini_api_key` is used to generate structured feedback from scraped comments.

## Google Map Scrapper

### What it does

The Google Maps script:

- Opens Google Maps in a browser using Playwright.
- Searches for your input query (for example: `restaurants in Kathmandu`).
- Iterates through result cards.
- Extracts store name, details, and visible social handles.
- Writes results to `google_map_scrapper/output.txt`.

### Run Google Map Scrapper

```bash
cd google_map_scrapper
python map.py
```

When prompted, enter the Google Maps search URL/query text.

### Output

- Scraped data file: `google_map_scrapper/output.txt`

## Insta Automation

### What it does

The Instagram script:

- Logs into Instagram using credentials from `.env`.
- Opens a target profile defined in `insta.py`.
- Collects likes and comments from recent posts.
- Saves raw scraped data to `instagram_scraped_data.json`.
- Sends comments to Gemini and writes summarized insights to `feedback.txt`.

### Run Insta Automation

From the project root:

```bash
python insta.py
```

### Output

- Raw post data: `instagram_scraped_data.json`
- AI feedback summary: `feedback.txt`

## Troubleshooting

- Browser not launching or Playwright errors:
  - Run `python -m playwright install` again.
- Instagram login issues:
  - Recheck `.env` keys and values.
  - Instagram UI selectors can change; update selectors in `insta.py` if needed.
- Missing package errors:
  - Ensure virtual environment is active.
  - Re-run dependency installs.

## Security Best Practices

- Never commit `.env` to version control.
- Use environment variables for secrets and API keys.
- Rotate credentials/API keys if they are exposed.

## Disclaimer

This project is for educational and research purposes. Respect platform terms of service, robots policies, and local laws when scraping or automating third-party services.
