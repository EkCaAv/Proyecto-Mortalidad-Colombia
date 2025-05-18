import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

file_path_mortalidad = os.path.join(DATA_DIR, 'Anexo1.NoFetal2019_CE_15-03-23.xlsx')
file_path_codigos_muerte = os.path.join(DATA_DIR, 'Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx')
file_path_divipola = os.path.join(DATA_DIR, 'Anexo3.Divipola_CE_15-03-23.xlsx')

def cargar_datos_mortalidad():
    try:
        df = pd.read_excel(file_path_mortalidad)
        return df
    except FileNotFoundError:
        print(f"Error: El archivo {file_path_mortalidad} no fue encontrado.")
        return pd.DataFrame()

def cargar_codigos_muerte():
    try:
        df = pd.read_excel(file_path_codigos_muerte)
        return df
    except FileNotFoundError:
        print(f"Error: El archivo {file_path_codigos_muerte} no fue encontrado.")
        return pd.DataFrame()

def cargar_divipola():
    try:
        df = pd.read_excel(file_path_divipola)
        return df
    except FileNotFoundError:
        print(f"Error: El archivo {file_path_divipola} no fue encontrado.")
        return pd.DataFrame()

def preparar_datos_mapa(df_mortalidad, df_divipola):
    if df_mortalidad.empty or df_divipola.empty:
        return pd.DataFrame(columns=['COD_DEPARTAMENTO', 'DEPARTAMENTO', 'TOTAL_MUERTES'])
    muertes_por_dpto = df_mortalidad.groupby('COD_DEPARTAMENTO').size().reset_index(name='TOTAL_MUERTES')
    divipola_dptos = df_divipola[['COD_DEPARTAMENTO', 'DEPARTAMENTO']].drop_duplicates(subset=['COD_DEPARTAMENTO'])
    mapa_data = pd.merge(muertes_por_dpto, divipola_dptos, on='COD_DEPARTAMENTO', how='left')
    mapa_data['DEPARTAMENTO'] = mapa_data['DEPARTAMENTO'].fillna('Desconocido')
    return mapa_data[['COD_DEPARTAMENTO', 'DEPARTAMENTO', 'TOTAL_MUERTES']]

def preparar_datos_linea_tiempo(df_mortalidad):
    if df_mortalidad.empty:
        return pd.DataFrame(columns=['MES', 'TOTAL_MUERTES'])
    muertes_por_mes = df_mortalidad.groupby('MES').size().reset_index(name='TOTAL_MUERTES')
    muertes_por_mes = muertes_por_mes.sort_values(by='MES')
    return muertes_por_mes[['MES', 'TOTAL_MUERTES']]

def preparar_datos_ciudades_violentas(df_mortalidad, df_divipola, df_codigos_muerte):
    if df_mortalidad.empty or df_divipola.empty:
        return pd.DataFrame(columns=['MUNICIPIO', 'DEPARTAMENTO', 'TOTAL_HOMICIDIOS'])

    if df_codigos_muerte.empty:
        return pd.DataFrame(columns=['MUNICIPIO', 'DEPARTAMENTO', 'TOTAL_HOMICIDIOS'])

    df_codigos_desc = df_codigos_muerte.rename(columns={
        'Código de la CIE-10 tres caracteres': 'COD_3_CAR',
        'Descripción de códigos mortalidad a tres caracteres': 'DESC_3_CAR',
        'Código de la CIE-10 cuatro caracteres': 'COD_4_CAR',
        'Descripcion  de códigos mortalidad a cuatro caracteres': 'DESC_4_CAR'
    })

    desc_4_car_lower = df_codigos_desc['DESC_4_CAR'].astype(str).str.lower()
    cod_3_car_clean = df_codigos_desc['COD_3_CAR'].astype(str).str.strip()

    cond_x95_3car = cod_3_car_clean == 'X95'
    cond_agresion_disparo = (
        desc_4_car_lower.str.contains('agresi', na=False) &
        (
            desc_4_car_lower.str.contains('disparo', na=False) |
            desc_4_car_lower.str.contains('arma de fuego', na=False)
        )
    )

    condicion_final_homicidios = cond_x95_3car | cond_agresion_disparo
    codigos_filtrados_df = df_codigos_desc[condicion_final_homicidios]

    if codigos_filtrados_df.empty:
        codigos_homicidio_identificados = []
    else:
        codigos_homicidio_identificados = codigos_filtrados_df['COD_4_CAR'].astype(str).str.strip().unique().tolist()

    if not codigos_homicidio_identificados:
        return pd.DataFrame(columns=['MUNICIPIO', 'DEPARTAMENTO', 'TOTAL_HOMICIDIOS'])
    
    df_mortalidad['COD_MUERTE_CLEAN'] = df_mortalidad['COD_MUERTE'].astype(str).str.strip()
    df_homicidios = df_mortalidad[df_mortalidad['COD_MUERTE_CLEAN'].isin(codigos_homicidio_identificados)]

    if df_homicidios.empty:
        return pd.DataFrame(columns=['MUNICIPIO', 'DEPARTAMENTO', 'TOTAL_HOMICIDIOS'])

    homicidios_por_ciudad = df_homicidios.groupby(['COD_DEPARTAMENTO', 'COD_MUNICIPIO']).size().reset_index(name='TOTAL_HOMICIDIOS')

    divipola_mpios_unicos = df_divipola[['COD_DEPARTAMENTO', 'COD_MUNICIPIO', 'MUNICIPIO', 'DEPARTAMENTO']].drop_duplicates(subset=['COD_DEPARTAMENTO', 'COD_MUNICIPIO'])
    
    ciudades_data = pd.merge(
        homicidios_por_ciudad,
        divipola_mpios_unicos,
        on=['COD_DEPARTAMENTO', 'COD_MUNICIPIO'],
        how='left'
    )

    ciudades_data.dropna(subset=['MUNICIPIO'], inplace=True)
    
    if ciudades_data.empty:
        return pd.DataFrame(columns=['MUNICIPIO', 'DEPARTAMENTO', 'TOTAL_HOMICIDIOS'])

    top_5_ciudades = ciudades_data.sort_values(by='TOTAL_HOMICIDIOS', ascending=False).head(5)

    return top_5_ciudades[['MUNICIPIO', 'DEPARTAMENTO', 'TOTAL_HOMICIDIOS']]

def preparar_datos_menor_mortalidad(df_mortalidad, df_divipola):
    if df_mortalidad.empty or df_divipola.empty:
        return pd.DataFrame(columns=['MUNICIPIO', 'DEPARTAMENTO', 'TOTAL_MUERTES'])
    muertes_por_ciudad = df_mortalidad.groupby('COD_MUNICIPIO').size().reset_index(name='TOTAL_MUERTES')
    divipola_mpios = df_divipola[['COD_MUNICIPIO', 'MUNICIPIO', 'DEPARTAMENTO']].drop_duplicates(subset=['COD_MUNICIPIO'])
    ciudades_data = pd.merge(muertes_por_ciudad, divipola_mpios, on='COD_MUNICIPIO', how='left')
    ciudades_data.dropna(subset=['MUNICIPIO'], inplace=True)
    bottom_10_ciudades = ciudades_data.sort_values(by='TOTAL_MUERTES', ascending=True).head(10)
    return bottom_10_ciudades[['MUNICIPIO', 'DEPARTAMENTO', 'TOTAL_MUERTES']]

def preparar_datos_causas_muerte(df_mortalidad, df_codigos_muerte):
    if df_mortalidad.empty or df_codigos_muerte.empty:
        return pd.DataFrame(columns=['Código', 'Nombre Causa', 'Total Casos'])

    df_codigos_limpio = df_codigos_muerte.rename(columns={
        'Código de la CIE-10 cuatro caracteres': 'COD_CAUSA_ORIGINAL',
        'Descripcion  de códigos mortalidad a cuatro caracteres': 'NOMBRE_CAUSA_ORIGINAL'
    })
    df_codigos_limpio['COD_CAUSA'] = df_codigos_limpio['COD_CAUSA_ORIGINAL'].astype(str).str.strip()
    df_codigos_limpio['NOMBRE_CAUSA'] = df_codigos_limpio['NOMBRE_CAUSA_ORIGINAL'].astype(str).str.strip()
    df_codigos_limpio = df_codigos_limpio[['COD_CAUSA', 'NOMBRE_CAUSA']].drop_duplicates(subset=['COD_CAUSA'])

    df_mortalidad['COD_MUERTE_CLEAN'] = df_mortalidad['COD_MUERTE'].astype(str).str.strip()
    causas_counts = df_mortalidad.groupby('COD_MUERTE_CLEAN').size().reset_index(name='TOTAL_CASOS')
    
    causas_data = pd.merge(
        causas_counts,
        df_codigos_limpio,
        left_on='COD_MUERTE_CLEAN',
        right_on='COD_CAUSA',
        how='left'
    )
    
    top_10_causas = causas_data.sort_values(by='TOTAL_CASOS', ascending=False).head(10)
    top_10_causas_final = top_10_causas[['COD_MUERTE_CLEAN', 'NOMBRE_CAUSA', 'TOTAL_CASOS']]
    top_10_causas_final = top_10_causas_final.rename(columns={
        'COD_MUERTE_CLEAN': 'Código',
        'NOMBRE_CAUSA': 'Nombre Causa',
        'TOTAL_CASOS': 'Total Casos'
    })
    top_10_causas_final['Nombre Causa'] = top_10_causas_final['Nombre Causa'].fillna('Descripción no encontrada')
    return top_10_causas_final

def preparar_datos_histograma_edad(df_mortalidad):
    if df_mortalidad.empty:
        return pd.DataFrame(columns=['RANGO_EDAD', 'TOTAL_MUERTES'])
    
    columna_edad_a_usar = 'GRUPO_EDAD1'
    bins = list(range(0, 86, 5)) + [float('inf')] 
    labels = [f'{i}-{i+4}' for i in range(0, 85, 5)] + ['85+']
    
    df_mortalidad_copy = df_mortalidad.copy()
    df_mortalidad_copy[columna_edad_a_usar] = pd.to_numeric(df_mortalidad_copy[columna_edad_a_usar], errors='coerce')
    df_mortalidad_copy.dropna(subset=[columna_edad_a_usar], inplace=True) 

    if df_mortalidad_copy.empty:
        return pd.DataFrame({'RANGO_EDAD': labels, 'TOTAL_MUERTES': 0})


    df_mortalidad_copy['RANGO_EDAD'] = pd.cut(
        df_mortalidad_copy[columna_edad_a_usar],
        bins=bins,
        labels=labels,
        right=False,
        include_lowest=True
    )
    distribucion_edad = df_mortalidad_copy.groupby('RANGO_EDAD', observed=False).size().reset_index(name='TOTAL_MUERTES')
    return distribucion_edad

def preparar_datos_sexo_departamento(df_mortalidad, df_divipola):
    if df_mortalidad.empty or df_divipola.empty:
        return pd.DataFrame(columns=['DEPARTAMENTO', 'SEXO_ETIQUETA', 'TOTAL_MUERTES'])
    
    muertes_sexo_dpto = df_mortalidad.groupby(['COD_DEPARTAMENTO', 'SEXO']).size().reset_index(name='TOTAL_MUERTES')
    sexo_map = {1: 'Hombre', 2: 'Mujer', 3: 'Indeterminado'} 
    muertes_sexo_dpto['SEXO_ETIQUETA'] = muertes_sexo_dpto['SEXO'].map(sexo_map).fillna('Desconocido')
    divipola_dptos = df_divipola[['COD_DEPARTAMENTO', 'DEPARTAMENTO']].drop_duplicates(subset=['COD_DEPARTAMENTO'])
    data_apilada = pd.merge(muertes_sexo_dpto, divipola_dptos, on='COD_DEPARTAMENTO', how='left')
    data_apilada['DEPARTAMENTO'] = data_apilada['DEPARTAMENTO'].fillna('Desconocido')
    return data_apilada[['DEPARTAMENTO', 'SEXO_ETIQUETA', 'TOTAL_MUERTES']]

if __name__ == '__main__':
    print(f"Cargando datos desde: {DATA_DIR}")
    
    df_mortalidad_raw = cargar_datos_mortalidad()
    df_codigos_raw = cargar_codigos_muerte()
    df_divipola_raw = cargar_divipola()

    if not df_divipola_raw.empty:
        print("\n--- Verificación de COD_MUNICIPIO para LETICIA en Divipola ---")

        if 'MUNICIPIO' in df_divipola_raw.columns:
            print(df_divipola_raw[df_divipola_raw['MUNICIPIO'].astype(str).str.upper().str.contains('LETICIA', na=False)])
        else:
            print("Advertencia: La columna 'MUNICIPIO' no se encontró en df_divipola_raw.")
    else:
        print("Advertencia: df_divipola_raw está vacío. No se puede verificar el código de Leticia.")


    print("\n--- Verificación de Carga ---")
    print(f"Mortalidad cargada: {not df_mortalidad_raw.empty}, Forma: {df_mortalidad_raw.shape if not df_mortalidad_raw.empty else 'Vacío'}")
    print(f"Códigos de Muerte cargados: {not df_codigos_raw.empty}, Forma: {df_codigos_raw.shape if not df_codigos_raw.empty else 'Vacío'}")
    print(f"Divipola cargada: {not df_divipola_raw.empty}, Forma: {df_divipola_raw.shape if not df_divipola_raw.empty else 'Vacío'}")

    if not df_mortalidad_raw.empty and not df_divipola_raw.empty:
        print("\n--- Probando MAPA ---")
        datos_mapa = preparar_datos_mapa(df_mortalidad_raw, df_divipola_raw)
        if not datos_mapa.empty: print(datos_mapa.head())

    if not df_mortalidad_raw.empty:
        print("\n--- Probando LÍNEA DE TIEMPO ---")
        datos_linea = preparar_datos_linea_tiempo(df_mortalidad_raw)
        if not datos_linea.empty: print(datos_linea)

    if not df_mortalidad_raw.empty and not df_divipola_raw.empty and not df_codigos_raw.empty:
        print("\n--- Probando CIUDADES MÁS VIOLENTAS ---")
        datos_violencia = preparar_datos_ciudades_violentas(df_mortalidad_raw, df_divipola_raw, df_codigos_raw)
        if not datos_violencia.empty: print(datos_violencia)
        else: print("No se generaron datos para ciudades violentas. Revisa los filtros y la lista de códigos.")


    if not df_mortalidad_raw.empty and not df_divipola_raw.empty:
        print("\n--- Probando CIUDADES CON MENOR MORTALIDAD ---")
        datos_menor_m = preparar_datos_menor_mortalidad(df_mortalidad_raw, df_divipola_raw)
        if not datos_menor_m.empty: print(datos_menor_m)

    if not df_mortalidad_raw.empty and not df_codigos_raw.empty:
        print("\n--- Probando PRINCIPALES CAUSAS DE MUERTE ---")
        datos_causas = preparar_datos_causas_muerte(df_mortalidad_raw, df_codigos_raw)
        if not datos_causas.empty: print(datos_causas)

    if not df_mortalidad_raw.empty:
        print("\n--- Probando HISTOGRAMA DE EDAD ---")

        datos_edad = preparar_datos_histograma_edad(df_mortalidad_raw)
        if not datos_edad.empty:
            print(datos_edad)


    if not df_mortalidad_raw.empty and not df_divipola_raw.empty:
        print("\n--- Probando MUERTES POR SEXO Y DEPARTAMENTO ---")
        datos_sexo_dpto = preparar_datos_sexo_departamento(df_mortalidad_raw, df_divipola_raw)
        if not datos_sexo_dpto.empty: print(datos_sexo_dpto.head(10))

def preparar_datos_mapa(df_mortalidad, df_divipola):
    if df_mortalidad.empty or df_divipola.empty:
        return pd.DataFrame(columns=['COD_DEPARTAMENTO', 'DEPARTAMENTO', 'TOTAL_MUERTES', 'COD_DPTO_GEO']) 
    
    muertes_por_dpto = df_mortalidad.groupby('COD_DEPARTAMENTO').size().reset_index(name='TOTAL_MUERTES')
    divipola_dptos = df_divipola[['COD_DEPARTAMENTO', 'DEPARTAMENTO']].drop_duplicates(subset=['COD_DEPARTAMENTO'])
    
    mapa_data = pd.merge(
        muertes_por_dpto,
        divipola_dptos,
        on='COD_DEPARTAMENTO',
        how='left'
    )
    mapa_data['DEPARTAMENTO'] = mapa_data['DEPARTAMENTO'].fillna('Desconocido')
 
    mapa_data['COD_DPTO_GEO'] = mapa_data['COD_DEPARTAMENTO'].astype(str).str.zfill(2)
    
    return mapa_data[['COD_DEPARTAMENTO', 'DEPARTAMENTO', 'TOTAL_MUERTES', 'COD_DPTO_GEO']]