

import pytest
from fastapi.testclient import TestClient
from main import app, BD, cargarDatos, getTransaction, cargarTransacciones

BD = cargarDatos()
transacciones = cargarTransacciones()
client = TestClient(app)

def test_obtener_historial_exito():
    response = client.get("/billetera/historial?numero=123")
    data = response.json()
    assert response.status_code == 200
    assert data["success"] == True
    assert data["saldo"] == 400
    assert data["total_transacciones"] == 2

def test_obtener_historial_cuenta_no_encontrada():
    response = client.get("/billetera/historial?numero=999")
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Cuenta no encontrada"


def test_obtener_historial_parametro_faltante():
    response = client.get("/billetera/historial")
    data = response.json()

    assert response.status_code == 422
    assert data["detail"][0]["msg"] == "field required"


def test_getTransaction_exito():
    numero = "123"
    resultados = getTransaction(numero, transacciones)

    assert len(resultados) == 2
    assert "123 transfirió 200" in resultados
    assert "21345 envió 100" in resultados

def test_getTransaction_cuenta_no_encontrada():
    numero = "999"
    resultados = getTransaction(numero, transacciones)
    assert len(resultados) == 0


def test_getTransaction_transacciones_vacias():
    numero = "456"
    resultados = getTransaction(numero, transacciones)
    assert len(resultados) == 0
