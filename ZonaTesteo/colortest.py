import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class ColorExtractor:
    def __init__(self, kernel_size_pasa_bajo=(11, 11), kernel_size_pasa_alto=(11, 11)):
        """
        Inicializa el extractor de color con filtros gaussianos.
        
        :param kernel_size_pasa_bajo: Tamaño del kernel para filtro pasa bajo.
        :param kernel_size_pasa_alto: Tamaño del kernel para filtro pasa alto.
        """
        self.kernel_size_pasa_bajo = kernel_size_pasa_bajo
        self.kernel_size_pasa_alto = kernel_size_pasa_alto

    def preprocesar_imagen(self, imagen):
        """
        Aplica filtros pasa bajo y pasa alto para suavizar y mejorar el contraste.
        
        :param imagen: Imagen original.
        :return: Imagen preprocesada.
        """
        # Filtro pasa bajo (suavizado)
        suavizada = cv2.GaussianBlur(imagen, self.kernel_size_pasa_bajo, 0)
        
        # Filtro pasa alto (resaltado de bordes)
        resaltada = cv2.addWeighted(imagen, 2.5, suavizada, -0.9, 0)
        
        return resaltada

    def generar_mascara(self, imagen):
        """
        Genera una máscara binaria basada en el contorno principal de la verdura.
        
        :param imagen: Imagen preprocesada.
        :return: Máscara binaria.
        """
        # Convertir a espacio de color HSV
        hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

        # Usar el canal de saturación para segmentar
        saturacion = hsv[:, :, 1]

        # Aplicar un umbral adaptativo en el canal de saturación
        _, umbral = cv2.threshold(saturacion, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Mostrar el umbral para depuración
        cv2.imshow("Umbral", umbral)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Encontrar contornos en el umbral
        contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Crear una máscara vacía
        mascara = np.zeros_like(saturacion)

        # Dibujar el contorno más grande en la máscara
        if contornos:
            contorno_principal = max(contornos, key=cv2.contourArea)
            area = cv2.contourArea(contorno_principal)

            # Filtrar contornos pequeños
            if area > 500:  # Ajusta el valor mínimo de área según tus imágenes
                cv2.drawContours(mascara, [contorno_principal], -1, 255, thickness=cv2.FILLED)
            else:
                print("No se encontró un contorno suficientemente grande.")

        # Mostrar la máscara para depuración
        cv2.imshow("Máscara Generada", mascara)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return mascara


    def calcular_rgb_promedio(self, imagen_original, mascara):
        """
        Calcula el color promedio RGB de la verdura y lo grafica en 3D.
        
        :param imagen_original: Imagen original.
        :param mascara: Máscara binaria.
        """
        # Aplicar la máscara a la imagen original
        imagen_mascarada = cv2.bitwise_and(imagen_original, imagen_original, mask=mascara)

        # Obtener únicamente los píxeles donde la máscara es blanca (valor 255)
        pixels_verdura = imagen_original[mascara == 255]

        # Verificar si hay píxeles válidos
        if pixels_verdura.size == 0:
            print("No se encontraron píxeles para calcular el promedio RGB.")
            return

        # Calcular el promedio RGB
        promedio_rgb = np.mean(pixels_verdura, axis=0)

        # Graficar en 3D el promedio RGB
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Normalizar el color para matplotlib
        color_promedio = [valor / 255 for valor in promedio_rgb]

        ax.scatter(promedio_rgb[2], promedio_rgb[1], promedio_rgb[0],  # OpenCV usa BGR, invertimos para RGB
                c=[color_promedio], s=200, edgecolor='k')
        ax.set_xlim(0, 255)
        ax.set_ylim(0, 255)
        ax.set_zlim(0, 255)
        ax.set_xlabel('R')
        ax.set_ylabel('G')
        ax.set_zlabel('B')
        ax.set_title('Color promedio RGB')

        plt.show()


    def mostrar_resultados(self, imagen_original, mascara):
        """
        Muestra la imagen original, la máscara, y la superposición de ambas.
        También plotea el punto RGB promedio con el color correspondiente.
        
        :param imagen_original: Imagen original.
        :param mascara: Máscara binaria.
        """
        # Aplicar la máscara para generar la superposición
        superpuesta = cv2.bitwise_and(imagen_original, imagen_original, mask=mascara)

        # Calcular el promedio RGB usando la máscara
        indices = np.where(mascara == 255)
        promedio_rgb = [
            np.mean(imagen_original[indices][:, i]) for i in range(3)
        ]

        # Normalizar el color para matplotlib (escala [0, 1])
        color_promedio = [valor / 255 for valor in promedio_rgb]

        # Mostrar las imágenes
        plt.figure(figsize=(16, 4))
        
        plt.subplot(1, 4, 1)
        plt.imshow(cv2.cvtColor(imagen_original, cv2.COLOR_BGR2RGB))
        plt.title('Imagen Original')
        plt.axis('off')

        plt.subplot(1, 4, 2)
        plt.imshow(mascara, cmap='gray')
        plt.title('Máscara Generada')
        plt.axis('off')

        plt.subplot(1, 4, 3)
        plt.imshow(cv2.cvtColor(superpuesta, cv2.COLOR_BGR2RGB))
        plt.title('Superposición')
        plt.axis('off')

        # Gráfico 3D del promedio RGB
        ax = plt.subplot(1, 4, 4, projection='3d')
        ax.scatter(promedio_rgb[0], promedio_rgb[1], promedio_rgb[2], 
                c=[color_promedio], s=100)  # El color del punto corresponde al promedio RGB
        ax.set_xlim(0, 255)
        ax.set_ylim(0, 255)
        ax.set_zlim(0, 255)
        ax.set_xlabel('R')
        ax.set_ylabel('G')
        ax.set_zlabel('B')
        ax.set_title('Promedio RGB')

        plt.tight_layout()
        plt.show()


# Ejemplo de uso
if __name__ == "__main__":
    # Cargar la imagen
    ruta_imagen = "C:\\Users\\Bernarda\\Desktop\\Proyecto IA\\DB\\Zanahoria\\zanahoria13.jpg"
    imagen = cv2.imread(ruta_imagen)

    if imagen is None:
        print("Error al cargar la imagen.")
    else:
        extractor = ColorExtractor()

        # Preprocesar la imagen
        imagen_preprocesada = extractor.preprocesar_imagen(imagen)

        # Generar máscara basada en el contorno
        mascara = extractor.generar_mascara(imagen_preprocesada)

        # Calcular el promedio RGB y graficar
        extractor.calcular_rgb_promedio(imagen, mascara)

        # Mostrar resultados
        extractor.mostrar_resultados(imagen, mascara)
