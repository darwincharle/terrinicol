import folium
from folium.plugins import MarkerCluster
from modules.data_manager import get_country_distribution

country_data = get_country_distribution(filtered_df)

def create_map(df):
    m = folium.Map(location=[20, 0], zoom_start=2, tiles='cartodbpositron')
    marker_cluster = MarkerCluster().add_to(m)
    
    for _, row in df.iterrows():
        popup_content = f"""
        <b>{row['nombre']}</b> ({row['simbolo']})<br>
        <i>Grupo:</i> {row['grupo']}<br>
        <i>Usos:</i> {', '.join(row['usos'][:3])}
        """
        
        folium.Marker(
            location=row['coords'],
            popup=popup_content,
            tooltip=f"Click para detalles",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(marker_cluster)
    
    return m