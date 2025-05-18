import dash
from dash import html, dcc, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import json
import os

from data_processing import (
    cargar_datos_mortalidad, cargar_codigos_muerte, cargar_divipola,
    preparar_datos_mapa, preparar_datos_linea_tiempo, preparar_datos_ciudades_violentas,
    preparar_datos_menor_mortalidad, preparar_datos_causas_muerte,
    preparar_datos_histograma_edad, preparar_datos_sexo_departamento
)

BASE_DIR_APP = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR_APP)
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

print("Iniciando carga y procesamiento de datos...")
df_mortalidad_raw = cargar_datos_mortalidad()
df_codigos_raw = cargar_codigos_muerte()
df_divipola_raw = cargar_divipola()

df_mapa = pd.DataFrame()
df_linea_tiempo = pd.DataFrame()
df_ciudades_violentas = pd.DataFrame()
df_menor_mortalidad = pd.DataFrame()
df_causas_muerte = pd.DataFrame()
df_histograma_edad = pd.DataFrame()
df_sexo_departamento = pd.DataFrame()

if df_mortalidad_raw.empty or df_codigos_raw.empty or df_divipola_raw.empty:
    print("Error: Uno o más archivos de datos crudos no se pudieron cargar.")
else:
    print("Datos crudos cargados. Procesando para visualizaciones...")
    df_mapa = preparar_datos_mapa(df_mortalidad_raw, df_divipola_raw)
    df_linea_tiempo = preparar_datos_linea_tiempo(df_mortalidad_raw)
    df_ciudades_violentas = preparar_datos_ciudades_violentas(df_mortalidad_raw, df_divipola_raw, df_codigos_raw)
    df_menor_mortalidad = preparar_datos_menor_mortalidad(df_mortalidad_raw, df_divipola_raw)
    df_causas_muerte = preparar_datos_causas_muerte(df_mortalidad_raw, df_codigos_raw)
    df_histograma_edad = preparar_datos_histograma_edad(df_mortalidad_raw)
    df_sexo_departamento = preparar_datos_sexo_departamento(df_mortalidad_raw, df_divipola_raw)
    print("Procesamiento de datos completado.")

print("Creando figuras de Plotly...")

geojson_file_path = os.path.join(DATA_DIR, 'colombia_departamentos.geojson')
geojson_colombia_dptos = None
geojson_cargado_ok = False
fig_mapa_creada_con_geojson = False

try:
    with open(geojson_file_path, 'r', encoding='utf-8') as f:
        geojson_colombia_dptos = json.load(f)
    geojson_cargado_ok = True
    print("Archivo GeoJSON cargado exitosamente.")
except FileNotFoundError:
    print(f"ADVERTENCIA: Archivo GeoJSON '{geojson_file_path}' no encontrado.")
except json.JSONDecodeError:
    print(f"ADVERTENCIA: Error al decodificar GeoJSON en '{geojson_file_path}'.")
except Exception as e:
    print(f"ADVERTENCIA: Otro error al cargar GeoJSON: {e}")

if not df_mapa.empty:
    if 'COD_DPTO_GEO' not in df_mapa.columns:
        print("Advertencia: 'COD_DPTO_GEO' no en df_mapa. Intentando crearla.")
        if 'COD_DEPARTAMENTO' in df_mapa.columns:
            df_mapa['COD_DPTO_GEO'] = df_mapa['COD_DEPARTAMENTO'].astype(str).str.zfill(2)
        else:
            print("Error: 'COD_DEPARTAMENTO' tampoco en df_mapa. No se puede crear mapa GeoJSON.")
            geojson_cargado_ok = False 
            

    if geojson_cargado_ok and 'COD_DPTO_GEO' in df_mapa.columns:
        try:
            fig_mapa = px.choropleth_mapbox(df_mapa,
                                           geojson=geojson_colombia_dptos,
                                           locations='COD_DPTO_GEO',
                                           featureidkey="properties.DPTO",
                                           color='TOTAL_MUERTES',
                                           color_continuous_scale="YlOrRd",
                                           mapbox_style="carto-positron",
                                           zoom=3.8, center={"lat": 4.5709, "lon": -74.2973},
                                           opacity=0.7,
                                           hover_name='DEPARTAMENTO',
                                           hover_data={'TOTAL_MUERTES': True, 'COD_DPTO_GEO': True, 'DEPARTAMENTO': False},
                                           labels={'TOTAL_MUERTES':'Total Muertes', 'COD_DPTO_GEO': 'Cód. Depto.'},
                                           title='Distribución de Muertes por Departamento (2019)')
            fig_mapa.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
            print("Figura de mapa creada con GeoJSON.")
            fig_mapa_creada_con_geojson = True
        except Exception as e:
            print(f"Error al crear choropleth_mapbox: {e}. Usando gráfico de barras.")
    
    if not fig_mapa_creada_con_geojson:
        print("Usando gráfico de barras como fallback para el mapa.")
        fig_mapa = px.bar(df_mapa.sort_values('TOTAL_MUERTES', ascending=False), 
                          x='DEPARTAMENTO', y='TOTAL_MUERTES', 
                          title='Total Muertes por Departamento (2019) (Mapa no disponible)',
                          labels={'TOTAL_MUERTES': 'Total Muertes', 'DEPARTAMENTO': 'Departamento'})
else:
    fig_mapa = px.bar(title='Muertes por Departamento (Datos no disponibles)')

if not df_linea_tiempo.empty:
    meses_map = {1:'Ene', 2:'Feb', 3:'Mar', 4:'Abr', 5:'May', 6:'Jun', 7:'Jul', 8:'Ago', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dic'}
    df_linea_tiempo['NOMBRE_MES'] = df_linea_tiempo['MES'].map(meses_map)
    df_linea_tiempo_sorted = df_linea_tiempo.set_index('MES').reindex(list(range(1,13))).reset_index()
    df_linea_tiempo_sorted['NOMBRE_MES'] = df_linea_tiempo_sorted['MES'].map(meses_map)
    fig_linea_tiempo = px.line(df_linea_tiempo_sorted.dropna(subset=['NOMBRE_MES']), x='NOMBRE_MES', y='TOTAL_MUERTES',
                               title='Total Muertes por Mes (2019)', markers=True,
                               labels={'TOTAL_MUERTES': 'Total Muertes', 'NOMBRE_MES': 'Mes'})
else:
    fig_linea_tiempo = px.line(title='Muertes por Mes (Datos no disponibles)')

if not df_ciudades_violentas.empty:
    df_ciudades_violentas['CIUDAD_DPTO'] = df_ciudades_violentas['MUNICIPIO'] + " (" + df_ciudades_violentas['DEPARTAMENTO'] + ")"
    fig_ciudades_violentas = px.bar(df_ciudades_violentas.sort_values('TOTAL_HOMICIDIOS', ascending=True),
                                    x='TOTAL_HOMICIDIOS', y='CIUDAD_DPTO', orientation='h',
                                    title='Top 5 Ciudades con Más Homicidios (2019)',
                                    labels={'TOTAL_HOMICIDIOS': 'Total Homicidios', 'CIUDAD_DPTO': 'Ciudad (Dpto)'})
else:
    fig_ciudades_violentas = px.bar(title='Top 5 Ciudades Violentas (Datos no disponibles)')

if not df_menor_mortalidad.empty:
    df_menor_mortalidad['CIUDAD_DPTO'] = df_menor_mortalidad['MUNICIPIO'] + " (" + df_menor_mortalidad['DEPARTAMENTO'] + ")"
    fig_menor_mortalidad = px.pie(df_menor_mortalidad, names='CIUDAD_DPTO', values='TOTAL_MUERTES',
                                  title='Top 10 Ciudades con Menor Número de Muertes (2019)', hole=0.4)
    fig_menor_mortalidad.update_traces(textposition='inside', textinfo='percent+label')
else:
    fig_menor_mortalidad = px.pie(title='Top 10 Ciudades Menor Mortalidad (Datos no disponibles)')

if not df_histograma_edad.empty:
    fig_histograma_edad = px.bar(df_histograma_edad, x='RANGO_EDAD', y='TOTAL_MUERTES',
                                 title='Distribución de Muertes por Rango de Edad (2019)',
                                 labels={'TOTAL_MUERTES': 'Total Muertes', 'RANGO_EDAD': 'Rango de Edad'})
    fig_histograma_edad.update_xaxes(categoryorder='array', categoryarray=df_histograma_edad['RANGO_EDAD'].tolist())
else:
    fig_histograma_edad = px.bar(title='Distribución de Muertes por Edad (Datos no disponibles)')

if not df_sexo_departamento.empty:
    df_sexo_dpto_sum = df_sexo_departamento.groupby('DEPARTAMENTO')['TOTAL_MUERTES'].sum().reset_index().sort_values('TOTAL_MUERTES', ascending=False)
    fig_sexo_departamento = px.bar(df_sexo_departamento, x='DEPARTAMENTO', y='TOTAL_MUERTES',
                                   color='SEXO_ETIQUETA', barmode='stack',
                                   title='Total Muertes por Sexo en Cada Departamento (2019)',
                                   labels={'TOTAL_MUERTES': 'Total Muertes', 'DEPARTAMENTO': 'Departamento', 'SEXO_ETIQUETA': 'Sexo'},
                                   category_orders={'DEPARTAMENTO': df_sexo_dpto_sum['DEPARTAMENTO'].tolist()},
                                   color_discrete_map={'Hombre':'#636EFA', 'Mujer':'#EF553B', 'Indeterminado':'#B6E880'})
else:
    fig_sexo_departamento = px.bar(title='Muertes por Sexo y Departamento (Datos no disponibles)')

print("Todas las figuras creadas.")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

print("Definiendo layout...")
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Análisis de Mortalidad en Colombia - 2019", className="text-center text-primary mt-4 mb-4"), width=12)),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='mapa-muertes', figure=fig_mapa), width=12, lg=6, className="mb-4"),
        dbc.Col(dcc.Graph(id='linea-tiempo-muertes', figure=fig_linea_tiempo), width=12, lg=6, className="mb-4")
    ]),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='ciudades-violentas', figure=fig_ciudades_violentas), width=12, lg=6, className="mb-4"),
        dbc.Col(dcc.Graph(id='menor-mortalidad', figure=fig_menor_mortalidad), width=12, lg=6, className="mb-4")
    ]),

    dbc.Row([
        dbc.Col([
            html.H3("Principales Causas de Muerte (2019)", className="text-center"),
            dash_table.DataTable(
                id='tabla-causas-muerte',
                columns=[{"name": i, "id": i} for i in df_causas_muerte.columns] if not df_causas_muerte.empty else [],
                data=df_causas_muerte.to_dict('records') if not df_causas_muerte.empty else [],
                style_cell={'padding': '5px', 'textAlign': 'left'},
                style_header={'backgroundColor': '#f8f9fa', 'fontWeight': 'bold'},
                style_data={'border': '1px solid #dee2e6'},
                page_size=10,
                filter_action="native", 
                sort_action="native",  
            )
        ], width=12, lg=6, className="mb-4"),
        dbc.Col(dcc.Graph(id='histograma-edad', figure=fig_histograma_edad), width=12, lg=6, className="mb-4")
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id='sexo-departamento', figure=fig_sexo_departamento), width=12, className="mb-4")
    ])
], fluid=True)
print("Layout definido.")

if __name__ == '__main__':
    print("Ejecutando servidor Dash...")
    app.run(debug=True)