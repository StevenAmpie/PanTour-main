#Test de ventana emergente para mostrar porv y sus opciones turisteicas
#Libreria Grafica
from PyQt5.QtWidgets import QApplication,QPushButton, QWidget , QLabel, QVBoxLayout , QDialog , QGridLayout , QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon,QPixmap,QRegion, QPainterPath
import json



#Genera la Ventana Principal
tourPan = QApplication([])
window = QWidget()
window.showFullScreen()
 
layout = QVBoxLayout()
button = QPushButton("Ventana Emergente")
layout.addWidget(button) 


window.setLayout(layout)  # Asignar el layout a la ventana principal
window.show()


with open('ProvinciasTest.json', 'r' , encoding = 'utf-8') as provfile:
    provsData = json.load(provfile)


#Crea caja para alinear elementos
def contentBox():#Colocar de para metros el nombre del lugar turistico y la img 
    ventanaAux = QWidget()
    contentBox = QVBoxLayout(ventanaAux)
    label = QLabel("Label")
    button = QPushButton("Boton")
    
    contentBox.addWidget(label)
    contentBox.addWidget(button)
    
    return ventanaAux
    
    
#Ventana emergente para mostrar provincia y sus opciones turisticas
def ventanaEmergente():
    
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
    nombreLabel = QLabel("Nombre Prov")
    descripLabel = QLabel("Descripcion")
    
    veLayout.addWidget(nombreLabel,0,0,1,2,alignment=Qt.AlignCenter)
    veLayout.addWidget(descripLabel,1,0,1,2,alignment=Qt.AlignCenter)
  
    
    for row in range(2):
        for col in range(2):
            veLayout.addWidget(contentBox(),row+2,col)
    
    ventanaEmergente.setLayout(veLayout)
   
    ventanaEmergente.exec_()
    
    


button.clicked.connect(ventanaEmergente)


window.show()

tourPan.exec_()