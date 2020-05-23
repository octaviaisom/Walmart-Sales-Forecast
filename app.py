import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go # or plotly.express as px

bar = go.Figure(data=go.Bar(x=['a','b','c'],y=[2, 3, 1])) # or any Plotly Express function e.g. px.bar(...)
# fig.add_trace( ... )
# fig.update_layout( ... )

import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=bar)
])

app.run_server(debug=True, use_reloader=False) 