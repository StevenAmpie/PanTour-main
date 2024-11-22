#Libreria Grafica
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import QTimer,Qt
#Libreria para Mapas
import geopandas as gpd
import matplotlib.pyplot as plt
import json


dataTest = {
    "Panamá": {
        "descripcion": "Comarca indígena formada en 1997 para otorgar autonomía a pueblos indígenas.",
        "sitios_turisticos": {
            "Turismo Ngäbe": {
                "descripcion": "Empresa de turismo ecológico que apoya proyectos de conservación natural en la comarca.",
                "comodidades": ["4 personas", "desayuno", "ticket aéreo", "hotel"],
                "precio": 150
            },
            "Tours": {
                "descripcion": "Rutas de ecoturismo por la comarca, incluyendo petroglifos y caminos arqueológicos.",
                "comodidades": ["6 personas", "paseo", "guía", "hotel"],
                "precio": 120
            },
            "Munä": {
                "descripcion": "Distrito con diversidad natural y cultural, con experiencias únicas de cultura ancestral.",
                "comodidades": ["2 personas", "desayuno", "paseo"],
                "precio": 90
            },
            "Cultura Ngäbe": {
                "descripcion": "Artesanías tradicionales como chaquiras y sombreros de fibra vegetal.",
                "comodidades": ["4 personas", "paseo", "artesanías"],
                "precio": 50
            }
        }
    }
}


class Provincias():
    def __init__(self,nombreProvincia,long,lat,data):
        self.nombreProvincia = nombreProvincia
        self.descripcion = data[f"{nombreProvincia}"]["descripcion"]
        self.long = long
        self.lat = lat
        self.data = data
        self.opcTuristicas = []
        #for nombreLugar in data[f"{nombreProvincia}"]["sitios_turisticos"]:
            #self.opcTuristicas.append(nombreLugar)  

 
    ##Genera Marcador en funcion de la latitud y longitud 
    def marcador(self):
        x,y = ax.transData.transform((self.long,self.lat))
        marcador = QPushButton("", window)
        marcador.setFixedSize(100,100)
        marcador.move(int(x),int(y-445))
        marcador.setIcon(QIcon("marcador.png"))
        marcador.setIconSize(marcador.size())
        marcador.setStyleSheet("""
        QPushButton {
            background-color: transparent; 
            border: none;
        }
        QPushButton:hover {
            background-color: rgba(100, 100, 255, 0.5); 
        }
        """)
        return marcador
        
    def loadOptions(self):
        for nombreLugar,lugar in self.data[f"{self.nombreProvincia}"]["sitios_turisticos"].items():
            opTuristica = lugarTuristico(nombreLugar,lugar["descripcion"],lugar["comodidades"],lugar["precio"])
            self.opcTuristicas.append(opTuristica)  
            
class lugarTuristico():
    def __init__(self,nombreLugar,descripcion,comodidades,precio):
        self.nombreLugar = nombreLugar
        self.descripcion = descripcion
        self.comodidades = comodidades
        self.precio = precio
                
#Crea caja para alinear elementos
#Recibe como atributo un objeto de "LugarTuristico"
def contentBox(lugarTuristico):
    ventanaAux = QWidget()
    contentBox = QVBoxLayout(ventanaAux)
    #aqui va el nombre de la opTuristica
    label = QLabel(lugarTuristico.nombreLugar)
    button = QPushButton()
    #aqui se coloca la ruta de la imagen (lugarturistico.img)
    button.setIcon(QIcon("imgtest.png"))
    
    contentBox.addWidget(label)
    contentBox.addWidget(button)
    
    return ventanaAux
    
    
#Ventana emergente para mostrar informacion de provincia y sus sitios turisticos
def ventanaEmergente(prov):
    
    sizex = window.width()//2
    sizey = window.height()//2 + int((window.height()//2)*0.35)
    
    x = window.x() +(window.width() - sizex)//2
    y = window.y() + (window.height() - sizey)//2
    
    
    ventanaEmergente = QDialog(window)
    ventanaEmergente.setGeometry(x, y, sizex, sizey)
    ventanaEmergente.setWindowFlags(Qt.FramelessWindowHint)
    ventanaEmergente.setStyleSheet("""
        QDialog {
            background-color: #ffffff;  
            border-radius: 12px;  
            border: 3px solid #000000;
        }
    """)
    veLayout = QGridLayout()
    nombreLabel = QLabel(prov.nombreProvincia)
    descripLabel = QLabel(prov.descripcion)
    
    veLayout.addWidget(nombreLabel,0,0,1,2,alignment=Qt.AlignCenter)
    veLayout.addWidget(descripLabel,1,0,1,2,alignment=Qt.AlignCenter)
  
    
    for row in range(2):
        for col in range(2):
            #pasarle cada opcion turistica almacenada en la lista 
            opTuristica = prov.opcTuristicas[(2*row)+col]
            veLayout.addWidget(contentBox(opTuristica),row+2,col)
    
    ventanaEmergente.setLayout(veLayout)
   
    ventanaEmergente.exec_()
    


#Cargar info de provs
#with open('ProvinciasTest.json', 'r' , encoding = 'utf-8') as provfile:
    #provsData = json.load(provfile)

#Genera la Ventana Principal
tourPan = QApplication([])
window = QWidget()

#Mostramos la ventana a pantalla completa y luego la escondemos 
window.showFullScreen()
window.setVisible(False)

#Pixeles por pulgadas(Es el que MPL usa por default para crear sus figuras)
dpi=100
#Se obtiene el tamano de la pantalla
xPixel =window.width()
yPixel = window.height()
#Traqueamos los datos
print (f"pixeles:{xPixel,yPixel}")

#Convertimos de pixeles a pulgadas
#Porque? MPL genera figuras en base a pulgadas.
#Recordar que nuestro objetivo es saber la resolucion de nuestra pantalla, para luego hacer la conversion a pulgadas 
# y genera una figura del tamano exacto de nuestra pantalla.
#Asi logramos mantener una escala uniforme con las coordenadas del JASON
xInch = xPixel/dpi
yInch = yPixel/dpi
#Traqueamos los datos
print(f"pulgadas:{xInch,yInch}")

#Carga el Mapa
file = 'Files/gadm41_PAN_1.json'  
panama = gpd.read_file(file)
#Crea la figura y los ejes en funcion del tamano de la pantalla
fig, ax = plt.subplots(figsize=(xInch,yInch))


# Dibuja el mapa sobre los ejes
panama.plot(ax=ax, color='lightblue', edgecolor='black')

#Esconde los ejes
#plt.axis('off')
#Convierte el Mapa a Imagen
plt.savefig('mapaPan.png')
plt.close(fig)



#Crear label con Mapa
labelPan = QLabel(window)
imgPan = QPixmap('mapaPan')
labelPan.setPixmap(imgPan)
#Ajusta el tamano del label al del Mapa
labelPan.resize(imgPan.width(), imgPan.height())


#Obtiene el tamano del label
xLabel = labelPan.width()
yLable = labelPan.height()
#Traqueamos los datos
print(f"Tamano Label{xLabel,yLable}")


#Se verifica el flujo final de la generacion de mapa, para ver si concuerda con la resolucion de la pantalla

#Conversion de cordenadas a pixeles
#x,y = ax.transData.transform((-79.5167,8.9833))
#Podemos hacer esto, ya que, como generamos el mapa en funcion de a resolucion de la pantalla
#la conversion va a ser de 1:1

#print(f"Pixel en X:{x}----Pixel en Y:{y}")
#Traqueamos los datos
#Lastimosamente
#Existe error de conversion :/, se contrarrestra con una constante(400)

#Trozteza,funciona a medio palo

#Sumar los 4 decimales que le siguen para obtener valor real(mmmh todavia falta revisar)




        
#panama = Provincias("Panamá",-79.5167,8.9833,dataTest)
#marcadortest = panama.marcador()
#panama.loadOptions()
#marcadortest.clicked.connect(lambda:ventanaEmergente(panama))

window.showFullScreen()

#print(panama.total_bounds)

tourPan.exec_()


