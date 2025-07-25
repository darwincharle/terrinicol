import os
import requests
from PIL import Image

ELEMENTS = ['lantano', 'cerio', 'neodimio', 'iterbio']  # Añade todos los elementos

def download_images():
    os.makedirs('assets/images/elements', exist_ok=True)
    
    for element in ELEMENTS:
        url = f'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Electron_shell_057_Lanthanum.svg/300px-Electron_shell_057_Lanthanum.svg.png'.replace('Lanthanum', element.capitalize())
        try:
            response = requests.get(url, timeout=10)
            with open(f'assets/images/elements/{element}.png', 'wb') as f:
                f.write(response.content)
            print(f'Descargada imagen para {element}')
        except:
            print(f'Error al descargar {element}')

if __name__ == '__main__':
    download_images()