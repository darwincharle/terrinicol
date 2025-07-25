import folium
from folium.plugins import MarkerCluster

def create_map(df):
    """
    Crea un mapa interactivo con los elementos filtrados
    
    Args:
        df: DataFrame con columnas 'nombre', 'simbolo', 'coords', 'pais', 'usos'
    
    Returns:
        Objeto folium.Map
    """
    if df.empty:
        return folium.Map(location=[20, 0], zoom_start=2)
    
    # Crear mapa centrado en los datos
    avg_lat = df['coords'].apply(lambda x: x[0]).mean()
    avg_lon = df['coords'].apply(lambda x: x[1]).mean()
    
    m = folium.Map(
        location=[avg_lat, avg_lon],
        zoom_start=3,
        tiles='cartodbpositron'
    )
    
    # Agrupar marcadores
    marker_cluster = MarkerCluster().add_to(m)
    
    # Añadir cada elemento
    for _, row in df.iterrows():
        popup_content = f"""
        <b>{row['nombre']} ({row['simbolo']})</b><br>
        <i>País:</i> {row['pais']}<br>
        <i>Usos principales:</i> {', '.join(row['usos'][:3])}
        """
        
        folium.Marker(
            location=row['coords'],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=f"{row['nombre']} - {row['pais']}",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(marker_cluster)
    
    return m