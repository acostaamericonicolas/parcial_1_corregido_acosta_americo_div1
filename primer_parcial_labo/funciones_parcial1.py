import json
import csv
import os
import random, sys

lista=[]
lista_marca=[]
lista_elementos_con_marca_nueva = []
lista_insumos_act=[]

def mostrar_menu(): #Menu del programa
    opcion=""
    print("****************** MENU *****************")
    print("1 - Cargar datos desde archivo") #Esta opción permite cargar el contenido del archivo "Insumos.csv" en una colección
    print("2 - Listar cantidad por marca")
    print("3 - Listar insumos por marca")
    print("4 - Buscar insumo por característica")
    print("5 - Listar insumos ordenados")# ASCENDENTE ante marcas iguales, por precio descendente.
    print("6 - Realizar compras")
    print("7 - Guardar en formato JSON") #Genera un archivo JSON con todos los productos cuyo nombre contiene la palabra Alimento"
    print("8 - Leer desde formato JSON")# y listar insumos"
    print("9 - Actualizar precios")
    print("10 - Agregar un nuevo producto a la lista")
    print("11 - Guardar todos los datos actualizados incluye las altas (.csv o .json)")
    print("12 - mostrar el stock total de los productos de La marca ingresada.")
    print("13 - Imprimir bajo stock en csv (2 o menos en stock)")
    print("14 - Salir del programa")
    print("****************** MENU *****************")
    while True:
        opcion = input("Ingrese una opción para continuar: ")
        if opcion.isdigit() and 1 <= int(opcion) <= 14:
            break
        else:
            print("Error: Ingrese nuevamente una opción válida (1 al 14).")
    return opcion

#Muestra todas las marcas y la cantidad .de insumos correspondientes a cada una
def mostrar_cantidad_por_marca(lista:list, key):
    lista_marca = []
    for elemento in lista:
        lista_marca.append(elemento[key].lower())
    lista_marca_sin_repetir=set(lista_marca)
    print("----------------------------------------------------")
    print(f'{"MARCA".ljust(24)} {"CANTIDAD".ljust(5)}')
    print("----------------------------------------------------")
    for marca in lista_marca_sin_repetir:
        retepiciones=lista_marca.count(marca)
        if retepiciones>1:
            #print(marca, "tiene", retepiciones, "insumos")
            
            print(f'{str(marca).ljust(24)} {str(retepiciones).ljust(5)}')
        else:
            #print(marca, "tiene", retepiciones, "insumo")
            print(f'{str(marca).ljust(24)} {str(retepiciones).ljust(5)}')
            #print(f'{marca:15} {"tiene"} {retepiciones:2} {"insumo."}')
    print("----------------------------------------------------")
#---------------- 3 ----------------------
#PARA CADA MARCA: EL NOMBRE Y PRECIO DE LOS INSUMOS

def mostrar_marca_y_precios(lista:list, key):
    for elemento in lista:
        lista_marca.append(elemento[key].lower())
    lista_marca_sin_repetir=set(lista_marca)
    for marca in lista_marca_sin_repetir:
        print("\n-",str(marca).upper(),"--->\n")
        for elemento in lista:
            if marca == elemento[key].lower():
                nombre = elemento["NOMBRE"]
                precio = elemento["PRECIO"]
                print(f'{str(nombre).ljust(24)} {str(precio).ljust(5)}')
    print("\n")

#El usuario ingresa una característica (por ejemplo, "Sin Granos") 
#y se listarán todos los insumos que poseen dicha característica

def mostrar_por_caracteristica(lista:list, key):
    caracteristica_ingresada=input("ingrese caracteristica: ")
    #validar ingreso de caracteristica
    validacion=0
    while validacion==0 or caracteristica_ingresada == "":
        for elemento in lista:
            if str(caracteristica_ingresada).lower() in str(elemento[key]).lower():
                validacion+=1
        if validacion==0 or caracteristica_ingresada == "":
            caracteristica_ingresada=input("Error! ingrese caracteristica: ")
        else:
            break
    print("-------------------------------------------------------")        
    print("-------- CARACTERISTICA INGRESADA -> ", str(caracteristica_ingresada).lower())
    print("-------------------------------------------------------")  
    for elemento in lista:
        if str(caracteristica_ingresada).lower() in str(elemento[key]).lower():
            print(f'{"*"} {elemento["NOMBRE"]}   {elemento["PRECIO"]}   {elemento["CARACTERISTICAS"]}')
    print("-------------------------------------------------------")  
        
#ordenados por marca de forma ascendente (A-Z) y, ante marcas iguales, por precio descendente.
def ordenar_listas_dict(lista: list, key: str, ascendente=True)->list:
    tamaño_lista = len(lista)
    for i in range(tamaño_lista-1):
        for j in range(i+1, tamaño_lista):
            if (lista[i][key]).isdigit():
                if (ascendente and float(lista[i][key]) > float(lista[j][key])) or (not ascendente and float(lista[i][key]) < float(lista[j][key])):
                    aux = lista[i] 
                    lista[i] = lista[j]  
                    lista[j] = aux
            else:
                if (ascendente and lista[i][key] > lista[j][key]) or (not ascendente and lista[i][key] < lista[j][key]):
                    aux = lista[i] 
                    lista[i] = lista[j]  
                    lista[j] = aux
    for i in range(tamaño_lista-1):
        for j in range(i+1, tamaño_lista):
            if (lista[i][key]==lista[j][key] and lista[i]["PRECIO"]<lista[j]["PRECIO"]):
                    aux = lista[i] 
                    lista[i] = lista[j]  
                    lista[j] = aux
    print("------------------------------------------------------------------------")
    print(f'{"*"}{"  MARCA".ljust(24)} {"PRECIO".rjust(5)} {"CARACTERISTICA".rjust(35)}')
    print("------------------------------------------------------------------------")

    for elemento in lista:
        caracteristica=elemento["CARACTERISTICAS"]
        caracteristica = caracteristica.split("~", 1)
        if len(caracteristica) > 1:
            resultado = caracteristica[0]
        else:
            resultado = caracteristica
        marca = elemento["MARCA"]
        precio = elemento["PRECIO"]
        #print(f'{"*"} {elemento["MARCA"]}    {elemento["PRECIO"]}    {resultado}')
        print(f'{"*"}{marca.ljust(24)} {str(precio).rjust(5)} {str(resultado).rjust(35)}')
        
    print("------------------------------------------------------------------------")
#Leer desde formato JSON: Permite mostrar un listado de los insumos guardados en el archivo JSON generado en la opción anterior.
def mostrar_elementos_js(lista:list)->list:
    with open("primer_parcial_labo\productos.json", "r") as file: #abro el archivo productos.js, lo recorro y convierto en lista de diccionarios 
        lista = []
        lista_elementos0 = []
        lista_elementos_js = []
        for linea in file: 
            lista.append(linea.replace("\n", ""))
        for linea in lista:
            lista_elementos0.append(linea.split(","))
        for elemento in lista_elementos0:
            lista_elementos_js.append({"ID": elemento[0], "NOMBRE": elemento[1],
                                "MARCA": elemento[2], "PRECIO": elemento[3], "CARACTERISTICAS": elemento[4]})
    print(lista_elementos_js)

#Actualizar precios: Aplica un aumento del 8.4% a todos los productos Los productos actualizados se guardan en el archivo "Insumos.csv".
def actualizar_precios(lista:list, key:str, porcentaje:float)->list:

    for elemento in lista:
        print(f"{'Precio anterior: '}             {elemento[key]}")
        elemento[key]=str(elemento[key]).replace("$","")
        elemento[key]=float(elemento[key])+(float(elemento[key])*porcentaje/100)
        #print(f"{'Precio con aumento del: '} {porcentaje}{'%'} {'$'}{elemento[key]:2f}")

def hacer_compras(lista):
    total = 0
    with open("primer_parcial_labo\compras.txt", "a") as file:
        file.write("\n------------------------------------------------------------------------------\n")
        file.write("                           FACTURA DE COMPRA\n")
        file.write(
            "\nCANTIDAD                   PRODUCTO/MARCA                     SUBTOTAL                    \n")
        file.write("\n")
        while True:
            # dato = input("Ingrese un dato (o escriba 'salir' para terminar): ")
            coincidencia = 0
            print("\n")
            marca_ingresada = input("ingrese marca: (o para terminar compra 'salir'): ").lower()
            print("\n")
            for elemento in lista:
                if (marca_ingresada == str(elemento["MARCA"]).lower()):
                    coincidencia += 1
            while (coincidencia == 0 and marca_ingresada != "salir"):
                print("\n")
                marca_ingresada = input(
                    "ERROR: ingrese marca de la lista (o para terminar compra 'salir'): ")
                print("\n")
                for elemento in lista:
                    if ((marca_ingresada == str(elemento["MARCA"]).lower()) or marca_ingresada == "salir"):
                        coincidencia += 1
            if marca_ingresada == 'salir':
                file.write(
                    "\n" + "TOTAL A PAGAR                                                $"+str(total)+"\n")
                file.close
                break
        # declaro la lista donde voy a appendear los id que coincidan con la caracteristica ingresada
            lista_id_caracteristica = []
            for elemento in lista:
                # appendeo los id que coincidan con la caracteristica
                if str(marca_ingresada) in str(elemento["MARCA"]).lower():
                    lista_id_caracteristica.append(elemento["ID"])

                    print("N° de producto:", str(elemento["ID"]), ",", str(elemento["NOMBRE"]),",", str(elemento["PRECIO"]))
            print("\n")
            producto_id = input("ingrese numero del producto: ")
            print("\n")
        # valido que numero de producto este en la lista id y que no sea alfabetico
            while ((producto_id not in lista_id_caracteristica) or producto_id.isalpha()):
                print("\n")
                producto_id = input("Error, ingrese numero del producto: ")
                print("\n")
            for elemento in lista:
                if elemento["ID"] == producto_id:
                    precio_producto = elemento["PRECIO"]
                    producto = elemento["NOMBRE"]
                    stock = elemento["stock"]
                    precio_producto = precio_producto.replace("$", "")
                    precio_producto = float(precio_producto)
                    if stock == 0:
                        print("No hay stock, ingrese otro producto.")
                    else:
                        print("El precio del producto es: $", str(precio_producto), "y el stock disponible es:", stock)
            print("\n")
            cantidad = "0"
            if stock != 0:
                cantidad = input("ingrese cantidad: ")
            # valido que la cantidad de productos este dentro del stock y que no sea alfabetico
            while ((cantidad.isalpha()) or (int(cantidad) > stock)):
                if stock == 0:
                    print("no hay stock, ingrese otro producto.")
                    break
                else:
                    print("\n")
                    cantidad = input("Error, ingrese una cantidad menor a " + str(stock) + ": ")
                    print("\n")
            for elemento in lista:
                if producto_id == elemento["ID"]:
                    elemento["stock"] = int(elemento["stock"]) - int(cantidad)

            cantidad = int(cantidad)
            subtotal = precio_producto*cantidad
            total += subtotal
            file.write(str(cantidad) + "                   " + producto +
                        ", " + marca_ingresada + "          " + str(subtotal) + "\n")
    with open("primer_parcial_labo\compras.txt", "r") as file:
        for linea in file.readlines():
            print(linea)

def obtener_productos_json ():
    with open("primer_parcial_labo\productos.json", "w", encoding="utf-8") as file:
        # with open("primer_parcial_labo\productos.json", "a", encoding="utf-8") as file:
        #     file.write("[")
        # copie el insumos.csv a un .json
        # abro "insumos.csv" modo lectura para obtener los insumos
        with open("primer_parcial_labo\insumos.csv", "r", encoding="utf-8") as file:
            for linea in file:
                linea = linea.lower()
                # filtrando los que tienen la palabra "alimento"
                lista = []
                lista_elementos0 = []
                lista_elementos = []
                for linea in file:
                    lista.append(linea.replace("\n", ""))
                for linea in lista:
                    lista_elementos0.append(linea.split(","))
                for elemento in lista_elementos0:
                    
                    if "alimento" in str(elemento).lower():
                        # lista_elementos.append({"ID": elemento[0], "NOMBRE": elemento[1],
                        #                         "MARCA": elemento[2], "PRECIO": elemento[3], "CARACTERISTICAS": elemento[4]})
                        elemento = ({   
                            "ID": elemento[0], 
                            "NOMBRE": elemento[1],
                            "MARCA": elemento[2], 
                            "PRECIO": elemento[3], 
                            "CARACTERISTICAS": elemento[4]
                        })
                        with open("primer_parcial_labo\productos.json", "a", encoding="utf-8") as file:
                            json.dump(elemento, file)
                            file.write("\n")
    print("-----------------------------")
    print("Se guardo como archivo JSON")
    print("-----------------------------")

def leer_desde_json():
    with open("primer_parcial_labo\productos.json", "r", encoding="utf-8") as file:
        print(f'{"------------------------------------------------------------------------------------------------------------------------"}')
        #print(f'{"MARCA"}            {"NOMBRE"}          {"PRECIO"}            {"CARACTERISTICAS"}')
        print(f'{"*"} {"MARCA".ljust(24)}   {"NOMBRE".ljust(32)}   {"PRECIO".ljust(20)} {"CARACTERISTICAS"}')
        print(f'{"------------------------------------------------------------------------------------------------------------------------"}')
        for linea in file:
            #print(linea)
            elemento = json.loads(linea) #convierto la linea en un diccionario
            print(f'{"*"} {str(elemento["MARCA"]).ljust(24)}   {str(elemento["NOMBRE"]).ljust(32)}   {str(elemento["PRECIO"]).ljust(10)} {elemento["CARACTERISTICAS"]}')
        print(f'{"------------------------------------------------------------------------------------------------------------------------"}')
            
def actualizar_precios_():
    with open("primer_parcial_labo\insumos.csv", "r", encoding="utf-8") as file:
        lista = []
        lista_elementos0 = []
        lista_elementos = []
        diccionario = {}
        for linea in file:
            lista.append(linea.replace("\n", ""))
        for linea in lista:
            lista_elementos0.append(linea.split(","))
        # hago una funcion nueva con MAP recorriendo "lista_elementos0" y le doy el formato dict con las claves por cada indice de la lista y ademas,
        # directamente paso a float el PRECIO que es con el que vouy a hacer cuentas.
        lista_elementos = list(map(lambda elemento: {"ID": elemento[0], "NOMBRE": elemento[1], "MARCA": elemento[2], "PRECIO": float(
            elemento[3].replace("$", "")), "CARACTERISTICAS": elemento[4]}, lista_elementos0))

        with open("primer_parcial_labo\insumos.csv", "w", encoding="utf-8") as file:
            for elemento in lista_elementos:
                porcentaje = 8.4

                elemento["PRECIO"] = elemento["PRECIO"] + \
                    (elemento["PRECIO"]*porcentaje/100)

                file.write(
                    f'{elemento["ID"]}{","}{elemento["NOMBRE"]}{","}{elemento["MARCA"]}{",$"}{elemento["PRECIO"]:.2f}{","}{elemento["CARACTERISTICAS"]}\n')
            print(
                "se realizo incremento del 8.4'%' a los precios. y se guardo en archivo insumos.csv")
            
def agregar_nuevo_producto(lista):
    with open("primer_parcial_labo\marcas.txt", "r", encoding="utf-8") as file:
        # diccionarios
        
        lista_marcas_nuevas=[]
        diccionario = {}
        for linea in file:
            lista_marcas_nuevas.append((linea.replace("\n","")).lower())
        print("Las marcas disponibles son:\n")
        for marca in lista_marcas_nuevas:
            print(marca)
        print("\n")
        marca_ingresada=input("ingrese una marca de las listadas: ").lower()
        while True:
            if (marca_ingresada.isdigit() or (marca_ingresada not in lista_marcas_nuevas)):
                print("Las marcas disponibles son:\n")
                for marca in lista_marcas_nuevas:
                    print(marca)
                print("\n")
                marca_ingresada=input("ingrese una marca de las listadas: ").lower()
            else:
                break
        print("Marca OK\n")
        lista_id=[]
        for elementos in lista:
            lista_id.append(elementos["ID"])
        # id=input("Ingrese ID del producto: ")

        id=random.randint(1,200)
        while id in lista_id:
            #id=input("ID existente, Ingrese ID valido: ")
            id=random.randint(1,200)

        nombre=input("Ingrese nombre del producto: ")
        while (not nombre.isalpha()):
            nombre=input("ERROR! Ingrese un nombre de producto correcto: ")
        precio=input("Ingrese precio del producto: $")
        while (not precio.isdigit()):
            precio=input("ERROR! Ingrese un precio de producto correcto: ")
        cont_carac=2
        caracteristicas=input("Ingrese caracteristicas del producto (1 a 3): ")
        while cont_carac < 4:
            cargar_otra=input("desea ingresar otra caracteristica?: (si/no)").lower()
            if cargar_otra == "no":
                break
            else:
                caracteristicas_=input("Ingrese caracteristicas del producto (1 a 3): ")
                caracteristicas+="~"+caracteristicas_
                cont_carac+=1
        
        lista_elementos_con_marca_nueva.append({"ID": str(id), "NOMBRE": nombre,
                                        "MARCA": marca_ingresada, "PRECIO": "$"+str(precio), "CARACTERISTICAS": caracteristicas})
        print(lista_elementos_con_marca_nueva)
        lista.append({"ID": str(id), "NOMBRE": nombre,
                                        "MARCA": marca_ingresada, "PRECIO": "$"+str(precio), "CARACTERISTICAS": caracteristicas})
        
def guardar_como_json_o_csv(lista_elementos):
    #lista_marcas_nuevas = agregar_nuevo_producto(lista)
    tipo=input("Ingrese 1 para guardarlo como .csv 2 para guardarlo como .json: ")
    while (tipo != "1" and tipo != "2"):
        tipo=input("Error! Ingrese 1 para .csv 2 para .json: ")
    nombre_archivo = input("Ingrese el nombre del archivo a crear: ")
    while nombre_archivo.isdigit():
        nombre_archivo = input("ERROR!! Ingrese el nombre del archivo correcto: ")
    nombre_archivo = nombre_archivo.replace(" ","_")
    directorio="primer_parcial_labo"
    if tipo == "1":
        nombre_archivo+=".csv"
        ruta=os.path.join(directorio, nombre_archivo)
        with open(ruta, "w", encoding="utf-8") as file:
            for elemento in lista_elementos:
                file.write(
                    f'{elemento["ID"]}{","}{elemento["NOMBRE"]}{","}{elemento["MARCA"]}{",$"}{elemento["PRECIO"]}{","}{elemento["CARACTERISTICAS"]}\n')
    elif tipo == "2":
        nombre_archivo+=".json"
        ruta=os.path.join(directorio, nombre_archivo)
        with open(ruta, "w", encoding="utf-8") as file:
            for elemento in lista_elementos:
                with open(ruta, "a", encoding="utf-8") as file:
                    json.dump(elemento, file)
                    file.write("\n") 

def calcular_stock_disponible(elemento):
    stock_a_calcular = random.randint(0, 10)
    elemento["stock"] = stock_a_calcular
    return elemento

# ------------------------ 12 -----------------------------
# opción stock por marca: Pedirle al usuario una marca y mostrar el stock total de los productos de esa marca.

def mostrar_marca_y_stock(lista:list, key):
    
    for elemento in lista:
        lista_marca.append(elemento[key].lower())
    lista_marca_sin_repetir=set(lista_marca)

    marca_ingresada = input("Ingrese marca: ")
    
    while True:
        try:
            if marca_ingresada.lower() in lista_marca_sin_repetir:
                marca_ingresada = marca_ingresada.lower()
                print("La marca es válida.")
                break  # Salir del bucle while si la marca es válida
            else:
                print("La marca no es válida.")
        except:
            print("Error al validar la marca.")

        marca_ingresada = input("Ingrese marca nuevamente: ")

    print("----------------------------------------------------")
    print(f'{"MARCA".ljust(24)} {"STOCK".ljust(5)}   {"PRODCUTO/S"}')
    print("----------------------------------------------------")
    stock=0
    contador =0
    for elemento in lista:
        if marca_ingresada.lower() == elemento[key].lower():
            #print("el stock es :"+ str(elemento["stock"]) + "  y el nombre :" + str(elemento["MARCA"]) + "  y el nombre :" + str(elemento["NOMBRE"]))
            stock += int(elemento["stock"])
            contador+=1
    print(f'{str(marca_ingresada).ljust(24)} {str(stock).ljust(5)}   {contador}')
    print("----------------------------------------------------")
    print("\n")


# ------------------------ 13 ------------------------------
# Agregar opción imprimir bajo stock. Que imprima en un archivo de
# texto en formato csv. Un listado con el nombre de producto y el stock de
# aquellos productos que tengan 2 o menos unidades de stock.

def guardar_bajo_stok_csv(lista:list):
    flag_crear_archivo = True
    for elemento in lista:
        if elemento["stock"] <= 2:
            if flag_crear_archivo:
                with open("./primer_parcial_labo/bajo_stock.csv", "w", encoding="utf-8") as file:
                    flag_crear_archivo = False
            with open("./primer_parcial_labo/bajo_stock.csv", "a", encoding="utf-8") as file:
                file.write(
                    f'{elemento["ID"]}{","}{elemento["NOMBRE"]}{","}{elemento["MARCA"]}{","}{elemento["PRECIO"]}{","}{elemento["CARACTERISTICAS"]}{","}{elemento["stock"]}\n')
        # print(f'{elemento["ID"]}{","}{elemento["NOMBRE"]}{","}{elemento["MARCA"]}{",$"}{elemento["PRECIO"]}{","}{elemento["CARACTERISTICAS"]}{","}{elemento["stock"]}\n')
        # print("----------------------------------------------------")





