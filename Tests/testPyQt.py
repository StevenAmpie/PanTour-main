#Libreria Grafica
from PyQt5.QtWidgets import QApplication,QPushButton, QWidget , QLabel, QVBoxLayout
from PyQt5.QtGui import QIcon,QPixmap
#Libreria para Mapas
import geopandas as gpd

import matplotlib.pyplot as plt

#Genera la Ventana Principal
tourPan = QApplication([])
window = QWidget()




window.showFullScreen()

tourPan.exec_()

# Era pa probar bs de tamaños, pero borre todo