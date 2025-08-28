# TCG Lookup

This script tracks and updates prices for your trading card game (TCG) collection and wantlist using TCGPlayer data. It merges your collection/wantlist CSVs with live price data, then outputs formatted Excel sheets for easy trading and tracking.

## Features

- Batch price lookup for your collection and wantlist
- Merges your CSVs with live price data
- Outputs formatted Excel sheets with color-coded price changes and printing types
- Automatically cleans up temporary files

## Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd tcg_lookup
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Prepare Your Data

- Place your collection CSV as `data/my_collection.csv`
- Place your wantlist CSV as `data/looking_for.csv`
- Ensure your CSVs have columns: `TCGPlayerId`, `Printing`, `Quanity`, etc.

### 5. Configure API Keys
- Sign up to https://justtcg.com/ and Generate your API key
- Edit `config.py` and set your TCGPlayer API key and base URL.

### 6. Run the Script

```bash
python main.py
```

## Output

- The script generates `data/trade_and_wantlist.xlsx` with two sheets:
  - **Looking_To_Trade**: your collection
  - **Looking_For**: your wantlist
- Temporary CSV files are deleted automatically.

## Disclaimer

**Prices are retrieved from TCGPlayer and are only updated when this file is regenerated. Actual prices may vary.**

## Troubleshooting

- If you get missing package errors, ensure your virtual environment is activated and requirements are installed.
- For API errors, check your API key and network connection.
