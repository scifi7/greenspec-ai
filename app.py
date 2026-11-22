"""GreenSpec AI - AI-assisted sustainable product design advisor (Streamlit app)."""
import os

import streamlit as st

from scoring import (
    COL_CARBON,
    COL_ENERGY,
    COL_MATERIAL,
    COL_RECYCLE,
    WEIGHTS,
    calculate_score,
    get_material_row,
    load_materials,
    rating_label,
)
from ui import CSS, hero_html, scorecard_html, section_html

# If the AI step errors with a model-not-found message, change this to a model
# name that is valid for your API account (see docs.claude.com).
MODEL = "claude-sonnet-5-5"

PROCESSES = [
    "Injection moulding",
    "Casting",
    "Extrusion",
    "Machining / fabrication",
    "Welding",
    "Pressing / stamping",
    "Textile weaving / knitting",
    "3D printing",
    "Other",
]
COUNTRIES = ["UAE", "European Union", "Other / International"]

# STEP 5 (Business & Research Lead): starter content only. Verify each point
# against official sources and extend to 3-4 solid bullets per region.
REGULATIONS = {
    "UAE": [
        "UAE Net Zero 2050 Strategic Initiative: national target for net-zero emissions by 2050.",
        "Federal Decree-Law No. 11 of 2024 on reducing climate change effects: emissions measurement and reporting duties.",
        "Federal Law No. 12 of 2018 on Integrated Waste Management: rules for waste handling and recycling.",
        "Restrictions on single-use plastic bags and products at federal and emirate level.",
    ],
    "European Union": [
        "European Green Deal: overall framework aiming for climate neutrality by 2050.",
        "Ecodesign for Sustainable Products Regulation (ESPR): durability, repairability and recyclability requirements.",
        "Packaging and Packaging Waste Regulation (PPWR): recyclability and recycled-content rules for packaging.",
        "Carbon Border Adjustment Mechanism (CBAM): carbon cost on imported steel, aluminium, cement and similar goods.",
    ],
    "Other / International": [
        "ISO 14001: environmental management systems.",
        "ISO 14040 / 14044: life cycle assessment (LCA) principles and requirements.",
        "ISO 14067: carbon footprint of products.",
        "GHG Protocol: widely used standard for measuring greenhouse gas emissions.",
    ],
}
INTERNATIONAL_KEY = "Other / International"


@st.cache_data
def get_materials():
    return load_materials("materials.csv")


def get_api_key():
    """Read the API key from Streamlit secrets, falling back to an env variable."""
    try:
        return st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        return os.environ.get("ANTHROPIC_API_KEY")


def get_suggestions(product, material, process, country, score, other_materials):
    """Ask Claude for two greener alternatives. Returns plain text."""
    import anthropic

    client = anthropic.Anthropic(api_key=get_api_key())
    prompt = f"""You are a sustainable product design advisor for small manufacturers.

Product: {product}
Current material: {material}
Manufacturing process: {process}
Country sold in: {country}
Current sustainability score: {score}/100 (higher is better)

Suggest exactly two greener alternative materials or processes for this specific product.
For each one:
1. Name it.
2. Explain in plain English why it is greener (carbon, recyclability, energy use).
3. Be honest about practical trade-offs for this product (strength, cost, durability, how it is made).

Only suggest options that are realistic for this product. If the current material is already
one of the best choices, say so and suggest the most sensible small improvements instead.
Where it makes sense, prefer materials from this list: {', '.join(other_materials)}.
Keep the whole answer under 200 words, with no headings."""

    message = client.messages.create(
        model=MODEL,
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(b.text for b in message.content if getattr(b, "type", "") == "text")


# ------------------------------- Page ---------------------------------------
st.set_page_config(page_title="GreenSpec AI", page_icon="🌿", layout="centered")
st.markdown(CSS, unsafe_allow_html=True)
st.markdown(hero_html(), unsafe_allow_html=True)

materials_df = get_materials()
material_names = materials_df[COL_MATERIAL].tolist()

with st.form("product_form"):
    product = st.text_input("Product name", placeholder="e.g. Steel office chair")
    material = st.selectbox("Main material", material_names)
    process = st.selectbox("Manufacturing process", PROCESSES)
    country = st.selectbox("Country sold in", COUNTRIES)
    submitted = st.form_submit_button("Get my GreenSpec score")

if submitted:
    if not product.strip():
        st.warning("Enter a product name to continue.")
        st.stop()

    row = get_material_row(materials_df, material)
    if row is None:
        st.error(f"'{material}' is not in the materials database. Pick a material from the list.")
        st.stop()

    carbon = float(row[COL_CARBON])
    recycle = float(row[COL_RECYCLE])
    energy = float(row[COL_ENERGY])
    score = calculate_score(carbon, recycle, energy)
    rating = rating_label(score)

    # ---- Scorecard ----
    st.markdown(section_html("Your scorecard"), unsafe_allow_html=True)
    bars = [
        ("Low carbon", 10 - carbon),
        ("Recyclability", recycle),
        ("Low energy use", 10 - energy),
    ]
    st.markdown(
        scorecard_html(product.strip(), material, process, country, score, rating, bars),
        unsafe_allow_html=True,
    )

    with st.expander("How is the score calculated?"):
        st.write(
            f"Score = ({WEIGHTS['carbon']} x low-carbon + {WEIGHTS['recyclability']} x recyclability "
            f"+ {WEIGHTS['energy']} x low-energy) x 10. Carbon and energy are inverted "
            "(10 minus the impact score) so that a higher number is always better."
        )

    # ---- AI suggestions ----
    st.markdown(section_html("Greener alternatives"), unsafe_allow_html=True)
    with st.container(border=True):
        if not get_api_key():
            st.info("AI suggestions are switched off because no API key is set.")
        else:
            with st.spinner("Asking Claude for greener options..."):
                try:
                    others = [m for m in material_names if m != material]
                    st.write(
                        get_suggestions(product.strip(), material, process, country, score, others)
                    )
                except Exception as exc:
                    st.error(f"Could not get AI suggestions: {exc}")

    # ---- Regulations ----
    st.markdown(section_html("Regulations that may apply"), unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(f"**{country}**")
        for point in REGULATIONS[country]:
            st.markdown(f"- {point}")
    if country != INTERNATIONAL_KEY:
        with st.expander("International standards"):
            for point in REGULATIONS[INTERNATIONAL_KEY]:
                st.markdown(f"- {point}")
