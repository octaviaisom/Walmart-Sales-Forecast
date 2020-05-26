import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import main

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

#-----------------------------------------------------------------------

#RETRIEVE PLOTS FROM MAIN.PY
store1 = main.store_plots()[0]
store2 = main.store_plots()[1]
store3 = main.store_plots()[2]
store4 = main.store_plots()[3]
dept1 = main.dept_plots()[0]
dept2 = main.dept_plots()[1]
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
    "margin-left": "23rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

tab_style = {
    "margin-left": "auto",
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
                    dbc.DropdownMenuItem("Overview", href="/"),
                    dbc.DropdownMenuItem(divider=True),

                    dbc.DropdownMenuItem("Exploratoy Data Analysis", header=True),
                    dbc.DropdownMenuItem("Stores", href="/stores"),
                    dbc.DropdownMenuItem("Departments", href="/depts"),
                    dbc.DropdownMenuItem(divider=True),

                    dbc.DropdownMenuItem("Predictive Modeling", header=True),
                    dbc.DropdownMenuItem("Modeling", href="/models"),
                    dbc.DropdownMenuItem("Forecasting", href="/fcast"),
                    dbc.DropdownMenuItem(divider=True),

                    dbc.DropdownMenuItem("Conclusion", href="/conclusion"),
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
content = html.Div(id="page_content", style=content_style)

#PAGE LAYOUT
app.layout = html.Div([dcc.Location(id="url"),sidebar, content])

#-----------------------------------------------------------------------

#RETRIEVE INPUTS FROM ROUTES, PASS COMPONENTS TO SIDEBAR AND CONTENT SECTIONS
@app.callback([Output("page_content", "children"),
                Output("sb_header", "children"),
                Output("sb_paragraph", "children"),
                Output("sb_progress", "children"),
                Output("nav_buttons", "children")], 
                [Input("url", "pathname")])

#-----------------------------------------------------------------------

#PAGE RENDERING/ROUTING
def render_page_content(pathname):
    
    if pathname == "/":
        #sidebar components
        header = html.H4("Walmart Sales Forecast", className="display-4")
        paragraph = html.P("This project explores the sales of several Walmart locations. Exploratory data analysis was performed at the store and department level, the findings were used to forecast sales", className="lead")
        progress_bar = dbc.Progress(value=0, style={"height": "3px"}, className="mb-3")
        buttons = [dbc.Button("Back", outline=True,color="info", className="mr-1", disabled=True),
                    dbc.Button("Next", href="/stores", outline=True,color="info", className="mr-1")]
        
        #content components
        content = html.Div(
                        [
                            dbc.Row(dbc.Col(html.Div(dcc.Graph(figure=sales)))),
                        ]
                    )
        return content, header, paragraph, progress_bar, buttons

#STORE PAGE ROUTE
    elif pathname == "/stores":
        #sidebar components
        header = html.H4("Exploratory Data Analysis", className="display-4")
        paragraph = html.P("In this section we aim to discover the siginificance of the stores' types", className="lead")
        progress_bar = dbc.Progress(value=25, style={"height": "3px"}, className="mb-3")
        buttons = [dbc.Button("Back", href="/", outline=True,color="info", className="mr-1"),
                   dbc.Button("Next", href="/depts", outline=True,color="info", className="mr-1")]
        
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

                            #content text
                            dbc.Row(dbc.Col(html.P("hhh"))),

                            #Charts
                            dbc.Row(
                                [
                                    dbc.Col(html.Div(dcc.Graph(figure=store3))),
                                    dbc.Col(html.Div(dcc.Graph(figure=store4))),
                                ]
                            ),

                            #content text
                            dbc.Row(dbc.Col(html.P("hhh"))),                              
                        ]
                    )

        return content, header, paragraph, progress_bar, buttons

#DEPT PAGE ROUTE
    elif pathname == "/depts":
        #sidebar components
        header = html.H4("Exploratory Data Analysis", className="display-4")
        paragraph = html.P("This sectoion analyzes the demand and stationarity of the departments", className="lead")
        progress_bar = dbc.Progress(value=50, style={"height": "3px"}, className="mb-3")
        buttons = [dbc.Button("Back", href="/stores", outline=True,color="info", className="mr-1"),
                   dbc.Button("Next", href="/models", outline=True,color="info", className="mr-1")]
        
        #content components
        content = html.Div(
                        [
                            #content text
                            dbc.Row(
                                [
                                    dbc.Col(html.P("hhh"))
                                ]
                            ),

                            #Charts
                            dbc.Row(
                                [
                                    dbc.Col(html.Div(dcc.Graph(figure=dept1)))
                                ]
                            ),
                             
                        ]
                    )

        return content, header, paragraph, progress_bar, buttons

#PRED. MODELING ROUTE
    elif pathname == "/models":
        #sidebar components
        header = html.H4("Exploratory Data Analysis", className="display-4")
        paragraph = html.P("ITS WORKING! consectetur rus semper eget. Amet dictum sit amet justo donec enim diam.", className="lead")
        progress_bar = dbc.Progress(value=75, style={"height": "3px"}, className="mb-3")
        buttons = [dbc.Button("Back", href="/depts",outline=True,color="info", className="mr-1"),
                   dbc.Button("Next", href="/conclusion",outline=True,color="info", className="mr-1")]
        
        #content components
        tab1_content = html.Div(
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
        tab2_content = html.Div(
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
        tab3_content = html.Div(
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

        content = html.Div(
            [dbc.Tabs(
                [
                    dbc.Tab(tab1_content, label="Tab 1", tab_style=tab_style,labelClassName="text-primary"),
                    dbc.Tab(tab2_content, label="Tab 2", labelClassName="text-primary"),
                    dbc.Tab(tab3_content, label="Tab 3",labelClassName="text-primary"),
                ]
            )        
        ])
        return content, header, paragraph, progress_bar, buttons

#CONCLUSION ROUTE
    elif pathname == "/conclusion":
        #sidebar components
        header = html.H4("Exploratory Data Analysis", className="display-4")
        paragraph = html.P("ITS WORKING! consectetur rus semper eget. Amet dictum sit amet justo donec enim diam.", className="lead")
        progress_bar = dbc.Progress(value=100, style={"height": "3px"}, className="mb-3")
        buttons = [dbc.Button("Back", href="/models",outline=True,color="info", className="mr-1"),
                    dbc.Button("Next", outline=True,color="info", className="mr-1", disabled=True)]
        
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