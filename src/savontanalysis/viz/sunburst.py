import plotly.express as px

def create_sunburst_plot(data, sample, db):
    path_cols = ["superkingdom", "phylum", "class", "order", "family", "genus", "species"]
    fig = px.sunburst(
        data,
        path = path_cols,
        values = sample,
        color = "phylum",
        color_discrete_sequence=px.colors.qualitative.Dark24,
        branchvalues="total",
    )

    return fig
