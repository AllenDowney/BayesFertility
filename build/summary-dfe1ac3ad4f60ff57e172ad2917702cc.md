# Projecting US Fertility Rates: What the Data Tells Us About the Future

*A Bayesian analysis of nearly 50 years of fertility data reveals dramatic declines ahead*

## The Question

How many children will recent generations of Americans have over their lifetimes? This seemingly simple question has profound implications for the future of the United States—from population size and economic growth to social policy and retirement systems.

Unlike period fertility rates (which measure births in a given year), **cohort fertility rates** (CFR) track specific birth cohorts throughout their reproductive years, providing a more stable measure of lifetime fertility. But here's the challenge: younger cohorts are still in their reproductive years. How can we project their completed fertility?

## Our Approach

We developed a Bayesian statistical model using data from the US Census Current Population Survey (CPS) spanning 1976-2024—nearly 50 years of fertility history covering over 1 million women aged 15-54.

### The Model

We built three versions of a hierarchical Bayesian model:

**Version 3.0 (Base Model)** uses a log-linear structure to model age-specific birth rates:
- **Cohort effects (α)**: Overall fertility level for each birth cohort
- **Age effects (β)**: The typical age-fertility profile (when people have children)
- **Gaussian random walk priors**: Ensures smooth changes across adjacent cohorts

**Version 4.0 (Extended Model)** adds a crucial new component:
- **Timing shifts (γ)**: Captures whether cohorts are having children earlier or later than average
- This allows us to separate *quantum* (how many children) from *tempo* (when they have them)

We used:
- **Resampling** to properly handle complex survey weights
- **nutpie sampler** for efficient Bayesian inference
- **Backtesting** against historical Census data for validation

## Key Findings

### 1. Dramatic Fertility Decline Ahead

Our model projects that cohort fertility rates will drop dramatically for recent generations:

![CFR Predictions](figs/cfr_prediction.png)

**The numbers are stark:**
- **Peak fertility**: Cohort born 1934 → CFR = 3.10 children per woman
- **Current levels**: Cohort born 1980 → CFR = 1.86 (already below replacement)
- **Projected decline**: Cohorts born 2000-2009 → CFR = 0.78-0.89

This represents a **70%+ decline** from peak fertility, bringing the US to levels comparable to South Korea (which currently has one of the world's lowest fertility rates).

### 2. A Two-Dimensional Decline

Version 4.0 reveals that recent cohorts face a **dual challenge**:

![Timing Shifts by Cohort](figs/timing_shift_effects.png)

- **Quantum decline**: Baseline fertility (α) is falling sharply for cohorts born after 1980
- **Tempo delay**: Recent cohorts are also postponing childbearing (positive γ), shifting fertility to older ages

**The postponement transition is clear:**
- Early cohorts (1930s): γ ≈ -0.065 (earlier childbearing)
- Middle cohorts (1950s-1970s): γ ≈ 0 (stable timing)
- Recent cohorts (1980s-2000s): γ up to +0.052 (delayed childbearing)

### 3. Model Validation: It Works!

We validated our model against historical Census data:

![CFR vs Census Data](figs/cfr_vs_actual.png)

**Validation results:**
- **Correlation**: 0.9998 (nearly perfect agreement)
- **Mean absolute difference**: 0.003 children per woman
- **Goodness of fit**: R² = 0.999, MAPE = 11.12%

The extended model (v4.0) provides **substantially better fit** than the base model (ΔWAIC ≈ 438), while maintaining excellent convergence (all 77 parameters have ESS > 400).

### 4. Model Comparison: Why Version 4.0?

![Model Comparison](figs/comparison_cfr.png)

While v3.0 and v4.0 produce similar projections for most cohorts, v4.0 offers crucial advantages:
- **Better statistical fit**: Superior on all metrics (WAIC, R², MAPE)
- **Richer insights**: Explicitly separates quantum from tempo
- **Demographic validity**: Captures the well-documented postponement transition
- **Projections for youngest cohorts differ**: v4.0 projects slightly higher CFR for some cohorts (e.g., 2000: 0.89 vs 0.87)

## Important Caveats

### Limited Data for Youngest Cohorts

The most recent cohorts have been observed over only a fraction of their reproductive years:

![Observed Age Ranges](figs/observed_age_ranges.png)

| Cohort | Observed Ages | % of Reproductive Span |
|--------|---------------|------------------------|
| 2000 | 15-24 | 33% |
| 2003 | 15-21 | 23% |
| 2006 | 15-18 | 13% |
| 2009 | 15 only | 3% |

**Implication**: Projections for cohorts born after 2000 rely heavily on model assumptions rather than direct observations. We won't know their actual completed fertility until the 2040s-2050s.

### The Identifiability Challenge

For cohorts with limited early data, the model cannot definitively distinguish between:
- **Low quantum + early timing**: Fewer children overall, but having them earlier
- **High quantum + delayed timing**: More children overall, but postponing them

This is captured by high posterior correlations between α and γ for young cohorts. The uncertainty is appropriately reflected in our wide credible intervals.

## What Does This Mean?

**If current trends continue:**

1. **Population dynamics**: Without immigration, the US population could decline significantly
2. **Economic impacts**: 
   - Smaller workforce relative to retirees
   - Pressure on Social Security and Medicare
   - Shifting housing demand
   - Changes in education systems
3. **Policy implications**: Understanding these trends is crucial for long-term planning

**Historical context**: This rate of decline is comparable to the post-baby boom decline (1960s-1980s), but starting from a much lower baseline and reaching historically unprecedented low levels.

**Conservative projections**: Our Gaussian random walk priors don't extrapolate declining trends—they assume recent patterns persist. Actual fertility could decline further or reverse depending on future conditions (policy changes, economic shifts, cultural changes).

## The Bottom Line

Using robust Bayesian methods and nearly 50 years of data, we project dramatic fertility declines for recent US birth cohorts. While substantial uncertainty remains—especially for the youngest cohorts still early in their reproductive years—the model provides a principled, data-driven framework for understanding long-term fertility trends.

The projections should be interpreted as **"what we would expect if recent patterns persist,"** not as forecasts of what will definitely occur. But the trends are clear, consistent, and have major implications for America's demographic future.

---

## Technical Details

**Methods**: Bayesian hierarchical log-linear model with Gaussian random walk priors
**Data**: CPS Fertility Supplement (1976-2024), 1.17M women aged 15-54
**Model**: PyMC with nutpie sampler, 4 chains × 4000 draws
**Validation**: Backtesting against historical Census cohort fertility tables
**Code**: Available at [github.com/AllenDowney/BayesFertility](https://github.com/AllenDowney/BayesFertility)

For full technical details, see the [Technical Report](tech_report.md).

---

*Last updated: January 2026*

