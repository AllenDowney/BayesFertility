"""Supporting code fot the BayesFertility repository."""

import re

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from scipy.stats import beta, norm

aibm_light_gray = "#F3F4F3"
aibm_medium_gray = "#767676"
aibm_green = "#0B8569"
light_green = "#AAC9B8"
aibm_orange = "#C55300"
light_orange = "#F4A26B"
aibm_purple = "#9657A5"
light_purple = "#CFBCD0"
aibm_blue = "#4575D6"
light_blue = "#C9D3E8"


def write_table(table, label, **options):
    """Write a table in LaTex format.

    table: DataFrame
    label: string
    options: passed to DataFrame.to_latex
    """
    filename = f"tables/{label}.tex"
    fp = open(filename, "w", encoding="utf8")
    s = table.to_latex(**options)
    fp.write(s)
    fp.close()


def write_pmf(pmf, label):
    """Write a Pmf object as a table.

    pmf: Pmf
    label: string
    """
    df = pd.DataFrame()
    df["qs"] = pmf.index
    df["ps"] = pmf.values
    write_table(df, label, index=False)


def underride(d, **options):
    """Add key-value pairs to d only if key is not in d.

    d: dictionary
    options: keyword args to add to d
    """
    for key, val in options.items():
        d.setdefault(key, val)

    return d


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

    x: x coordinate
    y: y coordinate
    """
    plt.legend(bbox_to_anchor=(x, y), loc="upper left", ncol=1)
    plt.tight_layout()


def value_counts(seq, **options):
    """Make a series of values and the number of times they appear.

    Returns a DataFrame because they get rendered better in Jupyter.

    Args:
        seq: sequence
        options: passed to pd.Series.value_counts

    returns: pd.Series
    """
    options = underride(options, dropna=False)
    series = pd.Series(seq).value_counts(**options).sort_index()
    series.index.name = "values"
    series.name = "counts"
    return pd.DataFrame(series)


def add_text(x, y, text, **options):
    """Add text to the current axes.

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


def add_logo(filename="logo-hq-small.png", location=(1.0, -0.25), size=(0.5, 0.25)):
    """Add a logo inside an inset axis positioned relative to the main plot."""

    logo = mpimg.imread(filename)

    # Create an inset axis in the given location (transAxes places it relative to the axes)
    ax = plt.gca()
    ax_inset = inset_axes(
        ax,
        width=size[0],
        height=size[1],
        loc="lower right",
        bbox_to_anchor=location,
        bbox_transform=ax.transAxes,
        borderpad=0,
    )

    # Display the logo
    ax_inset.imshow(logo)
    ax_inset.axis("off")

    return ax_inset


def add_subtext(text, x=0, y=-0.25):
    """Add a text label below the current plot.

    Args:
        text: string
    """
    ax = plt.gca()
    plt.figtext(
        x, y, text, ha="left", va="bottom", fontsize=8, transform=ax.transAxes
    )


def add_title(title, subtitle, pad=25):
    """Add a title and subtitle to the current plot.

    Args:
        title (str): Title of the plot
        subtitle (str): Subtitle of the plot
        pad (int): Padding between the title and subtitle
    """
    plt.title(title, loc="left", pad=pad)
    add_text(0, 1.02, subtitle)


def savefig(prefix, fig_number, extra_artist):
    """Save the current figure with the given filename.

    Args:
        fig_number (int): The figure number
        extra_artist: Additional artist to include in the bounding box
    """
    filename = f"{prefix}{fig_number:02d}"
    plt.savefig(
        filename, dpi=150, bbox_inches="tight", bbox_extra_artists=[extra_artist]
    )


def find_columns(df, prefix):
    """Find columns that start with a given prefix.

    Args:
        df: DataFrame
        prefix: string prefix

    Returns: list of column names
    """
    return [
        col
        for col in df.columns
        if col.startswith(prefix)
        and not col.endswith("skp")
        and not col.endswith("timing")
    ]


def extract_categorical_mapping(series):
    """Extract a mapping from categorical codes to descriptions.

    Args:
        series: pandas Series

    Returns: dictionary that maps from codes to descriptions
    """
    mapping = {}

    for item in series.unique():  # Process unique categorical values
        match = re.match(r"([-\d]+)\.\s(.+)", str(item).strip())
        if match:
            code, description = match.groups()
            mapping[int(code)] = description

    return mapping


def make_categorical_mappings(df, skip_cols=["age"]):
    """Make a mapping from variable names to dictionaries of codes and values.

    Args:
        df: DataFrame
        skip_cols: list of string column names to skip

    Returns: dictionary that maps from column names to dictionaries
    """
    categorical_mappings = {}

    for column in df.columns:
        if column in skip_cols:
            continue

        if isinstance(df[column].dtype, pd.CategoricalDtype):
            mapping = extract_categorical_mapping(df[column])
            categorical_mappings[column] = mapping

    return categorical_mappings


def estimate_proportion_jeffreys(success_series):
    """Estimate the proportion of successes using Jeffrey's prior.

    Args:
        success_series: Series of successes
        weights_series: Series of weights

    Returns: tuple of (p, lower, upper)
    """
    n = success_series.count()
    k = success_series.sum()
    p = k / n
    dist = beta(k + 1 / 2, n - k + 1 / 2)
    lower, upper = dist.ppf([0.025, 0.975])
    return p, lower, upper


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


def value_count_frame(data, columns, normalize=False):
    """Value counts for each column.

    Returns: DataFrame with one row per value, one column per variable
    """
    return pd.DataFrame(
        {col: data[col].value_counts(normalize=normalize) for col in columns}
    ).fillna(0)


def estimate_columns(df, columns, values):
    """Estimate the proportion of responses in each column that are in values.

    Args:
        df: DataFrame
        columns: list of column names
        values: list of values to count

    Returns: DataFrame with one row per column and columns p, low, high
    """
    res = pd.DataFrame(index=columns, columns=["p", "low", "high"])
    data = df[columns].replace(-7, np.nan)
    data["weight"] = df["weight"]

    for column in columns:
        subset = data.dropna(subset=column)
        series = subset[column].isin(values)
        weight = subset["weight"]
        res.loc[column] = estimate_proportion_wilson(series, weight, confidence_level=0.84)

    return res * 100


def estimate_value_map(df, columns, value_map):
    """For each item in value_map, estimate the proportion of responses
    in each column that are in the values.

    Args:
        df: DataFrame
        columns: list of column names
        value_map: map from a name to a list of values

    Returns: DataFrame with MultiIndex containing the keys from value_map
    at the top level and (p, low, high) at the next level
    """
    df_map = {
        key: estimate_columns(df, columns, values) for key, values in value_map.items()
    }
    keys = list(df_map.keys())
    dfs = list(df_map.values())
    return pd.concat(dfs, axis=1, keys=keys)


def estimate_gender_map(columns, gender_map, value_map):
    """Make a value_map for each gender.

    Args:
        columns: list of column names
        gender_map: map from gender name to DataFrame
        value_map: map from a name to a list of values

    Returns: DataFrame with MultiIndex containing the genders at the top level,
    the keys in value_map at the next level, and (p, low, high) at the next level.
    """
    keys = list(gender_map.keys())
    dfs = [estimate_value_map(df, columns, value_map) for df in gender_map.values()]
    return pd.concat(dfs, axis=1, keys=keys)


def plot_responses(
    summary, gender, response, issue_names, style, label_response=True, **options
):
    """Plot the estimated proportion of responses.

    Args:
        summary: DataFrame with estimated proportions
        gender: string
        response: string
        issue_names: map from column names to issue names
        style: string
        label_response: boolean, whether to label the response
        options: passed to plt.plot
    """
    names = [issue_names[col] for col in summary.index]

    key = (gender, response)
    estimate = summary[key]
    plt.hlines(names, estimate["low"], estimate["high"], **options)
    if label_response:
        label = f"{gender} {response}"
    else:
        label = f"{gender}"

    plt.plot(estimate["p"], names, style, label=label, **options)


def plot_responses_by_gender(summary, response, issue_names, **options):
    """Plot the estimated proportion of responses

    Args:
        summary: DataFrame with estimated proportions
        response: string
        issue_names: map from column names to issue names
        options: passed to plt.plot
    """
    options["color"] = aibm_green
    plot_responses(summary, "male", response, issue_names, "s", **options)
    options["color"] = aibm_orange
    plot_responses(summary, "female", response, issue_names, "o", **options)
    plt.grid(True, axis="y", color="lightgray", alpha=0.5)
    decorate(xlabel="Percent")


def round_into_bins(series, bin_width, low=0, high=None):
    """Rounds values down to the bin they belong in.

    series: pd.Series
    bin_width: number, width of the bins

    returns: array of bin values
    """
    if high is None:
        high = series.max()

    bins = np.arange(low, high + bin_width, bin_width)
    indices = np.digitize(series, bins)
    return bins[indices - 1]


def resample_rows_weighted(df, column="finalwgt"):
    """Resamples a DataFrame using probabilities proportional to given column.

    df: DataFrame
    column: string column name to use as weights

    returns: DataFrame
    """
    weights = df[column]
    sample = df.sample(n=len(df), replace=True, weights=weights)
    return sample


def resample_by_cycle(unweighted):
    """Resample a DataFrame, grouped by cycle.

    unweighted: DataFrame

    returns: DataFrame
    """
    dfs = []

    for name, group in unweighted.groupby("cycle"):
        df = resample_rows_weighted(group, "finalwgt")
        dfs.append(df)

    return pd.concat(dfs).reset_index(drop=True)