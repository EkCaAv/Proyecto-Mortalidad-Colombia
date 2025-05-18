# Proyecto-mortalidad-colombia
# Análisis Interactivo de Mortalidad en Colombia - 2019

**Nombre del Estudiante:** Erika Isabel Caita Avila
**Asignatura:** Aplicaciones 
**Fecha de Entrega:** 18 de mayo de 2025 

---

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Objetivos del Proyecto](#objetivos-del-proyecto)
3. [Tecnologías Utilizadas](#tecnologías-utilizadas)
4. [Desarrollo de la Aplicación Web](#desarrollo-de-la-aplicación-web)
    - [Funcionamiento General](#funcionamiento-general)
    - [Componentes Principales (Visualizaciones)](#componentes-principales-visualizaciones)
5. [Visualización e Interpretación de Datos](#visualización-e-interpretación-de-datos)
    - [Mapa: Distribución de Muertes por Departamento](#mapa-distribución-de-muertes-por-departamento)
    - [Gráfico de Líneas: Muertes por Mes](#gráfico-de-líneas-muertes-por-mes)
    - [Gráfico de Barras: Top 5 Ciudades Más Violentas](#gráfico-de-barras-top-5-ciudades-más-violentas)
    - [Gráfico Circular: Top 10 Ciudades con Menor Mortalidad](#gráfico-circular-top-10-ciudades-con-menor-mortalidad)
    - [Tabla: Principales Causas de Muerte](#tabla-principales-causas-de-muerte)
    - [Histograma: Distribución de Muertes por Edad](#histograma-distribución-de-muertes-por-edad)
    - [Gráfico de Barras Apiladas: Muertes por Sexo y Departamento](#gráfico-de-barras-apiladas-muertes-por-sexo-y-departamento)
6. [Despliegue de la Aplicación](#despliegue-de-la-aplicación)
    - [Plataforma Utilizada](#plataforma-utilizada)
    - [Proceso de Implementación](#proceso-de-implementación)
    - [Enlace a la Aplicación Desplegada](#enlace-a-la-aplicación-desplegada)
7. [Pruebas de Funcionalidad](#pruebas-de-funcionalidad)
8. [Conclusión](#conclusión)
9. [Posibles Mejoras Futuras](#posibles-mejoras-futuras)

---

## 1. Introducción
En el presente proyecto, se ha desarrollado una aplicación web interactiva para el análisis de los datos de mortalidad registrados en Colombia durante el año 2019. Esta herramienta busca transformar datos complejos en representaciones visuales comprensibles, permitiendo la identificación de patrones, tendencias y correlaciones clave. El enfoque se centra en proporcionar una interfaz intuitiva para la exploración de estos datos cruciales de salud pública.

## 2. Objetivos del Proyecto
*   Analizar los patrones de mortalidad en Colombia durante el año 2019.
*   Desarrollar una aplicación web dinámica utilizando Python, Plotly y Dash para la visualización interactiva de los datos.
*   Integrar múltiples informes gráficos que faciliten la interpretación de los datos y permitan una exploración visual intuitiva.
*   Desplegar la aplicación en una plataforma como servicio (PaaS) para asegurar su accesibilidad en línea.
*   Fortalecer competencias en el análisis de datos, desarrollo de aplicaciones web y despliegue en la nube.

## 3. Tecnologías Utilizadas
*   **Lenguaje de Programación:** Python 3.11 
*   **Análisis y Manipulación de Datos:** Pandas
*   **Visualización de Datos:** Plotly Express
*   **Framework de Aplicación Web:** Dash
*   **Componentes de Interfaz:** Dash Bootstrap Components
*   **Servidor WSGI (para despliegue):** Gunicorn
*   **Plataforma de Despliegue (PaaS):** Render
*   **Control de Versiones:** Git y GitHub

Python, junto con Pandas, Plotly y Dash, ofrece un ecosistema robusto y eficiente para este tipo de proyectos. Pandas facilita la carga, limpieza y transformación de los datos. Plotly Express permite la creación rápida de una amplia variedad de gráficos interactivos con código conciso. Dash integra estos gráficos en una aplicación web completamente funcional, permitiendo a los usuarios interactuar con los datos de forma dinámica sin necesidad de conocimientos de desarrollo web frontend complejos. Dash Bootstrap Components agiliza la creación de layouts responsivos y estéticamente agradables.

## 4. Desarrollo de la Aplicación Web

### Funcionamiento General
La aplicación web sigue un flujo de trabajo estándar:
1.  **Carga de Datos:** Los datos de mortalidad (`Anexo1.NoFetal2019_CE_15-03-23.xlsx`), códigos de causas de muerte (`Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx`) y la división político-administrativa de Colombia (`Anexo3.Divipola_CE_15-03-23.xlsx`) se cargan desde archivos Excel. Adicionalmente, se utiliza un archivo GeoJSON (`colombia_departamentos.geojson`) para la representación geográfica del mapa.
2.  **Procesamiento de Datos:** Utilizando Pandas, los datos crudos se limpian, transforman, fusionan y agrupan para generar los conjuntos de datos específicos requeridos por cada visualización. Este procesamiento se centraliza en el módulo `app/data_processing.py`.
3.  **Generación de Visualizaciones:** Con Plotly Express, se crean siete figuras interactivas distintas (mapa, gráficos de barras, líneas, circular, histograma) y una tabla de datos a partir de los DataFrames procesados.
4.  **Construcción del Dashboard:** El framework Dash se utiliza para ensamblar estas visualizaciones en un layout web coherente y navegable, estructurado en filas y columnas para una presentación organizada. Se emplean componentes de Dash Bootstrap para la estructura y el estilo visual. El archivo `app/app.py` contiene la lógica principal del dashboard y la definición del layout.
5.  **Interactividad:** Los gráficos generados por Plotly son inherentemente interactivos, permitiendo al usuario realizar zoom, pan (desplazamiento) y obtener información detallada al pasar el cursor sobre los elementos gráficos (tooltips). La tabla de datos también incluye funcionalidades de filtrado y ordenación nativas.

### Componentes Principales (Visualizaciones)
La aplicación presenta los siguientes elementos visuales, cada uno diseñado para responder a preguntas específicas sobre la mortalidad en Colombia:

#### Mapa: Distribución de Muertes por Departamento
*   **Propósito:** Visualizar geográficamente qué departamentos concentran el mayor y menor número de muertes, utilizando una escala de color para representar la magnitud.
*   **Interacción:** El usuario puede pasar el mouse sobre cada departamento para ver su nombre y el total de muertes. El mapa permite zoom y pan para una exploración detallada.
    ![Mapa de Mortalidad por Departamento](https://raw.githubusercontent.com/EkCaAv/Proyecto-Mortalidad-Colombia/develop/assets/images/mapa_distribucion_departamento.png) 

#### Gráfico de Líneas: Muertes por Mes
*   **Propósito:** Identificar patrones estacionales o tendencias en la mortalidad total a lo largo del año 2019.
*   **Interacción:** Al pasar el mouse sobre los puntos de datos, se muestra el mes y el total de muertes correspondiente.
    ![Gráfico de Líneas de Muertes por Mes](https://raw.githubusercontent.com/EkCaAv/Proyecto-Mortalidad-Colombia/develop/assets/images/total_muertes_mes.png)

#### Gráfico de Barras: Top 5 Ciudades Más Violentas
*   **Propósito:** Destacar las cinco ciudades que registraron el mayor número de homicidios, según los códigos CIE-10 X93, X94 y X95 (agresiones con armas de fuego).
*   **Interacción:** El detalle del total de homicidios y el nombre completo de la ciudad (y su departamento) se visualiza al pasar el mouse sobre cada barra.
    ![Top 5 Ciudades con Más Homicidios](https://raw.githubusercontent.com/EkCaAv/Proyecto-Mortalidad-Colombia/develop/assets/images/top_5_ciudades_homicidios.png)

#### Gráfico Circular: Top 10 Ciudades con Menor Mortalidad
*   **Propósito:** Identificar las diez ciudades con la menor cantidad de defunciones totales registradas en 2019.
*   **Interacción:** Al pasar el cursor sobre cada segmento del gráfico de dona, se revela el nombre de la ciudad, el porcentaje que representa y el número absoluto de muertes.
    ![Top 10 Ciudades con Menor Número de Muertes](https://raw.githubusercontent.com/EkCaAv/Proyecto-Mortalidad-Colombia/develop/assets/images/top_10_ciudades_menor_mortalidad.png)

#### Tabla: Principales Causas de Muerte
*   **Propósito:** Presentar de forma clara y concisa las diez causas de muerte más frecuentes en Colombia durante 2019, incluyendo su código CIE-10 y el total de casos.
*   **Interacción:** La tabla permite al usuario ordenar los datos por cualquiera de sus columnas y aplicar filtros nativos para buscar causas específicas.
    ![Principales Causas de Muerte](https://raw.githubusercontent.com/EkCaAv/Proyecto-Mortalidad-Colombia/develop/assets/images/principales_causas_muerte.png) 

#### Histograma: Distribución de Muertes por Edad
*   **Propósito:** Analizar la distribución de las defunciones según rangos de edad quinquenales, permitiendo identificar los grupos etarios con mayor incidencia de mortalidad dentro del conjunto de datos disponible.
*   **Interacción:** Al pasar el mouse sobre cada barra, se muestra el rango de edad específico y el total de muertes correspondiente.
    ![Distribución de Muertes por Rango de Edad](https://raw.githubusercontent.com/EkCaAv/Proyecto-Mortalidad-Colombia/develop/assets/images/distribucion_muertes_edad.png)

#### Gráfico de Barras Apiladas: Muertes por Sexo y Departamento
*   **Propósito:** Comparar el total de muertes entre hombres y mujeres dentro de cada departamento, así como la proporción de muertes con sexo indeterminado. Permite analizar diferencias significativas entre géneros a nivel regional.
*   **Interacción:** Al pasar el cursor sobre las secciones de cada barra apilada, se muestra el departamento, el sexo y el total de muertes para esa subcategoría.
    ![Total Muertes por Sexo en Cada Departamento](https://raw.githubusercontent.com/EkCaAv/Proyecto-Mortalidad-Colombia/develop/assets/images/total_muertes_sexo_departamento.png)

---

## 5. Visualización e Interpretación de Datos

### Hallazgos Relevantes del Mapa Departamental:
El mapa de coropletas evidencia que la mortalidad en Colombia durante 2019 no es homogénea. Departamentos como **Bogotá D.C. (38,760 muertes)** y **Antioquia (34,473 muertes)** concentran el mayor número de defunciones, lo cual es esperable dada su alta densidad poblacional y por ser los principales centros urbanos del país. Les siguen en magnitud Valle del Cauca y Atlántico. En contraste, departamentos de la región amazónica y Orinoquía como Vaupés, Guainía y Amazonas presentan las cifras más bajas, probablemente debido a una menor población y, potencialmente, a diferencias en el acceso y registro de datos.

### Tendencias en Muertes por Mes:
El gráfico de líneas del total de muertes por mes revela una fluctuación a lo largo de 2019. Se identifican picos de mortalidad en **julio (21,372 muertes)** y **diciembre (21,678 muertes)**, mientras que el mes con menor número de defunciones fue **febrero (17,974 muertes)**. Estas variaciones podrían estar influenciadas por factores estacionales (como enfermedades respiratorias en periodos fríos o lluviosos), dinámicas sociales particulares en ciertos meses, o incluso artefactos en los procesos de reporte.

### Análisis de Ciudades Violentas:
Las cinco ciudades con mayor número de homicidios, definidos por agresiones con armas de fuego (códigos CIE-10 X93-X95), en 2019 fueron:
1.  **Cali (Valle del Cauca):** 971 homicidios
2.  **Bogotá, D.C.:** 613 homicidios
3.  **Medellín (Antioquia):** 429 homicidios
4.  **Barranquilla (Atlántico D.E.):** 260 homicidios
5.  **Cúcuta (Norte de Santander):** 206 homicidios
Estos datos subrayan la concentración de este tipo de violencia en grandes centros urbanos, indicando áreas prioritarias para intervenciones de seguridad y prevención. La correcta identificación de municipios mediante la combinación de código de departamento y municipio fue crucial para obtener cifras precisas y evitar la sobreestimación observada inicialmente en algunos municipios capitales.

### Ciudades con Menor Mortalidad:
Las diez ciudades con el menor número total de defunciones en 2019 son principalmente municipios pequeños, varios con menos de 5 muertes registradas en todo el año, como **Taraipa (Vaupés), Bituima (Cundinamarca), y Mapiripana (Guainía)**, cada una con 1 defunción. Esto refleja la gran diversidad demográfica y territorial de Colombia.

### Principales Causas de Muerte:
La tabla de las diez principales causas de muerte muestra un predominio de enfermedades no transmisibles. El **Infarto agudo del miocardio, sin otra especificación (I219)** encabeza la lista con 35,088 casos. Le siguen la **Enfermedad pulmonar obstructiva crónica, no especificada (J449)** con 7,210 casos y la **Enfermedad pulmonar obstructiva crónica con infección aguda de las vías respiratorias inferiores (J440)** con 6,445 casos. La **Neumonía, no especificada (J189)** también es significativa (5,798 casos). Varios **tumores malignos** (estómago, bronquios/pulmón, mama) se encuentran entre las principales causas. Es relevante notar que la **Agresión con disparo de otras armas de fuego, y las no especificadas (X954)** aparece con 4,396 casos, indicando el impacto de la violencia. Los códigos **C61 (Tumor maligno de la próstata)** e **I10 (Hipertensión esencial primaria)** aparecen con "Descripción no encontrada", lo que indica que estos códigos no estaban presentes o no tenían una descripción asociada en el archivo de referencia de códigos (`Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx`) proporcionado para la actividad.

### Distribución Etaria de la Mortalidad:
**Es fundamental interpretar este histograma reconociendo una limitación significativa en los datos fuente proporcionados para la actividad: la columna `GRUPO_EDAD1` del archivo `Anexo1.NoFetal2019_CE_15-03-23.xlsx` solo contiene valores de edad hasta los 29 años.**
Considerando esta restricción, el gráfico muestra que la mayor cantidad de muertes dentro de este subconjunto de datos (0-29 años) se concentra en el rango de **20-24 años (115,453 muertes)**, seguido por el rango de **25-29 años (56,084 muertes)** y luego **15-19 años (40,740 muertes)**. Los grupos de **10-14 años (22,415 muertes)**, **5-9 años (5,143 muertes)** y **0-4 años (4,520 muertes)** muestran cifras menores en comparación. La ausencia total de barras para los rangos de edad de 30 años en adelante es una consecuencia directa de la limitación mencionada en los datos de entrada y no implica que no hubo muertes en esos grupos etarios en Colombia durante 2019.

### Mortalidad por Sexo y Departamento:
El gráfico de barras apiladas evidencia que, en la mayoría de los departamentos de Colombia, se registra un **mayor número de muertes en hombres que en mujeres** durante 2019. Esta tendencia es particularmente visible en departamentos con alta mortalidad general como **Bogotá D.C.** y **Antioquia**. La categoría de "sexo indeterminado" representa una fracción muy pequeña del total de defunciones en todos los departamentos, lo cual es consistente con la calidad esperada en el registro de esta variable. Estas diferencias sugieren la relevancia de considerar factores de riesgo y acceso a la salud diferenciados por sexo.

## 6. Despliegue de la Aplicación

### Plataforma Utilizada
La aplicación web fue desplegada utilizando **Render**.

### Proceso de Implementación
El proceso de despliegue siguió los siguientes pasos:
1.  **Preparación del Proyecto Local:** Se finalizó el desarrollo de la aplicación Dash (`app/app.py` y `app/data_processing.py`). Se generó el archivo `requirements.txt` y se limpió para incluir solo las dependencias esenciales. Se creó el archivo `Procfile` con el comando `web: gunicorn app.app:server`. Se verificó que todos los archivos de datos (`.xlsx`, `.geojson`) estuvieran correctamente referenciados.
2.  **Control de Versiones:** Se utilizó Git para el control de versiones y se subió el proyecto a un repositorio en GitHub. Se configuró un archivo `.gitignore` para excluir el entorno virtual y archivos de caché.
3.  **Configuración en Render:** Se creó una cuenta en Render y se conectó el repositorio de GitHub. Se configuró un nuevo "Web Service" especificando:
    *   **Nombre del servicio:** `proyecto-mortalidad-colombia` 
    *   **Región:** US East (N. Virginia) 
    *   **Rama a desplegar:** `main`
    *   **Runtime:** Python 3
    *   **Build Command:** `pip install -r requirements.txt`
    *   **Start Command:** `gunicorn app.app:server`
    *   **Plan:** Free Tier
4.  **Monitoreo y Solución de Problemas:** Se revisaron los logs de despliegue en Render. Un problema inicial fue un `ModuleNotFoundError` para `data_processing`, el cual se solucionó ajustando la importación en `app.py` a una importación relativa (`from .data_processing import ...`).
5.  **Verificación:** Se accedió a la URL pública proporcionada por Render para confirmar el correcto funcionamiento de la aplicación en línea.

### Enlace a la Aplicación Desplegada
https://proyecto-mortalidad-colombia.onrender.com/

## 7. Pruebas de Funcionalidad
*   Se verificó la correcta carga de datos y la visualización de los siete elementos gráficos especificados.
*   Se probó la interactividad básica de los gráficos (tooltips al pasar el mouse, zoom y pan en el mapa).
*   La tabla de causas de muerte demostró funcionar correctamente con sus opciones de ordenación y filtrado nativas.
*   Se confirmó que el layout de la aplicación es responsivo gracias al uso de Dash Bootstrap Components.
*   La aplicación se carga y funciona correctamente a través de la URL pública de despliegue en Render.
*   La aplicación desplegada en render por ser de un plan gratuito, los requisitos 0.1 CPU y 512 MB puede demorar hasta 3 minutos en construir la aplicación y mostrar el dashboard.

## 8. Conclusión
El desarrollo de esta aplicación web interactiva ha permitido realizar un análisis visual de los datos de mortalidad en Colombia para el año 2019. Las herramientas Python, Pandas, Plotly y Dash han demostrado ser un conjunto potente y flexible para la transformación de datos en insights visuales y accesibles.

Los principales hallazgos incluyen la concentración de la mortalidad en departamentos densamente poblados como Bogotá D.C. y Antioquia, picos de mortalidad en los meses de julio y diciembre, y la identificación de enfermedades cardiovasculares y pulmonares, así como tumores malignos y agresiones, entre las principales causas de defunción. Es importante destacar la limitación encontrada en los datos de edad, que solo abarcan hasta los 29 años, lo que impide un análisis completo de la distribución etaria de la mortalidad.

También se hizo un tratamiento especial a alguno de los archivos .xlsx, ya que por formatos de imagenes y espacios afectaba la lectura de la data, se solucionó eliminando estos formatos y dejando la data en limpio.

El proceso de desarrollo, desde el procesamiento de datos hasta el despliegue en una plataforma PaaS (Platform as a software) como Render, ha sido una experiencia de aprendizaje valiosa, reforzando competencias en el ciclo de vida completo de una aplicación de análisis de datos.

## 9. Posibles Mejoras Futuras
*   **Incorporación de Datos de Edad Completos:** Obtener y procesar un conjunto de datos que incluya todos los rangos de edad para un análisis de mortalidad más representativo.
*   **Filtros Interactivos Avanzados:** Implementar Dash Callbacks para permitir a los usuarios filtrar los datos dinámicamente por departamento, rango de edad, sexo o causa de muerte, actualizando los gráficos en consecuencia.
*   **Cálculo de Tasas de Mortalidad:** Integrar datos poblacionales para calcular y visualizar tasas de mortalidad (por 100,000 habitantes), lo que permitiría comparaciones más estandarizadas entre regiones con diferente tamaño poblacional.
*   **Análisis de Tendencias Temporales:** Incluir datos de años anteriores o posteriores para analizar la evolución de los patrones de mortalidad.
*   **Detalle a Nivel Municipal en Mapas:** Explorar la visualización de datos a nivel municipal en el mapa de coropletas, lo que requeriría un GeoJSON de municipios y un procesamiento de datos más granular.
*   **Personalización Avanzada de Estilos:** Mejorar la estética y la experiencia de usuario con CSS personalizado y un diseño de interfaz más elaborado.