import pandas as pd
import pickle
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

with open('combined_df.pkl', 'rb') as f:
    df = pickle.load(f)

graph_families = ['pa', 'sw', 'geo', 'geo_split', 'bn'] + [f'{k}_regular' for k in [3, 4, 6, 10]]
mu_values = sorted(df['mu'].unique())
s_values = sorted(df['s'].unique())
columns = [col for col in df.columns if col not in ['graph', 'index', 'mu', 's']]

color_map = {
    'pa': 'blue',
    'sw': 'red',
    'geo': 'green',
    'geo_split': 'teal',
    'bn': 'brown',
    '3_regular': 'purple',
    '4_regular': 'orange',
    '6_regular': 'cyan',
    '10_regular': 'pink',
    'regular': 'black'  # merged color when treating all regular graphs as one family
}

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Graph Data Visualizer'),

    html.Div([
        html.Label('Select X-axis:'),
        dcc.Dropdown(id='x-axis', options=[{'label': col, 'value': col} for col in columns], value=columns[0])
    ], style={'width': '45%', 'display': 'inline-block'}),

    html.Div([
        html.Label('Select Y-axis:'),
        dcc.Dropdown(id='y-axis', options=[{'label': col, 'value': col} for col in columns], value=columns[1])
    ], style={'width': '45%', 'display': 'inline-block', 'marginLeft': '5%'}),

    html.Div([
        html.Label('Graph Families:'),
        dcc.Checklist(
            id='graph-family',
            options=[{'label': fam, 'value': fam} for fam in graph_families],
            value=graph_families,
            inline=True
        )
    ], style={'marginTop': 20}),

    html.Div([
        dcc.Checklist(
            id='treat-regular-as-one',
            options=[{'label': 'Treat all regular graphs as one family', 'value': 'merge_regular'}],
            value=[],
            inline=True
        )
    ], style={'marginTop': 10}),

    html.Div([
        html.Label('Filter by mu:'),
        dcc.Checklist(
            id='mu-filter',
            options=[{'label': str(mu), 'value': mu} for mu in mu_values],
            value=mu_values,
            inline=True
        )
    ], style={'marginTop': 20}),

    html.Div([
        html.Label('Filter by s:'),
        dcc.Checklist(
            id='s-filter',
            options=[{'label': str(s), 'value': s} for s in s_values],
            value=s_values,
            inline=True
        )
    ], style={'marginTop': 20}),

    dcc.Graph(id='scatter-plot')
])

@app.callback(
    Output('scatter-plot', 'figure'),
    Input('x-axis', 'value'),
    Input('y-axis', 'value'),
    Input('graph-family', 'value'),
    Input('treat-regular-as-one', 'value'),
    Input('mu-filter', 'value'),
    Input('s-filter', 'value')
)
def update_plot(x_axis, y_axis, selected_families, merge_regular, selected_mu, selected_s):
    df['family'] = df['graph'].str.extract(r'(pa|sw|geo_split|geo|bn|\d+_regular)')

    filtered_df = df[
        df['family'].isin(selected_families) &
        df['mu'].isin(selected_mu) &
        df['s'].isin(selected_s)
    ].copy()

    if 'merge_regular' in merge_regular:
        filtered_df.loc[filtered_df['family'].str.contains('_regular'), 'family'] = 'regular'

    # Setup color map depending on merge
    used_color_map = {k: v for k, v in color_map.items() if k in filtered_df['family'].unique()}

    fig = px.scatter(
        filtered_df,
        x=x_axis,
        y=y_axis,
        color='family',
        color_discrete_map=used_color_map,
        hover_data=['graph', 'index', 'mu', 's']
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)
