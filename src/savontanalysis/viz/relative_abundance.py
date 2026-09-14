from typing import Any

import plotly.express as px
import pandas as pd
from pandas import DataFrame


def create_abundance_plot(data, col_name, top):
    col_names = list(data.columns)
    final_col = col_names.index("superkingdom")
    sample_list = col_names[final_col+1::]
    melted = melt_data(col_name, data, sample_list)
    if top > 0:
        melted = filter_top(melted, col_name, top)
    melted = melted.sort_values(["variable", "value"], ascending=False, kind = "stable")
    ax = plot_data(melted, col_name)
    return ax

def filter_top(data, colname, top):
    totals = data.groupby(colname)["value"].sum().sort_values(ascending=False)
    topx = totals.head(top).index.tolist()
    data = data.copy()
    data[colname] = data[colname].where(data[colname].isin(topx), "Other")

    data = (
        data.groupby(["variable", colname], as_index=False, sort=False)["value"].sum()

    )
    order = topx + ["Other"]
    data[colname] = pd.Categorical(data[colname], categories=order, ordered=True)

    return data

def melt_data(col_name, data, sample_list: list[Any]) -> DataFrame:
    data = data.reset_index()
    melted = pd.melt(data, id_vars=col_name, value_vars=sample_list)
    melted = melted.groupby(["variable", col_name], as_index = False, sort=False)["value"].sum()
    return melted


def plot_data(data, colname):
    print(data)
    fig = px.bar(data, x = "variable", color = colname, y = "value",
                 barmode="stack",
                 color_discrete_sequence=px.colors.qualitative.Dark24)
    fig.update_layout(
        xaxis_title = "Replicate / Sample",
        yaxis_title = "Relative abundance",
        yaxis_tickformat=".0%",
    )
    return fig
    # ax = sns.histplot(data, x = "variable", hue = colname, weights="value",
    #                   multiple="stack", palette="tab20c", shrink=0.8)
    # ax.set_ylabel("Percentage")
    # ax.set_xlabel("Samples / replicates")
    # legend = ax.get_legend()
    # legend.set_bbox_to_anchor((1,1))
    # ax.set_title(f"Relative abundance of {colname}")
    return ax


