import os
import json
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

TXT_FILE = os.path.join(DATA_DIR, 'datos.txt')
JSON_FILE = os.path.join(DATA_DIR, 'datos.json')
CSV_FILE = os.path.join(DATA_DIR, 'datos.csv')

def sincronizar_respaldos(lista_productos):
    """Sobrescribe los archivos con el estado actual exacto de la base de datos"""
    
    # 1. TXT (Modo 'w' para sobrescribir)
    with open(TXT_FILE, 'w', encoding='utf-8') as f:
        for p in lista_productos:
            # Puedes ajustar qué datos quieres en el TXT
            f.write(f"ID:{p['id']} | {p['nombre']} | Cantidad: {p['cantidad']} | Precio: ${p['precio']}\n")
            
    # 2. JSON (Modo 'w' para sobrescribir)
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(lista_productos, f, indent=4)
        
    # 3. CSV (Modo 'w' para sobrescribir)
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        if len(lista_productos) > 0:
            writer = csv.DictWriter(f, fieldnames=lista_productos[0].keys())
            writer.writeheader()
            writer.writerows(lista_productos)
        else:
            # Si se eliminaron todos los productos, vaciamos el archivo
            f.write("")

def leer_archivos():
    # Leer TXT
    datos_txt = []
    if os.path.exists(TXT_FILE):
        with open(TXT_FILE, 'r', encoding='utf-8') as f:
            datos_txt = f.readlines()
            
    # Leer JSON
    datos_json = []
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            try:
                datos_json = json.load(f)
            except json.JSONDecodeError:
                pass
                
    # Leer CSV
    datos_csv = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            datos_csv = list(reader)
            
    return {'txt': datos_txt, 'json': datos_json, 'csv': datos_csv}