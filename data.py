

class Cuenta:
    def __init__(self, numero, propietario, saldo, contactos):
        self.numero = numero
        self.propietario = propietario
        self.saldo = saldo
        self.contactos = contactos



def cargarDatos():
    # Agregar las cuentas a la lista
    BD = []
    BD.append(Cuenta("21345", "Arnaldo", 200, ["123", "456"]))
    BD.append(Cuenta("123", "Luisa", 400, ["456"]))
    BD.append(Cuenta("456", "Andrea", 300, ["21345"]))
    
    return BD

print("Cargar datos")
# Crear una lista para almacenar las cuentas
BD = cargarDatos()
print("Carga de datos finalizado")






