import cv2
import os
import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class ColorExtractor:
    """
    Clase para extraer el promedio de color RGB de una verdura, excluyendo el fondo,
    y almacenar los resultados en un archivo CSV.
    """

    def __init__(self, saturacion_aumento=1.5, archivo_salida="colores.csv"):
        """
        Inicializa el extractor con parámetros de saturación y archivo de salida.

        :param saturacion_aumento: Factor por el cual aumentar la saturación de la imagen.
        :param archivo_salida: Nombre del archivo CSV donde se almacenarán los resultados.
        """
        self.saturacion_aumento = saturacion_aumento
        self.archivo_salida = archivo_salida

        # Crear o sobrescribir el archivo CSV con la cabecera
        with open(self.archivo_salida, mode='w', newline='') as file:
            escritor = csv.writer(file)
            escritor.writerow(["NombreImagen", "Promedio_R", "Promedio_G", "Promedio_B"])

    def aumentar_saturacion(self, imagen):
        """
        Aumenta la saturación de una imagen en el espacio de color HSV.

        :param imagen: Imagen original en formato BGR.
        :return: Imagen con saturación aumentada.
        """
        hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        s = np.clip(s * self.saturacion_aumento, 0, 255).astype(np.uint8)
        hsv_aumentado = cv2.merge([h, s, v])
        return cv2.cvtColor(hsv_aumentado, cv2.COLOR_HSV2BGR)

    def generar_mascara_por_contornos(self, imagen):
        """
        Genera una máscara binaria basada en contornos para segmentar la verdura.

        :param imagen: Imagen original en formato BGR.
        :return: Máscara binaria donde los píxeles de la verdura son blancos.
        """
        # Convertir la imagen a escala de grises
        imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

        # Aplicar un desenfoque para suavizar bordes
        imagen_suavizada = cv2.GaussianBlur(imagen_gris, (5, 5), 0)

        # Detectar bordes con Canny
        bordes = cv2.Canny(imagen_suavizada, 50, 150)

        # Encontrar contornos en la imagen de bordes
        contornos, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Seleccionar el contorno más grande
        if not contornos:
            return np.zeros_like(imagen_gris)
        contorno_principal = max(contornos, key=cv2.contourArea)

        # Crear una máscara vacía y rellenar el contorno
        mascara = np.zeros_like(imagen_gris)
        cv2.drawContours(mascara, [contorno_principal], -1, 255, thickness=cv2.FILLED)

        return mascara

    def calcular_promedio_rgb(self, imagen, mascara):
        """
        Calcula el valor promedio de RGB usando una máscara binaria.

        :param imagen: Imagen original en formato BGR.
        :param mascara: Máscara binaria donde los píxeles de interés son blancos.
        :return: Diccionario con los valores promedio de R, G y B.
        """
        imagen_mascarada = cv2.bitwise_and(imagen, imagen, mask=mascara)
        valores_r = imagen_mascarada[:, :, 2][mascara > 0]
        valores_g = imagen_mascarada[:, :, 1][mascara > 0]
        valores_b = imagen_mascarada[:, :, 0][mascara > 0]
        promedio_r = np.mean(valores_r) if len(valores_r) > 0 else 0
        promedio_g = np.mean(valores_g) if len(valores_g) > 0 else 0
        promedio_b = np.mean(valores_b) if len(valores_b) > 0 else 0
        return {"R": promedio_r, "G": promedio_g, "B": promedio_b}

    def procesar_carpeta(self, carpeta_origen):
        """
        Recorre una carpeta de imágenes, extrae el promedio de color RGB de cada imagen
        y almacena los resultados en el archivo CSV.

        :param carpeta_origen: Ruta de la carpeta con las imágenes a procesar.
        """
        for subcarpeta in os.listdir(carpeta_origen):
            ruta_subcarpeta = os.path.join(carpeta_origen, subcarpeta)

            if os.path.isdir(ruta_subcarpeta):
                for archivo in os.listdir(ruta_subcarpeta):
                    if archivo.lower().endswith((".jpg", ".jpeg", ".png")):
                        ruta_imagen = os.path.join(ruta_subcarpeta, archivo)

                        # Cargar la imagen
                        imagen = cv2.imread(ruta_imagen)

                        # Aumentar saturación
                        imagen_saturada = self.aumentar_saturacion(imagen)

                        # Generar máscara por contornos
                        mascara = self.generar_mascara_por_contornos(imagen)

                        # Calcular promedio RGB
                        promedio_rgb = self.calcular_promedio_rgb(imagen_saturada, mascara)

                        # Guardar resultados en el CSV
                        with open(self.archivo_salida, mode='a', newline='') as file:
                            escritor = csv.writer(file)
                            escritor.writerow([archivo, promedio_rgb["R"], promedio_rgb["G"], promedio_rgb["B"]])

                        print(f"Procesada imagen: {archivo}, Promedio RGB: {promedio_rgb}")
    def plotear_rgb(self):
        """
        Lee el archivo colores.csv, genera un array con los puntos RGB,
        y plotea un gráfico 3D donde cada punto corresponde a una imagen.
        """
        # Leer el archivo CSV
        if not os.path.exists(self.archivo_salida):
            print(f"El archivo {self.archivo_salida} no existe. Por favor, genera el archivo primero.")
            return
        
        # Cargar datos desde el CSV
        df = pd.read_csv(self.archivo_salida)

        # Extraer columnas de R, G, B
        R = df['Promedio_R']
        G = df['Promedio_G']
        B = df['Promedio_B']

        # Crear el gráfico 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Scatter plot en 3D
        scatter = ax.scatter(R, G, B, c=list(zip(R / 255, G / 255, B / 255)), s=50)

        # Etiquetas
        ax.set_xlabel('Red (R)')
        ax.set_ylabel('Green (G)')
        ax.set_zlabel('Blue (B)')
        ax.set_title('Gráfico 3D de Colores Promedio (RGB)')

        # Mostrar el gráfico
        plt.show()
    
    def visualizar_mascaras(self, carpeta_origen, carpeta_destino_mascaras=None):
        """
        Genera y visualiza las máscaras binarias para las imágenes de una carpeta.
        Superpone las máscaras sobre las imágenes originales para validación visual.
        Opcionalmente, guarda las máscaras en un directorio.

        :param carpeta_origen: Ruta de la carpeta con las imágenes originales.
        :param carpeta_destino_mascaras: Ruta para guardar las máscaras superpuestas (opcional).
        """
        for subcarpeta in os.listdir(carpeta_origen):
            ruta_subcarpeta = os.path.join(carpeta_origen, subcarpeta)

            if os.path.isdir(ruta_subcarpeta):
                for archivo in os.listdir(ruta_subcarpeta):
                    if archivo.lower().endswith((".jpg", ".jpeg", ".png")):  # Filtrar imágenes
                        ruta_imagen = os.path.join(ruta_subcarpeta, archivo)

                        # Cargar la imagen
                        imagen = cv2.imread(ruta_imagen)

                        # Generar máscara binaria
                        mascara = self.generar_mascara_por_contornos(imagen)

                        # Convertir la máscara a 3 canales para superposición
                        mascara_color = cv2.cvtColor(mascara, cv2.COLOR_GRAY2BGR)

                        # Superponer la máscara sobre la imagen original
                        superpuesta = cv2.addWeighted(imagen, 0.7, mascara_color, 0.3, 0)

                        # Mostrar la imagen original, la máscara y la superposición
                        cv2.imshow("Imagen Original", imagen)
                        cv2.imshow("Máscara Binaria", mascara)
                        cv2.imshow("Superposición", superpuesta)

                        # Guardar la superposición si se especifica un destino
                        if carpeta_destino_mascaras:
                            ruta_destino_superpuesta = os.path.join(carpeta_destino_mascaras, archivo)
                            os.makedirs(os.path.dirname(ruta_destino_superpuesta), exist_ok=True)
                            cv2.imwrite(ruta_destino_superpuesta, superpuesta)
                            print(f"Superposición guardada en: {ruta_destino_superpuesta}")

                        # Esperar interacción del usuario antes de continuar
                        cv2.waitKey(0)

        # Cerrar todas las ventanas al finalizar
        cv2.destroyAllWindows()