import plotly.graph_objects as go # or plotly.express as px
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import main
from statsmodels.tsa.stattools import adfuller

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


sidebar_style = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "22rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

content_style = {
    "margin-left": "24rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

#SIDEBAR COMPONENTS
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

                        dbc.DropdownMenuItem("Exploratoy Data Analysis", header=True),
                        dbc.DropdownMenuItem("Stores"),
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
        html.H4("Title Here", className="display-4"),

        #sidebar paragraph
        html.P("Lorem ipsum dolor sit amet, consectetur rus semper eget. Amet dictum sit amet justo donec enim diam.", className="lead"),
        
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
    style=sidebar_style,
)




content = html.Div(id="page-content", style=content_style)
app.layout = html.Div([dcc.Location(id="url"),sidebar, content])
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])




def render_page_content(pathname):
#HOME PAGE
    if pathname == "/":
        narrative = ""
        sidebar_header = "Walmart Sales Analysis"
        store1 = main.store_plots()[0]
        store2 = main.store_plots()[1]
        store3 = main.store_plots()[2]
        store4 = main.store_plots()[3]
        dept1 = main.dept_plots()
        #dept2 = main.dept_plots()[1]
        model1 = main.model_plots()[0]
        model2 = main.model_plots()[1]
        sales = main.sales_plots()
        #overview content
        overview = html.Div(
            [
                dbc.Row(dbc.Col(html.P("hhh"))),

                dbc.Row(
                    [
                        dbc.Col(html.Div(dcc.Graph(figure=model1))),
                        dbc.Col(html.Div(dcc.Graph(figure=model2))),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(html.Div(dcc.Graph(figure=sales))),
                    
                    ]
                ),
            ]
        )
        
        return overview

#EDA OVERVIEW ROUTE
    elif pathname == "/exp_analysis":
        narrative = ""
        sidebar_header = "Exploratory Data Analysis"


        
        return narrative

#STORE PAGE ROUTE
    elif pathname == "/stores":
        narrative = ""
        sidebar_header = "Stores"

        #overview content
        bar = main.store_plots()
        overview = html.Div([
            dcc.Graph(figure=bar)
        ])

              
        return 

#DEPT PAGE ROUTE
    elif pathname == "/depts":
        narrative = ""
        sidebar_header = "Departments"

        #overview content
        bar = main.store_plots()
        overview = html.Div([
            dcc.Graph(figure=bar)
        ])

              
        return narrative, sidebar_header, depts

#PRED. MODELING ROUTE
    elif pathname == "/pred_models":
        narrative = ""
        sidebar_header = "Predictive Modeling"

        #overview content
        bar = main.store_plots()
        overview = html.Div([
            dcc.Graph(figure=bar)
        ])

               
        return narrative, sidebar_header, pred_models

#CONCLUSION ROUTE
    elif pathname == "/conclusion":
        narrative = ""
        sidebar_header = "Conclusion"

        #overview content
        bar = main.store_plots()
        overview = html.Div([
            dcc.Graph(figure=bar)
        ])

               
        return narrative, sidebar_header, conclusion

#404 ROUTE      
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognized."),
        ]
    )


if __name__ == "__main__":
    app.run_server()