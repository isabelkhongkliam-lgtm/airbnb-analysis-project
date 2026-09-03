# Exploratory Data Analysis of Airbnb Listings

A descriptive (non-predictive) EDA of a multi-city Airbnb dataset — 4,046 listings
across 9 countries and 13 cities. The project characterises the data, studies the
distributions of price, availability, reviews and ratings, and measures the
relationships among the numerical variables.

## How to run

**In VS Code (recommended)**

1. Open this folder in VS Code.
2. Open `airbnb_eda.ipynb` and select a Python kernel when prompted.
3. Click **Run All**. Figures are (re)written to `figures/` as the cells execute.

The notebook is delivered already executed, so every chart and table is visible
without running anything.

**From the terminal**

```bash
pip install -r requirements.txt
python airbnb_eda_src.py        # runs the same analysis as a plain script
python report_gen.py            # rebuilds report/Airbnb_EDA_Report.pdf
```

## Project structure

```
airbnb_eda/
├── airbnb_eda.ipynb            # main deliverable — the executed EDA notebook
├── airbnb_eda_src.py           # the notebook's paired source (jupytext "percent" format)
├── report_gen.py               # regenerates the PDF report from the figures
├── requirements.txt
├── README.md
├── data/
│   ├── airbnb_dataset.csv          # the original dataset (as provided)
│   ├── airbnb_cleaned.csv          # cleaned + feature-engineered dataset
│   └── descriptive_statistics.csv  # summary statistics table
├── figures/                    # 16 generated PNG charts (fig01 … fig16)
└── report/
    └── Airbnb_EDA_Report.pdf   # the written report (15 pages)
```

## Note on adapting the generic EDA brief to this dataset

The standard EDA guide assumes single-city columns such as `room_type`,
`minimum_nights`, `neighbourhood` and `reviews_per_month`. **This dataset contains
none of those.** The analysis therefore substitutes, and documents, the following:

| Guide assumes | Used here instead |
|---|---|
| `room_type` | `city` / `country` (the geographic categorical driver) |
| `minimum_nights` | availability windows + `review_score` |
| `reviews_per_month` | `no_of_reviews` |
| `neighbourhood` | `city` (+ `latitude` / `longitude`) |
| "host listings count" | engineered `host_listings_count` (listings per host) |
| — | engineered `amenities_count` (amenities per listing) |

## Headline findings

- **Price is right-skewed** — median **$120** vs a mean of **$225**; medians are used throughout.
- **Location dominates price** — median city price ranges more than ten-fold, from
  **$55 (Porto)** to **$573 (Hong Kong)**.
- **Numeric attributes barely relate to price** — every correlation with price is
  **|r| < 0.08** (strongest is `no_of_reviews` at −0.079).
- **Ratings show a ceiling effect** — **88.4%** of listings score 9 or above.
- Data quality is high: **no missing values, no duplicates**.

- ## Results & Insights

- **Price distribution:** Prices are heavily right‑skewed, with a median of $120 compared to a mean of $225. Using medians avoids distortion from extreme outliers.  
- **Location impact:** City and country dominate pricing. Median city prices vary more than ten‑fold, from $55 in Porto to $573 in Hong Kong.  
- **Weak numeric correlations:** Price shows almost no linear relationship with numeric attributes — the strongest correlation is with number of reviews (r = −0.079).  
- **Ratings ceiling effect:** 88.4% of listings score 9 or above, suggesting limited variance in review scores.  
- **Data quality:** The dataset is clean — no missing values, no duplicates, and engineered features (host_listings_count, amenities_count) add useful context.  
- **Visual highlights:**  
  - Distribution plots reveal strong skewness in price and review counts.  
  - Geographic scatter plots show clustering of listings in major urban centers.  
  - Heatmaps confirm weak correlations among most numeric variables.

