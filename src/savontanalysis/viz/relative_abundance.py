from typing import Any

import seaborn as sns
import pandas as pd
from pandas import DataFrame


def create_abundance_plot(data, col_name):
    col_names = list(data.columns)
    final_col = col_names.index("superkingdom")
    sample_list = col_names[final_col+1::]
    melted = melt_data(col_name, data, sample_list)
    ax = plot_data(melted, col_name)
    return ax


def melt_data(col_name, data, sample_list: list[Any]) -> DataFrame:
    data = data.reset_index()
    melted = pd.melt(data, id_vars=col_name, value_vars=sample_list)
    return melted

def plot_data(data, colname):

    ax = sns.histplot(data, x = "variable", hue = colname, weights="value",
                      multiple="stack", palette="tab20c", shrink=0.8)
    ax.set_ylabel("Percentage")
    ax.set_xlabel("Samples / replicates")
    legend = ax.get_legend()
    legend.set_bbox_to_anchor((1,1))
    ax.set_title(f"Relative abundance of {colname}")
    return ax


