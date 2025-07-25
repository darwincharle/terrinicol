import pandas as pd
import numpy as np
from typing import Dict, List

# Datos completos de elementos de tierras raras
def load_data() -> pd.DataFrame:
    """Carga el dataset completo de elementos de tierras raras con todas las propiedades necesarias"""
    elements = [
        {
            "nombre": "Lantano",
            "simbolo": "La",
            "numero_atomico": 57,
            "peso_atomico": 138.90547,
            "grupo": "Lantánidos",
            "densidad": 6.15,
            "punto_fusion": 920,
            "punto_ebullicion": 3464,
            "configuracion_electronica": "[Xe] 5d¹ 6s²",
            "electronegatividad": 1.10,
            "usos": ["Lentes de cámaras", "Baterías de vehículos eléctricos", "Catalizadores"],
            "origen": "Minerales monacita y bastnasita",
            "coords": [35.86166, 104.195397],  # Latitud, Longitud
            "pais": "China",
            "ubicaciones": ["China", "Australia", "Estados Unidos"],
            "descripcion": "El lantano es un metal blando, maleable y dúctil que se oxida rápidamente en aire."
        },
        {
            "nombre": "Cerio",
            "simbolo": "Ce",
            "numero_atomico": 58,
            "peso_atomico": 140.116,
            "grupo": "Lantánidos",
            "densidad": 6.77,
            "punto_fusion": 795,
            "punto_ebullicion": 3443,
            "configuracion_electronica": "[Xe] 4f¹ 5d¹ 6s²",
            "electronegatividad": 1.12,
            "usos": ["Pulido de vidrios", "Convertidores catalíticos", "Aleaciones de aluminio"],
            "origen": "Minerales monacita y bastnasita",
            "coords": [35.86166, 104.195397],  # Latitud, Longitud
            "pais": "China",
            "ubicaciones": ["China", "India", "Brasil"],
            "descripcion": "El cerio es el más abundante de los elementos de tierras raras."
        },
        {
            "nombre": "Praseodimio",
            "simbolo": "Pr",
            "numero_atomico": 59,
            "peso_atomico": 140.90766,
            "grupo": "Lantánidos",
            "densidad": 6.77,
            "punto_fusion": 935,
            "punto_ebullicion": 3127,
            "configuracion_electronica": "[Xe] 4f³ 6s²",
            "electronegatividad": 1.13,
            "usos": ["Imanes permanentes", "Aleaciones para motores", "Colorantes cerámicos"],
            "origen": "Minerales monacita",
            "coords": [35.86166, 104.195397],  # Latitud, Longitud
            "pais": "China",
            "ubicaciones": ["China", "Australia"],
            "descripcion": "Metal blando de color plateado que desarrolla una capa de óxido verde cuando se expone al aire."
        },
        # ... (Agrega aquí los demás elementos)
        {
            "nombre": "Itrio",
            "simbolo": "Y",
            "numero_atomico": 39,
            "peso_atomico": 88.90584,
            "grupo": "Metales de transición",
            "densidad": 4.47,
            "punto_fusion": 1526,
            "punto_ebullicion": 3336,
            "configuracion_electronica": "[Kr] 4d¹ 5s²",
            "electronegatividad": 1.22,
            "usos": ["Fósforos para LEDs", "Superconductores", "Tratamiento de cáncer"],
            "origen": "Minerales xenotima",
            "coords": [35.86166, 104.195397],  # Latitud, Longitud
            "pais": "China",
            "ubicaciones": ["China", "Rusia", "Australia"],
            "descripcion": "Aunque no es un lantánido, se clasifica como tierra rara por sus propiedades similares."
        }
    ]
    
    # Convertir a DataFrame con tipos de datos optimizados
    df = pd.DataFrame(elements)
    
    # Asegurar columnas críticas
    required_columns = {
        'usos': [],
        'ubicaciones': [],
        'descripcion': "Información no disponible",
        'densidad': 0.0,
        'punto_fusion': 0,
        'punto_ebullicion': 0
    }
    
    for col, default in required_columns.items():
        if col not in df.columns:
            df[col] = default
    
    return df

def filter_data(df: pd.DataFrame, search_term: str = None, groups: List[str] = None, 
                countries: List[str] = None, uses: List[str] = None, 
                density_range: tuple = (0, 10)) -> pd.DataFrame:
    """
    Filtra el dataframe según múltiples criterios
    
    Args:
        df: DataFrame con los datos
        search_term: Texto para buscar en nombre/símbolo
        groups: Lista de grupos químicos a filtrar
        countries: Lista de países a filtrar
        uses: Lista de aplicaciones a filtrar
        density_range: Tupla con (min, max) de densidad
    
    Returns:
        DataFrame filtrado
    """
    filtered = df.copy()
    
    # Búsqueda por texto
    if search_term:
        search_term = search_term.lower()
        filtered = filtered[
            filtered['nombre'].str.lower().str.contains(search_term) |
            filtered['simbolo'].str.lower().str.contains(search_term)
        ]
    
    # Filtros por listas
    if groups:
        filtered = filtered[filtered['grupo'].isin(groups)]
    
    if countries:
        filtered = filtered[filtered['pais'].isin(countries)]
    
    if uses:
        filtered = filtered[filtered['usos'].apply(
            lambda x: any(use.lower() in [u.lower() for u in x] for use in uses)
        )]
    
    # Filtro por rango de densidad
    filtered = filtered[
        (filtered['densidad'] >= density_range[0]) & 
        (filtered['densidad'] <= density_range[1])
    ]
    
    return filtered.reset_index(drop=True)

def get_usage_distribution(df: pd.DataFrame) -> Dict[str, int]:
    """Calcula la distribución de usos principales"""
    usage_counts = {}
    for uses in df['usos']:
        for use in uses:
            usage_counts[use] = usage_counts.get(use, 0) + 1
    return dict(sorted(usage_counts.items(), key=lambda item: item[1], reverse=True))

def get_country_distribution(df: pd.DataFrame) -> Dict[str, int]:
    """Calcula la distribución por país de origen"""
    return df['pais'].value_counts().to_dict()

# Pruebas de funcionamiento
if __name__ == "__main__":
    df = load_data()
    print(f"Elementos cargados: {len(df)}")
    print("\nMuestra de datos:")
    print(df[['nombre', 'simbolo', 'grupo', 'pais']].head())
    
    print("\nDistribución de usos:")
    print(get_usage_distribution(df))
    
    print("\nEjemplo de filtrado:")
    filtered = filter_data(
        df, 
        search_term="la",
        groups=["Lantánidos"],
        density_range=(6, 7)
    )
    print(filtered[['nombre', 'simbolo', 'densidad']])