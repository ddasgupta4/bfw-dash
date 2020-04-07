import plotly.express as px

"""
This is just stuff I copied and pasted from Alice's Google Collab - it can all be scrapped

"""


def relabel(BFWdf):
    BFWdf.label = BFWdf.label.astype(int)
    BFWdf['score'] = BFWdf['senet50']
    BFWdf['subgroup'] = BFWdf['a1']

    new_labels = ["Imposter", "Genuine"]
    palette = {new_labels[0]: "orange", new_labels[1]: "lightblue"}

    BFWdf["Tag"] = BFWdf["label"]
    BFWdf.loc[BFWdf["label"] == 0, "Tag"] = new_labels[0]
    BFWdf.loc[BFWdf["label"] == 1, "Tag"] = new_labels[1]

    return BFWdf


def violin_plot(BFWdf):
    fig = px.violin(
        BFWdf,
        y="score",  # score
        x='subgroup',  # subgroup
        color="Tag",
        box=True,  # shows boxplot inside violin
        title="Violin Plot Per Subgroup",
        violinmode='group',  # 'overlay', 'group'
        log_y=True,  # y-axis is log-scaled in cartesian coordinates
        category_orders={"Tag": ["Imposter", "Genuine"]}
        # keys need to correspond to column names, values are lists of strings in order
    ).update_xaxes(categoryorder="total ascending")

    return fig


def box_plot(BFWdf):
    fig = px.box(
        BFWdf,
        y="score",  # score
        x='subgroup',  # subgroup
        color="Tag",
        boxmode="group",  # 'overlay' 'group'
        notched=True,  # used notched shape so it narrows around the median
        title="Box Plot Per Subgroup",
        # points = "outliers",
        log_y=True,  # y-axis is log-scaled in cartesian coordinates
        category_orders={"Tag": ["Imposter", "Genuine"]}
        # keys need to correspond to column names, values are lists of strings in order
    ).update_xaxes(categoryorder="total ascending")

    return fig
