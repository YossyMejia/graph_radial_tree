import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Constantes ----------
# Definicion de la ubicacion del archivo de datos
df = pd.read_csv('D:\\User\\Documentos\\Semestres\\S2-2021\\Visualizacion\\Proyecto 1\\Datos\\Datos.csv')

# Orientaciones del grafico disponibles
orientaciones_disponibles = ["Horizontal", "Vertical"]

# Configuracion de color disponible
colores_disponibles = ["Por categoria", "Por valor comercial"]

# Tamanno de fuentes disponibles
tamannos_fuente = [15, 20, 25, 30, 35, 40]


# Funciones utiles ----------
def label_modif(trace):
    # Funcion para modificar el label de un trace individual
    label = "<b>" + trace.labels + "<b>"
    return label


def hover_template_modif(trace):
    # Funcion para modificar el hover template de un trace individual obteniendo datos del mismo objeto
    template = "<br><b>Categoria: <b>" + trace.labels + "<br><br><b>Ruta completa de la categoria: <b>" + \
               trace.parents + "<br><br><b>Valor comercial total :<b> %{value}, <br><br><b>Porcentaje de " \
                               "acaparacion dentro de la sub categoria :<b> %{percentParent}% "
    return template


def tranformar_orientacion(orientacion):
    # Funcion encargada de tomar una orientacion y retornar su acronimo
    if orientacion == orientaciones_disponibles[0]:
        return 'h'
    elif orientacion == orientaciones_disponibles[1]:
        return 'v'


def original_fig(color_type, deep):
    #Funcion encargada de crear el grafico original con una profundidad elegida por el usuario y una forma de color
    if color_type == colores_disponibles[0]:
        fig = px.icicle(df, path=[px.Constant("Todas las categorias"), 'Section', 'HS2', 'HS4'],
                        values="Trade_Value", maxdepth=deep, )
    elif color_type == colores_disponibles[1]:
        print(color_type)
        fig = px.icicle(df, path=[px.Constant("Todas las categorias"), 'Section', 'HS2', 'HS4'],
                        values="Trade_Value", maxdepth=deep, color_continuous_scale='blugrn' , color='Trade_Value')
    return fig


def creacion_icicle(deep, color_type, orientation, font_size):
    # Funcion encargada de crear un grafico icicle con una profundidad, color y orientacion elegida por el usuario

    # Definicion del grafico, su raiz y sus sub elementos
    fig = original_fig(color_type, deep)

    # Modifica la orientacion, el tamanno de letra del hoverlabel y el color de la raiz
    fig.update_traces(tiling=dict(orientation=orientation), selector=dict(type='icicle'),
                      hoverlabel_font_size=(font_size-5), root_color='lightgrey')

    # Modificar el layout del grafico, cambiando el margen, el tamanno del texto y actualizando el tipo de letra y color
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25), uniformtext=dict(minsize=font_size, mode='hide'),
                      title=dict(x=0.5), font_family="Arial", font_color="black",
                      coloraxis_colorbar=dict(title="<b>Valor comercial</b>"), height=900)

    # Ciclo para recorrer cada cubito del grafico (raiz, sub rama, hojas) y modificar sus datos individualmente
    fig.for_each_trace(
        lambda t: t.update(labels=label_modif(t), hovertemplate=hover_template_modif(t), textposition="middle center"))

    return fig


# Creacion y declaracion de la figura original, con profundidad 3, color por categoria,orientacion horizontal y
# tamanno de fuente 20
fig = creacion_icicle(3, colores_disponibles[0], 'h', 20)


# Inicializacion del bash y sus componentes
app = dash.Dash(__name__)
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Exportaciones anuales por categoria - Costa Rica - 2019",
                    style={'textAlign': 'center'}, className="header-title"
                ),  # Header title
                html.H3(children="Cada categoria muestra su valor comercial, lo cual es el precio real de venta en el "
                                 "mercado de los productos o servicios sin tomar en cuenta si inclusion de costos "
                                 "extra por fletes, seguros o impuestos.",
                        style={'textAlign': 'center'}, className="header-description"),
            ],
            className="header", style={'backgroundColor': '#F5F5F5'},
        ),  # Description below the header
        html.Div(
            children=[
                html.Div(children='Profundidad del arbol: ',
                         style={'fontSize': "19px", 'float': 'left', 'clear': 'none'},
                         className='menu-title'),
                dcc.Dropdown(
                    id='deep-filter',
                    options=[
                        {'label': valor, 'value': valor}
                        for valor in [2, 3, 4]
                    ],
                    value=3,
                    clearable=False,
                    searchable=False,
                    className='dropdown', style={'fontSize': "19px", 'textAlign': 'center', 'min-width': '65px',
                                                 'float': 'left', 'clear': 'none', 'margin-left': '5px'},
                ),
                html.Div(children='Orientacion del grafico: ',
                         style={'fontSize': "19px", 'float': 'left', 'clear': 'none',
                                'margin-left': '60px'}, className='menu-title'),
                dcc.Dropdown(
                    id='orientacion-filter',
                    options=[
                        {'label': valor, 'value': valor}
                        for valor in orientaciones_disponibles
                    ],
                    value=orientaciones_disponibles[0],
                    clearable=False,
                    searchable=False,
                    className='dropdown',
                    style={'fontSize': "19px", 'textAlign': 'center', 'size': '100%', 'min-width': '160px',
                           'float': 'left', 'clear': 'none', 'margin-left': '5px'}
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
                        figure=fig,
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
     Input("orientacion-filter", "value"),  # variable para la orientacion
     Input("font-filter", "value"),         # variable para el tamanno de fuente
     Input("color-filter", "value")],       # variable para la configuracion de color
)
def update_charts(deep, orientacion, font_size, color_config):
    # Funcion que recibe una profundidad para ser asignada a la figura, tambie recibe una orientacion y llama una
    # funcion para obtener el valor necesario (Horizontal -> h) y por ultimo el tipo de color a ser aplicado en el
    # grafico
    orientacion = tranformar_orientacion(orientacion)
    update_fig = creacion_icicle(deep, color_config, orientacion, font_size)
    return update_fig


if __name__ == '__main__':
    app.run_server(debug=True)
