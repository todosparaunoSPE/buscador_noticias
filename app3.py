# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 14:12:22 2024

@author: jperezr
"""

import streamlit as st
import requests
import datetime

# Función para obtener noticias usando Google Custom Search API
def get_google_search_results(query, api_key, cx):
    # Añadir dateRestrict para limitar los resultados a los últimos 12 meses (o al periodo que desees)
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cx}&dateRestrict=d1"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data['items']
    else:
        st.error(f"Error al obtener resultados de búsqueda: {response.status_code}")
        return []

# Función para extraer el año de un snippet o link
def extract_year_from_snippet(snippet):
    # Intentar encontrar un año en el snippet
    for year in range(2020, 2030):  # Buscar años de 2020 a 2029
        if str(year) in snippet:
            return year
    return None

# Función para mostrar resultados
def show_search_results(results):
    # Extraer y ordenar los resultados por año
    results_with_year = []
    for result in results:
        year = extract_year_from_snippet(result['snippet'])
        if year:
            results_with_year.append((result, year))
    
    # Ordenar por año en orden descendente
    results_with_year.sort(key=lambda x: x[1], reverse=True)
    
    if results_with_year:
        for result, year in results_with_year:
            st.subheader(f"{result['title']} ({year})")
            st.write(result['snippet'])
            st.write(f"[Leer más]({result['link']})")
            st.write("---")
    else:
        st.write("No se encontraron resultados recientes.")

# Añadir una sección de ayuda en el sidebar
with st.sidebar:
    st.header("Ayuda")
    st.write("""
    **¿Cómo usar esta aplicación?**
    1. Ingresa una palabra clave en el campo de búsqueda.
    2. Haz clic en el botón **Buscar Noticias**.
    3. Los resultados mostrarán noticias recientes sobre el tema ingresado.
    4. Haz clic en los enlaces para leer más detalles.
    
    **Nota:** Esta aplicación utiliza la API de Google Custom Search para buscar de igual manera noticias relacionadas con PensionISSSTE.
    """)
    
    
    # Agregar nombre y copyright en la barra lateral
    st.sidebar.write("Desarrollado por Javier Horacio Pérez Ricárdez")
    st.sidebar.write("© 2024 Todos los derechos reservados.")

# Título y explicación
st.title("Buscador de Noticias de PensionISSSTE")
st.write("Este es un buscador utilizando Google Custom Search API para encontrar noticias.")

# Obtener el año actual
current_date = datetime.datetime.now()
current_year = current_date.year

# Consulta para buscar solo noticias de 2024
query = f"PensionISSSTE 2024"

# Ingresar clave de API y el ID de motor de búsqueda (CSE)
api_key = "AIzaSyDxJEiJO435bWvXHITB05ApX-zLcoSdcSw"  # Sustituye con tu API Key
cx = "476d97aefc5e54cac"  # Tu ID de motor de búsqueda

# Campo de búsqueda con la consulta predeterminada que incluye 2024
query_input = st.text_input("Buscar noticias", query)

# Botón para iniciar la búsqueda
if st.button("Buscar Noticias"):
    if query_input:
        # Obtener los resultados de búsqueda de Google
        results = get_google_search_results(query_input, api_key, cx)
        show_search_results(results)
    else:
        st.warning("Por favor ingresa una palabra clave para buscar.")
        
        
        
        