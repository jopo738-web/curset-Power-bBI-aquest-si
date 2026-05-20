import os
from datetime import datetime
import requests  # Usaremos esta librería externa para demostrar la instalación

def ejecutar_analisis():
    print("🚀 Iniciando el Analizador Automático en GitHub Actions...")
    
    # 1. Comprobamos la conexión simulando una petición a una API pública
    try:
        response = requests.get("https://api.github.com", timeout=5)
        print(f"📡 Conexión de red en el servidor de GitHub: OK (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ Error de red: {e}")

    # 2. Procesamos unos datos de ejemplo
    productos = [
        {"nombre": "Laptop Pro", "precio": 1200},
        {"nombre": "Teclado Mecánico", "precio": 85},
        {"nombre": "Monitor 4K", "precio": 350}
    ]
    
    print("\n📊 Procesando inventario...")
    total_valor = sum(p["precio"] for p in productos)
    
    # 3. Generamos un reporte físico en el disco del servidor virtual
    fecha_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = f"reporte_{fecha_str}.txt"
    
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(f"=== REPORTE GENERADO AUTOMÁTICAMENTE ===\n")
        f.write(f"Fecha de ejecución: {datetime.now()}\n")
        f.write(f"Total de productos analizados: {len(productos)}\n")
        f.write(f"Valor total del inventario: ${total_valor}\n")
        f.write("========================================\n")
        for p in productos:
            f.write(f"- {p['nombre']}: ${p['precio']}\n")
            
    print(f"📝 ¡Reporte guardado con éxito como '{nombre_archivo}'!")
    print(f"💡 Contenido del reporte:\n")
    
    # Mostrar el contenido en la consola de GitHub Actions para que los alumnos lo vean
    with open(nombre_archivo, "r", encoding="utf-8") as f:
        print(f.read())

if __name__ == "__main__":
    ejecutar_analisis()
