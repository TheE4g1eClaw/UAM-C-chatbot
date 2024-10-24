import json

# Ruta del archivo JSON
ruta_json = 'data/planes_estudio/computacion.json'

# Abrir el archivo JSON

with open(ruta_json, encoding='utf-8') as archivo:
    datos = json.load(archivo)

# Ahora puedes trabajar con los datos del archivo JSON
# por ejemplo, imprimir el contenido
print(datos)