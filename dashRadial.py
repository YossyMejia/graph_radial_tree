import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from radial import *

# Inicializacion del bash para el grafico icicle y sus componentes ----
app = dash.Dash(__name__)
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Exportaciones anuales por categoria - Costa Rica - 2019",
                    style={'textAlign': 'center'}, className="header-title"
                ),  # Titulo
                html.H3(children="Cada categoria muestra su valor comercial, lo cual es el precio real de venta en el "
                                 "mercado de los productos o servicios sin tomar en cuenta si inclusion de costos "
                                 "extra por fletes, seguros o impuestos.",
                        style={'textAlign': 'center'}, className="header-description"),
            ],
            className="header", style={'backgroundColor': '#F5F5F5'},
        ),  # Descripcion y titulos
        html.Div(
            children=[
                html.Div(children='Profundidad del arbol: ',
                         style={'fontSize': "19px", 'float': 'left', 'clear': 'none'},
                         className='menu-title'),
                dcc.Dropdown(
                    id='deep-filter',
                    options=[
                        {'label': valor, 'value': valor}
                        for valor in profundidades
                    ],
                    value=3,
                    clearable=False,
                    searchable=False,
                    className='dropdown', style={'fontSize': "19px", 'textAlign': 'center', 'min-width': '65px',
                                                 'float': 'left', 'clear': 'none', 'margin-left': '5px'},
                ),
                html.Div(children='Tamaño del texto: ',
                         style={'fontSize': "19px", 'float': 'left', 'clear': 'none',
                                'margin-left': '60px'}, className='menu-title'),
                dcc.Dropdown(
                    id='font-filter',
                    options=[
                        {'label': valor, 'value': valor}
                        for valor in tamannos_fuente
                    ],
                    value=tamannos_fuente[1],
                    clearable=False,
                    searchable=False,
                    className='dropdown',
                    style={'fontSize': "19px", 'textAlign': 'center', 'size': '100%', 'min-width': '65px',
                           'float': 'left', 'clear': 'none', 'margin-left': '5px'}
                ),
                html.Div(children='Configuracion de color: ',
                         style={'fontSize': "19px", 'float': 'left', 'clear': 'none',
                                'margin-left': '60px'}, className='menu-title'),
                dcc.Dropdown(
                    id='color-filter',
                    options=[
                        {'label': valor, 'value': valor}
                        for valor in colores_disponibles
                    ],
                    value=colores_disponibles[0],
                    clearable=False,
                    searchable=False,
                    className='dropdown',
                    style={'fontSize': "19px", 'textAlign': 'center', 'size': '100%', 'min-width': '200px',
                           'float': 'left', 'clear': 'none', 'margin-left': '5px'}
                ),
            ],
            className='menu',
        ),

        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id='fig_update',
                        figure=fig_radial,
                    ),
                    style={'width': '100%', 'height': '150%', 'margin-top': '60px'},
                )
            ],
            className='graph',
        ),
    ]
)


@app.callback(
    Output("fig_update", "figure"),         # la salida es la figura actualziada
    [Input("deep-filter", "value"),         # variable para profundidad
     Input("font-filter", "value"),         # variable para el tamanno de fuente
     Input("color-filter", "value")],       # variable para la configuracion de color
)
def update_charts(deep, font_size, color_config):
    # Funcion que recibe una profundidad para ser asignada a la figura, tambie recibe una orientacion
    # y por ultimo el tipo de color a ser aplicado en el grafico
    update_fig = creacion_radial(deep, color_config, font_size)
    return update_fig
