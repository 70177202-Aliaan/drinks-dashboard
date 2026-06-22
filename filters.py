# =============================================================================
# filters.py — Sidebar Filters & Data Filtering Logic
# =============================================================================
# Contains all sidebar UI elements and returns a filtered dataframe
# based on user selections. Every chart and KPI in the dashboard reads
# from the dataframe returned by apply_filters().
# =============================================================================

import streamlit as st
import pandas as pd


# ── Sidebar branding ─────────────────────────────────────────────────────────

def render_sidebar_header():
    """Render the project logo, title, and description in the sidebar."""
    st.sidebar.markdown(
        """
        <div class="sidebar-header">
            <div class="logo-icon">🍺</div>
            <h1 class="sidebar-title">DrinkStats</h1>
            <p class="sidebar-subtitle">Global Alcohol EDA</p>
        </div>
        <div class="sidebar-description">
            Explore alcohol consumption patterns across <strong>193 countries</strong>.
            Analyse beer, spirit, and wine servings alongside total pure alcohol intake.
        </div>
        <hr class="sidebar-divider">
        """,
        unsafe_allow_html=True,
    )


# ── Navigation ────────────────────────────────────────────────────────────────

def render_navigation():
    """Render the radio-button navigation menu and return the selected page."""
    st.sidebar.markdown('<p class="sidebar-section-label">📌 NAVIGATION</p>', unsafe_allow_html=True)
    page = st.sidebar.radio(
        label="Go to",
        options=["📊 Dashboard Overview", "📈 Charts & Visualizations", "🗂️ Dataset Explorer"],
        label_visibility="collapsed",
        key="nav_radio",
    )
    st.sidebar.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    return page


# ── Filters ───────────────────────────────────────────────────────────────────

def apply_filters(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """
    Render all sidebar filters and return:
      - filtered_df  : dataframe after applying every active filter
      - selected_cols: list of numeric columns the user wants to analyse
    """
    st.sidebar.markdown('<p class="sidebar-section-label">🔧 FILTERS</p>', unsafe_allow_html=True)

    # ── 1. Country search box ────────────────────────────────────────────────
    search_term = st.sidebar.text_input(
        "🔍 Search Country",
        placeholder="e.g. France",
        key="country_search",
    )

    # ── 2. Beer servings range slider ────────────────────────────────────────
    beer_min, beer_max = int(df["beer_servings"].min()), int(df["beer_servings"].max())
    beer_range = st.sidebar.slider(
        "🍺 Beer Servings Range",
        min_value=beer_min,
        max_value=beer_max,
        value=(beer_min, beer_max),
        step=1,
        key="beer_slider",
    )

    # ── 3. Spirit servings range slider ──────────────────────────────────────
    spirit_min, spirit_max = int(df["spirit_servings"].min()), int(df["spirit_servings"].max())
    spirit_range = st.sidebar.slider(
        "🥃 Spirit Servings Range",
        min_value=spirit_min,
        max_value=spirit_max,
        value=(spirit_min, spirit_max),
        step=1,
        key="spirit_slider",
    )

    # ── 4. Wine servings range slider ────────────────────────────────────────
    wine_min, wine_max = int(df["wine_servings"].min()), int(df["wine_servings"].max())
    wine_range = st.sidebar.slider(
        "🍷 Wine Servings Range",
        min_value=wine_min,
        max_value=wine_max,
        value=(wine_min, wine_max),
        step=1,
        key="wine_slider",
    )

    # ── 5. Total alcohol range slider ────────────────────────────────────────
    alc_min = float(df["total_litres_of_pure_alcohol"].min())
    alc_max = float(df["total_litres_of_pure_alcohol"].max())
    alc_range = st.sidebar.slider(
        "🔬 Total Pure Alcohol (L)",
        min_value=alc_min,
        max_value=alc_max,
        value=(alc_min, alc_max),
        step=0.1,
        key="alc_slider",
    )

    st.sidebar.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    # ── 6. Feature selector (numeric columns only) ───────────────────────────
    st.sidebar.markdown('<p class="sidebar-section-label">📐 FEATURE SELECTOR</p>', unsafe_allow_html=True)
    numeric_cols = ["beer_servings", "spirit_servings", "wine_servings", "total_litres_of_pure_alcohol"]
    selected_cols = st.sidebar.multiselect(
        "Select features to analyse",
        options=numeric_cols,
        default=numeric_cols,
        key="feature_select",
    )
    if not selected_cols:
        selected_cols = numeric_cols  # fallback — never allow an empty selection

    st.sidebar.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.sidebar.markdown(
        '<p style="color:#555;font-size:0.75rem;text-align:center;">Built with ❤️ · Streamlit · Seaborn</p>',
        unsafe_allow_html=True,
    )

    # ── Apply filters ─────────────────────────────────────────────────────────
    filtered = df.copy()

    if search_term:
        filtered = filtered[
            filtered["country"].str.contains(search_term, case=False, na=False)
        ]

    filtered = filtered[
        (filtered["beer_servings"] >= beer_range[0])
        & (filtered["beer_servings"] <= beer_range[1])
        & (filtered["spirit_servings"] >= spirit_range[0])
        & (filtered["spirit_servings"] <= spirit_range[1])
        & (filtered["wine_servings"] >= wine_range[0])
        & (filtered["wine_servings"] <= wine_range[1])
        & (filtered["total_litres_of_pure_alcohol"] >= alc_range[0])
        & (filtered["total_litres_of_pure_alcohol"] <= alc_range[1])
    ]

    return filtered, selected_cols
