from menu import menu
import csv
import re
import json
import os
import random


def listar(nombre_archivo: str) -> list[dict]:
    lista = []  # Lista vacía que va a almacenar los elementos.

    try: #try para manejar cualquier excepcion.
        with open(nombre_archivo, 'r', encoding='utf-8') as file: 
            lineas = map(lambda linea: linea.strip().split(","), file) #en cada linea elimino los espacios en blaco y separadas en coma, y con map proceso esas lineas incluido el stock.
            for linea in lineas:
                if len(linea) == 5:
                    lista_dicts = {
                        "ID": linea[0],
                        "NOMBRE": linea[1],
                        "MARCA": linea[2],
                        "PRECIO": linea[3],
                        "CARACTERISTICAS": linea[4],
                        "STOCK": random.randint(0, 10) #importo random para poder generar un numero aleatorio.
                    }
                    lista.append(lista_dicts) #agrega los datos correspondientes en base al procesamiento de map en cada linea.
    except Exception:
        print(f"No se pudo abrir el archivo '{nombre_archivo}'.") #si hay error tira excepcion.

    return lista
#--------------------------------------------------------------------------------------------------------------------------------

def marcar_cantidad(lista: list[dict]) -> set:

    marcas = set() #set marcas para almacenar las marcas sin duplicados.

    for diccionario in lista:
        marca = diccionario.get('MARCA') #cada dict, se consigue el valor  de la clave 'MARCA' utilizando  get(). 
        #Si se encuentra un valor válido  se agrega la marca al set.
        if marca:
            marcas.add(marca) #Si se encuentra un valor válido  se agrega la marca al set.

    print("""
---------------------------------- 
Cantidad de elementos por marca:
----------------------------------  
        """)
    for marca in marcas: #itera sobre cada marca en el conjunto marcas.
        cantidad = len(list(filter(lambda x: x.get('MARCA') == marca, lista)))#la función filter junto con una expresión lambda para filtrar los elementos .
        print(f"* {marca} = {cantidad}")

#--------------------------------------------------------------------------------------------------------------------------------

def listar_insumos_por_marca(lista: list[dict]):
    marcas = set()  # Conjunto para almacenar las marcas sin duplicados

    for diccionario in lista:
        marca = diccionario.get('MARCA')  # Obtener el valor del índice 'MARCA' del diccionario
        if marca:  # Verificar si se encontró una marca válida
            marcas.add(marca)  # Agregar la marca al conjunto

    print("""
---------------------------------- 
Listado de insumos por marca:
----------------------------------  
        """)

    for marca in marcas:
        print(f"Marca: {marca}")
        insumos_filtrados = filter(lambda x: x.get('MARCA') == marca, lista)  # Filtrar insumos por marca

        insumos_lista = []  # Lista para almacenar los insumos de la marca actual

        for insumo in insumos_filtrados:
            nombre = insumo.get('NOMBRE')  # Obtener el nombre del insumo
            precio = insumo.get('PRECIO')  # Obtener el precio del insumo

            insumos_lista.append(f"  Nombre: {nombre}, Precio: {precio}")

        print('\n'.join(insumos_lista))  # Imprimir la lista completa de insumos de la marca
        print("." * 90)

#-------------------------------------------------------------------------------------------------------------------------

def buscar(lista: list[dict]):
    coincidencias = [] #Lista que va a recibir todas las coincidencias.

    for producto in lista: #itea en la lista de insumos.
        caracteristicas = producto["CARACTERISTICAS"] #se tiene el value de la clave lo que seria las caracteristicas.
        if re.match(rf'.*\b{clave.lower()}\b.*', caracteristicas.lower()): #el re match lo utilizo para buscar coincidencias por lo que se buscan coincidnecias en la palabra clave.
            coincidencias.append(producto) #cualquier caracteristica lo integro.

    if coincidencias: # si hay coincidencias imprimo toda la informacion.
        print("""
--------------------------------------------
 Coincidencias encontradas con su búsqueda:
--------------------------------------------""")
        
        for producto in coincidencias:
            marca = producto["MARCA"]
            caracteristicas = producto["CARACTERISTICAS"].split("~")
            caracteristicas_juntas = ", ".join(caracteristicas)  # Une las características en una cadena separada por comas
            print(f"Marca: {marca}")
            print(f"Característica: {caracteristicas_juntas}")
            print("." * 130)
    else:
        print("* Lo siento, no se han encontrado coincidencias.") #si no hay caracteristicas mando un mensaje.

#-----------------------------------------------------------------------------------------------------------------------

def ordenar_insumos(lista:list[dict])->list:
    insumos_ordenados = sorted(lista, key=lambda x: (x['MARCA'])) #utilizo el lambda para ejecutar la funcion sorted que me ordena por la marca.
    return insumos_ordenados #retorno esos insumos ordenados.


def listar_insumos_ordenados(lista:list)->list:
    insumos_ordenados = ordenar_insumos(lista) #Paso el resultado que obtuve al ordenarlo por marca.

    print("""
---------------------------------- 
Listado de insumos ordenados:
----------------------------------  
    """)

    for insumo in insumos_ordenados:
        caracteristicas = insumo['CARACTERISTICAS'].split("~")  # Separar las características.
        primera_caracteristica = caracteristicas[0] if caracteristicas else ""  # Obtengo una caracteristica o nada.

        print(f"ID: {insumo['ID']}, Nombre: {insumo['NOMBRE']}, Marca: {insumo['MARCA']}, Precio: {insumo['PRECIO']}, Características: {primera_caracteristica}")
        print("-"*130)

#-----------------------------------------------------------------------------------------------------------------------------

def mostrar_productos_por_marca(lista:list, marca:str)->list:
    productos = filter(lambda producto: producto['MARCA'].lower() == marca.lower(), lista) #utilizo filter para que me filtre todos los elementos por el valor marca, y lo condiciono con un lower.
    return list(productos) #retorno todos esos productos.

def realizar_compras(lista:list)->list:
    carrito_compras = [] #lista de compras vacia.
    total_compra = 0 #el contador de precio lo inicializo a 0.

    while True: #mientras sea verdad.
        marca = input("Ingrese la marca de los productos que desea comprar si desea finalizar o terminar escriba 'salir': ").lower() #Pido que el usuario ingrese la marca.
        if marca.lower() == 'salir': #para terminar con todo el bucle.
            break

        productos = mostrar_productos_por_marca(lista, marca) #llamo a la funcion de mostrar productos.
        if not productos:
            print(f"Lo siento, no se encontraron productos de la marca seleccionada.") #si no se encuentra en la lista se muestra el mensaje.
            continue #si no continuo.

        print("Productos disponibles:") #muestro los productos que hay disponibles en esa marca y su precio.
        for producto in productos:
            print(f"{producto['NOMBRE']} - Precio: {producto['PRECIO']}")

        opcion_elegida = int(input("Ingrese el producto que desea (poner de forma numerica segun el orden de la lista): ")) # el usuario ingresa cual quiere.
        if opcion_elegida < 1 or opcion_elegida > len(productos): #se verifica que la opcion no se exceda los limites.
            print(f"Lo siento, su opcion no se encuentra.")
            continue #sino continuo

        producto_elegido = productos[opcion_elegida - 1] #obtengo la resta de la cantidad  elegido.
        if producto_elegido['STOCK'] == 0: #si el numero random es 0 muestro mensaje.
            print(f"Lo siento, no hay stock disponible del producto seleccionado.")
            continue

        stock_disponible = producto_elegido['STOCK'] #incializo la variable. 
        stock = int(input(f"Ingrese la cantidad deseada: (stock disponible: {stock_disponible}):")) #el usuario ingresa la cantidad.
        if stock > stock_disponible:
            print(f"Lo siento, pero la cantidad excede el stock disponible ({stock_disponible}). Ingrese una cantidad menor.") #si el valor ingresado es mayor muestro mensaje.
            continue #continuo

        precio = (producto_elegido['PRECIO']).replace('$', '') #utilizo el replace asi la forma numerica se separa del signo.
        subtotal = float(precio)* stock #multiplico el precio por cantidad.
        total_compra += subtotal
        producto_elegido['STOCK'] -= stock #esto es para que se actualice el stock dependiendo de la cantidad seleccionada.
        
        carrito_compras.append({ #appendeo al carrito de compras.
            'Producto': producto_elegido['NOMBRE'],
            'Precio': producto_elegido['PRECIO'],
            'Cantidad': stock,
            'Subtotal': subtotal
        })

   
    if carrito_compras: #si hay productos en el carrito muestro el detalle.
         
        print(""" 
--------------------------
   Detalle de su compra:
--------------------------""") #lo muestro por pantalla.
        for item in carrito_compras:
            print(f"Producto: {item['Producto']}, Cantidad: {item['Cantidad']}, Subtotal: {item['Subtotal']}")

        print(f"*Total de la compra--> {total_compra}")

        nombre_factura = generar_nombre_factura()
        generar_factura(nombre_factura, carrito_compras, total_compra) #retorno el generar factura en base a la funcion de hacer un txt.
    else:
        print(f"No se han agregado productos al carrito de compras.") #si no hay productos muestro mensaje.

contador_factura = 0

def generar_nombre_factura() -> str:
    global contador_factura #investigue sobre la variable global y esta en este caso me permite modificar directamente la variable global y no solo la local de la función contar_factura.
    contador_factura += 1 #esto me permite generar nuevas facturas y no sobreescribirlas.
    nombre_factura = f"factura_{contador_factura}.txt"
    return nombre_factura


def generar_factura(nombre_factura: str, carrito_compras:str, total_compra:float):
    with open(nombre_factura, 'w') as file: #abro un file en formato txt.
        file.write("|Factura de su compra|\n")
        file.write("."*50 + "\n")
        for item in carrito_compras: #itero en los productos y muestro todos en la factura.
            file.write(f"--> Producto: {item['Producto']}\nCantidad: {item['Cantidad']}\nSubtotal: {item['Subtotal']}\n")
        file.write(f"*Total de su compra: {total_compra}\n")
    print(f"--> Se ha generado su facturación en el archivo {nombre_factura}. Gracias por su compra.")

#---------------------------------------------------------------------------------------------------------------------------

def guardar_json(rutaJSON: str, lista: list[dict]) -> None: #guardo como json para escritura.
    productos_filtrados = [producto for producto in lista if 'Alimento' in producto['NOMBRE']] #si esta producto con la palabra alimento en nombre los integro.

    with open(rutaJSON, 'w', encoding= 'utf-8') as file:
        json.dump(productos_filtrados, file, indent=4, ensure_ascii=False) #guardo ese producto identado para que quede legible.

ruta_csv = "insumos.csv"  # Ruta del archivo CSV
lista_productos = listar(ruta_csv)  # Obtener la lista de productos desde el archivo CSV

rutaJSON = "insumos.json"
guardar_json(rutaJSON, lista_productos)  # Guardar los productos en formato JSON

def leer_json(ruta: str) -> list[dict]: #para leer el json verifico si existe o no.
    try:
        with open(ruta, 'r') as file:
            productos = json.load(file)
        return productos
    except Exception as e:
        print(f"Error al leer el archivo JSON: {str(e)}")
        return []

#-------------------------------------------------------------------------------------------------------------------------

def aplicar_aumento(producto: dict)-> float: #Aplico aumento al producto de la lista.
    precio_actual = producto['PRECIO'] #consigo el valor del precio.
    precio_dividido = precio_actual.split('$') # separo el numero del precio con el signo.
    if len(precio_dividido) > 1: #si hay signo en el precio separado se fija si es mayor que 1 y aplica aumento.
        numero_precio = float(precio_dividido[1]) #convierte los numeros de precio separado en float.
        precio_actualizado = numero_precio * 1.084 #aplico aumento.
        producto['PRECIO'] = f"${precio_actualizado:.2f}"
    return producto


# Obtener la lista de productos
ruta_csv = 'Insumos.csv' #defino ruta.
lista_productos = listar(ruta_csv) 

# Aplicar el aumento utilizando la función map
lista_productos_actualizados = list(map(aplicar_aumento, lista_productos)) #utilizo map para aplicar el aumento a los productos.

def guardar_csv(ruta: str, lista_productos: list):
    with open(ruta, 'w', newline='', encoding='utf-8') as file:
        # Escribir productos con precios actualizados
        for producto in lista_productos: #se itera sobre la lista de productos.
            linea = f"{producto['ID']},{producto['NOMBRE']},{producto['MARCA']},{producto['PRECIO']},{producto['CARACTERISTICAS']}\n"
            file.write(linea)


ruta_actualizada = 'Insumos_actualizados.csv' # Guardar los productos actualizados en el archivo "Insumos.csv"

#-----------------------------------------------------------------------------------------------------------------------------------

def obtener_id():
    with open(nombre_archivo, 'r') as file:
        lineas = file.readlines() #se leen las lineas del csv.
        ultimo_id = 0
        for linea in lineas[1:]:  #omite la primera línea (encabezados)
            espacios = linea.strip().split(',') #se separana las palabras
            producto_id = int(espacios[0])
            if producto_id > ultimo_id: #verifico si el producto es mayor al id.
                ultimo_id = producto_id
        return ultimo_id + 1
    
def agregar_marca(marca:list)->str: #creo la funcion agregar marcas.
    marcas = [] #lista para guardarlas.
    with open("marcas.txt", "r") as file: #solo para tener el archivo disponible exporto su informacion.
        for linea in file: #recorro y le hago sus respectivos cambios de formato.
            marca = linea.strip()
            marcas.append(marca)
        return marcas

def agregar_producto(lista:list[dict]): #creo la funcion para agregar los productos.
    ultimo_id = obtener_id()
    marcas = agregar_marca(lista)
    print("Marcas con la que dispone--> ")
    for i in range(len(marcas)): #itera sobre la lista de marcas y muestra cada marca junto al indice.
        print(f"{i+1}.{marcas[i]}")
    indice = None
    while True: #Realizo esto para validar de que sea un numero y no otro caracter.
        try:
            indice = int(input("Ingrese el producto segun el orden en el que se encuentra--> "))
            break
        except ValueError:
            print("Ingrese un numero entero.")
    marca = marcas[indice-1] #obtine la marca segun el indice.

    for producto in lista:
        if producto["MARCA"] == marca:
            print("*La marca que ingreso ya se encuentra disponible.") #verifico si tengo la misma marca.
            return
        

    producto_ingresado = { #ingreso todos los datos correspondientes al producto ingresado.
        "ID": str(ultimo_id), "NOMBRE": input("Ingrese el nombre del producto--> ").upper(),"MARCA": marca.upper(),"PRECIO": float(input("Ingrese el precio del producto--> ")),"CARACTERISTICAS": [] #creo una lista vacia en caracteristicas asi verifico la cantidad.
    }

    caracteristicas = int(input("Ingrese cuantas caracteristicas desea ingresar--> ")) #ingreso cuantas caracteristicas.
    if caracteristicas < 1 or caracteristicas > 3: #si la cantidad es menor o mayor a 3 muestro un mensaje.
        print("*Lo siento, se excedio de caracteristicas.")
    else:
        for i in range(caracteristicas): #para cada caracteristica permito en un for ingresar el dato.
            caracteristica = input("Ingrese las caracteristicas--> ").upper()
            producto_ingresado["CARACTERISTICAS"].append(caracteristica)

        lista.append(producto_ingresado) #integro esas caracteristicas y las muestro.
        print("**Ya se realizo la carga**")
            
#------------------------------------------------------------------------------------------------------------------------------------

def guardar_producto_nuevo(lista:list[dict], opcion): #creo la funcion para mostrar el archivo.

    if opcion == "csv nuevo": #dependiendo la opcion que elija el usuario lo voy printear.
       archivo = guardar_producto_csv(lista_insumos)
       print(archivo)
    
    elif opcion == "agregar al csv":
        archivo = agregar_producto_csv(lista_insumos)
        print(archivo)
    
    elif opcion == "json nuevo":
        archivo = guardar_producto_json(lista_insumos)
        print(archivo)

    elif opcion == "agregar al json":
        archivo = agregar_producto_json(lista_insumos)
        print(archivo)
    else:
        print("Reingrese en que formato lo desea: 'csv' o 'json'--> ")

#hago diversos tipos de guardados de archivo en "w" para escribir uno o "a" para juntarlo a otro.

def agregar_producto_csv(lista_insumos:list):
    with open('insumos.csv', 'a') as file: #abro el file en formato csv ya existente con toda la informacion de los productos previos.
        for producto in lista_insumos:
            linea = f"{producto['ID']},{producto['NOMBRE']},{producto['MARCA']},{producto['PRECIO']},{producto['CARACTERISTICAS']}\n"
            file.write(linea)
    print("Datos guardados en formato CSV.") #esto solo agregaria la informacion


def guardar_producto_csv(lista_insumos:list):
    with open('archivoNuevo.csv', 'w') as file: #abro un file en formato csv con la nueva informacion ingresada.
        file.write(f"ID, NOMBRE, MARCA, PRECIO, CARACTERISTICAS")
        for producto in lista_insumos:
            linea = f"{producto['ID']},{producto['NOMBRE']},{producto['MARCA']},{producto['PRECIO']},{producto['CARACTERISTICAS']}\n"
            file.write(linea)
    print("Datos guardados en formato CSV.")


def agregar_producto_json(lista_insumos:list):
    with open('insumos.json', 'a') as file: #abro el file en formato json ya existente para que solo se agregue la informacion.
        json.dump(lista_insumos, file)
        file.write('\n')
    print("Datos guardados en formato Json.")


def guardar_producto_json(lista_insumos:list):
    with open('archivo.json', 'w') as file: #abro un nuevo file en formato json con la nueva infomarcion.
        for producto in lista_insumos:
            json.dump(lista_insumos, file)
            file.write('\n')
    print("Datos guardados en formato Json.")
        
#-------------------------------------------------------------------------------------------------------------
#""Hago todas las llamadas para el menu en base al número de opcion.
flag_bienvenida = False
nombre_archivo = None  # Variable para almacenar el nombre del archivo

while True:
    os.system("cls")

    match(menu()):
            case "0":
                print("Entendido, comencemos.")
                flag_bienvenida = True
            case "1":
                if flag_bienvenida:
                    if nombre_archivo is None:
                        nombre_archivo = input("Ingrese el nombre del archivo: ")
                        insumos = listar(nombre_archivo)
                else:
                    print("Debe poner confirmar para saber más información.")

            case "2":
                if flag_bienvenida:
                    if nombre_archivo is None:
                        print("Debe ingresar un archivo primero.")
                    else:
                        lista = listar(nombre_archivo)  # Pasa una lista vacía como argumento
                        marcar_cantidad(lista)
                        
                else:
                    print("Debe poner confirmar para saber más información.")

            case "3":
                if flag_bienvenida:
                    if nombre_archivo is None:
                        print("Debe ingresar un archivo primero.")
                    else:
                        lista = listar(nombre_archivo)  # Obtener la lista de insumos
                        listar_insumos_por_marca(lista)  # Mostrar los insumos por marca
                else:
                    print("Debe poner confirmar para saber más información.")

            case "4":
                if flag_bienvenida:
                    if nombre_archivo is None:
                        print("Debe ingresar un archivo primero.")
                    else:
                        clave = input("Ingrese la característica que desea buscar --> ")
                        clave = clave.lower()
                        lista = listar(nombre_archivo)
                        buscar(lista)

                else:
                    print("Debe poner confirmar para saber más información.")

            case "5":
                 if flag_bienvenida:
                    if nombre_archivo is None:
                        print("Debe ingresar un archivo primero.")
                    else:
                        lista_insumos = listar(nombre_archivo)  # Lista de insumos.
                        listar_insumos_ordenados(lista_insumos)
                        
                 else:
                     print("Debe poner confirmar para saber más información.")

            case "6":
                if flag_bienvenida:
                    if nombre_archivo is None:
                        print("Debe ingresar un archivo primero.")
                    else:
                        lista = listar(nombre_archivo)  
                        realizar_compras(lista)
                else:
                     print("Debe poner confirmar para saber más información.")

            case "7":
                if flag_bienvenida:
                    guardar_json(rutaJSON, lista_productos)  # Pasar la lista de productos a la función guardar_json  # Ruta donde se guardará el archivo JSON
 
                    print("Archivo JSON generado correctamente.")
                else:
                    print("Debe poner confirmar para saber más información.")

            case "8":
                if flag_bienvenida:
                    ruta_json = input("Ingrese el nombre del archivo JSON que desea leer: ")
                    productos_alimento = leer_json(ruta_json)  # Agrega el argumento "ruta_json"

                    # Mostrar los insumos guardados
                    print("Listado de insumos:")
                    for producto in productos_alimento:
                        print(f"Nombre: {producto['NOMBRE']}, Precio: {producto['PRECIO']}")
                    
                else:
                    print("Debe poner confirmar para saber más información.")

            case "9":
                if flag_bienvenida:
                    if nombre_archivo is None:
                        print("Debe ingresar un archivo primero.")
                    else:           
                        guardar_csv(ruta_actualizada, lista_productos_actualizados)      
                        ruta_actualizada = 'Insumos_actualizados.csv'
                else:
                    print("Debe poner confirmar para saber más información.")
            case "10":
                if flag_bienvenida:
                    if nombre_archivo is None:
                        print("Debe ingresar un archivo primero.")
                    else:
                        lista_insumos = []
                        agregar_producto(lista_insumos)
                
                else:
                    print("Debe poner confirmar para saber más información.")

            case "11":
                if flag_bienvenida:
                    if nombre_archivo is None:
                        print("Debe ingresar un archivo primero.")
                    else:
                        opcion = input("Ingrese el tipo de dato de formato en el que quiere guardar: csv nuevo, json nuevo, agregar al csv o agregar al json--> ")
                        guardar_producto_nuevo(lista_insumos, opcion)
                else:
                    print("Debe poner confirmar para saber más información.")
        
            case "12":
                if nombre_archivo is None:
                    print("Debe ingresar un archivo primero.")
                else:
                    salir = input("confirma salida? 01: ")
                    if(salir == "01"):
                        break
    input("Presione enter para continuar")

