import sys
import json
import requests
import os
import pandas as pd
import json


def post_completion(file_path):
    try:
        # Validar que el archivo existe
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo no existe: {file_path}")

        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(
                'http://127.0.0.1:5000/predict',
                files=files
            )
        response.raise_for_status()

        data = response.json()

        # Leer el CSV (asegúrate de ajustar la ruta al archivo CSV correcto)
        df = pd.read_csv('./diccionario/recetas.csv', encoding='ISO-8859-1')  # Cambia esto a la ruta de tu archivo CSV

        # Filtrar el DataFrame según el valor de prediction
        result = df[df['clase'] == data['prediction']]

        index = 0

        resultado = (
            "La Clase: " + str(int(result['clase'].values[index])) +
            " Es el Plato: " + result['plato'].values[index] +
            " Contiene estos posibles ingredientes: " + result['receta'].values[index] +
            " Ingredientes alergenos: " + result['alergia'].values[index]
        )
        return resultado
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return {"error 1": str(e)}
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}", file=sys.stderr)
        return {"error 2": str(e)}
    except Exception as e:
        print(f"Error inesperado: {e}", file=sys.stderr)
        return {"error 3": str(e)}

if __name__ == "__main__":
    
    # Leer la ruta del archivo de la entrada estándar
    file_path = sys.stdin.read().strip()
    print(f"Recibida ruta de archivo: '{file_path}'", file=sys.stderr)
    # Hacer la solicitud POST
    result = post_completion(file_path)
    
    # Imprimir el resultado como JSON
    print(json.dumps(result))