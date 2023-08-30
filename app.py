import pandas as pd
from dash import Dash, Input, Output, dcc, html, dash_table

data = pd.read_csv("amazon_prime_titles.csv", sep=',')
types = data['type'].sort_values().unique()

external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Amazon Prime Movies and TV Shows"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Img(src=r'assets/logo.png', alt="image", style={'height':'40%', 'width':'10%'}), 
                html.H1(
                    children="TV Shows and Movies", className="header-title"
                ),
                html.P(
                    children=(
                        "You can view the TV shows and movies shown"
                        " on Amazon Prime between 1920-2021 by type and genre."
                    ),
                    className="header-description",
                ),
            ],
            className="header",
            style={'textAlign': 'center'}
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Type", className="menu-title"),
                        dcc.Dropdown(
                            id="type-filter",
                            options=[
                                {"label": type, "value": type}
                                for type in types
                            ],
                            value="Example",
                            clearable=False,
                            #searchable=False,
                            className="dropdown",
                        ),
                    ],
                    style={"width": "15%"},
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Genre", className="menu-title"),
                        dcc.Dropdown(
                            id="genre-filter",
                            optionHeight = 90,
                            options=[
                                {"label": genre, "value": genre}
                                for genre in data["listed_in"].unique()
                            ],
                            value= "Example", #data["listed_in"].unique()[0]
                            clearable=False,
                            #searchable=False,
                            className="dropdown",
                        ),
                    ],
                    style={"width": "25%"},
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Year Range", className="menu-title"
                        ),
                        html.Div(
                        dcc.RangeSlider(
                            id="year-slider",
                            min=data["release_year"].min(),
                            max=data["release_year"].max(),
                            step=1,
                            value=[data["release_year"].min(), data["release_year"].max()],
                            tooltip={"placement": "bottomRight", "always_visible": True}
                        ),
                            style={'width': '300%'}
        ),
                    ],
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dash_table.DataTable(
                        id="data-table",
                        columns=[
                            {"name": "title", "id": "title"},
                            {"name": "cast", "id": "cast"},
                            {"name": "description", "id": "description"},
                        ],
                        data=data[["title", "cast", "description"]].to_dict("records"),
                        style_table={'height': '500px'},
                        style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto',
                            'textAlign': 'left',
                            'padding': '5px'
                        },
                        style_header={
                            'backgroundColor': 'black',
                            'color': 'white',
                            'textAlign': 'left',
                            'textTransform': 'uppercase'
                        },
                        fixed_rows={'headers': True},
                        style_cell={'minWidth': 90, 'maxWidth': 90, 'width': 90},
                        sort_action='native', 
                        sort_mode='single'  
                    ),
                    className="card",
                )
            ],
            className="wrapper",
        ),
        html.Div(
        "github: busekcoban",
            style={'text-align': 'right', 'margin-right': '10px'}
        )
    ]
)

@app.callback(
    Output("data-table", "data"),
    Input("type-filter", "value"),
    Input("year-slider", "value"),
    Input("genre-filter", "value"),
)
def update_table(selected_type, selected_years, selected_genre):
    filtered_data = data[
        (data["type"] == selected_type)
        & (data["release_year"] >= selected_years[0])
        & (data["release_year"] <= selected_years[1])
        & (data["listed_in"] == selected_genre)
    ]
    
    filtered_data = filtered_data[filtered_data["title"] != "Series_Project_UN_Test_UHD"]
    return filtered_data[["title", "cast", "description"]].to_dict("records")

if __name__ == "__main__":
    app.run_server(debug=True)
