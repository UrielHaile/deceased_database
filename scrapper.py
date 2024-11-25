import os
import zipfile
from bs4 import BeautifulSoup
import requests


class fetchingData():
    def __init__(self):
        self.url_main = "http://www.dgis.salud.gob.mx"
        try:
            self.page_to = requests.get("http://www.dgis.salud.gob.mx/contenidos/basesdedatos/da_defunciones_gobmx.html",timeout=10)
        except requests.exceptions.Timeout:
            print("Timed out")
        self.soup = BeautifulSoup(self.page_to.text, 'html.parser')
        self.tables = self.soup.findAll("table")
        self.name = [h3.get_text().replace(' ', '_')
                     for h3 in self.soup.findAll("h3")]

    def requesting_data(self, i):
        a = self.tables[i].findAll("a")
        self.createFolder(i)
        for enlace in a:
            url = enlace.get("href")
            if url:
                if not url.startswith('http'):
                    url = url[5:]
                    url = self.url_main+url
                #TO DO: Hacer el manejo de los evento como la desconexión o tiempo muy largo de espera.
                try:
                    archivo = requests.get(url, timeout=10)
                except requests.exceptions.Timeout:
                    print('TimedOut')
                if (archivo.status_code>=200 and archivo.status_code <=299):
                    name = url[url.rfind('/')+1:url.find('?'):1]
                    print(name)
                    with open(f'./{self.name[i]}/{name}', 'wb') as f:
                        f.write(archivo.content)
                    self.unzip(f'./{self.name[i]}/{name}')
                else:
                    print(f"Código de error: {archivo.status_code} ")
                    continue


    def createFolder(self, i):
        name_folder = self.name[i]
        if not os.path.exists(name_folder):
            os.mkdir(name_folder)
            print(f"Carpeta '{name_folder}' creada.")
        else:
            print(f"La carpeta '{name_folder}' ya existe.")

    def unzip(self, path_zip):
        with zipfile.ZipFile(path_zip, 'r') as zip_ref:
            # Extrae en el mismo directorio que el ZIP
            zip_ref.extractall(os.path.dirname(path_zip))
        print(f"Archivo descomprimido: {path_zip}")
        os.remove(path_zip)


def menu():
    i = 0
    while (i != 3):
        print("Requesting data.....")
        print("You will extract the following data:")
        print("0.-Catálogos de defunciones\n1.-Campos de defunciones\n2.-Registro de defunciones\n3.-salir")
        i = int(input("Ingresa el dato que desea extraer: "))
        if i == 3:
            break
        d = fetchingData()
        d.requesting_data(i)


menu()