# =============================================================================
# app.py — DrinkStats EDA Dashboard · Main Entry Point
# =============================================================================
# Responsibilities:
#   • Page configuration & global CSS theme
#   • Load dataset
#   • Render sidebar (via filters.py)
#   • Route to the correct page
#   • Render KPI cards and call chart functions (from charts.py)
# =============================================================================

import streamlit as st
import pandas as pd

from filters import render_sidebar_header, render_navigation, apply_filters
import charts as ch

# ─────────────────────────────────────────────────────────────────────────────
# 1. PAGE CONFIGURATION  (must be the very first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="DrinkStats · Global Alcohol EDA",
    page_icon="🍺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# 2. GLOBAL THEME  (dark premium CSS injected once)
# ─────────────────────────────────────────────────────────────────────────────

THEME_CSS = """
<style>
/* ── Base ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0e1117 !important;
    color: #e8eaf0 !important;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}
[data-testid="stHeader"] { background: transparent !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #12172b 0%, #0e1117 100%) !important;
    border-right: 1px solid #1e2540;
}
.sidebar-header   { text-align: center; padding: 1.2rem 0 0.5rem; }
.logo-icon        { font-size: 3rem; line-height: 1; }
.sidebar-title    { font-size: 1.6rem; font-weight: 800; margin: 0.3rem 0 0;
                    background: linear-gradient(135deg, #7b2ff7, #00d4ff);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.sidebar-subtitle { font-size: 0.78rem; color: #556; margin: 0; letter-spacing: 2px; text-transform: uppercase; }
.sidebar-description { font-size: 0.82rem; color: #8892a4; padding: 0.8rem 1rem;
                        background: #1a1f2e; border-radius: 10px; margin: 0.8rem 0; }
.sidebar-divider  { border: none; border-top: 1px solid #1e2540; margin: 0.8rem 0; }
.sidebar-section-label { font-size: 0.68rem; letter-spacing: 2px; color: #7b2ff7;
                          text-transform: uppercase; font-weight: 700; margin: 0.6rem 0 0.2rem; }

/* ── Radio buttons ── */
[data-testid="stRadio"] > div { gap: 0.3rem !important; }
[data-testid="stRadio"] label {
    background: #1a1f2e; border-radius: 8px; padding: 0.45rem 0.9rem;
    font-size: 0.88rem; color: #c5cae9; cursor: pointer;
    transition: background 0.2s;
}
[data-testid="stRadio"] label:hover  { background: #252d42; }

/* ── KPI Cards ── */
.kpi-grid { display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 1.4rem; }
.kpi-card {
    flex: 1; min-width: 160px;
    background: linear-gradient(135deg, #1a1f2e 0%, #12172b 100%);
    border: 1px solid #2a2f3f;
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    position: relative; overflow: hidden;
    box-shadow: 0 0 18px rgba(0,0,0,0.5);
}
.kpi-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: var(--accent, linear-gradient(90deg,#7b2ff7,#00d4ff));
    border-radius: 14px 14px 0 0;
}
.kpi-icon  { font-size: 1.5rem; margin-bottom: 0.4rem; }
.kpi-label { font-size: 0.72rem; color: #8892a4; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 0.25rem; }
.kpi-value { font-size: 1.9rem; font-weight: 800; color: #e8eaf0; line-height: 1; }
.kpi-sub   { font-size: 0.75rem; color: #556; margin-top: 0.2rem; }
/* Per-card accent colours */
.kpi-purple::before { background: linear-gradient(90deg,#7b2ff7,#a29bfe); }
.kpi-cyan::before   { background: linear-gradient(90deg,#00d4ff,#06d6a0); }
.kpi-coral::before  { background: linear-gradient(90deg,#ff6b6b,#ffd166); }
.kpi-gold::before   { background: linear-gradient(90deg,#ffd166,#ff9f43); }
.kpi-mint::before   { background: linear-gradient(90deg,#06d6a0,#00d4ff); }

/* ── Section headers ── */
.section-header {
    font-size: 1.4rem; font-weight: 700; margin: 0.4rem 0 1rem;
    border-left: 4px solid #7b2ff7; padding-left: 0.8rem;
    color: #e8eaf0;
}

/* ── Chart containers ── */
[data-testid="stPlotlyChart"],
[data-testid="stImage"] { border-radius: 12px; overflow: hidden; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 12px; border: 1px solid #2a2f3f; overflow: hidden;
    background: #1a1f2e;
}

/* ── Multiselect tags ── */
[data-baseweb="tag"] { background: #7b2ff720 !important; border: 1px solid #7b2ff7 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0e1117; }
::-webkit-scrollbar-thumb { background: #2a2f3f; border-radius: 3px; }
</style>
"""

st.markdown(THEME_CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 3. LOAD DATA
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data
def load_data() -> pd.DataFrame:
    """Load the drinks dataset once and cache it."""
    return pd.read_csv("drinks.csv")


df_raw = load_data()

# ─────────────────────────────────────────────────────────────────────────────
# 4. SIDEBAR  (logo → navigation → filters)
# ─────────────────────────────────────────────────────────────────────────────

render_sidebar_header()
page = render_navigation()
df, selected_cols = apply_filters(df_raw)

# ─────────────────────────────────────────────────────────────────────────────
# 5. HELPER  — KPI card HTML builder
# ─────────────────────────────────────────────────────────────────────────────

def kpi_card(icon: str, label: str, value: str, sub: str = "", accent_cls: str = "kpi-purple") -> str:
    """Return an HTML string for a single KPI card."""
    return f"""
    <div class="kpi-card {accent_cls}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>"""


# ─────────────────────────────────────────────────────────────────────────────
# 6. PAGE ROUTING
# ─────────────────────────────────────────────────────────────────────────────

# ── 6A. DASHBOARD OVERVIEW ───────────────────────────────────────────────────

if page == "📊 Dashboard Overview":

    st.markdown('<div class="section-header">📊 Dashboard Overview</div>', unsafe_allow_html=True)

    # ── KPI row ──────────────────────────────────────────────────────────────
    n_countries      = len(df)
    avg_beer         = df["beer_servings"].mean()
    avg_spirit       = df["spirit_servings"].mean()
    avg_wine         = df["wine_servings"].mean()
    avg_alc          = df["total_litres_of_pure_alcohol"].mean()

    kpis_html = (
        '<div class="kpi-grid">'
        + kpi_card("🌍", "Countries", f"{n_countries}", "after filters", "kpi-purple")
        + kpi_card("🍺", "Avg Beer Servings", f"{avg_beer:.1f}", "per country", "kpi-cyan")
        + kpi_card("🥃", "Avg Spirit Servings", f"{avg_spirit:.1f}", "per country", "kpi-coral")
        + kpi_card("🍷", "Avg Wine Servings", f"{avg_wine:.1f}", "per country", "kpi-gold")
        + kpi_card("🔬", "Avg Pure Alcohol (L)", f"{avg_alc:.2f}", "per country", "kpi-mint")
        + "</div>"
    )
    st.markdown(kpis_html, unsafe_allow_html=True)

    # ── Charts — row 1 ───────────────────────────────────────────────────────
    col1, col2 = st.columns([1, 1.8], gap="medium")

    with col1:
        st.markdown("##### 🍩 Beverage Category Share")
        if len(df) > 0:
            st.pyplot(ch.pie_chart(df), use_container_width=True)
        else:
            st.info("No data for the current filter selection.")

    with col2:
        st.markdown("##### 📊 Beer Servings Distribution")
        if len(df) > 0:
            st.pyplot(ch.histogram_chart(df, col="beer_servings"), use_container_width=True)
        else:
            st.info("No data for the current filter selection.")

    st.markdown("---")

    # ── Charts — row 2 ───────────────────────────────────────────────────────
    st.markdown("##### 🏆 Top 15 Countries · Total Pure Alcohol")
    if len(df) >= 3:
        st.pyplot(ch.bar_chart(df, top_n=min(15, len(df))), use_container_width=True)
    else:
        st.info("Filter too narrow — need at least 3 countries for the bar chart.")


# ── 6B. CHARTS & VISUALIZATIONS ──────────────────────────────────────────────

elif page == "📈 Charts & Visualizations":

    st.markdown('<div class="section-header">📈 Charts & Visualizations</div>', unsafe_allow_html=True)

    # Multiselect to pick which charts to show
    CHART_OPTIONS = [
        "Scatter Plot",
        "Correlation Heatmap",
        "Violin Plot",
        "Count Plot",
        "Box Plot",
        "Line Chart",
        "Area Chart",
        "Bubble Chart",
    ]
    chosen_charts = st.multiselect(
        "Select charts to display",
        options=CHART_OPTIONS,
        default=CHART_OPTIONS,
        key="chart_multiselect",
    )

    if len(df) < 2:
        st.warning("⚠️ Too few countries match the current filters. Relax the sliders to see charts.")
        st.stop()

    # Guard: need at least 2 selected numeric cols for multi-col charts
    safe_cols = selected_cols if len(selected_cols) >= 2 else ["beer_servings", "spirit_servings"]

    # Render each chosen chart
    for chart_name in chosen_charts:

        st.markdown(f"#### {chart_name}")

        if chart_name == "Scatter Plot":
            c1, c2 = st.columns(2)
            with c1:
                x_opt = st.selectbox("X axis", options=selected_cols,
                                     index=0, key="scatter_x")
            with c2:
                y_opt = st.selectbox("Y axis", options=selected_cols,
                                     index=min(3, len(selected_cols)-1), key="scatter_y")
            st.pyplot(ch.scatter_chart(df, x_col=x_opt, y_col=y_opt), use_container_width=True)

        elif chart_name == "Correlation Heatmap":
            if len(safe_cols) < 2:
                st.info("Select at least 2 features in the sidebar to show a heatmap.")
            else:
                st.pyplot(ch.heatmap_chart(df, selected_cols=safe_cols), use_container_width=True)

        elif chart_name == "Violin Plot":
            st.pyplot(ch.violin_chart(df, selected_cols=safe_cols), use_container_width=True)

        elif chart_name == "Count Plot":
            st.pyplot(ch.count_chart(df), use_container_width=True)

        elif chart_name == "Box Plot":
            st.pyplot(ch.box_chart(df, selected_cols=safe_cols), use_container_width=True)

        elif chart_name == "Line Chart":
            st.pyplot(ch.line_chart(df, selected_cols=safe_cols), use_container_width=True)

        elif chart_name == "Area Chart":
            st.pyplot(ch.area_chart(df), use_container_width=True)

        elif chart_name == "Bubble Chart":
            st.pyplot(ch.bubble_chart(df), use_container_width=True)

        st.markdown("---")


# ── 6C. DATASET EXPLORER ─────────────────────────────────────────────────────

elif page == "🗂️ Dataset Explorer":

    st.markdown('<div class="section-header">🗂️ Dataset Explorer</div>', unsafe_allow_html=True)

    # Meta KPIs
    meta_html = (
        '<div class="kpi-grid">'
        + kpi_card("📋", "Rows", f"{len(df)}", "after filters", "kpi-purple")
        + kpi_card("📐", "Columns", f"{len(df.columns)}", "total dataset", "kpi-cyan")
        + kpi_card("✅", "Selected Features", f"{len(selected_cols)}", "from sidebar", "kpi-coral")
        + kpi_card("🚫", "Missing Values", f"{df.isnull().sum().sum()}", "in filtered data", "kpi-gold")
        + "</div>"
    )
    st.markdown(meta_html, unsafe_allow_html=True)

    # Scrollable filtered dataframe
    st.markdown("##### 🔍 Filtered Data Table")
    display_cols = ["country"] + selected_cols
    st.dataframe(
        df[display_cols].reset_index(drop=True),
        use_container_width=True,
        height=430,
    )

    # Descriptive statistics
    st.markdown("##### 📊 Descriptive Statistics (filtered)")
    st.dataframe(
        df[selected_cols].describe().T.style.format("{:.2f}"),
        use_container_width=True,
    )

    # Download button
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv_bytes,
        file_name="drinks_filtered.csv",
        mime="text/csv",
    )
