from __future__ import division

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from subplots import PdfSubplots
from matplotlib.backends.backend_pdf import PdfPages

from helpers import NUMERIC_TYPES

import itertools


# TODO: Implement this for floats
def _draw_stacked_plot(dfgb, **kwargs):
    """
    Draw a vertical bar plot of multiple series
    stacked on top of each other

    Deals with some annoying pandas issues when
    drawing a DataFrame
    """

    #color_cycle = ax._get_lines.color_cycle

    if 'ax' in kwargs:
        ax = kwargs.pop('ax')
    else:
        ax = plt.gca()

    series_dict = {}

    for (key, srs) in dfgb:
        series_dict[key] = srs

    df_for_plotting = pd.DataFrame(series_dict)
    df_for_plotting.plot(kind="bar", stacked=True, ax=ax, **kwargs)


def _save_plots(dfgb, plot_func, output_file, *args, **kwargs):
    """
    Take a grouped dataframe and save a pdf of
    the histogrammed variables in that dataframe.
    TODO: Can we abstract this behavior...?
    """

    pdf = PdfPages(output_file)

    subplots = PdfSubplots(pdf, 3, 3)

    for (var, series) in dfgb._iterate_column_groupbys():

        subplots.next_subplot()
        try:
            plot_func(series, *args, **kwargs)
            plt.xlabel(var)
            subplots.end_iteration()
        except:
            subplots.skip_subplot()

    subplots.finalize()

    pdf.close()


def _series_hist(sgb, ax=None, normed=False, normalize=False, autobin=False,
                 addons=None, addon_args=None, *args, **kwargs):
    """
    Takes a pandas.SeriesGroupBy
    and plots histograms of the variable 'var'
    for each of the groups.
    May take a list of 'addons', which are functions
    that take additional action on the plotted data
    (for example, they may add specific decoration to
    the plot based on the data, such as a table or
    a custom legend)
    """

    if ax is None:
        ax = plt.gca()

    normed_or_normalize = normed or normalize

    if sgb.obj.dtype in NUMERIC_TYPES:
        plot_result = _series_hist_float(sgb, ax, normed=normed_or_normalize, autobin=autobin, *args, **kwargs)
    else:
        plot_result = _series_hist_nominal(sgb, ax, normalize=normed_or_normalize, *args, **kwargs)

    if sgb.obj.name:
        plt.xlabel(sgb.obj.name)

    if addons:
        for add_on_func in addons:
            if addon_args is None:
                addon_args = {}
            addon_args.update(plot_result)
            add_on_func(**addon_args)

    plt.legend(loc='best', fancybox=True)


def _series_hist_float(sgb, ax=None, autobin=False, normed=False, normalize=False,
                       stacked=False, *args, **kwargs):
    """
    Takes a pandas.SeriesGroupBy
    and plots histograms of the variable 'var'
    for each of the groups.
    """

    if ax is None:
        ax = plt.gca()

    if 'bins' in kwargs:
        bins = kwargs.pop('bins')
    else:
        bins = _get_variable_binning(sgb.obj)

    color_cycle = itertools.cycle(ax._get_lines.color_cycle)

    series_map = {}

    for (color, (key, srs)) in zip(color_cycle, sgb):

        if 'label' in kwargs.keys():
            label = kwargs['label']
        else:
            label = key

        if 'color' in kwargs.keys():
            color = kwargs['color']

        # if len(srs.values)==1 and 'bins' not in kwargs:
        #    kwargs['bins'] = [srs.values[0] - 0.05, srs.values[0] + 0.05]

        srs.hist(ax=ax, color=color, label=str(label), normed=normed, bins=bins, **kwargs)
        series_map[label] = srs

    return {'type': 'FLOAT', 'grouped': sgb, 'series_map': series_map, 'bins': bins}


def _series_hist_nominal(sgb, ax=None, normalize=False, dropna=False, *args, **kwargs):
    """
    Takes a pandas.SeriesGroupBy
    and plots histograms of the variable 'var'
    for each of the groups.
    """

    if ax is None:
        ax = plt.gca()

    color_cycle = ax._get_lines.color_cycle

    if dropna:
        vals = [val for val in set(sgb.obj.values) if val is not None]
    else:
        vals = [val for val in set(sgb.obj.values)]

    series_map = {}

    for (color, (key, srs)) in zip(color_cycle, sgb):

        if 'label' in kwargs.keys():
            label = kwargs['label']
        else:
            label = key

        if 'color' in kwargs.keys():
            color = kwargs['color']

        value_counts = srs.value_counts(normalize=normalize, dropna=dropna)[vals]
        value_counts.plot(kind='bar', ax=ax, color=color, label=label, **kwargs)
        series_map[label] = srs

    return {'type': 'NOMINAL', 'grouped': sgb, 'series_map': series_map}


def _grouped_hist(dfgb, var=None, *args, **kwargs):

    if var is not None:
        _series_hist(dfgb[var], *args, **kwargs)
    else:
        for (var, series) in dfgb._iterate_column_groupbys():
            plt.figure()
            try:
                _series_hist(series, *args, **kwargs)
                plt.xlabel(var)
            except TypeError as e:
                print "Failed to plot %s" % var
                print e


def _frame_scatter(df, x, y, **kwargs):
    """
    Takes a grouped data frame and draws a scatter
    plot of the suppied variables wtih a different
    color for each group
    """
    ax = plt.gca()
    plt.scatter(df[x], df[y], **kwargs)
    plt.xlabel(x)
    plt.ylabel(y)


def _grouped_scatter(dfgb, x, y, **kwargs):
    """
    Takes a grouped data frame and draws a scatter
    plot of the suppied variables wtih a different
    color for each group
    """
    ax = plt.gca()
    color_cycle = ax._get_lines.color_cycle
    for (color, (key, grp)) in zip(color_cycle, dfgb):
        plt.scatter(grp[x], grp[y], color=color, label=key, **kwargs)
    plt.legend(loc='best')
    plt.xlabel(x)
    plt.ylabel(y)


def _get_variable_binning(var, nbins=10, int_bound=40):
    """
    Get the binning of a variable.
    Deals with a number of special cases.
    For smooth distributions most of the time the maximum (minimum)
    occurs within 15% of the 98th (2nd) percentile, so we define
    extreme outliers as:

    if ( (var_max > p_50 + (p_98 - p_50) * 1.15) or
         (var_min < p_50 - (p_50 - p_02) * 1.15) )

    If an outlier is present, then use the expanded (by 15%) 98th
    (or 2nd) percentile as the bin edge. Otherwise we use the actual extremum.
    """

    var = var[np.isfinite(var)]

    var_min = min(var)
    var_max = max(var)

    if var_min == var_max:
        return np.array([var_min - 0.5, var_max + 0.5])

    # If all values are integers (not necessarily by type) between
    # -int_bound and +int_bound, then use unit spacing centered on
    # integers.
    if var_min > -int_bound and var_max < int_bound:

        if all(np.equal(np.mod(var, 1), 0)):
            return np.arange(var_min - 0.5, var_max + 1.5, 1)

    # Detect extreme outliers by the following heuristic.
    p_02, p_50, p_98 = np.percentile(var, (2, 50, 98))

    p_02_exp = p_50 - (p_50 - p_02) * 1.15
    p_98_exp = p_50 + (p_98 - p_50) * 1.15

    if (var_max > p_98_exp):
        var_max = p_98_exp

    if (var_min < p_02_exp):
        var_min = p_02_exp

    bins = np.arange(nbins + 1) / nbins * (var_max - var_min) + var_min

    return bins
