import requests
import getpass
import os
from .controlador import Controlador
import json


class ControladorUsuario(Controlador):

    def __init__(self):
        super(Controlador).__init__()
        self.usuario = ""
        self.contraseña = ""
        self.informacionUsuario = {}
        self.informacionVendedores = []
        self.vendedores = []

    def setContraseña(self, contraseña):
        self.contraseña = contraseña

    def setUsuario(self, usuario):
        self.usuario = usuario

    def getInformacionUsuario(self):
        return self.informacionUsuario

    def setInformacionUsuario(self, informacionUsuario):
        self.informacionUsuario = informacionUsuario

    def getInformacionVendedores(self):
        return self.informacionVendedores

    def crearCuenta(self):
        username = input("Nombre de usuario: ")
        contraseña = getpass.getpass("Ingrese su contraseña: ")
        segundaContraseña = getpass.getpass("Ingrese su contraseña de nuevo: ")
        while contraseña != segundaContraseña:
            print("Las contraseñas no coinciden, intente de nuevo")
            contraseña = getpass.getpass("Ingrese su contraseña: ")
            segundaContraseña = getpass.getpass(
                "Ingrese su contraseña de nuevo: ")
        telefono = input("Ingrese su telefono: ")
        direccion = input("Ingrese su direccion: ")
        tipo = input("Ingrese su tipo de usuario (Comprador/Vendedor): ").lower()
        while tipo != "comprador" and tipo != "vendedor":
            print("Opcion no valida, vuelva a intentarlo")
            tipo = input("Ingrese su tipo de usuario (Comprador/Vendedor): ").lower()
        url = ControladorUsuario.host + '/api/auth/register'
        user = {"username": username,
                "password": contraseña,
                "telefono": telefono,
                "direccion": direccion,
                "tipo": tipo}
        if tipo == "vendedor":
            establecimiento = input("Ingrese el nombre de su establecimiento: ")
            user["establecimiento"] = establecimiento
        response = requests.post(url, data=user)
        if response.status_code != 200:
            print("Error en el servidor o en las credenciales")
            accion = input("Desea volver a intentarlo (Si/No): ").capitalize()
            while accion != 'Si' and accion != 'No':
                print("Accion invalida, Intente de nuevo")
                accion = input("Desea volver a intentarlo (Si/No): ").capitalize()
            if accion == "Si":
                self.crearCuenta()
            else:
                return "no"
            return
        response_dict = json.loads(response.text)    
        Controlador.setJWT(response_dict["access"])
        Controlador.setRefresh(response_dict["refresh"])
        
        self.informacionUsuario = {
            "username": response_dict["user"]["username"],
            "telefono": response_dict["user"]["telefono"],
            "direccion": response_dict["user"]["direccion"],
            "tipo": response_dict["user"]["tipo"]
        }
        if response_dict["user"]["tipo"] == "vendedor":
            self.informacionUsuario["establecimiento"] =  response_dict["user"]["establecimiento"]

    def autenticar(self):
        usuario = input("Ingrese su usuario: ")
        contraseña = getpass.getpass("Ingrese su contraseña: ")
        self.setUsuario(usuario)
        self.setContraseña(contraseña)
        credenciales = {"username": self.usuario, "password": self.contraseña}
        url = ControladorUsuario.host + "/api/auth/login/"
        response = requests.post(url, data=credenciales)
        if response.status_code != 200:
            print("Credenciales incorrectas, intente de nuevo")
            accion = input("Desea volver a intentarlo (Si/No): ").capitalize()
            while accion != 'Si' and accion != 'No':
                print("Accion invalida, Intente de nuevo")
                accion = input("Desea volver a intentarlo (Si/No): ").capitalize()
            if accion == "Si":
                self.autenticar()
            else:
                return "no"
            return
        response_dict = json.loads(response.text)  
        Controlador.setJWT(response_dict['access'])
        Controlador.setRefresh(response_dict['refresh'])
        headers = {"Authorization": f"Bearer {ControladorUsuario.getJWT()}"}
        url = ControladorUsuario.host + "/api/auth/user"
        response =  requests.get(url, headers=headers)
        response_dict = json.loads(response.text) 
        self.informacionUsuario = {
            "username": response_dict["username"],
            "telefono": response_dict["telefono"],
            "direccion": response_dict["direccion"],
            "tipo": response_dict["tipo"]
        }
        if response_dict["tipo"] == "vendedor":
            self.informacionUsuario["establecimiento"] =  response_dict["establecimiento"]

    def refrescarJWT(self):
        url = 'api/auth/refresh'
        direccion = os.path.join(self.host, url)
        headers = {"Authorization": f"Bearer {Controlador.getRefresh()}"}
        response = requests.post(direccion, headers=headers)
        Controlador.setJWT(response['access'])
        Controlador.setRefresh(response['refresh'])

    def obtenerVendedores(self):
        url = ControladorUsuario.host + "/api/usuarios"

        response = requests.get(
            url,
            headers={'Authorization': f'Bearer {Controlador.getJWT()}'})
        
        response_dict = json.loads(response.text)
        self.informacionVendedores = response_dict
        if not self.informacionVendedores:
            self.vendedores = []
        else:
            self.vendedores = map(lambda x : x["establecimiento"], self.informacionVendedores)