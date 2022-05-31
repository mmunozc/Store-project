from .controlador import Controlador
import requests
import os
import json

class ControladorProducto(Controlador):
    def __init__(self):
        super(Controlador).__init__()
        self.vendedor = None
        self.informacionVendedor = None
        self.productos = []
        self.informacionProductos = []

    def setVendedor(self, vendedor):
        self.vendedor = vendedor

    def getVendedor(self):
        return self.vendedor

    def getInformacionProductos(self):
        return self.informacionProductos

    def setInformacionVendedor(self, informacionVendedor):
        self.informacionVendedor = informacionVendedor

    def obtenerProductos(self):
        url = ControladorProducto.host + "/api/productos"
        parameters = {"vendedor": self.vendedor}
        response = requests.get(
            url,
            headers={'Authorization': f'Bearer {Controlador.getJWT()}'},
            params=parameters
            )
        response_dict = json.loads(response.text)
        self.informacionProductos = response_dict
        for producto in response_dict:
            producto.pop("vendedor")
        self.productos = response_dict

    def getInformacionVendedor(self):
        return self.informacionVendedor

    def getProductos(self):
        return self.productos
    
    def borrarProducto(self, id_producto):
        url = ControladorProducto.host + "/api/productos/"
        response = requests.delete(
            url,
            headers={'Authorization': f'Bearer {Controlador.getJWT()}'},
            params={"id": id_producto}
            )
        if response.status_code == 204:
            print("Producto borrado correctamente")
        else:
            print("Error al borrar producto")

    def registrarProducto(self):

        nombre = input("Ingrese el nombre de su producto: ")
        precio = input("Ingrese el precio del producto: ")
        marca = input("Ingrese la marca del producto: ")
        disponibilidad = input("Ingrese la cantidad de productos disponibles: ")
        try:
            assert type(nombre) is str
            assert type(int(precio)) is int
            assert type(marca) is str
            assert type(int(disponibilidad)) is int
        except Exception:
            self.registrarProducto()
            return
        data = {
            "nombre":nombre, 
            "precio":precio, 
            "marca":marca, 
            "disponibilidad":disponibilidad
            }
        headers = {"Authorization": f"Bearer {Controlador.getJWT()}"}
        url = ControladorProducto.host + "/api/productos/"
        response = requests.post(url, data=data, headers=headers)
        if response.status_code != 201:
            print("Error al crear producto")
        else:
            print("Producto creado exitosamente")
