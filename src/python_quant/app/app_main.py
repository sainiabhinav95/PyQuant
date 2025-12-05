#!/usr/bin/env -S uv run --active
import polars as pl
from dash import Dash, html, dcc, Output, Input
import plotly.express as px


class WebApp:
    def __init__(self):
        self.app = Dash()
        self.app_setup()
        self.app_callbacks()
        self.app_layout()

    def app_setup(self):
        self.df = pl.read_csv(
            "https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv"
        )

    def app_callbacks(self):
        @self.app.callback(
            Output("graph-content", "figure"),
            Input("dropdown-selection", "value"),
        )
        def update_graph(selected_country):
            filtered_df = self.df.filter(pl.col("country") == selected_country)
            fig = px.line(
                filtered_df,
                x="year",
                y="lifeExp",
                title=f"Life Expectancy in {selected_country} Over the Years",
            )
            return fig

    def app_layout(self):
        # Polars: get unique countries as a Python list
        countries = self.df["country"].unique().to_list()
        default_country = (
            "Canada" if "Canada" in countries else (countries[0] if countries else None)
        )
        self.app.layout = [
            html.H1(children="PyQuant Dash App", style={"textAlign": "center"}),
            dcc.Dropdown(
                id="dropdown-selection",
                options=[{"label": c, "value": c} for c in countries],
                value=default_country,
                clearable=False,
            ),
            dcc.Graph(id="graph-content"),
        ]

    def run(self):
        self.app.run(debug=True, use_reloader=False)
