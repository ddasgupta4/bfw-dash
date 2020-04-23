import plotly.graph_objects as go


def relabel(BFWdf):
    BFWdf.label = BFWdf.label.astype(int)
    BFWdf['subgroup'] = BFWdf['a1']

    new_labels = ["Imposter", "Genuine"]

    BFWdf["Tag"] = BFWdf["label"]
    BFWdf.loc[BFWdf["label"] == 0, "Tag"] = new_labels[0]
    BFWdf.loc[BFWdf["label"] == 1, "Tag"] = new_labels[1]

    return BFWdf


def violin_plot(BFWdf, score):
    BFWdf['score'] = BFWdf[score]

    fig = go.Figure(px.violin(
        BFWdf,
        y="score",  # score
        x='subgroup',  # subgroup
        color="Tag",
        box=True,  # shows boxplot inside violin
        title="Violin Plot by Subgroup",
        violinmode='group',  # 'overlay', 'group'
        # log_y=True,  # y-axis is log-scaled in cartesian coordinates
        category_orders={"Tag": ["Imposter", "Genuine"]}
        # keys need to correspond to column names, values are lists of strings in order
    ).update_xaxes(categoryorder="category ascending"))

    fig.update_layout(legend_title='')

    return fig


def box_plot(BFWdf, score):
    BFWdf['score'] = BFWdf[score]

    fig = go.Figure(px.box(
        BFWdf,
        y="score",  # score
        x='subgroup',  # subgroup
        color="Tag",
        boxmode="group",  # 'overlay' 'group'
        notched=True,  # used notched shape so it narrows around the median
        title="Box Plot by Subgroup",
        points="outliers",
        # log_y=True,  # y-axis is log-scaled in cartesian coordinates
        category_orders={"Tag": ["Imposter", "Genuine"]}
        # keys need to correspond to column names, values are lists of strings in order
    ).update_xaxes(categoryorder="category ascending"))

    fig.update_layout(legend_title='')

    return fig


def sdm_curve(BFWDF, score):
    BFWDF['score'] = BFWDF[score]

    fig = go.Figure()

    fig.add_trace(go.Violin(x=BFWDF['subgroup'][BFWDF['Tag'] == 'Imposter'],
                            y=BFWDF['score'][BFWDF['Tag'] == 'Imposter'],
                            legendgroup='Imposter', scalegroup='Imposter', name='Imposter',
                            side='negative',
                            line_color='blue')
                  )
    fig.add_trace(go.Violin(x=BFWDF['subgroup'][BFWDF['Tag'] == 'Genuine'],
                            y=BFWDF['score'][BFWDF['Tag'] == 'Genuine'],
                            legendgroup='Genuine', scalegroup='Genuine', name='Genuine',
                            side='positive',
                            line_color='red')
                  )

    fig.update_traces(meanline_visible=True)
    fig.update_layout(violinmode='overlay',
                      title="SDM Curve by Subgroup",
                      xaxis_title="subgroup",
                      yaxis_title="score")
    fig.update_xaxes(categoryorder="category ascending")

    fig.update_layout(legend_title='')

    return fig


# DET and ROC curves

import pandas as pd
import plotly.express as px
from sklearn.metrics import roc_curve


def plot_det_from_grouped_df(grouped_bfw_df, group):
    """
        Plots the DET curve for all groups by which the given data frame is grouped
        :param grouped_bfw_df: Data frame groups generally either by Gender, Ethnicity, or Subgroup (combined G&E)
    """
    title = "DET Curve by " + group
    curve = plot_from_grouped_df(grouped_bfw_df, det_df_from_subgroup, plot_det_from_df)
    curve['layout']['title'].update(text=title)
    return curve


def plot_roc_from_grouped_df(grouped_bfw_df, group):
    """
    Plots the ROC curve for all groups by which the given data frame is grouped
    :param grouped_bfw_df: Data frame groups generally either by Gender, Ethnicity, or Subgroup (combined G&E)
    """
    title = "ROC Curve by " + group
    curve = plot_from_grouped_df(grouped_bfw_df, roc_df_from_subgroup, plot_roc_from_df)
    curve['layout']['title'].update(text=title)
    return curve


def plot_from_grouped_df(grouped_bfw_df, calc_func, plot_func):
    """
    Plots the curve for given data frame corresponding to the groups by which the data frame is grouped by
    where the curve type depends on the calc_func and plot_func (which should correspond)
    calc_func - A function that takes a grouped data frame and one group from that grouping and returns a data frame
    compatible with the given plot_func
    plot_func - A function that takes a calculated data frame from calc_func and plots the corresponding curve separated
    by subgroup
    """
    # Calculate the data frame
    df = calculate_from_grouped_df(grouped_bfw_df, calc_func)
    # Plot from data frame
    curve = plot_func(df)
    # Format and show
    format_curve(curve)
    return curve


def calculate_from_grouped_df(grouped_bfw_df, calc_func):
    """
    Calculates a data frame containing according to the given calc_func for all groups by which the given data frame
    is grouped.
    """
    return combined_from_subgroups(grouped_bfw_df, calc_func, grouped_bfw_df.groups.keys())


def combined_from_subgroups(grouped_bfw_df, calc_func, groups):
    """
    Calculates a data frame for the given groups that the given data frame is grouped by,
    according to the given calc func, concatenating the resulting data frames that calc_fun returns for each group.
    Also appends a 'subgroup' column corresponding to the group for coloration purposes.
    groups - List of groups that appear in grouped_bfw_df.groups.keys()
    """
    group_df = pd.DataFrame()
    for group in groups:
        temp_df = calc_func(grouped_bfw_df, group)
        temp_df['subgroup'] = group
        group_df = pd.concat([group_df, temp_df])
    return group_df


def det_df_from_subgroup(grouped_bfw_df, group):
    """
    Calculates a DET data frame for the given group (does not append a subgroup column)
    group - A String that is a member of grouped_bfw_df.groups.keys()
    """
    # Get the data frame for just the given group
    group_df = grouped_bfw_df.get_group(group)
    # Calculate det data frame using the labels (0 or 1) and the score [0, 1]
    det_df = pd.DataFrame(calculate_det_curves(group_df['label'].values.astype(int), group_df['score'].values))
    # Transpose since it is given horizontally
    det_df = det_df.T
    # Drop the top row since that row is just the indexing before transposing
    det_df = det_df.drop(0)
    det_df.columns = ['fpr', 'fnr', 'threshold']
    return det_df


def calculate_det_curves(y_true, scores):
    """
    Calculate false match rates, both for non-matches and matches
    :param y_true:   ground truth label, boolean (1 if match; else, 0)
    :param scores:   scores for each pair.
    :return:    list of tuples (false-match and false-non-match rates.
    """

    # y_pred = threshold_scores(scores, threshold)
    fpr, tpr, thresholds = roc_curve(y_true, scores, pos_label=1)
    fnr = 1 - tpr
    return fpr, fnr, thresholds


def roc_df_from_subgroup(grouped_bfw_df, group):
    """
    Calculates a ROC data frame for the given group (does not append a subgroup column)
    group - A String that is a member of grouped_bfw_df.groups.keys()
    """
    group_df = grouped_bfw_df.get_group(group)
    det_df = pd.DataFrame(calculate_roc_curves(group_df['label'].values.astype(int), group_df['score'].values))
    det_df = det_df.T
    det_df = det_df.drop(0)
    det_df.columns = ['fpr', 'tpr', 'threshold']
    return det_df


def calculate_roc_curves(y_true, scores):
    """
    Calculate false match rates and true match rates
    :param y_true:   ground truth label, boolean (1 if match; else, 0)
    :param scores:   scores for each pair.
    :return:    list of tuples (false-match and true-match rates.
    """
    return roc_curve(y_true, scores, pos_label=1)


def plot_det_from_df(det_df):
    """
    Plots the det curve colored by subgroup from the given dataframe, which must contain fpr, fnr, and subgroup columns
    """
    det_plot = px.line(det_df,
                       labels=dict(x="fpr", y="fnr", color="Subgroup"),
                       x=det_df['fpr'],
                       y=det_df['fnr'],
                       color=det_df['subgroup'],
                       log_x=True)
    # Set x-axis to have scientific notation
    det_plot.update_layout(
        xaxis=dict(
            showexponent='all',
            exponentformat='e'
        ))
    return det_plot


def plot_roc_from_df(roc_df):
    """
    Plots the roc curve colored by subgroup from the given data frame, which must contain fpr, tpr, and subgroup columns
    """
    roc_plot = px.line(roc_df,
                       labels=dict(x="fpr", y="tpr", color="Subgroup"),
                       x=roc_df['fpr'],
                       y=roc_df['tpr'],
                       color=roc_df['subgroup'])
    return roc_plot


def format_curve(curve):
    """Formats the given curve plot to be square 500 x 500 and a y-axis range from [0, 1]"""
    curve['layout'].update(autosize=True)
    curve['layout']['yaxis'].update(range=[0, 1])


def det_subgroup(BFWDF, score):
    BFWDF['score'] = BFWDF[score]
    subgroups = BFWDF.groupby(by="a1")

    fig = plot_det_from_grouped_df(subgroups, "Subgroup")

    return fig


def det_gender(BFWDF, score):
    BFWDF['score'] = BFWDF[score]
    sexes = BFWDF.groupby(by="g1")

    fig = plot_det_from_grouped_df(sexes, "Gender")

    return fig


def det_ethnicity(BFWDF, score):
    BFWDF['score'] = BFWDF[score]
    ethnicity = BFWDF.groupby(by="e1")

    fig = plot_det_from_grouped_df(ethnicity, "Ethnicity")

    return fig


def roc_subgroup(BFWDF, score):
    BFWDF['score'] = BFWDF[score]
    subgroups = BFWDF.groupby(by="a1")

    fig = plot_roc_from_grouped_df(subgroups, "Subgroup")

    return fig


def roc_gender(BFWDF, score):
    BFWDF['score'] = BFWDF[score]
    sexes = BFWDF.groupby(by="g1")

    fig = plot_roc_from_grouped_df(sexes, "Gender")

    return fig


def roc_ethnicity(BFWDF, score):
    BFWDF['score'] = BFWDF[score]
    ethnicity = BFWDF.groupby(by="e1")

    fig = plot_roc_from_grouped_df(ethnicity, "Ethnicity")

    return fig
