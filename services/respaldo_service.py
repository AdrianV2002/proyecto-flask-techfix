import os
import json
import csv

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
txt_file = os.path.join(basedir, 'respaldo.txt')
json_file = os.path.join(basedir, 'respaldo.json')
csv_file = os.path.join(basedir, 'respaldo.csv')

class RespaldoService:
    @staticmethod
    def sincronizar_respaldos(lista_dicts):
        # Guardar en TXT
        with open(txt_file, 'w', encoding='utf-8') as f:
            for p in lista_dicts:
                f.write(f"{p['id']},{p['nombre']},{p['cantidad']},{p['precio']}\n")
        
        # Guardar en JSON
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(lista_dicts, f, indent=4)
            
        # Guardar en CSV
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            if lista_dicts:
                writer = csv.DictWriter(f, fieldnames=lista_dicts[0].keys())
                writer.writeheader()
                writer.writerows(lista_dicts)

    @staticmethod
    def leer_archivos():
        data = {'txt': [], 'json': [], 'csv': []}
        try:
            if os.path.exists(txt_file):
                with open(txt_file, 'r', encoding='utf-8') as f:
                    data['txt'] = f.readlines()
            if os.path.exists(json_file):
                with open(json_file, 'r', encoding='utf-8') as f:
                    data['json'] = json.load(f)
            if os.path.exists(csv_file):
                with open(csv_file, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    data['csv'] = list(reader)
        except Exception:
            pass
        return data