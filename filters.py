# =============================================================================
# filters.py — Sidebar Filters & Data Filtering Logic
# =============================================================================
# Contains all sidebar UI elements and returns a filtered dataframe
# based on user selections. Every chart and KPI in the dashboard reads
# from the dataframe returned by apply_filters().
# =============================================================================

from __future__ import annotations          # FIX 1: makes all type hints strings at
                                            # runtime — required for Python < 3.9 compat.
                                            # Without this, tuple[...] crashes on import.

import streamlit as st
import pandas as pd
from typing import Tuple, List             # FIX 2: use typing module as extra safety net


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

# FIX 3: Changed return type from tuple[pd.DataFrame, list[str]]
#         to Tuple[pd.DataFrame, List[str]] — works on ALL Python versions
def apply_filters(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
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
    # FIX 4: Guard against min == max (e.g. after heavy filtering) — slider
    #         crashes with a Streamlit error when min_value == max_value
    if beer_min == beer_max:
        beer_max = beer_min + 1
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
    if spirit_min == spirit_max:          # FIX 4 (same guard)
        spirit_max = spirit_min + 1
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
    if wine_min == wine_max:              # FIX 4 (same guard)
        wine_max = wine_min + 1
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
    # FIX 5: Round to 1 decimal to avoid floating-point precision issues
    #         where min/max look different but are actually equal (e.g. 0.0 vs 0.000001)
    alc_min = round(alc_min, 1)
    alc_max = round(alc_max, 1)
    if alc_min == alc_max:                # FIX 4 (same guard for float slider)
        alc_max = round(alc_min + 0.1, 1)
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
        selected_cols = numeric_cols  # FIX 6: fallback — never allow empty selection
                                      # (was already present but documented here clearly)

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
