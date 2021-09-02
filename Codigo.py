
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Definicion de la ubicacion del archivo de datos
df = pd.read_csv('D:\\User\\Documentos\\Semestres\\S2-2021\\Visualizacion\\Proyecto 1\\Datos\\Datos.csv')


# Definicion del grafico original que se muestra sin filtros
fig = px.icicle(df, path=[px.Constant("Todas las categorias"), 'Section', 'HS2', 'HS4'],
                values="Trade_Value", maxdepth=3,  # color_continuous_scale='blugrn',
                title="<b>Exportaciones anuales por categoria - Costa Rica - 2019<b>")  # , color='Trade_Value')


def label_modif(trace):
    # Funcion para modificar el label del trace
    label = "<b>" + trace.labels + "<b>"
    return label


def hover_template_modif(trace):
    # Funcion para modificar el hover template de cada trace
    label = "<br><b>Categoria: <b>" + trace.labels + "<br><b>Ruta completa de la categoria: <b>" + trace.parents + \
            "<br><b>Trade value total :<b> %{value}, <br><b>Porcentaje dentro de la sub categoria :<b> %{" \
            "percentParent}% "
    return label


# Modifica la orientacion, el tamanno de letra del hoverlabel y el color de la raiz
fig.update_traces(tiling=dict(orientation='h'), selector=dict(type='icicle'), hoverlabel_font_size=15,
                  root_color='lightgrey')

# Modificar el layout del grafico, cambiando el margen, el tamanno del texto y actualizando el tipo de letra y color
fig.update_layout(margin=dict(t=50, l=25, r=25, b=25), uniformtext=dict(minsize=20, mode='hide'), title=dict(x=0.5),
                  font_family="Arial",
                  font_color="black",
                  title_font_family="Arial",
                  title_font_color="black",
                  title_font_size=23,
                  legend_title_font_color="black",
                  legend_bgcolor="red",
                  showlegend=True,
                  coloraxis_colorbar=dict(title="<b>Valor comercial</b>"),
                  height = 900
                  )


# Ciclo para recorrer cada cubito del grafico (raiz, sub rama, hojas) y modificar sus datos individualmente
fig.for_each_trace(
    lambda t: t.update(labels=label_modif(t), hovertemplate=hover_template_modif(t), textposition="middle center")
)

# Muestra la figura y guarda una copia de html en la ruta especificada
#fig.show()
#fig.write_html("iciclePlot.html")


app = dash.Dash(__name__)
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Ejemplo de subtitulo", style={'textAlign': 'center'}, className="header-title"
                ),  # Header title
                html.H2(children="Exportaciones anuales por categoria - Costa Rica - 2019",
                       style={'fontSize': "30px", 'textAlign': 'center'}, className="header-emoji"),
            ],
            className="header", style={'backgroundColor': '#F5F5F5'},
        ),  # Description below the header

        html.Div(
            children=[
                html.Div(children='Profundidad', style={'fontSize': "24px"}, className='menu-title'),
                dcc.Dropdown(
                    id='deep-filter',
                    options=[
                        {'label': valor, 'value': valor}
                        for valor in [2, 3, 4]
                    ],  # 'deep name' is the filter
                    value=3,
                    clearable=False,
                    searchable=False,
                    className='dropdown', style={'fontSize': "24px", 'textAlign': 'center'},
                ),
            ],
            className='menu',
        ),  # the dropdown function

        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id='fig_update',
                        figure=fig,
                    ),
                    style={'width': '100%', 'height': '150%',  'margin': '0'},
                )
            ],
            className='graph',
        ),
    ]
)  # The graph


@app.callback(
    Output("fig_update", "figure"), #the output is the scatterchart
    [Input("deep-filter", "value")], #the input is the deep-filter
)
def update_charts(deep):

    figUpdate = px.icicle(df, path=[px.Constant("Todas las categorias"), 'Section', 'HS2', 'HS4'],
                    values="Trade_Value", maxdepth=deep,  # color_continuous_scale='blugrn',
                    title="<b>Exportaciones anuales por categoria - Costa Rica - 2019<b>")  # , color='Trade_Value')

    # Modifica la orientacion, el tamanno de letra del hoverlabel y el color de la raiz
    figUpdate.update_traces(tiling=dict(orientation='h'), selector=dict(type='icicle'), hoverlabel_font_size=15,
                      root_color='lightgrey')

    # Modificar el layout del grafico, cambiando el margen, el tamanno del texto y actualizando el tipo de letra y color
    figUpdate.update_layout(margin=dict(t=50, l=25, r=25, b=25), uniformtext=dict(minsize=20, mode='hide'), title=dict(x=0.5),
                      font_family="Arial",
                      font_color="black",
                      title_font_family="Arial",
                      title_font_color="black",
                      title_font_size=23,
                      legend_title_font_color="black",
                      legend_bgcolor="red",
                      showlegend=True,
                      coloraxis_colorbar=dict(title="<b>Valor comercial</b>")
                      )

    # Ciclo para recorrer cada cubito del grafico (raiz, sub rama, hojas) y modificar sus datos individualmente
    figUpdate.for_each_trace(
        lambda t: t.update(labels=label_modif(t), hovertemplate=hover_template_modif(t), textposition="middle center")
    )

    return figUpdate #return the scatterchart according to the filter

if __name__ == '__main__':
    app.run_server(debug = True)

# TODO: Cambiar tamanno raiz, cambiar colores, agreagar innovacion de poder seleccionar la maxima profundidad
# Decir que el tamanno de la raiz es grande debido a la profundidad que se solicita
