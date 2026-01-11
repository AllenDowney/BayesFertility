# US Fertility Is Heading for Historic Lows

Recent generations of Americans are on track to have far fewer children than any previous generation. Using Bayesian modeling to project forward, cohorts born in the 2000s could end up with fewer than 1 child per woman on average—a level of fertility comparable to present-day South Korea.

The following figure shows cohort fertility rates (CFR) for US women born from 1920 to 2009. For older cohorts, these are observed rates—we know how many children they had over their lifetimes. For younger cohorts still in their reproductive years, the solid lines show our model's projections based on data through 2024.

![CFR Predictions](figs/cfr_prediction.png)

The trend is dramatic:

* Fertility peaked with the cohort born in 1934, who had 3.10 children per woman on average.
* Women born in 1980 have already completed most of their childbearing years with 1.86 children—below the replacement rate of 2.1.
* The model projects that women born in 2000 will have just 0.89 children on average, while those born in 2009 will have 0.78.

That would take the US to fertility levels we've never seen before.

## How the Model Works

To make these projections, I built a Bayesian hierarchical model using CPS fertility data from 1976-2024, covering 1.17 million women aged 15-54. The model estimates the following parameters:

* **Cohort effects (α)**: How fertile is this generation overall?
* **Age effects (β)**: At what ages do people typically have children?
* **Timing shifts (γ)**: Is this cohort having children earlier or later than usual?

The timing shifts make it possible to distinguish *how many* children people have (quantum) versus *when* they have them (tempo). As we'll see, both are changing for recent cohorts.

## A Two-Dimensional Decline

The next figure shows the cohort effects—that is, a fertility level for each generation.

![Cohort Effects](figs/cohort_effects.png)

There are three distinct eras:

* The baby boom generations (born 1930s-1950s) had high fertility
* Gen X and early Millennials (born 1960s-1980s) saw steady decline
* Recent cohorts (born 1990s-2000s) show accelerating decline

But that's only part of the story. Recent generations are also postponing childbearing. The following figure shows timing shifts—positive values mean having children later, negative means earlier.

![Timing Shifts by Cohort](figs/timing_shift_effects.png)

The transition is clear:

* Early cohorts (1930s-1940s): negative timing shifts, having children relatively early
* Middle cohorts (1950s-1970s): near zero, stable timing
* Recent cohorts (1980s-2000s): increasingly positive, postponing childbearing

The recent cohorts ...

## Validation

We can validate the model on cohorts who have already completed their childbearing. The following figure compares our model's estimates (for cohorts with observed data at most ages) against actual completed fertility from Census data.

![CFR vs Census Data](figs/cfr_vs_actual.png)

The agreement is nearly perfect—the mean absolute difference is just 0.003 children per woman. For cohorts where we have complete data, the model works very well.

But for the youngest cohorts we have limited data.
For the cohort born in 2000, we've only observed them from ages 15-24, covering just one-third of their reproductive span. For those born in 2009, we've only seen age 15—about 3% of their total reproductive years.

Projections for these cohorts rely on the model's assumptions, not just on observed data. The model uses Gaussian random walks to model generational changes -- which assumes that in the absence of evidence, each cohort will be similar to the previous one. 

Importantly, the model does *not* extrapolate declining trends—it doesn't assume the recent decline will continue indefinitely, but it also doesn't assume trends will reverse. For the youngest cohorts, the projections tend to level off rather than continuing downward. If something changes dramatically—new policies, economic shifts, cultural reversals—actual fertility could differ substantially from these projections.

## Effect of Timing Shifts

I tested several versions of this model. Version 3.0 is simpler—it just has cohort effects and age effects, without the timing shifts.  Version 4.0 fits the data substantially better, as we should expect with more parameters.

The following figure compares their CFR projections:

![Model Comparison](figs/comparison_cfr.png)

For most cohorts, the projections are nearly identical. But for some younger cohorts, v4.0 projects slightly higher fertility.

That said, the timing shifts alone aren't enough to change the overall story -- the projections remain very low.

## Implications

This rate of decline would have a range of implications:

**Population dynamics**: Without increased immigration, the US population would decline significantly. 

**Economic impacts**: A smaller workforce relative to the number of retirees puts pressure on Social Security and Medicare. Housing demand shifts as fewer families form. School systems will need to adjust to smaller cohorts.

**Historical context**: This rate of decline is comparable to the post-baby boom transition (1960s-1980s), but starting from a much lower baseline. The US has never seen fertility this low.

**Policy questions**: Understanding whether people want fewer children or face barriers to having children they want is crucial for policy responses. The model projections suggest recent cohorts will have fewer children, but they don't tell us why.

## Summary

Using Bayesian methods and nearly 50 years of fertility data, we can project cohort fertility rates for generations still in their reproductive years. The projections show dramatic declines ahead—potentially to historically unprecedented levels.

These projections should be interpreted as "what we would expect if recent patterns persist," not as definitive forecasts. Fertility can and does respond to changing circumstances. But demographic trends have momentum—they don't reverse quickly or easily.

Substantial uncertainty remains, especially for the youngest cohorts. We won't know their actual completed fertility until the 2040s or 2050s. But the trends are consistent and clear: unless something changes, US fertility is heading for historic lows.

---

**DATA AND METHODS**: The analysis uses [CPS Fertility Supplement](https://www.census.gov/data/datasets/time-series/demo/cps/cps-supp_cps-repwgt/cps-fertility.html) data from 1976-2024, covering 1.17 million women aged 15-54. The model is a Bayesian hierarchical log-linear model with Gaussian random walk priors, fit using PyMC. The model accounts for complex survey weights through resampling and was validated against historical Census cohort fertility tables. All code and notebooks are available at [github.com/AllenDowney/BayesFertility](https://github.com/AllenDowney/BayesFertility). For complete technical details, see the [Technical Report](tech_report.md).

---

*January 2026*

