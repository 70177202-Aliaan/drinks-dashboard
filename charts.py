# =============================================================================
# charts.py — All Chart / Visualization Functions
# =============================================================================
# Every function accepts a filtered dataframe (and optional column list) and
# returns a Matplotlib Figure ready for st.pyplot().  No Streamlit calls live
# inside these functions — they are pure chart factories.
# =============================================================================

import matplotlib
matplotlib.use("Agg")   # non-interactive backend — required for Streamlit

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# ── Shared palette & style ────────────────────────────────────────────────────

DARK_BG      = "#0e1117"
CARD_BG      = "#1a1f2e"
ACCENT_1     = "#7b2ff7"   # purple
ACCENT_2     = "#00d4ff"   # cyan
ACCENT_3     = "#ff6b6b"   # coral
ACCENT_4     = "#ffd166"   # gold
ACCENT_5     = "#06d6a0"   # mint
TEXT_PRIMARY = "#e8eaf0"
TEXT_MUTED   = "#8892a4"
GRID_COLOR   = "#2a2f3f"

PALETTE   = [ACCENT_1, ACCENT_2, ACCENT_3, ACCENT_4, ACCENT_5, "#ff9f43", "#a29bfe"]
NEON_CMAP = LinearSegmentedColormap.from_list("neon", [ACCENT_1, ACCENT_2, ACCENT_5])

# Pretty column labels (used on axes / legends)
COL_LABELS = {
    "beer_servings":               "Beer Servings",
    "spirit_servings":             "Spirit Servings",
    "wine_servings":               "Wine Servings",
    "total_litres_of_pure_alcohol":"Total Pure Alcohol (L)",
}


def _base_fig(rows=1, cols=1, h=5, w=10):
    """Return a figure + axes with the shared dark theme applied."""
    fig, ax = plt.subplots(rows, cols, figsize=(w, h))
    fig.patch.set_facecolor(DARK_BG)
    axes = [ax] if rows == 1 and cols == 1 else ax.flatten()
    for a in (axes if isinstance(axes, (list, np.ndarray)) else [axes]):
        a.set_facecolor(CARD_BG)
        a.tick_params(colors=TEXT_MUTED, labelsize=9)
        a.xaxis.label.set_color(TEXT_MUTED)
        a.yaxis.label.set_color(TEXT_MUTED)
        a.title.set_color(TEXT_PRIMARY)
        for spine in a.spines.values():
            spine.set_edgecolor(GRID_COLOR)
        a.grid(color=GRID_COLOR, linewidth=0.5, linestyle="--", alpha=0.6)
    return fig, ax


def _label(s: str) -> str:
    return COL_LABELS.get(s, s.replace("_", " ").title())


# ─────────────────────────────────────────────────────────────────────────────
# OVERVIEW PAGE CHARTS
# ─────────────────────────────────────────────────────────────────────────────

def pie_chart(df: pd.DataFrame) -> plt.Figure:
    """
    Donut-style pie chart showing the share of total servings contributed
    by beer, spirits, and wine across the filtered countries.
    """
    totals = {
        "Beer":    df["beer_servings"].sum(),
        "Spirits": df["spirit_servings"].sum(),
        "Wine":    df["wine_servings"].sum(),
    }
    labels = list(totals.keys())
    sizes  = list(totals.values())
    colors = [ACCENT_1, ACCENT_2, ACCENT_5]

    fig, ax = _base_fig(h=5, w=6)
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=None,
        autopct="%1.1f%%",
        colors=colors,
        startangle=140,
        wedgeprops=dict(width=0.55, edgecolor=DARK_BG, linewidth=2),
        pctdistance=0.75,
    )
    for at in autotexts:
        at.set_color(TEXT_PRIMARY)
        at.set_fontsize(10)
        at.set_fontweight("bold")

    legend_patches = [mpatches.Patch(color=c, label=l) for c, l in zip(colors, labels)]
    ax.legend(
        handles=legend_patches,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.08),
        ncol=3,
        frameon=False,
        labelcolor=TEXT_PRIMARY,
        fontsize=9,
    )
    ax.set_title("Beverage Category Share", fontsize=13, fontweight="bold", pad=14)
    fig.tight_layout()
    return fig


def histogram_chart(df: pd.DataFrame, col: str = "beer_servings") -> plt.Figure:
    """
    Histogram with a KDE overlay for the chosen numeric column.
    """
    fig, ax = _base_fig(h=4.5, w=8)
    ax.set_facecolor(CARD_BG)
    data = df[col].dropna()

    ax.hist(data, bins=25, color=ACCENT_1, edgecolor=DARK_BG, linewidth=0.6, alpha=0.8, label="Count")
    ax2 = ax.twinx()
    ax2.set_facecolor(CARD_BG)
    ax2.tick_params(colors=TEXT_MUTED, labelsize=8)
    sns.kdeplot(data=data, ax=ax2, color=ACCENT_2, linewidth=2, label="KDE", fill=False)
    ax2.set_ylabel("Density", color=TEXT_MUTED, fontsize=9)
    ax2.set_ylim(bottom=0)
    for spine in ax2.spines.values():
        spine.set_edgecolor(GRID_COLOR)

    ax.set_xlabel(_label(col), fontsize=10)
    ax.set_ylabel("Number of Countries", fontsize=10)
    ax.set_title(f"Distribution of {_label(col)}", fontsize=13, fontweight="bold")
    fig.tight_layout()
    return fig


def bar_chart(df: pd.DataFrame, top_n: int = 15) -> plt.Figure:
    """
    Horizontal bar chart — Top N countries by total pure alcohol consumption.
    """
    top = (
        df[["country", "total_litres_of_pure_alcohol"]]
        .sort_values("total_litres_of_pure_alcohol", ascending=True)
        .tail(top_n)
    )

    fig, ax = _base_fig(h=max(4.5, top_n * 0.35), w=9)
    bar_colors = [PALETTE[i % len(PALETTE)] for i in range(len(top))]
    bars = ax.barh(top["country"], top["total_litres_of_pure_alcohol"],
                   color=bar_colors, edgecolor=DARK_BG, linewidth=0.4, height=0.65)

    # Value labels
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.05, bar.get_y() + bar.get_height() / 2,
                f"{w:.1f}", va="center", ha="left", color=TEXT_PRIMARY, fontsize=8)

    ax.set_xlabel("Total Litres of Pure Alcohol", fontsize=10)
    ax.set_title(f"Top {top_n} Countries · Total Pure Alcohol", fontsize=13, fontweight="bold")
    ax.tick_params(axis="y", labelsize=8.5)
    fig.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# CHARTS & VISUALIZATIONS PAGE
# ─────────────────────────────────────────────────────────────────────────────

def scatter_chart(df: pd.DataFrame,
                  x_col: str = "beer_servings",
                  y_col: str = "total_litres_of_pure_alcohol") -> plt.Figure:
    """
    Scatter plot with a linear regression trend line.
    """
    fig, ax = _base_fig(h=5, w=8)
    x, y = df[x_col].dropna(), df[y_col].dropna()
    common = df[[x_col, y_col]].dropna()

    ax.scatter(common[x_col], common[y_col],
               color=ACCENT_2, alpha=0.7, edgecolors=DARK_BG, linewidth=0.4, s=50, zorder=3)

    # Trend line
    if len(common) > 2:
        m, b = np.polyfit(common[x_col], common[y_col], 1)
        x_line = np.linspace(common[x_col].min(), common[x_col].max(), 200)
        ax.plot(x_line, m * x_line + b, color=ACCENT_3, linewidth=1.8, linestyle="--", label="Trend")
        ax.legend(frameon=False, labelcolor=TEXT_PRIMARY, fontsize=9)

    ax.set_xlabel(_label(x_col), fontsize=10)
    ax.set_ylabel(_label(y_col), fontsize=10)
    ax.set_title(f"{_label(x_col)} vs {_label(y_col)}", fontsize=13, fontweight="bold")
    fig.tight_layout()
    return fig


def heatmap_chart(df: pd.DataFrame, selected_cols: list) -> plt.Figure:
    """
    Correlation heatmap of the selected numeric columns.
    """
    corr = df[selected_cols].corr()
    labels = [_label(c) for c in selected_cols]

    fig, ax = _base_fig(h=5, w=6)
    mask = np.zeros_like(corr, dtype=bool)
    mask[np.triu_indices_from(mask)] = True   # upper triangle → blank

    sns.heatmap(
        corr,
        ax=ax,
        mask=mask,
        annot=True,
        fmt=".2f",
        cmap=NEON_CMAP,
        linewidths=1,
        linecolor=DARK_BG,
        cbar_kws={"shrink": 0.7},
        xticklabels=labels,
        yticklabels=labels,
    )
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right", fontsize=8.5, color=TEXT_MUTED)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=8.5, color=TEXT_MUTED)
    ax.set_title("Correlation Heatmap", fontsize=13, fontweight="bold")
    fig.tight_layout()
    return fig


def violin_chart(df: pd.DataFrame, selected_cols: list) -> plt.Figure:
    """
    Violin plots of all selected numeric columns, displayed side-by-side.
    """
    melted = df[selected_cols].melt(var_name="Beverage", value_name="Servings")
    melted["Beverage"] = melted["Beverage"].map(_label)

    fig, ax = _base_fig(h=5.5, w=max(7, len(selected_cols) * 2.2))
    sns.violinplot(
        data=melted, x="Beverage", y="Servings", hue="Beverage",
        ax=ax, palette=PALETTE[:len(selected_cols)],
        inner="quartile", linewidth=1.2, cut=0, legend=False,
    )
    ax.set_xlabel("Beverage Category", fontsize=10)
    ax.set_ylabel("Servings / Litres", fontsize=10)
    ax.set_title("Distribution Shape per Beverage Type (Violin)", fontsize=13, fontweight="bold")
    ax.set_xticks(range(len(ax.get_xticklabels())))
    ax.set_xticklabels(ax.get_xticklabels(), rotation=15, ha="right", fontsize=9)
    fig.tight_layout()
    return fig


def count_chart(df: pd.DataFrame) -> plt.Figure:
    """
    Count-plot style chart: number of countries bucketed into alcohol
    consumption tiers (Low / Medium / High / Very High).
    """
    bins   = [-0.01, 2.5, 5.0, 8.0, 100]
    labels = ["Low (0–2.5)", "Medium (2.5–5)", "High (5–8)", "Very High (>8)"]
    tier_col = pd.cut(df["total_litres_of_pure_alcohol"], bins=bins, labels=labels)
    counts = tier_col.value_counts().reindex(labels, fill_value=0)

    fig, ax = _base_fig(h=4.5, w=7)
    bar_colors = [ACCENT_5, ACCENT_4, ACCENT_3, ACCENT_1]
    bars = ax.bar(counts.index, counts.values,
                  color=bar_colors, edgecolor=DARK_BG, linewidth=0.5, width=0.55)

    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.5,
                str(int(h)), ha="center", va="bottom", color=TEXT_PRIMARY, fontsize=10, fontweight="bold")

    ax.set_xlabel("Consumption Tier", fontsize=10)
    ax.set_ylabel("Number of Countries", fontsize=10)
    ax.set_title("Countries by Alcohol Consumption Tier", fontsize=13, fontweight="bold")
    ax.set_xticks(range(len(counts.index)))
    ax.set_xticklabels(counts.index, fontsize=9)
    fig.tight_layout()
    return fig


def box_chart(df: pd.DataFrame, selected_cols: list) -> plt.Figure:
    """
    Side-by-side box plots for each selected numeric column.
    """
    melted = df[selected_cols].melt(var_name="Beverage", value_name="Servings")
    melted["Beverage"] = melted["Beverage"].map(_label)

    fig, ax = _base_fig(h=5, w=max(7, len(selected_cols) * 2.2))
    sns.boxplot(
        data=melted, x="Beverage", y="Servings", hue="Beverage", ax=ax,
        palette=PALETTE[:len(selected_cols)], legend=False,
        flierprops=dict(marker="o", markersize=4, alpha=0.5, color=ACCENT_3),
        linewidth=1.2,
    )
    ax.set_xlabel("Beverage Category", fontsize=10)
    ax.set_ylabel("Servings / Litres", fontsize=10)
    ax.set_title("Box Plot — Spread & Outliers", fontsize=13, fontweight="bold")
    ax.set_xticks(range(len(ax.get_xticklabels())))
    ax.set_xticklabels(ax.get_xticklabels(), rotation=15, ha="right", fontsize=9)
    fig.tight_layout()
    return fig


def line_chart(df: pd.DataFrame, selected_cols: list) -> plt.Figure:
    """
    Line chart showing each selected metric ranked by total pure alcohol.
    X-axis represents countries sorted by alcohol consumption (rank).
    """
    sorted_df = df.sort_values("total_litres_of_pure_alcohol").reset_index(drop=True)

    fig, ax = _base_fig(h=5, w=10)
    for col, color in zip(selected_cols, PALETTE):
        ax.plot(sorted_df.index, sorted_df[col], label=_label(col),
                color=color, linewidth=1.6, alpha=0.9)

    ax.set_xlabel("Countries (sorted by alcohol consumption ↑)", fontsize=10)
    ax.set_ylabel("Servings / Litres", fontsize=10)
    ax.set_title("Consumption Trends Across Countries (Ranked)", fontsize=13, fontweight="bold")
    ax.legend(frameon=False, labelcolor=TEXT_PRIMARY, fontsize=9,
              loc="upper left", ncol=min(2, len(selected_cols)))
    fig.tight_layout()
    return fig


def area_chart(df: pd.DataFrame) -> plt.Figure:
    """
    Stacked area chart — cumulative beverage servings sorted by beer servings.
    Gives a feel for how drink categories layer on top of each other.
    """
    sorted_df = df.sort_values("beer_servings").reset_index(drop=True)

    fig, ax = _base_fig(h=5, w=10)
    cols   = ["beer_servings", "spirit_servings", "wine_servings"]
    colors = [ACCENT_1, ACCENT_2, ACCENT_5]

    ax.stackplot(
        sorted_df.index,
        [sorted_df[c] for c in cols],
        labels=[_label(c) for c in cols],
        colors=colors,
        alpha=0.75,
    )
    ax.set_xlabel("Countries (sorted by beer servings ↑)", fontsize=10)
    ax.set_ylabel("Cumulative Servings", fontsize=10)
    ax.set_title("Stacked Area — Beverage Servings per Country", fontsize=13, fontweight="bold")
    ax.legend(frameon=False, labelcolor=TEXT_PRIMARY, fontsize=9, loc="upper left")
    fig.tight_layout()
    return fig


def bubble_chart(df: pd.DataFrame) -> plt.Figure:
    """
    Bubble chart: beer servings vs wine servings, bubble size = spirit servings.
    Top-10 countries by total alcohol are labelled.
    """
    top10 = df.nlargest(10, "total_litres_of_pure_alcohol")

    fig, ax = _base_fig(h=5.5, w=9)
    sc = ax.scatter(
        df["beer_servings"], df["wine_servings"],
        s=df["spirit_servings"] * 0.7 + 5,
        c=df["total_litres_of_pure_alcohol"],
        cmap=NEON_CMAP, alpha=0.65, edgecolors=DARK_BG, linewidth=0.4,
    )
    cbar = fig.colorbar(sc, ax=ax, shrink=0.8)
    cbar.set_label("Total Pure Alcohol (L)", color=TEXT_MUTED, fontsize=8)
    cbar.ax.yaxis.set_tick_params(color=TEXT_MUTED, labelcolor=TEXT_MUTED)

    for _, row in top10.iterrows():
        ax.annotate(row["country"],
                    xy=(row["beer_servings"], row["wine_servings"]),
                    fontsize=7.5, color=TEXT_PRIMARY, alpha=0.85,
                    xytext=(4, 4), textcoords="offset points")

    ax.set_xlabel("Beer Servings", fontsize=10)
    ax.set_ylabel("Wine Servings", fontsize=10)
    ax.set_title("Bubble Chart · Beer vs Wine (size = Spirit Servings)", fontsize=13, fontweight="bold")
    fig.tight_layout()
    return fig
