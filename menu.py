from Datapar import *


def menu():

    print("""
    *** Menu de opciones ***"
    -----------------------
    Bienvenido, comenzamos? 0
    1. Cargar datos.
    2. Listar cantidad por marca.
    3. Listar insumos por marca.
    4. Buscar insumo por característica.
    5. Listar insumos ordenados.
    6. Realizar compras.
    7. Guardar en formato JSON.
    8. Leer desde formato JSON.
    9. Actualizar precios.
    10. Agregar Marca.
    11. Ingrese de que tipo de formato desea guardar el archivo (csv o json).
    12. Salir""")
    opcion = input("Ingrese una opcion numerica: ")
    return opcion