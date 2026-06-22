# 🍺 DrinkStats — Global Alcohol EDA Dashboard

> A professional, premium-dark Streamlit dashboard for exploratory data analysis
> of global alcohol consumption across **193 countries**.

---

## 📌 Project Overview

DrinkStats is a fully interactive EDA dashboard built with **Streamlit**, **Pandas**,
**Matplotlib**, and **Seaborn**. It lets analysts explore beer, spirit, and wine
consumption patterns worldwide through dynamic filters, KPI cards, and eight
distinct chart types — all styled with a modern neon-dark premium theme.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🎨 Premium Dark UI | Custom CSS with gradient cards, neon glows, and rounded corners |
| 🔧 Dynamic Filters | Country search, range sliders for all 4 metrics, feature selector |
| 📊 Dashboard Overview | 5 KPI cards + Pie chart + Histogram + Top-15 Bar chart |
| 📈 Charts & Visualizations | 8 chart types selectable via multiselect widget |
| 🗂️ Dataset Explorer | Filtered table, descriptive stats, CSV download |
| ⚡ Real-time Updates | Every chart and KPI responds instantly to filter changes |
| ☁️ Deployment Ready | Compatible with Streamlit Community Cloud |

---

## 🛠️ Technologies Used

- **Python 3.10+**
- **Streamlit** — web app framework
- **Pandas** — data wrangling & filtering
- **NumPy** — numerical operations
- **Matplotlib** — chart rendering (Agg backend)
- **Seaborn** — statistical visualizations

---

## 📁 Project Structure

```
drinks_dashboard/
│
├── app.py            # Main entry point — page config, theme, layout, routing
├── filters.py        # Sidebar UI — navigation, all filters, filtered dataframe
├── charts.py         # Chart factory — one function per visualization
├── drinks.csv        # Source dataset (193 countries × 5 columns)
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

---

## ⚙️ Installation

```bash
# 1. Clone or download the project folder
git clone https://github.com/your-username/drinks-dashboard.git
cd drinks-dashboard

# 2. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Running the Project

```bash
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`.

---

## 📊 Dashboard Sections

### 1. Dashboard Overview
Provides a high-level summary with five KPI cards (country count, average beer /
spirit / wine servings, average pure alcohol), a donut pie chart showing beverage
category share, a histogram of beer serving distribution, and a horizontal bar
chart of the top-15 countries by alcohol consumption.

### 2. Charts & Visualizations
Users select which of the eight charts to display via a multiselect widget:

| Chart | Insight |
|---|---|
| Scatter Plot | Relationship between any two chosen metrics + trend line |
| Correlation Heatmap | Lower-triangle heatmap of selected numeric columns |
| Violin Plot | Distribution shape & density per beverage category |
| Count Plot | Countries bucketed into four consumption tiers |
| Box Plot | Spread, quartiles, and outliers per category |
| Line Chart | Metric trends across countries ranked by alcohol intake |
| Area Chart | Stacked beverage servings sorted by beer consumption |
| Bubble Chart | Beer vs Wine, bubble size = Spirit, colour = Pure Alcohol |

### 3. Dataset Explorer
Shows meta KPIs (rows, columns, selected features, missing values), a scrollable
filtered dataframe, descriptive statistics table, and a CSV download button.

---

## 💡 Insights

- **Beer dominates** globally — it accounts for the largest share of servings in
  most countries, especially in Europe and the Americas.
- **Wine consumption** is concentrated in a handful of Western European nations;
  most countries have very low wine servings.
- **Spirit servings** are highest in Eastern Europe and parts of Asia.
- There is a **strong positive correlation** between beer servings and total pure
  alcohol consumption (r ≈ 0.84).
- Many countries cluster near zero across all metrics, indicating large populations
  with abstinence-dominant cultures.

---

## ✅ Conclusion

DrinkStats demonstrates how a clean, modular Streamlit architecture can deliver
a professional analytics experience. The separation of concerns across `app.py`,
`filters.py`, and `charts.py` makes the codebase easy to extend — adding a new
chart requires only a new function in `charts.py` and a single line in `app.py`.

---

*Built for the University of Lahore · Embedded Systems Department · Spring 2026*
