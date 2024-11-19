from redimensionador import Redimensionador

def main():
    # Solicitar al usuario que seleccione el método de redimensionado
    metodo = input("Selecciona el método de redimensionado (padding, cropping, simple): ").strip().lower()
    if metodo not in ["padding", "cropping", "simple"]:
        print("Método no válido. Por favor, selecciona uno de los siguientes: padding, cropping, simple.")
        return

    # Directorios
    carpeta_origen = "C:\\Users\\Bernarda\\Desktop\\Proyecto IA\\DB"
    carpeta_destino = "C:\\Users\\Bernarda\\Desktop\\Proyecto IA\\Test_Redim"

    # Crear una instancia de Redimensionador
    redimensionador = Redimensionador(tamaño_objetivo=(256, 256))

    # Procesar las imágenes
    try:
        redimensionador.procesar_carpeta(metodo, carpeta_origen, carpeta_destino)
        print("Procesamiento completado.")
    except Exception as e:
        print(f"Error durante el procesamiento: {e}")

if __name__ == "__main__":
    main()