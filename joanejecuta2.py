import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def extraer_titulares():
    print("🚀 [CI/CD] Iniciando Extractor de Titulares en la Nube...")
    url = "https://www.marca.com/"
    
    # Añadimos un User-Agent para simular un navegador real y evitar bloqueos
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        print(f"📡 Conectando con {url}...")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Conexión exitosa. Procesando el HTML...")
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscamos los elementos que contienen los titulares en Marca (suelen usar etiquetas h2 o h3 con clases de titulares)
            # Nota: Usamos selectores genéricos comunes de su estructura para asegurar capturar contenido
            titulares = soup.select('header h2, .ue-c-cover-content__headline, h2.ue-c-cover-content__headline-custom')
            
            print(f"\n📰 TITULARES DESTACADOS DE HOY ({datetime.now().strftime('%d/%m/%Y %H:%M')})")
            print("=" * 60)
            
            contador = 0
            for t in titulares:
                texto = t.get_text().strip()
                # Filtramos textos vacíos o demasiado cortos
                if texto and len(texto) > 10:
                    contador += 1
                    print(f"{contador}. 🔥 {texto}")
                
                # Limitamos a los 15 primeros para no saturar la consola
                if contador >= 15:
                    break
                    
            if contador == 0:
                print("⚠️ No se pudieron extraer titulares estructurados. Es posible que el diseño web haya cambiado.")
            print("=" * 60)
            
        else:
            print(f"❌ Error al acceder a la web. Código de estado: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ocurrió un error durante el scraping: {e}")

if __name__ == "__main__":
    extraer_titulares()
