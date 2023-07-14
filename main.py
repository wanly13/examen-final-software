
import uvicorn
from fastapi import FastAPI , HTTPException
import os
import time
from fastapi.middleware.cors import CORSMiddleware
#from data import cargarDatos
import datetime




app = FastAPI()
app.add_middleware (
    CORSMiddleware, 
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

from pydantic import BaseModel

app = FastAPI()

class Contacto(BaseModel):
    minumero: str

@app.get("/billetera/contactos")
def obtener_contactos(minumero: str):
    try:
        
        data = search_contactos(minumero)
        response = {
            "success": True,
            "data": data
        }
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class Pago(BaseModel):
    minumero: str
    numerodestino: str
    valor: float

@app.get("/billetera/pagar")
def realizar_pago(minumero: str, numerodestino: str, valor: float):
    try:
        minumero = "21345"
        numerodestino = "123"
        valor = 50
        pagarYape(minumero , numerodestino , valor )
        
        response = {
            "success": True,
            "data": datetime.datetime.now().date()
        }
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/billetera/historial")
def obtener_historial(numero: str):
    try:
        saldo = None
        for cuenta in BD:
            if cuenta.numero == numero:
                saldo = cuenta.saldo

        transacciones = cargarTransacciones()  # Cargar las transacciones

        response = {
            "success": True,
            "saldo": saldo,
            "transacciones": getTransaction(numero, transacciones),  # Pasar las transacciones como argumento
            "total_transacciones": len(transacciones)
        }
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




# ------------ Datos de la cuenta y carga de datos
class Cuenta:
    def __init__(self, numero, propietario, saldo, contactos):
        self.numero = numero
        self.propietario = propietario
        self.saldo = saldo
        self.contactos = contactos
        
        
class Cuenta_minimo200:
    def __init__(self, numero, propietario, saldo, contactos, limite_diario):
        self.numero = numero
        self.propietario = propietario
        self.saldo = saldo
        self.contactos = contactos
        self.limite_diario = limite_diario
        

class Transacciones:
    def __init__(self, n_emisor, receptor, envio):
        self.n_emisor = n_emisor
        self.receptor = receptor
        self.envio = envio
        
        
def cargarDatos():
    # Agregar las cuentas a la lista
    BD = []
    BD.append(Cuenta("21345", "Arnaldo", 200, ["123", "456"]))
    BD.append(Cuenta("123", "Luisa", 400, ["456"]))
    BD.append(Cuenta("456", "Andrea", 300, ["21345"]))    
    return BD
class Transacciones:
    def __init__(self, n_emisor, receptor, envio):
        self.n_emisor = n_emisor
        self.receptor = receptor
        self.envio = envio
        
def cargarTransacciones():
    trasns = []
    trasns.append(Transacciones("21345", "123", 200))
    trasns.append(Transacciones("123", "21345", 100))
    trasns.append(Transacciones("21345", "123", 300))
    return trasns


print("Cargar datos")
BD = cargarDatos()
transacciones = cargarTransacciones()
print("Carga de datos finalizado")


# ------------ Implementacion de funciones de las APIs 

def search_contactos(numero):
    contactos = []
    for cuenta in BD:
        if cuenta.numero == numero:
            for contacto_numero in cuenta.contactos:
                for cuenta_contacto in BD:
                    if cuenta_contacto.numero == contacto_numero:
                        contactos.append(cuenta_contacto.propietario)
            break
    return contactos

def pagarYape(minumero, numerodestino, valor):
    for cuenta in BD:
        if cuenta.numero == numerodestino:
            cuenta.saldo += valor
            transacciones.append(Transacciones(minumero, numerodestino ,valor))
            print(BD[1].saldo)
            break
  
    
def pagarYape_min200(minumero, numerodestino, valor):
    for cuenta in BD:
        if cuenta.numero == minumero:
            if valor <= cuenta.limite_diario:
                for cuenta_destino in BD:
                    if cuenta_destino.numero == numerodestino:
                        cuenta_destino.saldo += valor
                        break
            else:
                raise ValueError("Excede el límite diario de transferencia")
            break

    
def getTransaction(numero, transacciones):
    resultados = []
    for transaccion in transacciones:
        if transaccion.n_emisor == numero:
            resultados.append(f"{transaccion.n_emisor} transfirió {transaccion.envio}")
        if transaccion.receptor == numero:
            resultados.append(f"{transaccion.receptor} envió {transaccion.envio}")
    return resultados




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
