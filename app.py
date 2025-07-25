import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import plotly.express as px
import wikipedia
from modules.data_manager import load_data, filter_data
from modules.map_visualization import create_map
from modules.wiki_integration import get_wiki_content, get_wiki_image
from modules.quiz_engine import show_quiz

# Configuración de página (DEBE SER LO PRIMERO EN EL SCRIPT)
st.set_page_config(
    page_title="RareEarth Explorer Pro",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar estilos CSS personalizados
def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Cargar datos con caché
@st.cache_data
def load_app_data():
    return load_data()

df = load_app_data()

# --- Sidebar Avanzado ---
with st.sidebar:
    st.title("🔍 Filtros Avanzados")
    
    # Búsqueda por texto
    search_term = st.text_input("Buscar por nombre o símbolo:")
    
    # Filtros múltiples
    col1, col2 = st.columns(2)
    with col1:
        group_filter = st.multiselect(
            "Grupo químico",
            options=sorted(df['grupo'].unique()),
            default=[]
        )
    with col2:
        country_filter = st.multiselect(
            "País de origen",
            options=sorted(df['pais'].unique()),
            default=[]
        )
    
    # Filtro por usos con selección múltiple
    all_uses = sorted(list(set(uso for sublist in df['usos'] for uso in sublist)))
    uses_filter = st.multiselect(
        "Aplicaciones principales",
        options=all_uses,
        default=[]
    )
    
    # Filtro por propiedades físicas
    with st.expander("⚙️ Propiedades físicas"):
        density_range = st.slider(
            "Densidad (g/cm³)",
            min_value=float(df['densidad'].min()),
            max_value=float(df['densidad'].max()),
            value=(float(df['densidad'].min()), float(df['densidad'].max()))
        )

# Aplicar filtros
filtered_df = filter_data(
    df,
    search_term,
    group_filter,
    country_filter,
    uses_filter,
    density_range
)

# --- Main UI ---
st.title("🧪 RareEarth Explorer Pro")
st.markdown("""
<div class="header-subtitle">
Una plataforma interactiva para explorar elementos de tierras raras basada en principios de diseño centrado en el usuario
</div>
""", unsafe_allow_html=True)

# Barra de pestañas principal
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dashboard", 
    "🗺️ Mapa Global", 
    "📚 Enciclopedia", 
    "🧠 Cuestionario"
])

with tab1:
    # Métricas resumen
    st.subheader("Resumen Estadístico")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Elementos filtrados", len(filtered_df))
    with col2:
        st.metric("Grupos representados", filtered_df['grupo'].nunique())
    with col3:
        st.metric("Países con reservas", filtered_df['pais'].nunique())
    
    # Gráficos interactivos
    st.subheader("Distribución de Elementos")
    chart_type = st.radio(
        "Tipo de visualización:",
        ["Barras", "Pie"],
        horizontal=True,
        key="chart_type"
    )
    
    if chart_type == "Barras":
        st.bar_chart(filtered_df['grupo'].value_counts())
    else:
        fig = px.pie(
            filtered_df,
            names='grupo',
            title='Distribución por grupo químico',
            hole=0.3
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Mapa interactivo mejorado
    st.subheader("Distribución Geográfica")
    with st.spinner("Cargando mapa interactivo..."):
        if not filtered_df.empty:
            map_obj = create_map(filtered_df)
            st_folium(map_obj, width=1200, height=600)
        else:
            st.warning("No hay datos para mostrar en el mapa. Ajusta los filtros.")
    
    # Análisis geográfico
    st.write("#### Concentración por país")
    if not filtered_df.empty:
        country_stats = filtered_df['pais'].value_counts().reset_index()
        st.dataframe(
            country_stats.rename(columns={'count': 'Número de elementos'}),
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("No hay datos geográficos para mostrar")

with tab3:
    # Vista detallada con Wikipedia
    if not filtered_df.empty:
        selected_element = st.selectbox(
            "Selecciona un elemento para investigación detallada:",
            filtered_df['nombre'],
            key="element_selector"
        )
        
        element_data = filtered_df[filtered_df['nombre'] == selected_element].iloc[0]
        
        # Diseño en columnas
        col_img, col_data = st.columns([1, 2])
        
        with col_img:
            # Imagen con caché y fallback
            img = get_wiki_image(selected_element)
            st.image(
                img, 
                caption=f"Imagen de {selected_element}",
                use_column_width=True
            )
            st.caption(f"Símbolo: {element_data['simbolo']} | Número atómico: {element_data['numero_atomico']}")
        
        with col_data:
            # Información técnica
            st.markdown(f"""
            ### Propiedades Clave
            - **Grupo**: {element_data['grupo']}
            - **Peso atómico**: {element_data['peso_atomico']}
            - **Densidad**: {element_data['densidad']} g/cm³
            - **Punto de fusión**: {element_data['punto_fusion']} °C
            - **Principales países productores**: {', '.join(element_data['ubicaciones']) if 'ubicaciones' in element_data else 'Datos no disponibles'}
            
            ### Aplicaciones Industriales
            {''.join(f'- {use}\n' for use in element_data['usos'])}
            """)
            
            # Wikipedia integration with loading state
            with st.expander("📖 Información científica detallada (Wikipedia)"):
                with st.spinner("Cargando contenido científico..."):
                    try:
                        wiki_content = get_wiki_content(selected_element)
                        st.markdown(wiki_content[:1500] + "...")  # Limit preview
                        st.markdown(f"[Leer más en Wikipedia]({wikipedia.page(selected_element + ' (elemento)').url})")
                    except:
                        st.error("No se pudo cargar la información de Wikipedia")
    else:
        st.warning("No hay elementos seleccionados. Ajusta los filtros.")

with tab4:
    # Sistema de cuestionarios interactivo
    show_quiz(filtered_df)

# --- Elementos de diseño profesional ---
st.markdown("""
<style>
/* Animaciones sutiles */
.stApp {
    animation: fadeIn 0.5s ease-in;
}

/* Mejoras de usabilidad */
[data-testid="stExpander"] .st-emotion-cache-1q7spjk {
    transition: all 0.3s ease;
}
[data-testid="stExpander"] .st-emotion-cache-1q7spjk:hover {
    background-color: #f0f2f6;
}

/* Diseño responsive */
@media (max-width: 768px) {
    .st-emotion-cache-1v0mbdj {
        width: 100% !important;
    }
    .st-emotion-cache-1r6slb0 {
        padding: 1rem 0.5rem !important;
    }
}
</style>
""", unsafe_allow_html=True)