import plotly.express as px

def create_sunburst_plot(data):
    col_names = list(data.columns)

    path_cols = ["superkingdom", "phylum", "class", "order", "family", "genus", "species"]
    print(path_cols)
    fig = px.sunburst(
        data,
        path = path_cols,
        values = "rep1",
        color = "phylum",
        color_discrete_sequence=px.colors.qualitative.Dark24,
        branchvalues="total",
    )

    return fig
