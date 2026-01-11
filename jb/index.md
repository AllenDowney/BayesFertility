# Bayesian Fertility Rate Projections

## About This Project

Fertility rates in the United States and other developed countries have been declining for several decades. Understanding these trends and projecting future fertility patterns is crucial for policy planning in areas such as education, healthcare, and social security. This project uses Bayesian statistical methods to model historical fertility patterns and project future cohort fertility rates using data from the US Census Current Population Survey (CPS).

## Motivation

Cohort fertility rates measure the average number of children born to women in a specific birth cohort over their reproductive lifetime. Unlike period fertility rates (which measure births in a given year), cohort fertility rates better capture long-term trends and can reveal generational shifts in reproductive behavior.

Recent trends suggest that cohorts born after 1980 may experience substantially lower lifetime fertility than previous generations. This has important implications for:
- **Demographic projections**: Population growth and aging patterns
- **Economic planning**: Labor force size and dependency ratios
- **Social policy**: Healthcare, education, and retirement systems

## Key Questions

This project addresses several key questions:

1. **What are the long-term fertility trends** for recent birth cohorts?
2. **How low might fertility rates go** for cohorts currently in their reproductive years?
3. **Can we reliably project future fertility** using historical patterns?
4. **How well do model predictions validate** against historical Census data?

## Contents

- [Technical Report](tech_report.md) - **Full analysis**: Comprehensive documentation of data sources, methodology, Bayesian model specification, results, validation, and projections.

## Methodology Overview

Our approach uses a **Bayesian hierarchical log-linear model** to capture age-specific fertility patterns across birth cohorts:

- **Data**: US Census Current Population Survey (CPS) data from 1976-2024
- **Model structure**: Log-linear model with cohort and age effects
- **Priors**: Gaussian random walk priors to capture smooth temporal changes
- **Validation**: Backtesting against historical Census data
- **Projection**: Posterior predictive distributions for future cohort fertility

The model accounts for survey weights through resampling, ensuring that results reflect the actual US population rather than just the survey respondents.

## Key Findings

Preliminary results suggest:

- **Declining fertility** for cohorts born after 1980
- **Projected CFR** could drop below 1.0 child per woman for cohorts born in the 2000s
- **Model validation** shows good agreement with historical Census data, increasing confidence in projections
- **Uncertainty quantification** provides credible intervals for all projections

For detailed findings, see the [Technical Report](tech_report.md).

## Data Sources

- **IPUMS CPS**: Historical CPS data (June 1976 - June 2022)
- **US Census Bureau**: June 2024 CPS data
- **Census Historical Tables**: Validation data for model checking

## About the Model

The Bayesian approach provides several advantages:

- **Uncertainty quantification**: All estimates include credible intervals
- **Flexibility**: Can incorporate prior knowledge and handle missing data
- **Validation**: Enables rigorous backtesting and out-of-sample prediction
- **Interpretability**: Parameters have clear demographic interpretations

---

*This project is a work in progress. Results are preliminary and subject to revision.*

