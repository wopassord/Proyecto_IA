import os
from redimensionador import Redimensionador
from filtrador_gaussiano import FiltradorGaussiano
from color_extractor import ColorExtractor

class ProcesadorImagenes:
    """
    Clase que gestiona el flujo de procesamiento de imágenes.
    """

    def __init__(self, tamaño_objetivo=(256, 256)):
        """
        Inicializa el procesador con redimensionador y filtrador gaussiano.

        :param tamaño_objetivo: Tamaño objetivo de las imágenes redimensionadas.
        """
        self.redimensionador = Redimensionador(tamaño_objetivo=tamaño_objetivo)
        self.filtrador_gaussiano = FiltradorGaussiano()
        self.color_extractor = ColorExtractor()

    def redimensionar_carpeta(self, carpeta_origen, carpeta_destino):
        """
        Redimensiona todas las imágenes en carpeta_origen y las guarda en carpeta_destino.

        :param carpeta_origen: Ruta de la carpeta de entrada.
        :param carpeta_destino: Ruta de la carpeta de salida.
        """
        print("Iniciando redimensionamiento...")
        self.redimensionador.procesar_carpeta("padding", carpeta_origen, carpeta_destino)
        print("Redimensionamiento completado.")

    def aplicar_filtros_gaussianos(self, carpeta_origen, carpeta_destino):
        """
        Aplica filtros pasa bajo y pasa alto a todas las imágenes en carpeta_origen
        y guarda los resultados en carpeta_destino.

        :param carpeta_origen: Ruta de la carpeta de entrada.
        :param carpeta_destino: Ruta de la carpeta de salida.
        """
        print("Iniciando aplicación de filtros gaussianos...")
        self.filtrador_gaussiano.procesar_carpeta(carpeta_origen, carpeta_destino)
        print("Aplicación de filtros gaussianos completada.")

    def extraer_colores(self, carpeta_origen):
        self.color_extractor.procesar_carpeta(carpeta_origen)
