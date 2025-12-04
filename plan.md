# Project Plan

## Summary of Jupyter Notebooks

### 1. fertility_cps.ipynb - Census CPS Fertility Analysis

**Purpose**: Model and project cohort fertility rates using US Census Current Population Survey (CPS) data.

**Data Sources**:
- IPUMS CPS data (Extract 11): June 1976 to June 2022 (28 samples)
- June 2024 CPS data from Census Bureau
- Historical Census time series tables for validation

**Key Features**:
- Groups respondents into 3-year bins by birth cohort and age group
- Handles survey weighting through resampling and explicit weighting methods
- Implements a Bayesian log-linear model using PyMC with:
  - Gaussian random walk priors for cohort effects (α)
  - Gaussian random walk priors for age effects (β)
  - Log-linear model: λ = exp(α + β) for age-specific birth rates (ASBR)
  - Cumulative sum of ASBRs to model parity
  - Poisson likelihood for observed parity data
- Performs backtesting by making predictions with different cutoff years (1976-2024)
- Validates model predictions against Census historical data
- Projects future Cohort Completed Fertility Rates (CFR) for recent cohorts

**Main Findings**:
- Model predicts declining CFR starting with cohorts born around 1980
- Projects CFR could drop below 1.0 for cohorts born in the 2000s
- Model fits historical Census data well, increasing confidence in projections

---

### 2. fertility_nsfg.ipynb - NSFG Fertility Analysis

**Purpose**: Model and project cohort fertility rates using National Survey of Family Growth (NSFG) data.

**Data Sources**:
- NSFG data from multiple cycles (1982 through 2022-23)
- Historical Census time series tables for validation

**Key Features**:
- Similar modeling approach to the CPS notebook
- Groups respondents into 3-year bins by birth cohort and age group
- Handles stratified sampling weights by cycle
- Uses same Bayesian log-linear model structure:
  - Gaussian random walk priors for cohort and age effects
  - Log-linear model for ASBR
  - Cumulative sum to model parity
  - Poisson likelihood
- Projects CFR for future cohorts
- Compares results to Census data for validation

**Main Findings**:
- Confirms declining fertility trends in recent cohorts (1990s and 2000s)
- Projects substantial decline in CFR over next 30 years
- Suggests CFR could drop below 1.0 between 2040-2050 if trends continue

---

### 3. fertility2.ipynb - Model Prototype/Example

**Purpose**: Appears to be an experimental or learning notebook with a simplified model structure.

**Key Features**:
- Contains a basic PyMC model structure similar to the other notebooks
- Uses placeholder/random data for demonstration
- Shows core model components:
  - Gaussian random walk for cohort effects
  - Normal prior for age effects (simpler than random walk)
  - Log-linear model and cumulative sum structure
  - Poisson likelihood
- Much simpler and shorter than the other two notebooks
- Likely serves as a prototype or educational example

---

## Common Modeling Approach

All three notebooks use a similar Bayesian framework:

1. **Data Preparation**: Group respondents by birth cohort and age, handle survey weights
2. **Model Structure**: Log-linear model with cohort and age effects
3. **Priors**: Gaussian random walks to capture smooth temporal changes
4. **Likelihood**: Poisson distribution for observed parity counts
5. **Prediction**: Use posterior samples to project future fertility rates

## Regression Testing Strategy for Model Revisions

When revising the model in `fertility_cps.ipynb`, we need to save just enough data to reproduce and compare three key outputs:

1. **Graph of cohort effects** (alpha)
2. **Graph of age effects** (beta)  
3. **Predicted CFR** (at age 48)

### What to Save

For each model version, save a single file containing:

1. **Cohort effects** (`alpha_summary`):
   - Mean, HDI lower, HDI upper for each cohort
   - Cohort labels for x-axis

2. **Age effects** (`beta_summary`):
   - Mean, HDI lower, HDI upper for each age group
   - Age labels for x-axis

3. **Predicted CFR** (`pred_cfr_age48`):
   - Mean predicted CFR at age 48 for each cohort
   - HDI lower and upper bounds
   - Cohort labels for x-axis

### File Format

Save as a single HDF5 file (or JSON) with a simple structure:
```
results/
  fertility_cps_v1.0.h5  # or .json
  fertility_cps_v2.0.h5
  ...
```

Each file contains:
- `alpha_summary` - DataFrame with columns: cohort, mean, hdi_lower, hdi_upper
- `beta_summary` - DataFrame with columns: age, mean, hdi_lower, hdi_upper  
- `cfr_age48` - DataFrame with columns: cohort, mean, hdi_lower, hdi_upper
- `model_version` - string identifier
- `timestamp` - when the model was run

### Simple Functions

```python
def save_baseline_results(version, alpha_summary, beta_summary, cfr_age48):
    """Save baseline results for regression testing."""
    filename = f"results/fertility_cps_{version}.h5"
    alpha_summary.to_hdf(filename, key='alpha')
    beta_summary.to_hdf(filename, key='beta')
    cfr_age48.to_hdf(filename, key='cfr_age48')
    pd.Series({'version': version, 'timestamp': pd.Timestamp.now()}).to_hdf(
        filename, key='metadata'
    )

def load_baseline_results(version):
    """Load baseline results."""
    filename = f"results/fertility_cps_{version}.h5"
    return {
        'alpha': pd.read_hdf(filename, key='alpha'),
        'beta': pd.read_hdf(filename, key='beta'),
        'cfr_age48': pd.read_hdf(filename, key='cfr_age48'),
    }

def plot_comparison(version1, version2):
    """Plot side-by-side comparison of two model versions."""
    v1 = load_baseline_results(version1)
    v2 = load_baseline_results(version2)
    # Plot three comparison graphs
```

### Usage in Notebook

After fitting the model and generating predictions:

```python
# Prepare data for saving
alpha_summary_save = pd.DataFrame({
    'cohort': cohort_labels,
    'mean': alpha_summary['mean'],
    'hdi_lower': alpha_summary['hdi_3%'],
    'hdi_upper': alpha_summary['hdi_97%']
})

beta_summary_save = pd.DataFrame({
    'age': age_labels,
    'mean': beta_summary['mean'],
    'hdi_lower': beta_summary['hdi_3%'],
    'hdi_upper': beta_summary['hdi_97%']
})

cfr_age48_save = pd.DataFrame({
    'cohort': cohort_labels,
    'mean': mean_cumulative_rate[48],
    'hdi_lower': low[48],
    'hdi_upper': high[48]
})

# Save baseline
save_baseline_results('v1.0', alpha_summary_save, beta_summary_save, cfr_age48_save)
```

When comparing versions, load both and plot them together to see differences.

## Recent Changes

### Notebook Reorganization
- Split `fertility_cps.ipynb` into two notebooks:
  - `process_cps.md`: Handles all data preprocessing (loading, cleaning, binning, resampling, aggregation)
  - `fertility_cps2.md`: Focuses on modeling and comparison, loads preprocessed data from HDF5
- Moved notebooks to `notebooks/` folder
- Updated file paths to use `../data/` for data files

### Data Preprocessing Improvements (`process_cps.md`)
- Updated to load single data file `cps_00013.dta.gz` which includes 2024 data (29 samples: June 1976 to June 2024)
- Removed separate 2024 data loading and merging code
- Changed CFR computation from resampling to direct weighted mean calculation using `np.average()` with weights
- Added `cfr_cps` to the preprocessed HDF5 output file for comparison with Census data
- Fixed NaN handling in weighted mean calculation
- Added comparison code to compare weighted vs sampled datasets
- **Current status**: Using resampled data for modeling (works correctly)
- **Known issue**: Weighted data produces incorrect results, especially for age effects. Root cause not yet identified. The weighted and sampled datasets are similar, but the model fails with weighted data.

### Regression Testing Implementation
- Moved `save_baseline_results()` and `load_baseline_results()` functions to `utils.py` for reuse across notebooks
- Implemented HDF5-based storage for model version comparison with backward compatibility (checks for both `cfr_df` and `cfr_age48` keys)
- Saves three key outputs: cohort effects (alpha), age effects (beta), and predicted CFR
- Updated to use `cfr_df` variable name instead of `cfr_age48` throughout
- Changed CFR age from 48 to 42 to match CPS range (40-44)
- Added comparison plotting code to visualize differences between model versions
- Version 3.0 implemented with `random_walk_sigma` as a hyperparameter (commented out in current version)

### Code Quality
- Set random seeds for reproducibility (resampling and MCMC)
- Updated comparison plots to be three separate figures instead of subplots
- Fixed FutureWarning in pandas groupby operations
- Fixed typos and placeholder text in notebooks
- Synced `fertility_cps2.md` and `fertility_cps3.md` to be consistent except for model differences and version numbers

## Current Status

- **Model is working correctly** with resampled data
- **Model versions**: 
  - v2.0: Uses fixed `random_walk_sigma` parameter
  - v3.0: Has `random_walk_sigma` as hyperparameter (currently commented out)
- **Data preprocessing**: Using resampled data (not weighted) due to model issues with weighted data

## Known Issues

1. **Weighted data produces incorrect results**: When using explicitly weighted data (instead of resampling), the model produces incorrect results, especially for age effects. The weighted and sampled datasets are similar, but the model fails with weighted data. Possible causes:
   - Non-integer observed values in Poisson likelihood (weighted sums are continuous, not integers)
   - Scale/normalization issues with weighted data
   - Need for different likelihood function for weighted continuous data
   - Root cause not yet identified

## Next Steps

1. **Investigate weighted data issue**: Determine why the model fails with weighted data despite similar input values
2. **Consider alternative likelihood**: For weighted data, may need to use Normal likelihood or other continuous distribution instead of Poisson
3. **Model refinement**: Continue improving model structure and validation
4. **Documentation**: Document model versioning scheme and decision rationale

