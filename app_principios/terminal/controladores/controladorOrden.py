from .controlador import Controlador
import requests
import os
import json

class ControladorOrden(Controlador):

    def __init__(self):
        super(Controlador).__init__()
        self.vendedor = ""
        self.orden = []

    def seleccionarVendedor(self, vendedor):
        self.vendedor = vendedor
        self.productos = {}

    def agregarProducto(self, producto):
        self.orden.append(producto)

    def realizarOrden(self):
        url = ControladorOrden.host + "/api/ordenes/"
        if not self.orden:
            print("No ha seleccionado ningun producto")
        for ords in self.orden:
            if "producto" in ords:
                response = requests.post(
                    url,
                    headers={'Authorization': f'Bearer {Controlador.getJWT()}'}, data=ords)
                # print(ords) #! bug
                if response.status_code != 201:
                    print("Error al enviar orden")
                else:
                    print("Orden enviada correctamente")

    def obtenerOrdenes(self):
        url = ControladorOrden.host + "/api/ordenes"
        response = requests.get(
            url,
            headers={'Authorization': f'Bearer {Controlador.getJWT()}'})
        response_dict = json.loads(response.text)
        self.orden = response_dict
    
    def despachar(self, id_orden):
        url = ControladorOrden.host + "/api/ordenes/"
        response = requests.patch(
            url,
            headers={'Authorization': f'Bearer {Controlador.getJWT()}'},
            params={"id": id_orden}
            )
        if response.status_code == 201:
            print("Orden despachada correctamente")
        else:
            print("Error al despachar orden")

    def cancelarOrden(self, id_orden):
        url = ControladorOrden.host + "/api/ordenes/"
        response = requests.delete(
            url,
            headers={'Authorization': f'Bearer {Controlador.getJWT()}'},
            params={"id": id_orden}
            )
        if response.status_code == 204:
            print("Orden borrada correctamente")
        else:
            print("Error al borrar orden")
