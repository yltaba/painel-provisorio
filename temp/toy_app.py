import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Sample data
df = pd.DataFrame({
    "Category": ["A", "B", "C", "D"],
    "Values": [4, 1, 2, 3]
})

# Create a simple bar plot
fig = px.bar(df, x="Category", y="Values", title="Sample Bar Plot")

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'}, children=[
    html.H1("Dashboard Title", style={'textAlign': 'center', 'color': '#333'}),
    
    # Cards
    html.Div(style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': '20px'}, children=[
        html.Div(style={'border': '1px solid #ccc', 'borderRadius': '5px', 'padding': '10px', 'width': '30%'}, children=[
            html.H3("Card 1", style={'textAlign': 'center'}),
            html.P("Some information about Card 1.", style={'textAlign': 'center'})
        ]),
        html.Div(style={'border': '1px solid #ccc', 'borderRadius': '5px', 'padding': '10px', 'width': '30%'}, children=[
            html.H3("Card 2", style={'textAlign': 'center'}),
            html.P("Some information about Card 2.", style={'textAlign': 'center'})
        ]),
        html.Div(style={'border': '1px solid #ccc', 'borderRadius': '5px', 'padding': '10px', 'width': '30%'}, children=[
            html.H3("Card 3", style={'textAlign': 'center'}),
            html.P("Some information about Card 3.", style={'textAlign': 'center'})
        ])
    ]),
    
    # Plot
    html.Div(style={'border': '1px solid #ccc', 'borderRadius': '5px', 'padding': '10px'}, children=[
        dcc.Graph(
            id='example-graph',
            figure=fig
        )
    ])
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)