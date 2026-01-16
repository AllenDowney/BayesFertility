# US Fertility Is Heading for Historic Lows

Recent generations of Americans are on track to have fewer children than previous generations. Based on projections from a Bayesian model, cohorts born in the 2000s could end up with fewer than 1 child per woman on average—a level of fertility comparable to present-day South Korea.

The following figure shows the results from the model for US women born from 1920 to 2009, along with observed cohort fertility rates (CFR) from Census data.

![CFR Predictions](figs/cfr_vs_actual_v3.png)

The trend is dramatic:

* Fertility peaked with the cohort born in 1934, who had 3.1 children per woman on average.
* Women born in 1980 have already completed most of their childbearing years with 1.9 children—below the replacement rate of 2.1.
* The model projects that women born in 2000 will have just 0.9 children on average, while those born in 2009 will have 0.8.

The shaded areas show a 94% credible interval for the projections, showing increasing uncertainty for the youngest cohorts.

## How the Model Works

To make these projections, I built a Bayesian hierarchical model using CPS fertility data from 1976-2024, which includes 1.17 million women aged 15-54. The model estimates two key parameters:

* **Cohort effects (α)**: For each 3-year cohort group, this parameter quantifies overall fertility level.
* **Age effects (β)**: For each 3-year age group, this parameter quantifies age-specific fertility.

The parameters are on a log scale, so they're not easy to interpret in absolute terms. Instead, we should think of them as differences in fertility between groups.


## Cohort and age effects

The next figure shows the cohort effects—that is, a fertility level for each generation.

![Cohort Effects](figs/cohort_effects_v3.png)

The cohort effects capture the overall fertility level for each generation. 

* Fertility was highest among the cohorts born between 1925 and 1940, who were the parents of the Baby Boomers.
* Fertility was lower but mostly unchanged among cohorts born between 1950 and 1985.
* Fertility has declined substantially among cohorts born after 1985.

The next figure shows the age effects—the typical age pattern of childbearing.

![Age Effects](figs/age_effects_v3.png)

The age effects show that fertility peaks in the mid-20s and declines thereafter.

By combining cohort and age effects, we can project lifetime fertility for cohorts still in their reproductive years.
This version of the model does not take into account timing effects, but we will explore a version that does -- and see that it does not affect the predictions much.

## Assumptions and Validation

We can validate the model on cohorts who have already completed their childbearing. The first figure above shows both our model's predictions and observed completed fertility from Census data. The agreement is very good.

But for the youngest cohorts we have limited data.
For the cohort born in 2000, we've only observed them from ages 15-24, covering just one-third of their reproductive span. For those born in 2009, we've only seen age 15—about 3% of their total reproductive years.

Projections for these cohorts rely on the model's assumptions, not just on observed data. The model uses Gaussian random walks to model generational changes -- which assumes that in the absence of evidence, each cohort will be similar to the previous one. 

Importantly, the model does not extrapolate declining trends -- that is, it doesn't assume the recent decline will continue indefinitely, but it also doesn't assume trends will reverse. For the youngest cohorts, the projections level off rather than continuing downward. 

Going forward, if something changes dramatically—new policies, economic shifts, cultural reversals—actual fertility could differ substantially from these projections.

## Model Extensions

I also tested an extended version of the model (v4) that accounts for timing shifts—whether cohorts are having children earlier or later than the typical age pattern. The extended model fits the data better, but the projections it produces are not substantially different. The following figure shows the differences.

![Model Comparison](figs/comparison_cfr_v4.png)

Details of the extended model are in the [Technical Report](tech_report.md).

## Summary

Using Bayesian methods and nearly 50 years of fertility data, we can project cohort fertility rates for generations still in their reproductive years. The projections predict dramatic declines to historically unprecedented levels.

These projections should be interpreted as "what we would expect if recent patterns persist." Fertility can and does respond to changing circumstances -- but demographic trends have momentum.
They don't reverse quickly or easily.

Substantial uncertainty remains, especially for the youngest cohorts. We won't know their actual completed fertility until the 2040s or 2050s. But unless something changes, US fertility is heading for historic lows.

---

**DATA AND METHODS**: The analysis uses [CPS Fertility Supplement](https://www.census.gov/data/datasets/time-series/demo/cps/cps-supp_cps-repwgt/cps-fertility.html) data from 1976-2024, covering 1.17 million women aged 15-54. The model is a Bayesian hierarchical log-linear model with Gaussian random walk priors, fit using PyMC. The model accounts for survey weights by resampling and was validated against historical Census cohort fertility tables. All code and notebooks are available at [github.com/AllenDowney/BayesFertility](https://github.com/AllenDowney/BayesFertility). For complete technical details, see the [Technical Report](tech_report.md).

---

*January 2026*

