"""Utility functions for data analysis and visualization."""

import os
import re

import arviz as az
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymc as pm
import seaborn as sns
from IPython.display import Audio, display
from matplotlib import font_manager
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from scipy.stats import beta, norm

# =============================================================================
# Matplotlib Configuration
# =============================================================================

AIBM_COLORS = {
    # AIBM brand colors
    "light_gray": "#F3F4F3",
    "medium_gray": "#767676",
    "green": "#0B8569",
    "light_green": "#AAC9B8",
    "orange": "#C55300",
    "light_orange": "#F4A26B",
    "purple": "#9657A5",
    "light_purple": "#CFBCD0",
    "blue": "#4575D6",
    "light_blue": "#C9D3E8",
    # Additional colors from coolers.co
    "dark_gray": "#404040",
    "dark_purple": "#28112B",
    "dark_green": "#002500",
    "amber": "#F5BB00",
    "oxford_blue": "#000022",
    "bittersweet": "#FF6666",
    "crimson": "#D62839",
}


def configure_plot_style():
    """Configure the default matplotlib style for AIBM plots.

    This function sets up the default style for plots, including:
    - Figure size and DPI
    - Color scheme
    - Font settings
    - Grid and spine settings
    - Tick settings

    The settings can be overridden for individual plots as needed.
    """
    # Figure size and DPI
    plt.rcParams["figure.dpi"] = 100
    plt.rcParams["figure.figsize"] = [6.75, 3.5]  # inches

    # Default color cycle
    colors = [
        AIBM_COLORS["green"],
        AIBM_COLORS["orange"],
        AIBM_COLORS["blue"],
        AIBM_COLORS["purple"],
    ]
    cycler = plt.cycler(color=colors)
    plt.rc("axes", prop_cycle=cycler)

    # Font settings
    # Try to use PT Sans, fall back to system fonts if not available
    if "PT Sans" in [f.name for f in font_manager.fontManager.ttflist]:
        plt.rcParams["font.family"] = "PT Sans"
    else:
        plt.rcParams["font.family"] = "sans-serif"
        plt.rcParams["font.sans-serif"] = [
            "DejaVu Sans",
            "Arial",
            "Helvetica",
            "sans-serif",
        ]

    plt.rcParams["legend.fontsize"] = "small"

    # Tick and label colors
    plt.rcParams["axes.edgecolor"] = AIBM_COLORS["medium_gray"]
    plt.rcParams["xtick.color"] = AIBM_COLORS["medium_gray"]
    plt.rcParams["ytick.color"] = AIBM_COLORS["medium_gray"]
    plt.rcParams["axes.labelcolor"] = AIBM_COLORS["medium_gray"]

    # Default spine settings (can be overridden per plot)
    plt.rcParams["axes.spines.top"] = False
    plt.rcParams["axes.spines.right"] = False
    plt.rcParams["axes.spines.left"] = False
    plt.rcParams["axes.spines.bottom"] = False

    # Default grid settings (can be overridden per plot)
    plt.rcParams["grid.color"] = AIBM_COLORS["light_gray"]
    plt.rcParams["grid.linestyle"] = "-"
    plt.rcParams["grid.linewidth"] = 1
    plt.rcParams["axes.grid"] = False  # Disable grid by default
    plt.rcParams["axes.grid.axis"] = "y"

    # Tick mark settings
    plt.rcParams["xtick.major.size"] = 0
    plt.rcParams["xtick.minor.size"] = 0
    plt.rcParams["ytick.major.size"] = 0
    plt.rcParams["ytick.minor.size"] = 0


# Apply the default style
configure_plot_style()

# =============================================================================
# File I/O Functions
# =============================================================================


def write_table(table, label, **options):
    """Write a table in LaTex format.

    Args:
        table: DataFrame
        label: string
        options: passed to DataFrame.to_latex
    """
    filename = f"tables/{label}.tex"
    os.makedirs("tables", exist_ok=True)
    with open(filename, "w", encoding="utf8") as fp:
        s = table.to_latex(**options)
        fp.write(s)


def write_pmf(pmf, label):
    """Write a Pmf object as a table.

    Args:
        pmf: Pmf
        label: string
    """
    df = pd.DataFrame()
    df["qs"] = pmf.index
    df["ps"] = pmf.values
    write_table(df, label, index=False)


def savefig(prefix, fig_number, extra_artists=[], dpi=150):
    """Save the current figure with the given filename.

    Args:
        prefix: string prefix for filename
        fig_number: The figure number
        extra_artists: List of additional artist to include in the bounding box
        dpi: Dots per inch for the saved image
    """
    filename = f"{prefix}{fig_number:02d}"
    if extra_artists:
        plt.savefig(
            filename, dpi=dpi, bbox_inches="tight", bbox_extra_artists=extra_artists
        )
    else:
        plt.savefig(filename, dpi=dpi)


# =============================================================================
# Data Manipulation Functions
# =============================================================================


def underride(d, **options):
    """Add key-value pairs to d only if key is not in d.

    Args:
        d: dictionary
        options: keyword args to add to d

    Returns:
        Updated dictionary
    """
    for key, val in options.items():
        d.setdefault(key, val)
    return d


def value_counts(seq, **options):
    """Make a series of values and the number of times they appear.

    Returns a DataFrame because they get rendered better in Jupyter.

    Args:
        seq: sequence
        options: passed to pd.Series.value_counts

    Returns:
        pd.DataFrame with value counts
    """
    options = underride(options, dropna=False)
    series = pd.Series(seq).value_counts(**options).sort_index()
    series.index.name = "values"
    series.name = "counts"
    return pd.DataFrame(series)


def value_count_frame(data, columns, normalize=False):
    """Value counts for each column.

    Returns: DataFrame with one row per value, one column per variable
    """
    return pd.DataFrame(
        {col: data[col].value_counts(normalize=normalize) for col in columns}
    ).fillna(0)


def round_into_bins(series, bin_width, low=0, high=None):
    """Rounds values down to the bin they belong in.

    series: pd.Series
    bin_width: number, width of the bins

    returns: Series of bin values (with NaN preserved)
    """
    if high is None:
        high = series.max()

    bins = np.arange(low, high + bin_width, bin_width)
    indices = np.digitize(series, bins)
    result = pd.Series(bins[indices - 1], index=series.index, dtype="float")

    result[series.isna()] = np.nan
    return result




# =============================================================================
# Statistical Functions
# =============================================================================


def estimate_proportion_jeffreys(success_series, confidence_level=0.95):
    """Estimate proportion using Jeffreys prior.

    Args:
        success_series: Boolean series (True = success)
        confidence_level: Confidence level (e.g., 0.95)

    Returns:
        tuple: (proportion, lower_bound, upper_bound)
    """
    success_series = success_series.astype(float)
    n = len(success_series)
    k = success_series.sum()

    # Jeffreys prior: Beta(0.5, 0.5)
    alpha = k + 0.5
    beta_param = n - k + 0.5

    # Calculate posterior mean
    proportion = alpha / (alpha + beta_param)

    # Calculate credible interval
    dist = beta(alpha, beta_param)
    lower = dist.ppf((1 - confidence_level) / 2)
    upper = dist.ppf(1 - (1 - confidence_level) / 2)

    return proportion, lower, upper


def estimate_proportion_wilson(success_series, weights_series, confidence_level=0.95):
    """Calculate the weighted proportion and Wilson score interval for weighted data.

    Args:
        success_series (pd.Series): A boolean series where True represents a success.
        weights_series (pd.Series): A series of weights corresponding to the success_series.
        confidence_level (float): The confidence level for the Wilson score interval

    Returns:
    weighted_proportion (float): The weighted proportion of successes.
    lower (float): The lower bound of the Wilson score interval.
    upper (float): The upper bound of the Wilson score interval.
    """
    # Ensure the series are aligned and of correct type
    success_series = success_series.astype(float)
    weights_series = weights_series.astype(float)

    # Calculate weighted proportion
    total_weight = weights_series.sum()
    weighted_successes = (success_series * weights_series).sum()
    p = weighted_successes / total_weight

    # Calculate the z-score for the given confidence level
    z = norm.ppf(1 - (1 - confidence_level) / 2)

    # Wilson score interval adjusted for weighted data
    denominator = 1 + z**2 / total_weight
    center = (p + z**2 / (2 * total_weight)) / denominator
    sd = np.sqrt((p * (1 - p) + z**2 / (4 * total_weight)) / total_weight) / denominator

    # Lower and upper bounds of the Wilson interval
    lower = center - z * sd
    upper = center + z * sd

    return p, lower, upper





# =============================================================================
# Basic Plotting Functions
# =============================================================================


def decorate(**options):
    """Decorate the current axes.

    Call decorate with keyword arguments like
    decorate(title='Title',
             xlabel='x',
             ylabel='y')

    The keyword arguments can be any of the axis properties
    https://matplotlib.org/api/axes_api.html
    """
    legend = options.pop("legend", True)
    loc = options.pop("loc", "best")
    ax = plt.gca()
    ax.set(**options)

    handles, labels = ax.get_legend_handles_labels()
    if handles and legend:
        ax.legend(handles, labels, loc=loc)

    plt.tight_layout()


def anchor_legend(x, y):
    """Place the upper left corner of the legend box.

    Args:
        x: x coordinate
        y: y coordinate
    """
    plt.legend(bbox_to_anchor=(x, y), loc="upper left", ncol=1)
    plt.tight_layout()


def add_text(x, y, text, **options):
    """Add text to the current axes.

    Args:
        x: float
        y: float
        text: string
        options: keyword arguments passed to plt.text
    """
    ax = plt.gca()
    underride(
        options,
        transform=ax.transAxes,
        color="0.2",
        ha="left",
        va="bottom",
        fontsize=9,
    )
    plt.text(x, y, text, **options)


def remove_spines():
    """Remove the spines of a plot but keep the ticks visible."""
    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Ensure ticks stay visible
    ax.xaxis.set_ticks_position("bottom")
    ax.yaxis.set_ticks_position("left")


def add_logo(filename="logo-hq-small.png", location=(1.0, -0.35), size=(0.5, 0.25)):
    """Add a logo inside an inset axis positioned relative to the main plot.

    Args:
        filename: path to logo image
        location: tuple of (x, y) coordinates
        size: tuple of (width, height)

    Returns:
        The inset axis containing the logo
    """
    logo = mpimg.imread(filename)

    # Create an inset axis in the given location
    ax = plt.gca()
    fig = ax.figure
    ax_inset = inset_axes(
        ax,
        width=size[0],
        height=size[1],
        loc="lower right",
        bbox_to_anchor=location,
        bbox_transform=fig.transFigure,
        borderpad=0,
    )

    # Display the logo
    ax_inset.imshow(logo)
    ax_inset.axis("off")
    
    # Restore the original axes as current
    plt.sca(ax)

    return ax_inset


def add_subtext(text, x=0, y=-0.35):
    """Add a text label below the current plot.

    Args:
        text: string
        x: x coordinate
        y: y coordinate

    Returns:
        The text object
    """
    ax = plt.gca()
    fig = ax.figure
    return plt.figtext(
        x, y, text, ha="left", va="bottom", fontsize=8, transform=fig.transFigure
    )


def add_title(title, subtitle, pad=25, x=0, y=1.02):
    """Add a title and subtitle to the current plot.

    Args:
        title: Title of the plot
        subtitle: Subtitle of the plot
        pad: Padding between the title and subtitle
        x: x coordinate for subtitle
        y: y coordinate for subtitle
    """
    plt.title(title, loc="left", pad=pad)
    add_text(x, y, subtitle)


# =============================================================================
# BayesFertility-Specific Functions
# =============================================================================


def resample_rows_weighted(df, column="finalwgt"):
    """Resamples a DataFrame using probabilities proportional to given column.

    df: DataFrame
    column: string column name to use as weights

    returns: DataFrame
    """
    weights = df[column]
    sample = df.sample(n=len(df), replace=True, weights=weights)
    return sample


def load_idata_or_sample(
    model: pm.Model, filename: str, force_run: bool = False, **sample_options
) -> az.InferenceData:
    """
    Runs PyMC sampling and saves the results to a NetCDF file, or loads existing results from the file.

    Load existing idata if the file exists and force_run is False.
    Runs the sampler and saves the idata if the file doesn't exist or force_run is True.

    Args:
        model (pm.Model):
            The PyMC model object to sample from.
        filename (str):
            Path to the NetCDF file to save to or load from.
        force_run (bool):
            If true, run the sampler even if the file exists.
        **sample_options:
            Additional keyword arguments passed directly to `pm.sample()`.

    Returns:
        az.InferenceData:
            The idata (posterior samples) as an ArviZ InferenceData object.

    """
    if os.path.exists(filename) and not force_run:
        idata = az.from_netcdf(filename)
        print(f"Loaded idata from {filename}")
    else:
        with model:
            idata = pm.sample(**sample_options)

        az.to_netcdf(idata, filename)
        print(f"Saved new idata to {filename}")

    return idata


# =============================================================================
# Regression Testing Functions
# =============================================================================


def save_baseline_results(version, alpha_summary, beta_summary, cfr_df, cohort_labels, age_labels):
    """Save baseline results for regression testing.
    
    Args:
        version: string version identifier (e.g., 'v1.0')
        alpha_summary: DataFrame with cohort effects summary
        beta_summary: DataFrame with age effects summary
        cfr_df: Series or DataFrame with CFR predictions
        cohort_labels: array of cohort labels
        age_labels: array of age labels
    """
    os.makedirs("results", exist_ok=True)
    filename = f"results/fertility_cps_{version}.h5"
    
    # Prepare alpha data
    alpha_df = pd.DataFrame({
        'cohort': cohort_labels,
        'mean': alpha_summary['mean'].values,
        'hdi_lower': alpha_summary['hdi_3%'].values,
        'hdi_upper': alpha_summary['hdi_97%'].values
    })
    
    # Prepare beta data
    beta_df = pd.DataFrame({
        'age': age_labels,
        'mean': beta_summary['mean'].values,
        'hdi_lower': beta_summary['hdi_3%'].values,
        'hdi_upper': beta_summary['hdi_97%'].values
    })
    
    # Prepare CFR data
    if isinstance(cfr_df, pd.Series):
        cfr_data = pd.DataFrame({
            'cohort': cfr_df.index,
            'mean': cfr_df.values
        })
    else:
        # Assume DataFrame with 'cohort', 'mean', 'low', 'high' columns
        # Use the 'cohort' column, not the index
        cfr_data = pd.DataFrame({
            'cohort': cfr_df['cohort'].values,
            'mean': cfr_df['mean'].values
        })
        if 'low' in cfr_df.columns:
            cfr_data['hdi_lower'] = cfr_df['low'].values
        if 'high' in cfr_df.columns:
            cfr_data['hdi_upper'] = cfr_df['high'].values
    
    # Save to HDF5
    alpha_df.to_hdf(filename, key='alpha', mode='w')
    beta_df.to_hdf(filename, key='beta', mode='a')
    cfr_data.to_hdf(filename, key='cfr_df', mode='a')
    
    # Save metadata
    metadata = pd.Series({
        'version': version,
        'timestamp': pd.Timestamp.now().isoformat()
    })
    metadata.to_hdf(filename, key='metadata', mode='a')
    
    print(f"Saved baseline results to {filename}")


def load_baseline_results(version):
    """Load baseline results for comparison.
    
    Args:
        version: string version identifier (e.g., 'v1.0')
        
    Returns:
        dict with keys 'alpha', 'beta', 'cfr_df', 'metadata'
    """
    filename = f"results/fertility_cps_{version}.h5"
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Baseline results not found: {filename}")
    
    # Check which key exists for backward compatibility
    try:
        pd.read_hdf(filename, key='cfr_df')
        cfr_key = 'cfr_df'
    except KeyError:
        try:
            pd.read_hdf(filename, key='cfr_age48')
            cfr_key = 'cfr_age48'
        except KeyError:
            raise KeyError(f"Neither 'cfr_df' nor 'cfr_age48' found in {filename}")
    
    return {
        'alpha': pd.read_hdf(filename, key='alpha'),
        'beta': pd.read_hdf(filename, key='beta'),
        'cfr_df': pd.read_hdf(filename, key=cfr_key),
        'metadata': pd.read_hdf(filename, key='metadata')
    }


# =============================================================================
# System Functions
# =============================================================================


def beep(duration=0.5, frequency=440):
    """Make a beep sound to notify when a long-running process completes.
    
    Args:
        duration: Duration of the beep in seconds (default: 0.5)
        frequency: Frequency of the beep in Hz (default: 440, A4 note)
    
    Uses IPython Audio to play a sine wave beep. Works in Jupyter notebooks.
    """
    sample_rate = 22050

    t = np.linspace(0, duration, int(sample_rate * duration))
    beep_sound = np.sin(2 * np.pi * frequency * t)

    display(Audio(beep_sound, rate=sample_rate, autoplay=True))
