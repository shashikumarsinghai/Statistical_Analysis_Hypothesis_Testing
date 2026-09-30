from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import pandas as pd
import os


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
VIS_DIR = os.path.join(BASE_DIR, "visualizations")
REPORT_DIR = os.path.join(BASE_DIR, "report")

os.makedirs(REPORT_DIR, exist_ok=True)

OUTPUT_FILE = os.path.join(
    REPORT_DIR,
    "Statistical_Analysis_Hypothesis_Testing_Report.docx"
)


# --------------------------------------------------
# Load saved results
# --------------------------------------------------

segment_stats = pd.read_csv(
    os.path.join(DATA_DIR, "segment_descriptive_statistics.csv")
)

results_summary = pd.read_csv(
    os.path.join(DATA_DIR, "statistical_test_results.csv")
)


# --------------------------------------------------
# Create document
# --------------------------------------------------

doc = Document()

# Page margins
section = doc.sections[0]
section.top_margin = Inches(0.7)
section.bottom_margin = Inches(0.7)
section.left_margin = Inches(0.8)
section.right_margin = Inches(0.8)


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def add_heading(text, level=1):
    heading = doc.add_heading(text, level=level)
    return heading


def add_paragraph(text="", bold_prefix=None):
    paragraph = doc.add_paragraph()

    if bold_prefix and text.startswith(bold_prefix):
        run = paragraph.add_run(bold_prefix)
        run.bold = True
        paragraph.add_run(text[len(bold_prefix):])
    else:
        paragraph.add_run(text)

    return paragraph


def set_cell_text(cell, text, bold=False):
    cell.text = ""
    paragraph = cell.paragraphs[0]
    run = paragraph.add_run(str(text))
    run.bold = bold
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def shade_cell(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def add_dataframe_table(dataframe, title=None):
    if title:
        paragraph = doc.add_paragraph()
        run = paragraph.add_run(title)
        run.bold = True
        run.font.size = Pt(11)

    table = doc.add_table(
        rows=1,
        cols=len(dataframe.columns)
    )

    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"

    # Header
    for i, column in enumerate(dataframe.columns):
        set_cell_text(
            table.rows[0].cells[i],
            column,
            bold=True
        )
        shade_cell(table.rows[0].cells[i], "D9EAF7")

    # Rows
    for _, row in dataframe.iterrows():
        cells = table.add_row().cells

        for i, value in enumerate(row):
            if isinstance(value, float):
                value = f"{value:.4f}"

            set_cell_text(cells[i], value)

    doc.add_paragraph()


def add_image(filename, width=6.2):
    path = os.path.join(VIS_DIR, filename)

    if os.path.exists(path):
        paragraph = doc.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

        run = paragraph.add_run()
        run.add_picture(
            path,
            width=Inches(width)
        )

        doc.add_paragraph()


# --------------------------------------------------
# Title Page
# --------------------------------------------------

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

run = title.add_run(
    "Statistical Analysis and Hypothesis Testing in Python"
)
run.bold = True
run.font.size = Pt(20)

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER

run = subtitle.add_run(
    "Analysis of Order Profit Across Customer Segments"
)
run.bold = True
run.font.size = Pt(14)

doc.add_paragraph()

paragraph = doc.add_paragraph()
paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
paragraph.add_run(
    "YuvaIntern – Virtual Data Science with Python Apprentice Internship"
)

doc.add_paragraph()

paragraph = doc.add_paragraph()
paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
paragraph.add_run(
    "Statistical Analysis Project – Week 3"
)

doc.add_page_break()


# --------------------------------------------------
# 1. Introduction
# --------------------------------------------------

add_heading("1. Introduction", 1)

add_paragraph(
    "This project applies statistical analysis and hypothesis testing "
    "techniques in Python to investigate whether average order profit "
    "differs among Consumer, Corporate, and Home Office customer segments."
)

add_paragraph(
    "The analysis uses the Superstore dataset and focuses on order-level "
    "profit rather than individual product-line transactions. Statistical "
    "tests, confidence intervals, effect size, visualizations, and a "
    "non-parametric robustness check are used to evaluate the research question."
)


# --------------------------------------------------
# 2. Research Question
# --------------------------------------------------

add_heading("2. Research Question and Hypotheses", 1)

add_paragraph(
    "Research Question: Does average order profit differ significantly "
    "among Consumer, Corporate, and Home Office customers?"
)

add_paragraph(
    "H₀ (Null Hypothesis): The mean order profit is equal across Consumer, "
    "Corporate, and Home Office segments."
)

add_paragraph(
    "H₁ (Alternative Hypothesis): At least one customer segment has a "
    "different mean order profit."
)

add_paragraph(
    "The significance level was set at α = 0.05."
)


# --------------------------------------------------
# 3. Data and Cleaning
# --------------------------------------------------

add_heading("3. Data and Data Preparation", 1)

add_paragraph(
    "The Superstore dataset contains 10,800 raw rows and 21 columns. "
    "The first 9,994 rows represent the main transaction dataset used "
    "for the analysis. The remaining records were associated with "
    "returns-related information and were excluded from the primary analysis."
)

add_paragraph(
    "The cleaned dataset contains 9,994 transaction rows. Duplicate "
    "transaction rows were removed through the selection of the main "
    "transaction portion of the dataset. The analytical fields required "
    "for this hypothesis test were complete."
)

add_paragraph(
    "Because individual orders can contain multiple product-line records, "
    "the data was aggregated to the order level. The resulting analytical "
    "dataset contains 5,009 orders."
)

add_paragraph(
    "A check of Order ID and Segment showed that no order contained more "
    "than one customer segment. Therefore, each order could be assigned "
    "unambiguously to one segment."
)


# --------------------------------------------------
# 4. Methodology
# --------------------------------------------------

add_heading("4. Methodology", 1)

add_paragraph(
    "The primary statistical method was a one-way ANOVA because the research "
    "question compares the mean order profit across three independent customer "
    "segments."
)

add_paragraph(
    "Levene's test was first used to examine equality of variances. "
    "The distribution of order profit was also examined visually because "
    "the data contains skewness and extreme observations."
)

add_paragraph(
    "The analysis also calculated 95% confidence intervals for each segment "
    "mean and eta-squared (η²) as an effect-size measure."
)

add_paragraph(
    "Because the order-profit distribution contains substantial skewness "
    "and outliers, a Kruskal-Wallis test was performed as a non-parametric "
    "robustness check."
)


# --------------------------------------------------
# 5. Descriptive Statistics
# --------------------------------------------------

add_heading("5. Descriptive Statistics", 1)

add_paragraph(
    "The following table summarizes order-level profit for each customer segment."
)

# Keep only useful columns if present
preferred_columns = [
    "Segment",
    "count",
    "mean",
    "median",
    "std",
    "min",
    "max"
]

available_columns = [
    col for col in preferred_columns
    if col in segment_stats.columns
]

descriptive_table = segment_stats[available_columns].copy()

# Round numerical columns
for column in descriptive_table.columns:
    if column != "Segment":
        descriptive_table[column] = descriptive_table[column].round(2)

add_dataframe_table(
    descriptive_table,
    "Table 1. Order-level profit descriptive statistics"
)


# --------------------------------------------------
# 6. Statistical Test Results
# --------------------------------------------------

add_heading("6. Statistical Test Results", 1)

results_table = results_summary.copy()

results_table["Statistic"] = results_table["Statistic"].round(4)
results_table["p_value"] = results_table["p_value"].round(4)

add_dataframe_table(
    results_table,
    "Table 2. Statistical hypothesis test results"
)


# --------------------------------------------------
# 7. Levene's Test
# --------------------------------------------------

add_heading("7. Levene's Test", 1)

add_paragraph(
    "Levene's test produced a test statistic of 0.1695 and a p-value of "
    "0.8441. Because the p-value is greater than 0.05, there is insufficient "
    "evidence to conclude that the variances differ significantly across "
    "the three customer segments."
)

add_paragraph(
    "Therefore, the equal-variance assumption for the one-way ANOVA is "
    "reasonably supported from this test."
)


# --------------------------------------------------
# 8. One-way ANOVA
# --------------------------------------------------

add_heading("8. One-way ANOVA", 1)

add_paragraph(
    "The one-way ANOVA produced an F-statistic of 0.7084 and a p-value "
    "of 0.4925."
)

add_paragraph(
    "Since the p-value is greater than the significance level of 0.05, "
    "the null hypothesis is not rejected."
)

add_paragraph(
    "Therefore, this analysis does not provide statistically significant "
    "evidence that average order profit differs among Consumer, Corporate, "
    "and Home Office customers."
)

add_paragraph(
    "Failing to reject the null hypothesis does not prove that the three "
    "population means are exactly equal."
)


# --------------------------------------------------
# 9. Confidence Intervals
# --------------------------------------------------

add_heading("9. Confidence Intervals", 1)

add_paragraph(
    "The estimated mean order profits and their 95% confidence intervals were:"
)

ci_table = pd.DataFrame({
    "Segment": [
        "Consumer",
        "Corporate",
        "Home Office"
    ],
    "Mean Order Profit": [
        51.86,
        60.75,
        66.34
    ],
    "95% CI Lower": [
        38.31,
        43.27,
        45.34
    ],
    "95% CI Upper": [
        65.42,
        78.23,
        87.33
    ]
})

add_dataframe_table(
    ci_table,
    "Table 3. Mean order profit and 95% confidence intervals"
)

add_paragraph(
    "The confidence intervals overlap substantially. This is consistent "
    "with the ANOVA result, which did not identify a statistically significant "
    "difference among the segment means."
)


# --------------------------------------------------
# 10. Effect Size
# --------------------------------------------------

add_heading("10. Effect Size", 1)

add_paragraph(
    "The eta-squared (η²) effect size was approximately 0.0003."
)

add_paragraph(
    "This means customer segment accounts for approximately 0.03% of the "
    "variation in order profit in this analysis. The effect is therefore "
    "very small in terms of the proportion of variance explained."
)


# --------------------------------------------------
# 11. Kruskal-Wallis
# --------------------------------------------------

add_heading("11. Kruskal-Wallis Robustness Check", 1)

add_paragraph(
    "The Kruskal-Wallis test was performed because the order-profit "
    "distribution contains skewness and extreme observations."
)

add_paragraph(
    "The test produced an H-statistic of 1.8403 and a p-value of 0.3985."
)

add_paragraph(
    "Because the p-value is greater than 0.05, the Kruskal-Wallis test "
    "also does not provide statistically significant evidence of differences "
    "among the three customer segments."
)

add_paragraph(
    "The agreement between the ANOVA and Kruskal-Wallis results provides "
    "a consistent finding for this dataset."
)


# --------------------------------------------------
# 12. Visualizations
# --------------------------------------------------

add_heading("12. Visual Analysis", 1)

add_paragraph(
    "The following visualizations support the statistical analysis by "
    "showing the distribution, mean estimates, and order counts across "
    "the three customer segments."
)

add_heading("12.1 Order Profit Distribution by Segment", 2)

add_image(
    "01_order_profit_distribution_by_segment.png"
)

add_paragraph(
    "The boxplot shows substantial variation and several extreme observations "
    "in order profit across all three segments."
)

add_heading("12.2 Mean Order Profit with 95% Confidence Intervals", 2)

add_image(
    "02_mean_order_profit_95ci.png"
)

add_paragraph(
    "The mean-profit chart displays the estimated mean for each segment "
    "together with 95% confidence intervals. The substantial overlap "
    "between the intervals is consistent with the hypothesis-test results."
)

add_heading("12.3 Average Order Profit by Segment", 2)

add_image(
    "03_average_order_profit_by_segment.png"
)

add_paragraph(
    "The average order profit is approximately 51.86 for Consumer, "
    "60.75 for Corporate, and 66.34 for Home Office orders. "
    "These observed differences were not statistically significant."
)

add_heading("12.4 Number of Orders by Segment", 2)

add_image(
    "04_order_count_by_segment.png"
)

add_paragraph(
    "Consumer has the largest number of orders, followed by Corporate "
    "and Home Office. The different group sizes were retained in the "
    "statistical analysis rather than artificially balancing the groups."
)


# --------------------------------------------------
# 13. Conclusion
# --------------------------------------------------

add_heading("13. Conclusion", 1)

add_paragraph(
    "The objective of this analysis was to determine whether average order "
    "profit differs significantly among Consumer, Corporate, and Home Office customers."
)

add_paragraph(
    "The one-way ANOVA produced an F-statistic of 0.7084 with a p-value "
    "of 0.4925. Since the p-value is greater than 0.05, the null hypothesis "
    "was not rejected."
)

add_paragraph(
    "Therefore, the analysis does not provide statistically significant "
    "evidence that average order profit differs among the three customer segments."
)

add_paragraph(
    "The Kruskal-Wallis robustness check produced a p-value of 0.3985 "
    "and reached the same overall conclusion."
)

add_paragraph(
    "Although the observed sample means differ, the effect size was very "
    "small (η² ≈ 0.0003), indicating that customer segment explained only "
    "a very small proportion of the variation in order-level profit."
)


# --------------------------------------------------
# 14. Practical Implications
# --------------------------------------------------

add_heading("14. Practical Implications", 1)

add_paragraph(
    "The results suggest that customer segment alone may not be an important "
    "explanatory factor for differences in order-level profit in this dataset."
)

add_paragraph(
    "Other variables such as discount, product category, region, sales volume, "
    "and product-level characteristics could potentially contribute more to "
    "profit variation."
)

add_paragraph(
    "These results describe an association in the analyzed dataset and should "
    "not be interpreted as evidence of a causal relationship."
)


# --------------------------------------------------
# 15. Limitations
# --------------------------------------------------

add_heading("15. Limitations", 1)

limitations = [
    "The analysis uses an observational dataset, so causal conclusions cannot be established.",
    "Order profit contains substantial skewness and extreme values.",
    "The dataset represents a specific Superstore sample and may not generalize to all businesses or customer populations.",
    "Customer segment was analyzed as the primary grouping variable; other potentially important explanatory variables were not included in the ANOVA.",
    "Aggregating transactions to the order level improves the unit of analysis, but orders may still share characteristics related to customers, products, regions, or time periods."
]

for item in limitations:
    doc.add_paragraph(item, style="List Bullet")


# --------------------------------------------------
# 16. Future Work
# --------------------------------------------------

add_heading("16. Future Work", 1)

add_paragraph(
    "Future analysis could investigate the effects of discount, product category, "
    "region, sales, and other variables using regression or other multivariable "
    "statistical methods."
)


# --------------------------------------------------
# 17. Tools and Libraries
# --------------------------------------------------

add_heading("17. Tools and Python Libraries", 1)

libraries = [
    "Python",
    "Pandas",
    "NumPy",
    "SciPy",
    "Statsmodels",
    "Matplotlib",
    "Seaborn",
    "Jupyter Notebook"
]

for library in libraries:
    doc.add_paragraph(library, style="List Bullet")


# --------------------------------------------------
# Save document
# --------------------------------------------------

doc.save(OUTPUT_FILE)

print("Report generated successfully.")
print(f"File: {OUTPUT_FILE}")