import cv2
import os
import numpy as np

class FiltradorGaussiano:
    """
    Clase para aplicar filtros gaussianos pasa bajo y pasa alto a imágenes.
    """

    def __init__(self, kernel_pasa_bajo=(9, 9), kernel_pasa_alto=(5, 5)):
        """
        Inicializa el filtrador gaussiano con tamaños de kernel para pasa bajo y pasa alto.

        :param kernel_pasa_bajo: Tamaño del kernel para el filtro pasa bajo.
        :param kernel_pasa_alto: Tamaño del kernel para el filtro pasa alto.
        """
        self.kernel_pasa_bajo = kernel_pasa_bajo
        self.kernel_pasa_alto = kernel_pasa_alto

    def aplicar_suavizado_y_resaltado(self, imagen):
        """
        Aplica un filtro pasa bajo para suavizar y luego un filtro pasa alto para aumentar el contraste.

        :param imagen: Imagen original (numpy array).
        :return: Imagen procesada (numpy array).
        """
        # Suavizado con filtro pasa bajo
        imagen_suavizada = cv2.GaussianBlur(imagen, self.kernel_pasa_bajo, 0)

        # Aumento de contraste con filtro pasa alto
        imagen_resaltada = cv2.addWeighted(imagen, 1.5, imagen_suavizada, -0.5, 0)

        return imagen_resaltada

    def procesar_carpeta(self, carpeta_origen, carpeta_destino):
        """
        Recorre una carpeta de imágenes, aplica suavizado y resaltado, y guarda los resultados.

        :param carpeta_origen: Ruta de la carpeta de entrada.
        :param carpeta_destino: Ruta de la carpeta de salida.
        """
        # Recorrer todas las subcarpetas y archivos
        for subcarpeta in os.listdir(carpeta_origen):
            ruta_subcarpeta_origen = os.path.join(carpeta_origen, subcarpeta)
            ruta_subcarpeta_destino = os.path.join(carpeta_destino, subcarpeta)

            # Crear la carpeta destino si no existe
            os.makedirs(ruta_subcarpeta_destino, exist_ok=True)

            # Procesar cada archivo de imagen en la subcarpeta
            for archivo in os.listdir(ruta_subcarpeta_origen):
                if archivo.lower().endswith((".jpg", ".jpeg", ".png")):  # Filtrar imágenes
                    ruta_imagen_origen = os.path.join(ruta_subcarpeta_origen, archivo)
                    ruta_imagen_destino = os.path.join(ruta_subcarpeta_destino, archivo)

                    # Cargar la imagen
                    imagen = cv2.imread(ruta_imagen_origen)

                    # Aplicar suavizado y resaltado
                    imagen_procesada = self.aplicar_suavizado_y_resaltado(imagen)

                    # Guardar la imagen procesada
                    cv2.imwrite(ruta_imagen_destino, imagen_procesada)
                    print(f"Guardada imagen procesada: {ruta_imagen_destino}")
