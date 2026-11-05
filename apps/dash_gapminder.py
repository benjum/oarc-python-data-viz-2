"""Gapminder in Dash: explicit callbacks.  Run with:  python dash_gapminder.py"""
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

# particular to JupyterHub use:
import os
prefix = os.environ.get("JUPYTERHUB_SERVICE_PREFIX", "/")   # e.g. /user/<you>/

gap = px.data.gapminder()

# Local computer:
# app = Dash(__name__)
# In JupyterHub:
app = Dash(__name__,
           routes_pathname_prefix="/",
           requests_pathname_prefix=f"{prefix}proxy/8050/")

app.layout = html.Div([
    html.H3("Gapminder in Dash"),
    html.Div([
        dcc.Dropdown(sorted(gap.continent.unique()), "Asia", id="continent",
                     clearable=False, style={"width": "200px"}),
        dcc.Slider(1952, 2007, step=5, value=2007, id="year",
                   marks={y: str(y) for y in range(1952, 2008, 10)}),
    ], style={"display": "grid", "gridTemplateColumns": "220px 1fr", "gap": "16px"}),
    html.Div([
        dcc.Graph(id="scatter", style={"flex": "3"}),
        dcc.Graph(id="history", style={"flex": "2"}),
    ], style={"display": "flex"}),
], style={"fontFamily": "sans-serif", "padding": "8px"})


# Callback 1: two widgets -> scatter figure
@app.callback(Output("scatter", "figure"),
              Input("continent", "value"), Input("year", "value"))
def update_scatter(continent, year):
    d = gap[(gap.continent == continent) & (gap.year == year)]
    fig = px.scatter(d, x="gdpPercap", y="lifeExp", size="pop", hover_name="country",
                     custom_data=["country"], log_x=True, size_max=45,
                     range_y=[25, 90], title=f"{continent}, {year} (hover a country)")
    return fig


# Callback 2: hovering on the scatter -> line chart of that country
@app.callback(Output("history", "figure"),
              Input("scatter", "hoverData"), Input("continent", "value"))
def update_history(hover, continent):
    if hover:
        country = hover["points"][0]["customdata"][0]
    else:
        country = gap[gap.continent == continent].country.iloc[0]
    d = gap[gap.country == country]
    return px.line(d, x="year", y="lifeExp", markers=True, range_y=[25, 90],
                   title=country)


if __name__ == "__main__":
    app.run(debug=True)
