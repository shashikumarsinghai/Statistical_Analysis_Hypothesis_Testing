# Statistical Analysis and Hypothesis Testing in Python

## Week 3 – YuvaIntern Data Science Internship

This project applies statistical analysis and hypothesis testing techniques in Python to investigate whether average order profit differs among Consumer, Corporate, and Home Office customer segments.

## Research Question

Does average order profit differ significantly among Consumer, Corporate, and Home Office customers?

## Hypotheses

**Null Hypothesis (H₀):**  
The mean order profit is equal across Consumer, Corporate, and Home Office segments.

**Alternative Hypothesis (H₁):**  
At least one customer segment has a different mean order profit.

## Dataset

The analysis uses the Superstore dataset.

The original dataset contains 10,800 rows. The primary transaction dataset contains 9,994 rows and was used for the analysis.

Because individual orders can contain multiple product-line records, transactions were aggregated to the order level.

The final analytical dataset contains **5,009 orders**.

## Methodology

The following statistical methods were used:

- Levene's Test
- One-way ANOVA
- 95% Confidence Intervals
- Eta-squared (η²) effect size
- Kruskal-Wallis Test

The significance level was set to:

**α = 0.05**

## Results

### Levene's Test

- Statistic: **0.1695**
- p-value: **0.8441**

The result does not provide evidence of significantly different variances across the three customer segments.

### One-way ANOVA

- F-statistic: **0.7084**
- p-value: **0.4925**

The p-value is greater than 0.05, so the null hypothesis was not rejected.

The analysis does not provide statistically significant evidence that average order profit differs among the three customer segments.

### Effect Size

- Eta-squared (η²): **0.0003**

Customer segment explains approximately **0.03% of the variation** in order profit in this analysis.

### Kruskal-Wallis Test

- H-statistic: **1.8403**
- p-value: **0.3985**

The non-parametric robustness check also does not provide statistically significant evidence of differences among the three customer segments.

## Visualizations

The project includes four visualizations:

1. Order Profit Distribution by Customer Segment
2. Mean Order Profit with 95% Confidence Intervals
3. Average Order Profit by Segment
4. Number of Orders by Segment

## Project Structure

```text
Statistical_Analysis_Hypothesis_Testing/
│
├── data/
│   ├── superstore.csv
│   ├── segment_descriptive_statistics.csv
│   └── statistical_test_results.csv
│
├── notebooks/
│   └── Hypothesis_Testing.ipynb
│
├── visualizations/
│   ├── 01_order_profit_distribution_by_segment.png
│   ├── 02_mean_order_profit_95ci.png
│   ├── 03_average_order_profit_by_segment.png
│   └── 04_order_count_by_segment.png
│
├── report/
│   └── Statistical_Analysis_Hypothesis_Testing_Report.docx
│
├── create_report.py
├── requirements.txt
├── .gitignore
└── README.md

```

## Tools and Libraries

- Python
- Pandas
- NumPy
- SciPy
- Statsmodels
- Matplotlib
- Seaborn
- Jupyter Notebook
- python-docx

## Conclusion

The one-way ANOVA did not provide statistically significant evidence that average order profit differs among Consumer, Corporate, and Home Office customers.

The Kruskal-Wallis robustness check produced a consistent result.

Although the observed sample means differ, the effect size was very small (η² = 0.0003), indicating that customer segment explains approximately 0.03% of the variation in order-level profit.

## Limitations

- The analysis uses an observational dataset, so causal conclusions cannot be established.
- Order profit contains substantial skewness and extreme values.
- The dataset represents a specific Superstore sample and may not generalize to all businesses or customer populations.
- Other variables such as discount, product category, region, and sales were not included in the primary ANOVA.