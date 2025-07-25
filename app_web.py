import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
import wikipedia
import folium
from streamlit_folium import st_folium
import os

# Configuración de la página
st.set_page_config(
    page_title="RareEarth Explorer",
    page_icon="🔬",
    layout="wide"
)

# Cargar datos (similar a tu SAMPLE_DATA)
@st.cache_data
def load_data():
    return pd.DataFrame([
        {
            "nombre": "Lantano", "simbolo": "La", "numero_atomico": 57,
            "peso_atomico": 138.90547, "grupo": "Lantánidos",
            "usos": ["Lentes", "Baterías"], "origen": "Minerales monacita",
            "coords": [35.86166, 104.195397], "pais": "China"
        },
        # ... (todos tus otros elementos)
    ])

df = load_data()

# --- Sidebar (Filtros) ---
st.sidebar.title("🔍 Filtros")
nombre_query = st.sidebar.text_input("Buscar por nombre:")
grupo_seleccionado = st.sidebar.selectbox("Filtrar por grupo:", ["Todos"] + list(df['grupo'].unique()))
uso_seleccionado = st.sidebar.selectbox("Filtrar por uso:", ["Todos"] + list(set(uso for sublist in df['usos'] for uso in sublist)))

# Aplicar filtros
filtered_df = df.copy()
if nombre_query:
    filtered_df = filtered_df[filtered_df['nombre'].str.contains(nombre_query, case=False)]
if grupo_seleccionado != "Todos":
    filtered_df = filtered_df[filtered_df['grupo'] == grupo_seleccionado]
if uso_seleccionado != "Todos":
    filtered_df = filtered_df[filtered_df['usos'].apply(lambda x: uso_seleccionado in x)]

# --- Página principal ---
st.title("🔍 Explorador de Elementos de Tierras Raras")
st.write("""
Una herramienta interactiva para explorar las propiedades, usos y distribución geográfica 
de los elementos de tierras raras.
""")

# Mostrar tabla filtrada
st.subheader("📊 Tabla de Elementos")
st.dataframe(
    filtered_df[['nombre', 'simbolo', 'numero_atomico', 'grupo']],
    use_container_width=True,
    height=300
)

# Pestañas
tab1, tab2, tab3 = st.tabs(["📝 Detalles", "🗺️ Mapa", "📚 Wikipedia"])

with tab1:
    if not filtered_df.empty:
        elemento_seleccionado = st.selectbox(
            "Selecciona un elemento:",
            filtered_df['nombre']
        )
        
        elemento = filtered_df[filtered_df['nombre'] == elemento_seleccionado].iloc[0]
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Mostrar imagen desde Wikipedia
            try:
                wiki_page = wikipedia.page(f"{elemento['nombre']} (elemento)")
                img_url = next(img for img in wiki_page.images if img.lower().endswith(('.jpg', '.png')))
                img = Image.open(BytesIO(requests.get(img_url).content))
                st.image(img, caption=elemento['nombre'], width=300)
            except:
                st.warning("No se pudo cargar la imagen desde Wikipedia")
        
        with col2:
            st.markdown(f"""
            ### {elemento['nombre']} ({elemento['simbolo']})
            
            - **Número atómico**: {elemento['numero_atomico']}
            - **Peso atómico**: {elemento['peso_atomico']}
            - **Grupo**: {elemento['grupo']}
            - **Origen**: {elemento['origen']}
            
            #### Usos principales:
            {''.join(f'- {uso}\n' for uso in elemento['usos'])}
            """)

with tab2:
    st.subheader("Distribución Geográfica")
    
    # Crear mapa con Folium
    m = folium.Map(location=[20, 0], zoom_start=2)
    
    for _, row in df.iterrows():
        folium.Marker(
            location=row['coords'],
            popup=f"{row['nombre']} ({row['simbolo']})",
            tooltip=row['pais']
        ).add_to(m)
    
    # Mostrar mapa en Streamlit
    st_folium(m, width=1200, height=600)

with tab3:
    st.subheader("Información desde Wikipedia")
    if not filtered_df.empty:
        elemento = filtered_df.iloc[0]
        try:
            wiki_info = wikipedia.summary(f"{elemento['nombre']} (elemento)")
            st.markdown(wiki_info)
            st.markdown(f"[Leer más en Wikipedia]({wikipedia.page(f'{elemento['nombre']} (elemento)').url})")
        except:
            st.error("No se pudo cargar información desde Wikipedia")

# Ejecutar con: streamlit run app_web.py