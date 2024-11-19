import cv2
import os
import numpy as np

class Redimensionador:
    """
    Clase que realiza diferentes métodos de redimensionamiento para imágenes.
    """

    def __init__(self, tamaño_objetivo=(256, 256)):
        """
        Inicializa el redimensionador con un tamaño objetivo.
        
        :param tamaño_objetivo: Tupla (ancho, alto) que define el tamaño final de la imagen.
        """
        self.tamaño_objetivo = tamaño_objetivo

    def redimensionar_con_padding(self, imagen):
        """
        Redimensiona la imagen preservando la proporción y agrega padding para alcanzar el tamaño objetivo.
        """
        alto_original, ancho_original = imagen.shape[:2]
        ancho_objetivo, alto_objetivo = self.tamaño_objetivo

        # Calcular proporciones
        ratio_original = ancho_original / alto_original
        ratio_objetivo = ancho_objetivo / alto_objetivo

        # Determinar nueva escala
        if ratio_original > ratio_objetivo:  # Imagen más ancha que el objetivo
            nuevo_ancho = ancho_objetivo
            nuevo_alto = int(ancho_objetivo / ratio_original)
        else:  # Imagen más alta que el objetivo
            nuevo_ancho = int(alto_objetivo * ratio_original)
            nuevo_alto = alto_objetivo

        # Redimensionar la imagen preservando la proporción
        imagen_redimensionada = cv2.resize(imagen, (nuevo_ancho, nuevo_alto))

        # Crear una nueva imagen con fondo negro
        imagen_final = np.zeros((alto_objetivo, ancho_objetivo, 3), dtype=np.uint8)

        # Calcular offset para centrar la imagen redimensionada
        x_offset = (ancho_objetivo - nuevo_ancho) // 2
        y_offset = (alto_objetivo - nuevo_alto) // 2

        # Insertar la imagen redimensionada en el centro
        imagen_final[y_offset:y_offset + nuevo_alto, x_offset:x_offset + nuevo_ancho] = imagen_redimensionada

        return imagen_final

    def cropping_inteligente(self, imagen):
        """
        Recorta la región de interés de la imagen (bounding box) y la redimensiona al tamaño objetivo.
        """
        # Convertir a escala de grises y binarizar
        imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        _, binaria = cv2.threshold(imagen_gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Encontrar contornos
        contornos, _ = cv2.findContours(binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contornos:
            raise ValueError("No se encontraron contornos en la imagen.")

        # Seleccionar el contorno más grande
        contorno_principal = max(contornos, key=cv2.contourArea)

        # Obtener el bounding box que contiene la verdura
        x, y, w, h = cv2.boundingRect(contorno_principal)

        # Recortar la imagen alrededor de la verdura
        imagen_recortada = imagen[y:y + h, x:x + w]

        # Redimensionar la región recortada al tamaño objetivo
        imagen_redimensionada = cv2.resize(imagen_recortada, self.tamaño_objetivo)

        return imagen_redimensionada

    def redimensionar_simple(self, imagen):
        """
        Redimensiona directamente la imagen al tamaño objetivo, sin preservar proporciones.
        """
        return cv2.resize(imagen, self.tamaño_objetivo)

    def procesar_carpeta(self, metodo, carpeta_origen, carpeta_destino):
        """
        Procesa todas las imágenes de las subcarpetas de carpeta_origen según el método de redimensionado
        y guarda los resultados en carpeta_destino.
        """
        # Validar método
        if metodo not in ["padding", "cropping", "simple"]:
            raise ValueError(f"Método no válido: {metodo}. Selecciona: 'padding', 'cropping', 'simple'.")

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

                    # Aplicar el método seleccionado
                    if metodo == "padding":
                        imagen_resultado = self.redimensionar_con_padding(imagen)
                    elif metodo == "cropping":
                        imagen_resultado = self.cropping_inteligente(imagen)
                    elif metodo == "simple":
                        imagen_resultado = self.redimensionar_simple(imagen)

                    # Guardar la imagen redimensionada
                    cv2.imwrite(ruta_imagen_destino, imagen_resultado)
                    print(f"Guardada: {ruta_imagen_destino}")
