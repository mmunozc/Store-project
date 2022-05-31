import requests
import os
from prettytable import PrettyTable
import getpass
from controladores.controladorUsuario import ControladorUsuario
from controladores.controladorProducto import ControladorProducto
from controladores.controladorOrden import ControladorOrden


class Terminal:
    def __init__(self):
        self.controladorUsuario = ControladorUsuario()
        self.controladorProducto = ControladorProducto()
        self.controladorOrden = ControladorOrden()
        self.interfacesAbiertas = 1

    def realizarOrden(self):
        self.controladorOrden.realizarOrden()

    def mostrarInformacionVendedor(self):
        table1 = PrettyTable()
        table1.field_names = ["nombre", "telefono",
                              "tipo", "establecimiento", "direccion"]
        table1.add_row(
            [field[1] for field in self.controladorProducto.getInformacionVendedor().items() if field[0] != "id"])
        print("Informacion de vendedor asociado")
        print(table1)
        table2 = PrettyTable()
        if not self.controladorProducto.getProductos():
            print("No hay productos disponibles")
        table2.field_names = ["id", "Nombre", "Precio", "Marca", "Disponibilidad"]
        for producto in self.controladorProducto.getProductos():
            table2.add_row([field[1] for field in producto.items()])
        print("Informacion de productos ofrecidos por este vendedor")
        print(table2)

    def verificarDisponibilidadProducto(self, producto, cantidad):
        existeProducto = False
        hayDisponibilidad = False
        for prod in self.controladorProducto.getInformacionProductos():
            if prod["nombre"] == producto:
                existeProducto = True
            if existeProducto:
                hayDisponibilidad = cantidad <= prod["disponibilidad"]
                break
        if not existeProducto:
            print("El producto seleccionado no existe")
        if not hayDisponibilidad:
            print("No hay las cantidades suficientes para satisfacer la órden")
        return existeProducto and hayDisponibilidad

    def verVendedores(self):
        self.controladorUsuario.obtenerVendedores()
        self.mostrarVendedores()
        vendedor = input(
            "Seleccione un vendedor (Nombre de Establecimiento): ")
        self.controladorProducto.setVendedor(vendedor)
        for vend in self.controladorUsuario.getInformacionVendedores():
            if vend["establecimiento"] == vendedor:
                self.controladorProducto.setInformacionVendedor(vend)
                break
        while not (self.controladorProducto.getVendedor() in self.controladorUsuario.vendedores):
            print("Vendedor inválido, seleccione de nuevo")
            vendedor = input("Seleccione un vendedor: ")
            self.controladorProducto.setVendedor(vendedor)
            for vend in self.controladorUsuario.getInformacionVendedores():
                if vend["establecimiento"] == vendedor:
                    self.controladorProducto.setInformacionVendedor(vend)
        accion = input(
            "Desea ver los productos ofrecidos por este Vendedor (Si/No): ").capitalize()
        if accion == "Si":
            self.controladorProducto.obtenerProductos()
            self.mostrarInformacionVendedor()
            accion = input(
                "Desea agregar un nuevo producto a su órden (Si/No): ").capitalize()
            while accion == "Si":
                producto = input("Ingrese el producto que desea agregar: ")
                cantidad = input(
                    "Ingrese la cantidad que desea agregar de este producto: ")
                cantidad = int(cantidad)
                if not self.verificarDisponibilidadProducto(producto, cantidad):
                    continue
                else:
                    for prod in self.controladorProducto.getInformacionProductos():
                        if prod["nombre"] == producto:
                            nuevoProducto = {
                                "costo": (prod["precio"] * cantidad),
                                "cantidad": cantidad,
                                "completado": False,
                                "producto": prod["id"],
                            }
                            self.controladorOrden.agregarProducto(
                                nuevoProducto)
                            break
                    # print(self.controladorOrden.orden) # !bug
                accion = input(
                    "Desea agregar un nuevo producto a su órden (Si/No): ").capitalize()

    def cancelarOrden(self):
        id_orden = input("Ingrese el numero de identificacion \"id\" de la orden que desea cancelar: ")
        while not id_orden.isnumeric():
            print("el id ingresado no es numerico, intente de nuevo")
            accion = input("Desea Regresar a las opciones anteriores (Si/No)").capitalize()
            if accion == "Si":
                return
            id_orden = input("Ingrese el \"id\" de la orden que desea cancelar: ")
        id_orden = int(id_orden)
        self.controladorOrden.cancelarOrden(id_orden)

    def verProductosVendedor(self):
        vendedor = self.controladorUsuario.getInformacionUsuario()["establecimiento"]
        self.controladorProducto.setVendedor(vendedor)
        usuario = self.controladorUsuario.getInformacionUsuario().copy()
        self.controladorProducto.setInformacionVendedor(usuario)
        self.controladorProducto.obtenerProductos()
        self.mostrarInformacionVendedor()

    def seleccionarAccionComprador(self):
        accion = input(
            "Desea ver vendedores, enviar una órden, ver estado de sus ordenes,\n cancelar una orden o salir (Vendedores/Enviar/Ordenes/Cancelar/Salir): ").capitalize()
        acciones = {"Vendedores", "Enviar", "Ordenes", "Cancelar","Salir"}
        while not (accion in acciones):
            print("Accion invalida, vuelva a intentar")
            accion = input(
                "Desea ver vendedores, enviar una órden, ver estado de sus ordenes,\n cancelar una orden o salir (Vendedores/Enviar/Ordenes/Cancelar/Salir): ").capitalize()
        if accion == 'Vendedores':
            self.verVendedores()
        elif accion == "Enviar":
            self.realizarOrden()
        elif accion == "Ordenes":
            self.verOrdenesComprador()
        elif accion == "Cancelar":
            self.cancelarOrden()
        else:
            self.interfacesAbiertas = 0

    def verOrdenesVendedor(self):
        self.controladorOrden.obtenerOrdenes()
        establecimiento = self.controladorUsuario.getInformacionUsuario()["establecimiento"]
        self.controladorProducto.setVendedor(establecimiento)
        self.controladorProducto.obtenerProductos()
        self.mostrarInformacionOrdenVendedor()
    

    def mostrarInformacionOrdenComprador(self):
        table = PrettyTable()
        table.field_names = ["id", "Producto", "Costo","Cantidad",  "Vendedor"]
        for orden in self.controladorOrden.orden:
            row = []
            for key, val in orden.items():
                row.append(val)
            if "vendedor" in orden:
                table.add_row(row)
        print(table)


    def verOrdenesComprador(self):
        self.controladorOrden.obtenerOrdenes()
        for orden in self.controladorOrden.orden:
            del orden["completado"]
            del orden["comprador"]
            if orden["producto"]:
                orden["vendedor"] = orden["producto"]["vendedor"]["establecimiento"]
                orden["producto"] = orden["producto"]["nombre"]
        self.mostrarInformacionOrdenComprador()


    def mostrarVendedores(self):
        table = PrettyTable()
        table.field_names = ["nombre", "telefono",
                             "tipo", "establecimiento", "direccion"]
        for vendedor in self.controladorUsuario.getInformacionVendedores():
            if vendedor:
                table.add_row([field[1] for field in vendedor.items() if field[0] != "id"])
        print(table)


    def mostrarInformacionOrdenVendedor(self):
        table = PrettyTable()
        table.field_names = ["id", "Comprador", "telefono", "Producto", "Costos",
                             "Cantidades",  "Completado"]
        for orden in self.controladorOrden.orden:
            if table:
                row = []
                for field in orden.items():
                    if field[0] == "comprador":
                        row.append(field[1]["username"])
                        row.append(field[1]["telefono"])
                    elif field[0] == "producto":
                        for prod in self.controladorProducto.getInformacionProductos():
                            if field[1] == prod["id"]:
                                row.append(prod["nombre"])
                    else:
                        row.append(field[1])
                table.add_row(row)
        print(table)

    def quitarProducto(self):
        id_producto = input("Ingrese el id del producto que desea quitar: ")
        while not id_producto.isnumeric():
            print("id no valido")
            accion = input("Desea volver a intentarlo (Si/No)").capitalize()
            if accion == "No":
                return
            id_producto = input("Ingrese el id del producto que desea quitar: ")
        id_producto = int(id_producto)
        self.controladorProducto.borrarProducto(id_producto)

    def despacharOrden(self):
        id_orden = input("ingrese el id de la orden que desea despachar: ")
        while not id_orden.isnumeric():
            print("Id invalido")
            accion = input("Desea volver a intentarlo? (Si/No): ").capitalize()
            if accion == "No":
                return
        id_orden = int(id_orden)
        self.controladorOrden.despachar(id_orden)

    def seleccionarAccionVendedor(self):
        accion = input(
            "Desea ver sus órdenes, registrar productos, Ver productos, quitar productos,\n o despachar una orden o salir (Ordenes/Registrar/Ver/Quitar/Despachar/Salir): ").capitalize()

        acciones = {"Registrar", "Ordenes", "Ver", "Quitar", "Despachar","Salir"}
        while not (accion in acciones):
            print("Acción inválida, vuelva a intentar")
            accion = input(
                "Desea ver sus órdenes, registrar productos, quitar productos,\n o despachar una orden o salir (Ordenes/Registrar/Quitar/Despachar/Salir): ").capitalize()
        if accion == 'Ordenes':
            self.verOrdenesVendedor()
        elif accion == "Registrar":
            self.controladorProducto.registrarProducto()
        elif accion == "Quitar":
            self.quitarProducto()
        elif accion == "Despachar":
            self.despacharOrden()
        elif accion == "Ver":
            self.verProductosVendedor()
        else:
            self.interfacesAbiertas = 0
            

    def comenzar(self):
        accion = input(
            "Desea ingresar o registrarse (Ingresar/Registrarse): ")
        accion = accion.capitalize()
        while accion != "Ingresar" and accion != "Registrarse":
            print("Acción inválida, intenta de nuevo")
            accion = input(
                "Desea ingresar o registrarse (Ingresar/Registrarse): ").capitalize()
        if accion == "Ingresar":
            if self.controladorUsuario.autenticar() == "no":
                self.interfacesAbiertas = 0
        else:
            if self.controladorUsuario.crearCuenta() == "no":
                self.interfacesAbiertas = 0

    def correr(self):
        self.comenzar()
        while self.interfacesAbiertas:
            if self.controladorUsuario.getInformacionUsuario()["tipo"] == 'comprador':
                self.seleccionarAccionComprador()
            elif self.controladorUsuario.getInformacionUsuario()["tipo"] == 'vendedor':
                self.seleccionarAccionVendedor()
        print("Se ha cerrado la aplicación")


def main():
    terminal = Terminal()
    terminal.correr()


if __name__ == "__main__":
    main()
