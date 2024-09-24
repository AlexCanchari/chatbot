import pandas as pd
import json

# Simulando el input JSON
input_json = '{"classname": "34", "prediction": 34}'
data = json.loads(input_json)

# Leer el CSV (asegúrate de ajustar la ruta al archivo CSV correcto)
df = pd.read_csv('./diccionario/recetas.csv', encoding='ISO-8859-1')  # Cambia esto a la ruta de tu archivo CSV

# Filtrar el DataFrame según el valor de prediction
result = df[df['clase'] == data['prediction']]

index = 0

resultado = (
    "La Clase: " + str(int(result['clase'].values[index])) +
    "\nEs el Plato: " + result['plato'].values[index] +
    "\nContiene estos posibles ingredientes: " + result['receta'].values[index] +
    "\nIngredientes alérgenos: " + result['alergia'].values[index]
)
print(resultado)

            
    