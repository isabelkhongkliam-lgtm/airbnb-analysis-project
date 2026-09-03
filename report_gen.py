"""Generate the Airbnb EDA PDF report with reportlab (offline)."""
from pathlib import Path
from PIL import Image as PILImage
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                PageBreak, Table, TableStyle, KeepTogether,
                                ListFlowable, ListItem, HRFlowable)

FIG = Path("figures")
OUT = "report/Airbnb_EDA_Report.pdf"
INK = colors.HexColor("#12313F")
BLUE = colors.HexColor("#2A6F97")
LIGHT = colors.HexColor("#EAF2F6")
GREY = colors.HexColor("#5B6B73")

USABLE_W = letter[0] - 2 * 0.9 * inch

# ---------- styles ----------
ss = getSampleStyleSheet()
def S(name, parent=None, **kw):
    return ParagraphStyle(name, parent=parent or ss["Normal"], **kw)

body = S("body", fontName="Helvetica", fontSize=10.3, leading=15.5,
         alignment=TA_JUSTIFY, spaceAfter=8, textColor=colors.HexColor("#1A1A1A"))
h1 = S("h1", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=INK,
       spaceBefore=16, spaceAfter=7)
h2 = S("h2", fontName="Helvetica-Bold", fontSize=12, leading=16, textColor=BLUE,
       spaceBefore=10, spaceAfter=5)
caption = S("cap", fontName="Helvetica-Oblique", fontSize=8.8, leading=11.5,
            textColor=GREY, alignment=TA_CENTER, spaceAfter=10, spaceBefore=3)
oii = S("oii", parent=body, fontSize=9.9, leading=14.5, spaceAfter=5,
        leftIndent=8)
title = S("title", fontName="Helvetica-Bold", fontSize=26, leading=31,
          textColor=INK, alignment=TA_CENTER)
subtitle = S("subtitle", fontName="Helvetica", fontSize=13, leading=18,
             textColor=BLUE, alignment=TA_CENTER)
meta = S("meta", fontName="Helvetica", fontSize=10, leading=15,
         textColor=GREY, alignment=TA_CENTER)
bullet = S("bullet", parent=body, spaceAfter=3)

def fig(name, width=USABLE_W * 0.86):
    p = FIG / name
    iw, ih = PILImage.open(p).size
    w = width; h = w * ih / iw
    return Image(str(p), width=w, height=h)

def imgblock(name, cap):
    return KeepTogether([fig(name), Paragraph(cap, caption)])

def oii_block(obs, interp, impl):
    return [Paragraph(f"<b>Observation.</b> {obs}", oii),
            Paragraph(f"<b>Interpretation.</b> {interp}", oii),
            Paragraph(f"<b>Implication.</b> {impl}", oii), Spacer(1, 6)]

story = []
P = lambda t, s=body: story.append(Paragraph(t, s))
SP = lambda h=8: story.append(Spacer(1, h))

# ---------- Title page ----------
SP(90)
story.append(HRFlowable(width="40%", thickness=2, color=BLUE,
                        spaceAfter=18, hAlign="CENTER"))
P("Exploratory Data Analysis<br/>of Airbnb Listings", title)
SP(14)
P("A descriptive, non-predictive analysis of a multi-city dataset", subtitle)
SP(24)
story.append(HRFlowable(width="40%", thickness=1, color=colors.HexColor("#C9D6DD"),
                        spaceAfter=20, hAlign="CENTER"))
P("4,046 listings &nbsp;&bull;&nbsp; 9 countries &nbsp;&bull;&nbsp; 13 cities", meta)
SP(6)
P("Prepared in Python (pandas, matplotlib, seaborn)", meta)
SP(6)
P("September 2026", meta)
story.append(PageBreak())

# ---------- Abstract ----------
P("Abstract", h1)
P("This project presents an exploratory data analysis (EDA) of an Airbnb listings "
  "dataset spanning 4,046 properties across nine countries and thirteen cities. The "
  "goal is descriptive rather than predictive: to characterise the data, study the "
  "distributions of price, availability, reviews and ratings, and measure the "
  "relationships among numerical variables. Prices are strongly right-skewed "
  "(median $120 versus a mean of $225), so medians and quartiles are used throughout. "
  "The dominant and most robust pattern is that <b>listing price is associated above all "
  "with location</b>: median city prices range more than ten-fold, from $55 in Porto to "
  "$573 in Hong Kong. In contrast, the available numeric attributes — review count, "
  "review score, availability and amenity count — are <b>essentially uncorrelated with "
  "price</b> (all |r| &lt; 0.08), and review scores show a pronounced ceiling effect "
  "(88% of listings score 9 or above). The analysis is candid about the dataset's "
  "limitations, including its curated multi-city composition and the absence of common "
  "price drivers such as room type and property size.")

# ---------- 1. Introduction ----------
P("1. Introduction", h1)
P("Short-term rental platforms such as Airbnb publish large volumes of structured "
  "information about individual properties — where they are, how much they cost, how "
  "available they are, and how guests have rated them. In aggregate this data can reveal "
  "how accommodation markets behave, but raw listings are difficult to interpret without "
  "systematic analysis. Exploratory data analysis is the standard first step: it uses "
  "descriptive statistics and visualisation to summarise a dataset, expose its structure "
  "and surface patterns worth deeper study, all before any modelling is attempted. This "
  "report applies that approach to a multi-city Airbnb dataset.")

# ---------- 2. Problem statement ----------
P("2. Problem Statement", h1)
P("Airbnb listing data combines location, price, availability, review activity, ratings "
  "and host characteristics. Understanding which of these characteristics are associated "
  "with differences in price and availability is valuable, but the raw data is voluminous, "
  "skewed and mixed in type, which makes direct interpretation unreliable. The problem "
  "addressed here is to explore the dataset systematically and determine which listing "
  "characteristics are associated with differences in price, availability and guest "
  "engagement — while being explicit about what the data can and cannot support.")

# ---------- 3. Aim & objectives ----------
P("3. Aim and Objectives", h1)
P("<b>Aim.</b> To conduct a systematic exploratory analysis of Airbnb listings and "
  "identify important patterns, trends and relationships associated with property prices "
  "and availability.")
P("<b>Objectives.</b>")
objs = ["Understand the structure and characteristics of the dataset.",
        "Clean the data and engineer analysis-ready features.",
        "Generate descriptive statistical summaries for the key numerical variables.",
        "Study the distributions of price, reviews, ratings and availability.",
        "Compare listings across cities and countries.",
        "Measure correlations among the numerical variables.",
        "Present clear visualisations with evidence-based interpretation."]
story.append(ListFlowable([ListItem(Paragraph(o, bullet), leftIndent=6) for o in objs],
                          bulletType="bullet", start="•", leftIndent=14))

# ---------- 4. Dataset description ----------
P("4. Dataset Description", h1)
P("The dataset contains <b>4,046 listings</b> described by 18 substantive columns after "
  "removing an exported index column. The variables fall into four groups:")
grp = ["<b>Identifiers &amp; text:</b> id, url, name, description, host_id, host_name, amenities.",
       "<b>Geographic:</b> country (9 values), city (13 values), latitude, longitude.",
       "<b>Price:</b> price (USD per night).",
       "<b>Behaviour &amp; quality:</b> availability_30/60/90/365, no_of_reviews, review_score (0–10)."]
story.append(ListFlowable([ListItem(Paragraph(g, bullet), leftIndent=6) for g in grp],
                          bulletType="bullet", start="•", leftIndent=14))
SP(4)
P("<b>A note on adapting the generic guide to this dataset.</b> The standard EDA brief "
  "assumes a single-city dataset with <font face='Helvetica-Oblique'>room_type</font>, "
  "<font face='Helvetica-Oblique'>minimum_nights</font>, "
  "<font face='Helvetica-Oblique'>neighbourhood</font> and "
  "<font face='Helvetica-Oblique'>reviews_per_month</font>. This dataset contains none of "
  "those. The analysis therefore substitutes <b>city / country</b> as the categorical "
  "driver in place of room type, uses <b>review score and availability</b> in place of "
  "minimum-nights analyses, and engineers two features in the spirit of the guide: "
  "<b>amenities_count</b> (number of amenities per listing) and <b>host_listings_count</b> "
  "(listings per host). This substitution is documented rather than hidden.")

# ---------- 5. Tools ----------
P("5. Tools and Technologies", h1)
P("The analysis was carried out in <b>Python</b> using <b>pandas</b> and <b>NumPy</b> for "
  "data manipulation and <b>Matplotlib</b> and <b>Seaborn</b> for visualisation. The work "
  "is delivered as a runnable Jupyter notebook (openable in VS Code) together with this "
  "report. No machine-learning model is built; scikit-learn is not required.")

# ---------- 6. Preprocessing ----------
P("6. Data Preprocessing and Cleaning", h1)
P("The dataset arrived in good condition, which kept cleaning light. Every decision is "
  "recorded below:")
clean = ["<b>No missing values and no duplicates.</b> A column-by-column check returned "
         "zero nulls, zero duplicate rows and zero duplicate listing ids.",
         "<b>Dropped the exported index column</b> (\"Unnamed: 0\"), which merely repeated "
         "the row number.",
         "<b>Engineered amenities_count</b> by parsing the amenities list and counting items.",
         "<b>Engineered host_listings_count</b> as the number of listings per host_id.",
         "<b>Validated ranges:</b> no negative or zero prices, and all availability values "
         "lie within 0–365.",
         "<b>Outliers kept, not deleted.</b> Extreme prices (up to $11,681) are treated as "
         "legitimate luxury listings and retained for all statistics; for visual clarity "
         "some charts are capped at the 99th percentile ($1,393), which affects only 41 "
         "listings and is stated on each affected chart."]
story.append(ListFlowable([ListItem(Paragraph(c, bullet), leftIndent=6) for c in clean],
                          bulletType="bullet", start="•", leftIndent=14))

# ---------- 7. EDA ----------
story.append(PageBreak())
P("7. Exploratory Data Analysis", h1)

# descriptive stats table
P("Descriptive statistics.", h2)
P("The table below summarises the numerical variables (all counts are 4,046). For the "
  "skewed price variable the median ($120) is far below the mean ($225), confirming the "
  "influence of a small number of very expensive listings.")
tbl_rows = [["Variable", "Mean", "Median", "Std", "Min", "25%", "75%", "Max"],
            ["price", "224.7", "120.0", "399.0", "9", "68", "250", "11,681"],
            ["availability_30", "10.8", "7.0", "10.8", "0", "0", "20", "30"],
            ["availability_60", "24.7", "21.0", "21.8", "0", "0", "45", "60"],
            ["availability_90", "40.7", "40.0", "32.9", "0", "4", "71", "90"],
            ["availability_365", "171.6", "169.0", "134.4", "0", "31", "306", "365"],
            ["no_of_reviews", "37.8", "15.0", "54.9", "1", "4", "49", "533"],
            ["review_score", "9.31", "9.0", "0.93", "2", "9", "10", "10"],
            ["amenities_count", "23.9", "22.0", "11.6", "1", "15", "31", "76"],
            ["host_listings_count", "1.23", "1.0", "0.89", "1", "1", "1", "11"]]
t = Table(tbl_rows, hAlign="LEFT", colWidths=[1.9*inch] + [0.62*inch]*7)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), BLUE),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 8),
    ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
    ("ALIGN", (0, 0), (0, -1), "LEFT"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C9D6DD")),
    ("TOPPADDING", (0, 0), (-1, -1), 3.5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
]))
story.append(t)
SP(12)

# 7.1 univariate
P("7.1 Univariate Analysis", h2)
story.append(imgblock("fig01_price_distribution.png",
    "Fig 1. Price distribution (≤ 99th percentile). Median $120, mean $225 — a right-skewed spread."))
story.append(imgblock("fig02_price_log_distribution.png",
    "Fig 2. Price on a log10 scale, revealing an approximately log-normal shape once the skew is removed."))
story.append(imgblock("fig03_listings_by_country.png",
    "Fig 3. Listings by country. The United States dominates; China is a very small slice (13)."))
story.append(imgblock("fig04_top_cities_by_listings.png",
    "Fig 4. Top cities by number of listings. New York is the single largest market."))
story.append(imgblock("fig05_availability365_distribution.png",
    "Fig 5. 365-day availability. A large block sits at zero; the median is 169 days."))
story.append(imgblock("fig06_reviews_distribution.png",
    "Fig 6. Number of reviews (≤ 99th percentile). Right-skewed; median 15."))
story.append(imgblock("fig07_review_score_distribution.png",
    "Fig 7. Review scores concentrate at 9–10 — a clear ceiling effect."))
story.append(imgblock("fig08_amenities_count_distribution.png",
    "Fig 8. Amenities per listing. Median 22, ranging from 1 to 76."))
story += oii_block(
    "Price spans $9–$11,681 but is extremely right-skewed (skewness ≈ 13.5); the median is "
    "$120 while the mean is $225, and the middle 50% of listings fall between $68 and $250. "
    "The United States contributes the most listings (1,061) and New York the most of any "
    "city (532). Median availability is 169 days, though 18.8% of listings show zero "
    "availability. Review counts are right-skewed (median 15), and review scores cluster at "
    "the top (88.4% score 9 or above).",
    "A small number of luxury listings inflate the mean, so the median is the honest measure "
    "of a typical price. The dataset is a curated multi-city sample rather than a census, and "
    "the compressed review-score scale carries little discriminating information.",
    "All cross-group comparisons below use medians, and review score is unlikely to explain "
    "much price variation.")

# 7.2 bivariate
story.append(PageBreak())
P("7.2 Bivariate Analysis", h2)
story.append(imgblock("fig09_price_by_city_box.png",
    "Fig 9. Price by city (capped, ordered by median). Hong Kong stands far above the rest."))
story.append(imgblock("fig10_median_price_by_city.png",
    "Fig 10. Median price by city — a more than ten-fold range from Porto to Hong Kong."))
story.append(imgblock("fig11_median_price_by_country.png",
    "Fig 11. Median price by country. Hong Kong and China lead; Portugal and Spain trail."))
story.append(imgblock("fig12_price_vs_reviews.png",
    "Fig 12. Price vs number of reviews — no visible trend."))
story.append(imgblock("fig13_price_by_review_score.png",
    "Fig 13. Price by review score — broadly flat across the (top-heavy) score range."))
story.append(imgblock("fig14_price_vs_amenities.png",
    "Fig 14. Price vs amenities count — no meaningful relationship."))
story += oii_block(
    "Median price ranges from $55 in Porto to $573 in Hong Kong, a more than ten-fold "
    "spread across cities, with a similar pattern by country. In contrast, the scatterplots "
    "of price against review count, review score and amenity count show no visible trend.",
    "Location is by far the strongest correlate of price in this dataset, whereas the "
    "measured numeric attributes move very little with price.",
    "Any statement about a 'typical' Airbnb price must condition on city or country; the "
    "numeric listing attributes on their own are poor guides to price.")

# 7.3 multivariate
P("7.3 Multivariate and Correlation Analysis", h2)
story.append(imgblock("fig15_correlation_heatmap.png",
    "Fig 15. Correlation heatmap. Price shows near-zero correlation with every numeric variable."))
story.append(imgblock("fig16_geographic_scatter.png",
    "Fig 16. Geographic spread of listings, coloured by log price — distinct city clusters worldwide."))
story += oii_block(
    "The strongest linear correlation between price and any numeric variable is only −0.079 "
    "(number of reviews); every |r| is below 0.08. The four availability windows correlate "
    "strongly with one another (as expected) but not with price.",
    "There is essentially no linear association between price and the available numeric "
    "variables. Correlation does not imply causation — and here even the association itself "
    "is negligible.",
    "A price model built from these numeric features alone would perform poorly; the usable "
    "signal lives in the categorical location fields, not in these measurements.")

# ---------- 8. Key findings ----------
story.append(PageBreak())
P("8. Key Findings", h1)
finds = [
 "<b>Structure &amp; quality:</b> 4,046 listings × 18 substantive columns, with no missing "
 "values and no duplicates.",
 "<b>Price:</b> strongly right-skewed — median $120, mean $225, middle-50% $68–$250.",
 "<b>Most listings:</b> New York (532) among cities and the United States (1,061) among countries.",
 "<b>Highest typical price:</b> Hong Kong — median $573 by city and $589 by country.",
 "<b>Location vs price:</b> a more than ten-fold spread in median city price ($55 Porto → $573 Hong Kong).",
 "<b>Reviews vs price:</b> negligible negative correlation (−0.079).",
 "<b>Availability:</b> varies widely by city — highest in Istanbul (median 331 days), lowest in Sydney (65).",
 "<b>Ratings:</b> a strong ceiling effect — 88.4% of listings score 9 or above.",
 "<b>Correlation summary:</b> no numeric variable is meaningfully correlated with price (all |r| &lt; 0.08).",
 "<b>Overall insight:</b> price is driven overwhelmingly by location, not by the measured numeric attributes."]
story.append(ListFlowable([ListItem(Paragraph(f, bullet), leftIndent=6) for f in finds],
                          bulletType="1", leftIndent=16))

# ---------- 9. Discussion ----------
P("9. Discussion", h1)
P("The findings point consistently to location as the organising force behind price. Cities "
  "differ by an order of magnitude in their median nightly price, and the geographic scatter "
  "shows those differences as distinct clusters. This is intuitive: a night's accommodation "
  "in central Hong Kong is simply a different economic good than one in Porto. What is more "
  "striking is how little the other measured variables matter. Review counts, review scores, "
  "availability and amenity counts are all but uncorrelated with price. Part of the "
  "explanation is statistical — review scores in particular are compressed near the top of "
  "their range, leaving little variance to correlate with anything. But part is structural: "
  "the variables that usually drive nightly price, such as property type, size and exact "
  "neighbourhood, are not present in this dataset. The weak correlations are therefore best "
  "read as evidence that price information here lives in the categorical geography rather "
  "than in the available numeric fields.")

# ---------- 10. Limitations ----------
P("10. Limitations", h1)
lims = ["The dataset is a curated multi-city sample, not a census; the United States and New "
        "York are over-represented and China is very small (13 listings), so its figures are unstable.",
        "Review score shows a ceiling effect (most values 9–10), limiting its analytical value.",
        "Extreme prices are retained as legitimate luxury listings but still influence means.",
        "The data is a cross-sectional snapshot with no time dimension, so seasonality and "
        "booking history cannot be studied.",
        "Common price drivers — room/property type, size, exact neighbourhood, minimum nights — "
        "are absent, which partly explains the weak numeric correlations with price.",
        "Correlation does not establish causation, and in this dataset the associations are in "
        "any case negligible."]
story.append(ListFlowable([ListItem(Paragraph(l, bullet), leftIndent=6) for l in lims],
                          bulletType="bullet", start="•", leftIndent=14))

# ---------- 11. Conclusion ----------
P("11. Conclusion", h1)
P("This project performed a descriptive exploratory analysis of 4,046 Airbnb listings across "
  "nine countries and thirteen cities. Because prices are strongly right-skewed, medians and "
  "quartiles were used throughout. The clearest and most robust result is that listing price "
  "is associated above all with location: median city prices span more than ten-fold, from "
  "$55 in Porto to $573 in Hong Kong. The available numeric attributes — review count, review "
  "score, availability and amenity count — are essentially uncorrelated with price, and review "
  "scores are compressed near the top of their scale. Taken together, the analysis shows how "
  "exploratory data analysis turns raw accommodation data into interpretable insight, while "
  "remaining honest about what the dataset can and cannot reveal.")

# ---------- 12. References ----------
P("12. References", h1)
refs = ["Airbnb listings dataset (provided as airbnb_dataset.csv), 4,046 records across 9 "
        "countries and 13 cities.",
        "McKinney, W. (2010). Data Structures for Statistical Computing in Python. pandas.",
        "Hunter, J. D. (2007). Matplotlib: A 2D Graphics Environment.",
        "Waskom, M. (2021). seaborn: statistical data visualization."]
story.append(ListFlowable([ListItem(Paragraph(r, bullet), leftIndent=6) for r in refs],
                          bulletType="bullet", start="•", leftIndent=14))

# ---------- footer ----------
def footer(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setStrokeColor(colors.HexColor("#C9D6DD"))
        canvas.setLineWidth(0.5)
        canvas.line(0.9*inch, 0.72*inch, letter[0]-0.9*inch, 0.72*inch)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(GREY)
        canvas.drawString(0.9*inch, 0.56*inch, "Exploratory Data Analysis of Airbnb Listings")
        canvas.drawRightString(letter[0]-0.9*inch, 0.56*inch, f"Page {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate(OUT, pagesize=letter, topMargin=0.85*inch,
                        bottomMargin=0.9*inch, leftMargin=0.9*inch, rightMargin=0.9*inch,
                        title="Exploratory Data Analysis of Airbnb Listings",
                        author="EDA Project")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("Wrote", OUT)
