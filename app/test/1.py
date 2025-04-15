class MiExcepcionPersonalizada(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)


def dividir(a, b):
    if b == 0:
        raise MiExcepcionPersonalizada("No se puede dividir por cero.")
    return a / b

try:
    resultado = dividir(10, 0)
except MiExcepcionPersonalizada as e:
    print(f"¡Error!: {e}")
