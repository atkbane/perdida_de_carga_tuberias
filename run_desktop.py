"""
main.py
=======
Punto de entrada de la aplicación de cálculo de pérdidas de carga.
"""
import sys
from PySide6.QtWidgets import QApplication
from interfaz import VentanaPerdidaCarga


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    ventana = VentanaPerdidaCarga()
    ventana.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()