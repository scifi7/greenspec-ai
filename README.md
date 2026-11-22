# GreenSpec AI

AI-assisted sustainable product design advisor. Enter a product, its main material,
manufacturing process and market, and get a sustainability scorecard, AI-generated greener
alternatives (Claude), and the regulations that may apply.

## Files
- `app.py` - Streamlit web app
- `scoring.py` - scoring logic (weights live here)
- `ui.py` - green colour palette, CSS and HTML for the scorecard
- `.streamlit/config.toml` - Streamlit theme colours
- `materials.csv` - materials database (15 materials, scores per kg, 1-10)
- `requirements.txt` - Python dependencies

## Run locally
1. `pip install -r requirements.txt`
2. Create `.streamlit/secrets.toml` containing: `ANTHROPIC_API_KEY = "your-key-here"`
3. `streamlit run app.py`

Never commit your API key. `.streamlit/secrets.toml` is listed in `.gitignore`.

## Deploy
Push to GitHub, then create an app on Streamlit Community Cloud pointing at `app.py`.
Add `ANTHROPIC_API_KEY` under the app's Secrets settings.
