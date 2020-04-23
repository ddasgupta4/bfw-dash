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
        # title="Violin Plot Per Subgroup",
        violinmode='group',  # 'overlay', 'group'
        # log_y=True,  # y-axis is log-scaled in cartesian coordinates
        category_orders={"Tag": ["Imposter", "Genuine"]}
        # keys need to correspond to column names, values are lists of strings in order
    ).update_xaxes(categoryorder="category ascending"))

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
        # title="Box Plot Per Subgroup",
        points="outliers",
        # log_y=True,  # y-axis is log-scaled in cartesian coordinates
        category_orders={"Tag": ["Imposter", "Genuine"]}
        # keys need to correspond to column names, values are lists of strings in order
    ).update_xaxes(categoryorder="category ascending"))

    return fig


def mock_det():
    test_det_df = pd.DataFrame()
    subgroups = ['AF', 'AM', 'BF', 'BM', 'IF', 'IM', 'WF', 'WM']

    count = 1
    for sub in subgroups:
        temp_df = pd.DataFrame()
        # The domain of the fabricated fnr-fpr function is from 0-10
        temp_df['FPR'] = [(i / 10000) for i in range(100)]
        # Parent function is 1/x, multiplied by counts to produce distinct curves
        temp_df['FNR'] = count / temp_df['FPR']
        temp_df['FNR'] = temp_df['FNR'] / 80000
        # Add subgroup
        temp_df['subgroup'] = sub
        # Add to total data frame
        test_det_df = pd.concat([test_det_df, temp_df])
        count += 1

    det = px.line(test_det_df,
                  labels=dict(x="FPR", y="FPR", color="Subgroup"),
                  x=test_det_df['FPR'],
                  y=test_det_df['FNR'],
                  color=test_det_df['subgroup'],
                  log_x=True,
                  log_y=False,
                  line_shape="spline",
                  title="Detection Error Tradeoff (DET) Curve"
                  )
    return det


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
                      # title="SDM Curve Per Subgroup",
                      xaxis_title="subgroup",
                      yaxis_title="score")
    fig.update_xaxes(categoryorder="category ascending")

    return fig


import pandas as pd
import plotly.express as px
from sklearn.metrics import roc_curve


def plot_det_from_grouped_df(grouped_bfw_df, group):
    """
    Plots the DET curve for given data frame corresponding to the groups by which the data frame is grouped by.
    """
    # Calculate the data frame
    det_df = calculate_det_from_grouped_df(grouped_bfw_df)
    # Plot from data frame
    det_curve = plot_det_from_df(det_df)
    # Format and show
    format_det_curve(det_curve, group)
    return det_curve


def calculate_det_from_grouped_df(grouped_bfw_df):
    """
    Calculates a DET data frame containing fpr and fnr as a function of threshold with an additional label for subgroup
    for the given data frame corresponding to the groups by which the data frame is grouped by.
    """
    return combined_det_from_subgroups(grouped_bfw_df, grouped_bfw_df.groups.keys())


def combined_det_from_subgroups(grouped_bfw_df, groups):
    """
    Calculates a DET data frame for the given groups that the given data frame is grouped by.
    groups - List of groups that appear in grouped_bfw_df.groups.keys()
    """
    group_df = pd.DataFrame()
    # For every group given, calculate the data frame for that group, append the group label in 'subgroup' column
    # and add to end of data frame to be returned (group_df)
    for group in groups:
        temp_df = det_df_from_subgroup(grouped_bfw_df, group)
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


def format_det_curve(det_curve, group):
    """Formats the given DET curve plot to be square 500 x 500 and a y-axis range from [0, .6]"""
    det_curve['layout'].update(autosize=True)
    # det_curve['layout'].update(width=500, height=500, autosize=False)
    det_curve['layout']['yaxis'].update(range=[0, 1])

    title = "DET Curve by " + group

    det_curve['layout']['title'].update(text=title)


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
    ethnicities = BFWDF.groupby(by="e1")

    fig = plot_det_from_grouped_df(ethnicities, "Ethnicity")

    return fig
