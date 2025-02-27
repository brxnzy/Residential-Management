import requests

def validar_cedula(cedula):
    url = f"https://api.digital.gob.do/v3/cedulas/{cedula}/validate"
    headers = {"accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if response.status_code == 200:
            print(f"¿Cédula válida? {data.get('valid', False)}")
        else:
            print(f"Error {response.status_code}: {data}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Prueba con una cédula
cedula_test = "001-1793795-3"
validar_cedula(cedula_test)


