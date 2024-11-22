#
from reserva import Ui_MainWindow
from despedida import Ui_MainWindow2
from Presentacion import Ui_MainWindow3
#Libreria Grafica
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,QPixmap,QFont
from PyQt5.QtCore import QTimer,Qt, QSize, QRect

#Libreria para Mapas
import geopandas as gpd
import matplotlib.pyplot as plt
import json

global name #CAMBIO STEVEN: VARIABLE GLOBAL PARA EL NOMBRE DE LA ATRACCION TURISTICA EN CADA RESERVA

global precio #CAMBIO STEVEN: VARIABLE GLOBAL PARA EL PRECIO DE LA ATRACCION TURISTICA EN CADA RESERVA

global subTotal

global totalPersonas

global abono


font = QFont("Arial", 12)


class Provincias():

    global subTotal
    subTotal = 0
    

    global totalPersonas
    totalPersonas = 0
    
    global abono
    abono = 0
 

    def __init__(self,nombreProvincia,long,lat,data):
        self.nombreProvincia = nombreProvincia
        self.descripcion = data[f"{nombreProvincia}"]["descripcion"]
        self.long = long
        self.lat = lat
        self.data = data
        self.opcTuristicas = []
         
    ##Genera Marcador en funcion de la latitud y longitud 
    def marcador(self):
        # Transformar coordenadas geográficas a píxeles
        x, y = ax.transData.transform((self.long, self.lat))
    
        # Invertir el eje Y
        y = labelPan.height() - int(y)  # Reflejar las coordenadas en el eje Y
        y -= 80 #Correccion de error

        # Redondear X e Y para que sean enteros
        x = int(x)

        marcador = QPushButton(f"{self.nombreProvincia}", window)
        marcador.setFont(font)
        marcador.move(x, y)  # Usar las coordenadas ajustadas
        marcador.setIcon(QIcon("marcador.png"))
        marcador.setIconSize(QSize(100,100))
        marcador.setStyleSheet("""
        QPushButton {
            background-color: transparent; 
            border: none;
            
            color: black; 
        }
        QPushButton:hover {
            background-color: rgba(100, 100, 255, 0.5); 
          }
        """)
        marcador.clicked.connect(lambda: ventanaEmergenteProv(self))
        return marcador

        
    def loadOptions(self):
        for nombreLugar,lugar in self.data[f"{self.nombreProvincia}"]["lugares_turisticos"].items():
            opTuristica = lugarTuristico(nombreLugar,lugar["descripcion"],lugar["servicios_incluidos"],lugar["precio"])
            self.opcTuristicas.append(opTuristica)  
            
class lugarTuristico():
    def __init__(self,nombreLugar,descripcion,servicios,precio):
        self.nombreLugar = nombreLugar
        self.descripcion = descripcion
        self.servicios = servicios
        self.precio = precio
                
#Crea caja para alinear elementos
#Recibe como atributo un objeto de "LugarTuristico"
def contentBox(lugarTuristico):    
    ventanaAux = QWidget()
    contentBox = QVBoxLayout(ventanaAux)
    #aqui va el nombre de la opTuristica
    
    ########################################################################################################
    label = QLabel(lugarTuristico.nombreLugar)
    label.setFont(font)
    button = QPushButton()

    #aqui se coloca la ruta de la imagen (lugarturistico.img)
    img = f"{lugarTuristico.nombreLugar}.jpg"
    img = img.lower()
    #print(img)
    button.setIcon(QIcon(f"Files/sitiosTuristicos/{img}"))
    button.setIconSize(QSize(500,500))


    pantallaReserva.nombreSitio.setText("")
    pantallaReserva.precioSitio.setText("")
    pantallaReserva.cantperso.setValue(0)

    ##CAMBIO STEVEN: AGREGUE UN ATRIBUTO PARA LA VARIABLE GLOBAL

    button.clicked.connect(lambda: ventanaEmergenteLugar(lugarTuristico, lugarTuristico.nombreLugar, lugarTuristico.precio))
    
    
    contentBox.addWidget(label)
    contentBox.addWidget(button)
    
    return ventanaAux
    
    
def ventanaEmergenteProv(prov):
    # Tamaño y posición de la ventana emergente
    sizex = window.width() // 2
    sizey = window.height() // 2 + int((window.height() // 2) * 0.35)
    x = window.x() + (window.width() - sizex) // 2
    y = window.y() + (window.height() - sizey) // 2

    ventanaEmergente = QDialog(window)
    ventanaEmergente.setGeometry(x, y, sizex, sizey)
    ventanaEmergente.setWindowFlags(Qt.FramelessWindowHint)

    # Estilo de la ventana
    ventanaEmergente.setStyleSheet("""
        QDialog {
            background-color: #f9f9f9;  
            border-radius: 15px;  
            border: 2px solid #4CAF50;
        }
    """)

    veLayout = QGridLayout()

    # Título de la provincia
    nombreLabel = QLabel(prov.nombreProvincia)
    nombreLabel.setFont(QFont("Arial", 18, QFont.Bold))
    nombreLabel.setAlignment(Qt.AlignCenter)
    nombreLabel.setStyleSheet("color: #2C3E50; margin-bottom: 10px;")

    # Descripción
    descripLabel = QLabel(prov.descripcion)
    descripLabel.setFont(QFont("Arial", 12))
    descripLabel.setWordWrap(True)
    descripLabel.setAlignment(Qt.AlignJustify)
    descripLabel.setStyleSheet("color: #34495E; margin: 10px;")

    veLayout.addWidget(nombreLabel, 0, 0, 1, 2, alignment=Qt.AlignCenter)
    veLayout.addWidget(descripLabel, 1, 0, 1, 2, alignment=Qt.AlignCenter)

    # Opciones turísticas
    for row in range(2):
        for col in range(2):
            opTuristica = prov.opcTuristicas[(2 * row) + col]
            veLayout.addWidget(contentBox(opTuristica), row + 2, col)

    # Botón de cierre
    buttonClose = QPushButton("Cerrar")
    buttonClose.setFont(QFont("Arial", 10, QFont.Bold))
    buttonClose.setStyleSheet("""
        QPushButton {
            background-color: #E74C3C;
            color: white;
            border-radius: 10px;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #C0392B;
        }
    """)
    buttonClose.clicked.connect(ventanaEmergente.close)

    veLayout.addWidget(buttonClose, 4, 0, 1, 2, alignment=Qt.AlignCenter)

    ventanaEmergente.setLayout(veLayout)
    ventanaEmergente.exec_()

def ventanaEmergenteLugar(lugar, nombreLugar, precioLugar):
    global name, precio
    name = nombreLugar
    precio = precioLugar

    # Tamaño y posición de la ventana emergente
    sizex = window.width() // 2
    sizey = window.height() // 2 + int((window.height() // 2) * 0.35)
    x = window.x() + (window.width() - sizex) // 2
    y = window.y() + (window.height() - sizey) // 2

    ventanaEmergente = QDialog(window)
    ventanaEmergente.setGeometry(x, y, sizex, sizey)
    ventanaEmergente.setWindowFlags(Qt.FramelessWindowHint)

    # Estilo de la ventana
    ventanaEmergente.setStyleSheet("""
        QDialog {
            background-color: #fefefe;  
            border-radius: 15px;  
            border: 2px solid #3498DB;
        }
    """)

    veLayout = QGridLayout()

    # Nombre del lugar
    nombreLabel = QLabel(lugar.nombreLugar)
    nombreLabel.setFont(QFont("Arial", 18, QFont.Bold))
    nombreLabel.setStyleSheet("color: #2980B9; margin-bottom: 10px;")
    nombreLabel.setAlignment(Qt.AlignCenter)

    # Descripción
    descripLabel = QLabel(lugar.descripcion)
    descripLabel.setWordWrap(True)
    descripLabel.setFont(QFont("Arial", 12))
    descripLabel.setStyleSheet("color: #34495E; margin: 10px;")
    descripLabel.setAlignment(Qt.AlignJustify)

    # Servicios
    serviciosLabel = QLabel(f"Servicios Incluidos:\n{lugar.servicios}")
    serviciosLabel.setWordWrap(True)
    serviciosLabel.setFont(QFont("Arial", 12))
    serviciosLabel.setStyleSheet("color: #16A085;")

    # Precio
    precioLabel = QLabel(f"Precio: ${lugar.precio}")
    precioLabel.setFont(QFont("Arial", 14, QFont.Bold))
    precioLabel.setStyleSheet("color: #27AE60;")

    # Imagen
    imgLabel = QLabel()
    img = f"{lugar.nombreLugar}.jpg"
    img = img.lower()
    imgLabel.setPixmap(QPixmap(f"Files/sitiosTuristicos/{img}"))
    imgLabel.setScaledContents(True)
    imgLabel.setFixedSize(250, 250)

    # Botón de cerrar
    buttonClose = QPushButton("Cerrar")
    buttonClose.setStyleSheet("""
        QPushButton {
            background-color: #E74C3C;
            color: white;
            border-radius: 10px;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #C0392B;
        }
    """)
    buttonClose.clicked.connect(ventanaEmergente.close)

    # Botón de reserva
    buttonReserva = QPushButton("Reservar")
    buttonReserva.setStyleSheet("""
        QPushButton {
            background-color: #2ECC71;
            color: white;
            border-radius: 10px;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #27AE60;
        }
    """)
    buttonReserva.clicked.connect(lambda: mostrarReserva(pantallaReserva))

    veLayout.addWidget(nombreLabel, 0, 0, 1, 2, alignment=Qt.AlignCenter)
    veLayout.addWidget(descripLabel, 1, 0, 1, 2, alignment=Qt.AlignCenter)
    veLayout.addWidget(serviciosLabel, 2, 0, alignment=Qt.AlignCenter)
    veLayout.addWidget(imgLabel, 2, 1, alignment=Qt.AlignCenter)
    veLayout.addWidget(precioLabel, 3, 0, alignment=Qt.AlignCenter)
    veLayout.addWidget(buttonClose, 4, 0, alignment=Qt.AlignCenter)
    veLayout.addWidget(buttonReserva, 4, 1, alignment=Qt.AlignCenter)

    ventanaEmergente.setLayout(veLayout)
    ventanaEmergente.exec_()

    
    
'''def ventanaEmergenteLugar(lugar, nombreLugar, precioLugar):
    
    global name #CAMBIO STEVEN VAR GLOBAL
    global precio

    name = nombreLugar #CAMBIO STEVEN, VARIABLE GLOBAL ASIGNADA CON EL NOMBRE DE LA ATRACCION DEPENDIENDO DEL MARCADOR

    precio = precioLugar #CAMBIO STEVEN, VARIABLE GLOBAL ASIGNADA CON EL NOMBRE DE LA ATRACCION DEPENDIENDO DEL MARCADOR


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
    ########################################################################################################
    nombreLabel = QLabel(lugar.nombreLugar)
    nombreLabel.setFont(font)
    ########################################################################################################
    descripLabel = QLabel(lugar.descripcion)
    descripLabel.setWordWrap(True)
    descripLabel.setFont(font)
    ########################################################################################################
    serviciosLabel = QLabel(f"Servicios Incluidos:\n{lugar.servicios}")
    serviciosLabel.setWordWrap(True)
    serviciosLabel.setFont(font)
    precioLabel = QLabel(f"Precio: ${lugar.precio}")
    precioLabel.setFont(font)
    imgLabel = QLabel()
    img = f"{lugar.nombreLugar}.jpg"
    img = img.lower()
    imgLabel.setPixmap(QPixmap(f"Files/sitiosTuristicos/{img}"))
    imgLabel.setFixedSize(500,500)
    ########################################################################################################
    buttonClose = QPushButton("Close")
    ########################################################################################################
    buttonReserva = QPushButton("Reserva")

    
    buttonReserva.clicked.connect(lambda: mostrarReserva(pantallaReserva)) ####

    
    veLayout.addWidget(nombreLabel,0,0,1,2,alignment=Qt.AlignCenter)
    veLayout.addWidget(descripLabel,1,0,1,2,alignment=Qt.AlignCenter)
    veLayout.addWidget(serviciosLabel,2,0,alignment=Qt.AlignCenter)
    veLayout.addWidget(imgLabel,2,1,alignment=Qt.AlignCenter)
    veLayout.addWidget(precioLabel,3,0,alignment=Qt.AlignCenter)
    
    veLayout.addWidget(buttonClose,4,0)
    veLayout.addWidget(buttonReserva,4,1)

    
    
    buttonClose.clicked.connect(ventanaEmergente.close)
    
    
    ventanaEmergente.setLayout(veLayout)
   
    ventanaEmergente.exec_()'''
    


#Crea los objetos para cada provincia y carga sus metodos
def loadProvs():
    for clave,provincia in provsData.items():
        prov = Provincias(clave,provincia["long"],provincia["lat"],provsData)
        marcador = prov.marcador()
        prov.loadOptions()
        provs.append(prov)
        marcadoresProv.append(marcador)
        

#Cargar info de provs
with open('Files/ProvinciasData2.0.json', 'r' , encoding = 'utf-8') as provfile:
    provsData = json.load(provfile)

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
plt.axis('off')
#Convierte el Mapa a Imagen
plt.savefig('mapaPan.png')
plt.close(fig)


#Crear label con Mapa
labelPan = QLabel(window)
imgPan = QPixmap('mapaPan')
labelPan.setPixmap(imgPan)
#Ajusta el tamano del label al del Mapa
labelPan.adjustSize()


#Obtiene el tamano del label
xLabel = labelPan.width()
yLable = labelPan.height()
#Traqueamos los datos
print(f"Tamano Label{xLabel,yLable}")

        
provs = []       
marcadoresProv = []

loadProvs()



#print(provs)
#print(marcadoresProv)
Reserva =QMainWindow()
pantallaReserva = Ui_MainWindow()
pantallaReserva.setupUi(Reserva)


pantallaReserva.precioSitio = QLabel(pantallaReserva.centralwidget)
pantallaReserva.precioSitio.setGeometry(QRect(423, 72, 300, 30))

pantallaReserva.nombreSitio = QLabel(pantallaReserva.centralwidget)
pantallaReserva.nombreSitio.setGeometry(QRect(420, 34, 300, 30))

pantallaReserva.subTotalLabel = QLabel(pantallaReserva.centralwidget)
pantallaReserva.subTotalLabel.setGeometry(QRect(450, 123,300 , 30))

pantallaReserva.inputTotalAdeudado = QLabel(pantallaReserva.groupBox_3)
pantallaReserva.inputTotalAdeudado.setGeometry(QRect(100, 260, 200, 16))
pantallaReserva.inputTotalAdeudado.setObjectName("totaladeudado")


pantallaReserva.descuentoTotal = QLabel(pantallaReserva.groupBox_2)
pantallaReserva.descuentoTotal.setGeometry(QRect(70, 80, 71, 21))
pantallaReserva.descuentoTotal.setObjectName("descuento")


pantallaReserva.subTotalLabel.setText("")




#CODE STEVEN:


#######################################################


#EVENTOS DE LA PANTALLA DE RESERVA:

pantallaReserva.btnregresar.clicked.connect(lambda:ocultarVentanaReserva(pantallaReserva))
pantallaReserva.btnabonar.clicked.connect(lambda: check_radio(pantallaReserva))

pantallaReserva.btnreservar.clicked.connect(lambda: completarReserva())

pantallaReserva.intronom.textChanged.connect(lambda: validar_nombre(pantallaReserva))
pantallaReserva.introcedula.textChanged.connect(lambda: validar_cedula(pantallaReserva))
pantallaReserva.intrnumtelefono.textChanged.connect(lambda: validar_telefono(pantallaReserva))
pantallaReserva.introedad.textChanged.connect(lambda: validar_edad(pantallaReserva))
pantallaReserva.intromail.textChanged.connect(lambda: validar_email(pantallaReserva))
pantallaReserva.intropais.textChanged.connect(lambda: validar_pais(pantallaReserva))
pantallaReserva.cantperso.valueChanged.connect(lambda: validar_cantidad_personas(pantallaReserva))

pantallaReserva.btnAgregarReserva.clicked.connect(lambda: validarDatos(pantallaReserva))

pantallaReserva.btnabonar.clicked.connect(lambda: validarAbono())

Despedida =QMainWindow()
pantallaDespedida = Ui_MainWindow2()
pantallaDespedida.setupUi(Despedida)

Presentacion =QMainWindow()
pantallaPresentacion = Ui_MainWindow3()
pantallaPresentacion.setupUi(Presentacion)

#pantallaReserva.input_abono.textChanged.connect(lambda: validarAbono())



 

# METODOS DE LA VENTANA RESERVA 

def validarAbono():
    
    global abono 

    abono = int(pantallaReserva.input_abono.text())

    pantallaReserva.abono.setText(f"Abono: ${abono}")

    



    '''if int(pantallaReserva.input_abono.text()) > subTotal:
            
            pantallaReserva.introduzAbono.setText("*Ingrese su nombre*")
            pantallaReserva.introduzAbono.setStyleSheet("color: red")
            error = True'''

def completarReserva():

    try:

        global subTotal
        global totalPersonas  
        descuentoTotal = 0
        global abono 

        flag = 0
        flag = subTotal



        if(subTotal>2000):
            subTotal-=flag*0.05
            descuentoTotal+=5
            

        if(int(pantallaReserva.introedad.text()) >=  60):
            subTotal-=flag*0.1
            descuentoTotal+=10
        
        if(totalPersonas >= 3):
            subTotal-=flag*0.15
            descuentoTotal+=15
        
        subTotal -= abono

        # Limpiar los campos si es necesario

    
        
        #validarAbono()

        pantallaReserva.inputTotalAdeudado.setText(f"${subTotal}")

        subTotal = 0
        totalPersonas = 0

        

        pantallaReserva.descuentoTotal.setText(f": {descuentoTotal}%")

        reiniciarReserva()

    except ValueError:
        
        pass

 
def depurarDatos():
    pantallaReserva.intronom.setText("")
    pantallaReserva.introcedula.setText("")
    pantallaReserva.intrnumtelefono.setText("")
    pantallaReserva.introedad.setText("")
    pantallaReserva.intropais.setText("")
    pantallaReserva.intromail.setText("")
    pantallaReserva.introduzAbono.setText("")
    pantallaReserva.cantperso.setValue(0)
      # Limpiar los campos si es necesario
    pantallaReserva.nomfac.setText("Nombre: ")
    pantallaReserva.cedulafac.setText("Cédula: ")
    pantallaReserva.telefonofac.setText("Teléfono: ")
    pantallaReserva.sexofac.setText("Sexo: ")
    pantallaReserva.edadfac.setText("Edad: ")
    pantallaReserva.paisfac.setText("País: ")
    pantallaReserva.mailfac.setText("E-mail: ")
    pantallaReserva.cantpersonfac.setText("Cantidad de personas: ")
    pantallaReserva.abono.setText("Abono: ")
    pantallaReserva.inputTotalAdeudado.setText("")
    pantallaReserva.descuentoTotal.setText("")
    pantallaReserva.subTotalLabel.setText("")
    pantallaReserva.nombreSitio.setText("")
    pantallaReserva.precioSitio.setText("")




def reiniciarReserva():
    QTimer.singleShot(5000, depurarDatos)


def mostrarReserva(self):
        
        Reserva.show()
        self.nombreSitio.setText(name)
        self.precioSitio.setText(precio)

def ocultarVentanaReserva(self):

    self.cantperso.setValue(0)
   
    Reserva.hide()


def validarDatos(self):

        error = False

        if len(self.intronom.text()) == 0:
            
            self.introduzcanom.setText("*Ingrese su nombre*")
            self.introduzcanom.setStyleSheet("color: red")
            error = True
       
        if len(self.introcedula.text()) == 0:
            self.introduzcacedula.setText("*Ingrese su cédula*")
            self.introduzcacedula.setStyleSheet("color: red")
            error = True
        if len(self.intrnumtelefono.text()) == 0:
            self.introduzcatelefono.setText("*Ingrese su teléfono*")
            self.introduzcatelefono.setStyleSheet("color: red")
            error = True
        if len(self.introedad.text()) == 0:
            self.introduzcaedad.setText("*Ingrese su edad*")
            self.introduzcaedad.setStyleSheet("color: red")
            error = True
        if len(self.intropais.text()) == 0:
            self.introduzcapais.setText("*Ingrese su país*")
            self.introduzcapais.setStyleSheet("color: red")
            error = True
        if len(self.intromail.text()) == 0:
            self.introduzcaEmail.setText("*Ingrese su email*")
            self.introduzcaEmail.setStyleSheet("color: red")
            error = True
        if self.cantperso.value() == 0:
            self.introduzcacantperson.setText("*Ingrese personas*")
            self.introduzcacantperson.setStyleSheet("color: red")
            
            error = True

        if error:
            print("Hay campos que no se han llenado correctamente.")
        else:
        # Aquí puedes guardar los datos o realizar otras acciones
            print("Datos guardados correctamente")
            global totalPersonas
            totalPersonas += self.cantperso.value()
            agregarSubTotal(pantallaReserva)
            

def CrearReservar(self):
        global totalPersonas
    # Obtener los datos de los campos
        self.nombre = self.intronom.text()  # Usamos .text() para obtener el valor del campo
        self.cedula = self.introcedula.text()  # Lo mismo aquí
        self.telefono = self.intrnumtelefono.text()  
        self.sexo = self.escsexo.currentText()  # Usamos currentText() para obtener el valor seleccionado
        self.edad = self.introedad.text()
        self.pais = self.intropais.text()
        self.Email = self.intromail.text()
        self.CantidadPersonas = totalPersonas  # Para QSpinBox usamos .value() en lugar de .text()

    # Validación de los campos
        
        pantallaReserva.cantperso.setValue(0)

        self.nomfac.setText(f"Nombre: {self.nombre}")
        self.cedulafac.setText(f"Cédula: {self.cedula}")
        self.telefonofac.setText(f"Teléfono: {self.telefono}")
        self.sexofac.setText(f"Sexo: {self.sexo}")
        self.edadfac.setText(f"Edad: {self.edad}")
        self.paisfac.setText(f"País: {self.pais}")
        self.mailfac.setText(f"E-mail: {self.Email}")
        self.cantpersonfac.setText(f"Cantidad de personas: {self.CantidadPersonas}")

    # Limpiar los campos si es necesario
        '''self.intronom.setText("")
        self.introcedula.setText("")
        self.intrnumtelefono.setText("")
        self.introedad.setText("")
        self.intropais.setText("")
        self.intromail.setText("")
        self.cantperso.setValue(0)'''

def agregarSubTotal(self):

    global subTotal
    

    
    subTotal += float(precio)*self.cantperso.value() 
    self.subTotalLabel.setText(f'${str(subTotal)}')

    CrearReservar(pantallaReserva)


    subTotal = float(subTotal)



def check_radio(self):
        try:
            if self.radioButton.isChecked():
                print('Usted ha realizado el abono')
            else:
                print('No seleccionó la opción abonar')
        except Exception as e:
            print(f"Error en check_radio: {e}")


# Crear las funciones de validación para cada campo
def validar_nombre(self):
    try:
        nombre = self.intronom.text()
        if len(nombre) > 0:  # Si el campo no está vacío
            self.introduzcanom.setText("")
            self.introduzcanom.setStyleSheet("")

    except Exception as e:
        print(f"Error en validar_nombre: {e}")

def validar_cedula(self):
    try:
        cedula = self.introcedula.text()
        if len(cedula) > 0:  # Si el campo no está vacío
            self.introduzcacedula.setText("")
            self.introduzcacedula.setStyleSheet("")

    except Exception as e:
        print(f"Error en validar_cedula: {e}")

def validar_telefono(self):
    try:
        telefono = self.intrnumtelefono.text()
        if len(telefono) > 0:  # Si el campo no está vacío
            self.introduzcatelefono.setText("")
            self.introduzcatelefono.setStyleSheet("")

    except Exception as e:
        print(f"Error en validar_telefono: {e}")

def validar_edad(self):
    try:
        edad = self.introedad.text()
        if len(edad) > 0:  # Si el campo no está vacío
            self.introduzcaedad.setText("")
            self.introduzcaedad.setStyleSheet("")

    except Exception as e:
        print(f"Error en validar_edad: {e}")

def validar_email(self):
    try:
        email = self.intromail.text()
        if len(email) > 0:  # Si el campo no está vacío
            self.introduzcaEmail.setText("")
            self.introduzcaEmail.setStyleSheet("")

    except Exception as e:
        print(f"Error en validar_email: {e}")

def validar_pais(self):
    try:
        pais = self.intropais.text()
        if len(pais) > 0:  # Si el campo no está vacío
            self.introduzcapais.setText("")
            self.introduzcapais.setStyleSheet("")

    except Exception as e:
        print(f"Error en validar_pais: {e}")

def validar_cantidad_personas(self):
    try:
        if self.cantperso.value() > 0:  # Si la cantidad es válida
            self.introduzcacantperson.setText("")
            self.introduzcacantperson.setStyleSheet("")
        
    except Exception as e:
        print(f"Error en validar_cantidad_personas: {e}")

def cerrarPrograma():
    QApplication.instance().quit()

def mostrarDespedida():


    Despedida.setWindowFlags(Qt.WindowCloseButtonHint)
    Despedida.show()

    QTimer.singleShot(1800, cerrarPrograma)


pantallaReserva.btnDespedida.clicked.connect(mostrarDespedida)


def iniciarApp():

    Presentacion.hide()
    
    QTimer.singleShot(500, lambda: window.showFullScreen())

    

###########################################################
pantallaPresentacion.btnIniciar = QPushButton(pantallaPresentacion.centralwidget)
pantallaPresentacion.btnIniciar.setGeometry(QRect(400, 543, 81, 31))
pantallaPresentacion.btnIniciar.setStyleSheet("background:white")
pantallaPresentacion.btnIniciar.setText("Iniciar")

pantallaPresentacion.btnIniciar.clicked.connect(lambda: iniciarApp())

tituloLabel =  QLabel("PANA-TOUR", window)
tituloLabel.setFont(QFont("Arial", 64, QFont.Bold))
tituloLabel.move(660,90)
tituloLabel.setStyleSheet("background: white; color: black")

bandera = QLabel(window)
bandera.setMinimumSize(QSize(180, 130))
bandera.setMaximumSize(QSize(180, 130))
bandera.setPixmap(QPixmap(f"bandera.png"))
bandera.move(1270,90)
bandera.setScaledContents(True)


salir = QPushButton(f"Salir", window)
salir.move(1800, 50)  
salir.setStyleSheet("background:red")

salir.clicked.connect(lambda: cerrarPrograma())

Presentacion.show()
tourPan.exec_()


