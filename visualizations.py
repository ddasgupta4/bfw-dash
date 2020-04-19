import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


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
        # title="Violin Plot Per Subgroup",
        violinmode='group',  # 'overlay', 'group'
        # log_y=True,  # y-axis is log-scaled in cartesian coordinates
        category_orders={"Tag": ["Imposter", "Genuine"]}
        # keys need to correspond to column names, values are lists of strings in order
    ).update_xaxes(categoryorder="category ascending")

    return fig


def box_plot(BFWdf):
    fig = px.box(
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
    ).update_xaxes(categoryorder="category ascending")

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


def sdm_curve(data):
    fig = go.Figure()

    fig.add_trace(go.Violin(x=data['subgroup'][data['Tag'] == 'Imposter'],
                            y=data['score'][data['Tag'] == 'Imposter'],
                            legendgroup='Imposter', scalegroup='Imposter', name='Imposter',
                            side='negative',
                            line_color='blue')
                  )
    fig.add_trace(go.Violin(x=data['subgroup'][data['Tag'] == 'Genuine'],
                            y=data['score'][data['Tag'] == 'Genuine'],
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
