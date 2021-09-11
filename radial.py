import plotly.express as px
from constants import *

# Funciones utiles para la creacion del grafico ----------
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


def original_fig(color_type, deep):
    # Funcion encargada de crear el grafico original con una profundidad elegida por el usuario y una forma de color
    if color_type == colores_disponibles[0]:
        fig = px.sunburst(df, path=[px.Constant("Todas las categorias"), 'Section', 'HS2', 'HS4'],
                        values="Trade_Value", maxdepth=deep, )
    elif color_type == colores_disponibles[1]:
        fig = px.sunburst(df, path=[px.Constant("Todas las categorias"), 'Section', 'HS2', 'HS4'],
                        values="Trade_Value", maxdepth=deep, color_continuous_scale='blugrn', color='Trade_Value')
    return fig

def creacion_radial(deep, color_type, font_size):
    # Funcion encargada de crear un grafico icicle con una profundidad, color y orientacion elegida por el usuario

    # Definicion del grafico, su raiz y sus sub elementos
    fig = original_fig(color_type, deep)

    # Modifica la orientacion, el tamanno de letra del hoverlabel y el color de la raiz
    fig.update_traces(selector=dict(type='icicle'),
                      hoverlabel_font_size=(font_size), root_color='lightgrey')

    # Modificar el layout del grafico, cambiando el margen, el tamanno del texto y actualizando el tipo de letra y color
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25), uniformtext=dict(minsize=font_size, mode='hide'),
                      title=dict(x=0.5), font_family="Arial", font_color="black",
                      coloraxis_colorbar=dict(title="<b>Valor comercial</b>"), height=1100)

    # Ciclo para recorrer cada cubito del grafico (raiz, sub rama, hojas) y modificar sus datos individualmente
    fig.for_each_trace(
        lambda t: t.update(labels=label_modif(t), hovertemplate=hover_template_modif(t),))
                           #textposition="middle center"))

    return fig

# Creacion y declaracion de la figura original, con profundidad 3, color por categoria,orientacion horizontal y
# tamanno de fuente 20
fig_radial = creacion_radial(3, colores_disponibles[0], 20)
