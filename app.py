import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import main

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

#RETRIEVE PLOTS FROM MAIN.PY
store1 = main.store_plots()[0]
store2 = main.store_plots()[1]
store3 = main.store_plots()[2]
store4 = main.store_plots()[3]
#dept1 = main.dept_plots()
#dept2 = main.dept_plots()[1]
#model1 = main.model_plots()[0]
#model2 = main.model_plots()[1]
sales = main.sales_plots()

#-----------------------------------------------------------------------

#STYLING DICST
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

#-----------------------------------------------------------------------

#SIDEBAR COMPONENTS
sidebar = html.Div(
    [
        #dropdown menu
        html.Div(
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
        ),
        
        #sidebar header
        html.Div(id="sb_header"),

        #sidebar paragraph
        html.Div(id="sb_paragraph"),
        
        #progress bar
        html.Div(id="sb_progress"),

        #navi buttons
        html.Div(id="nav_buttons")
    ],
    
    style=sidebar_style,
)

#CONTENT (RIGHT PANE) COMPONENTS
content = html.Div(id="page-content", style=content_style)

#PAGE LAYOUT
app.layout = html.Div([dcc.Location(id="url"),sidebar, content])

#-----------------------------------------------------------------------

#RETRIEVE INPUTS FROM ROUTES, PASS COMPONENTS TO SIDEBAR AND CONTENT SECTIONS
@app.callback([Output("page-content", "children"),
                Output("sb_header", "children"),
                Output("sb_paragraph", "children"),
                Output("sb_progress", "children"),
                Output("nav_buttons", "children")], 
                [Input("url", "pathname")])

#-----------------------------------------------------------------------

#APP ROUTING
def render_page_content(pathname):
    #HOME PAGE
    if pathname == "/":
        #sidebar components
        header = html.H4("Exploratory Data Analysis", className="display-4")
        paragraph = html.P("ITS WORKING! consectetur rus semper eget. Amet dictum sit amet justo donec enim diam.", className="lead")
        progress_bar = dbc.Progress(value=0, style={"height": "3px"}, className="mb-3")
        buttons = [dbc.Button("BackX", outline=True,color="info", className="mr-1"),
                   dbc.Button("NextX", outline=True,color="info", className="mr-1")]
        
        #content components
        content = html.Div(
            [
                #content text
                dbc.Row(dbc.Col(html.P("hhh"))),

                #Charts
                dbc.Row(
                    [
                        dbc.Col(html.Div(dcc.Graph(figure=store1))),
                        dbc.Col(html.Div(dcc.Graph(figure=store2))),
                    ]
                ),
            ]
        )
        
        return content, header, paragraph, progress_bar, buttons

#EDA OVERVIEW ROUTE
    elif pathname == "/exp_analysis":
        narrative = ""
        


        
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