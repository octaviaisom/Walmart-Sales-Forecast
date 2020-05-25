import plotly.graph_objects as go # or plotly.express as px
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
#import main

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])



# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "25rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "27rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

#will be retured by each app
narrative = "A simple sidebar layout with navigation linksA simple sidebar layout with navigation links A simple sidebar layout with navigation linksA simple sidebar layout with navigation links"
sidebar_header = "Unique Header"


sidebar = html.Div(
    [
        #dropdown menu
        html.Div(
            [
                dbc.DropdownMenu(
                    label="Menu",
                    color='link',
                    children=[
                        dbc.DropdownMenuItem("Overview"),
                        dbc.DropdownMenuItem(divider=True),

                        dbc.DropdownMenuItem("Exploratoy Analysis", header=True),
                        dbc.DropdownMenuItem("Stores", active=True),
                        dbc.DropdownMenuItem("Departments"),
                        dbc.DropdownMenuItem(divider=True),

                        dbc.DropdownMenuItem("Predictive Modeling", header=True),
                        dbc.DropdownMenuItem("Modeling"),
                        dbc.DropdownMenuItem("Forecasting"),
                        dbc.DropdownMenuItem(divider=True),

                        dbc.DropdownMenuItem("Conclusion"),
                    ],
                ),

            ]
        ),
        
        #sidebar header
        html.H4(sidebar_header, className="display-4"),

        #sidebar paragraph
        html.P(narrative, className="lead"),
        
        #progress bar
        html.Div(dbc.Progress(value=50, style={"height": "3px"}, className="mb-3")),

        #navi buttons
        html.Div(
            [

                dbc.Button("Back", outline=True,color="info", className="mr-1"),
                dbc.Button("Next", outline=True,color="info", className="mr-1"),

            ]
        )
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"),sidebar, content])


# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 4)],
    [Input("url", "pathname")],
)

def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 4)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])


def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:

        bar = main.store_plots()

        page1 = html.Div([
            dcc.Graph(figure=bar)
        ])
        
        return page1
    elif pathname == "/page-2":
        return html.P("This is the content of page 2. Yay!")
    elif pathname == "/page-3":
        return html.P("Oh cool, this is page 3!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognized..."),
        ]
    )


if __name__ == "__main__":
    app.run_server()