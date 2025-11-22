# ==========================
# Módulos
# ==========================

import os
import csv
import copy

# ==========================
# Constantes
# ==========================

SEPARADOR = 90
NOMBRE_ARCHIVO = "paises.csv"
COLUMNAS_ARCHIVO = ["nombre", "poblacion", "superficie", "continente"]

# ==========================
# Funciones Principales
# ==========================

def mostrarMenu(): #MENU PRINCIPAL
    """Muestra el menú principal y gestiona las opciones."""

    while True:
        print("\n" + "*" * SEPARADOR)
        print("1. Agregar Países")
        print("2. Actualizar País")
        print("3. Buscar País")
        print("4. Filtrar Países")
        print("5. Mostrar Estadísticas")
        print("6. Mostrar Países")
        print("0. Salir")
        print("*" * SEPARADOR)

        opcion = input("[-] Ingrese una opción: ").strip()
        match opcion:
            case "1":
                mostrarOpcion(1, "Agregar Países")
                ingresarPaises()

            case "2":
                mostrarOpcion(2, "Actualizar País")
                actualizarPais()

            case "3":
                mostrarOpcion(3, "Buscar País")
                mostrarPais()

            case "4":
                mostrarOpcion(4, "Filtrar Países")
                filtrarPaises()

            case "5":
                mostrarOpcion(5, "Mostrar Estadísticas")
                mostrarEstadisticas(obtenerPaises())

            case "6":
                mostrarOpcion(6, "Mostrar Países")
                mostrarPaises(obtenerPaises())

            case "0":
                print("\n\n" + "Saliendo del sistema...")
                break

            case _:
                print("[X] Opción no válida. Por favor ingrese un número del 1 al 6. (0 para salir)")

def ingresarPaises(): #OPCION 1 DEL MENU
    """Permite al usuario ingresar uno o muchos paises en un archivo .csv"""


    # Obtengo un listado con los registros del archivo.csv
    paises = obtenerPaises()

    # Inicio la carga de un país y luego verifico si desea agregar otro.
    while True:
        # Creo un país y lo guardo en la lista de paises para su posterior guardado en archivo .csv
        pais = crearPais()
        paises.append(pais)

        # Verifico si el usuario desea agregar otro.
        agregarSiguiente = input("[-] Presione 'S' para agregar el siguiente: (ENTER para volver) ")

        # Vuelvo al menú principal
        if agregarSiguiente.strip().lower() != "s":
            print("[!] Volviendo al menú...")
            break

    # Hago un único guardado con todos los países.
    guardarPaises(paises)

def actualizarPais(): #OPCION 2 DEL MENU
    """Busca un país por el nombre y si lo encuentra,
    permite modificar los valores de sus capos (población o superficie)"""

    # Obtengo lista con los paises
    paises = obtenerPaises()
    if not paises:
        print("\t" + "[X] No hay paises cargados.")
        return

    nombre = input("[-] Ingrese el nombre del país a modificar: ").strip()

    if not nombre:
        print("\t" + "[X] El nombre del país no puede estar vacío.")
        return

    # Busco el país
    indice = buscarPais(nombre, paises)
    if indice == -1:
        print("\t" + f"[X] No se pudo encontrar el país '{nombre}'")
        return

    # Listar información previa a la modificación.
    listarPais(paises[indice], True)

    # Permitir al usuario elegír el campo a modificar
    while True:
        print("\n" + "[!] Menú de Actualización")
        print("\t" + "1. Modificar Población")
        print("\t" + "2. Modificar Superficie")
        print("\t" + "0. Cancelar")
        print("\t" + "[!] Presione cúalquier otra tecla para guardar y salir. (ENTER)")

        opcion = input("[-] Ingrese una opción: ").strip()
        match opcion:
            case "1":
                paises[indice]['poblacion'] = cargarCampoPoblacion()

            case "2":
                paises[indice]['superficie'] = cargarCampoSuperficie()

            case "0":
                print("[!] Sin actualizaciones")
                break

            case _:
                guardarPaises(paises)
                break

def mostrarPais(): #OPCION 3 DEL MENU
    """Busca un país en el archivo y lista su información, tambien lista resultados similares a la busqueda"""

    # Obtengo lista con los paises
    paises = obtenerPaises()
    if not paises:
        print("\t" + "[X] No hay paises cargados.")
        return

    nombre = input("[-] Ingrese el nombre del país a consultar: ").strip()

    if not nombre:
        print("\t" + "[X] El nombre del país no puede estar vacío.")
        return

    # Busco el país por coincidencia exacta.
    indice = buscarPais(nombre, paises)
    if indice == -1:
        print("\t" + f"[X] No se pudo encontrar el país '{nombre}'.")
        # return
    else:
        # Muestro el país
        listarPais(paises[indice])

    # Busco y muestros países por coincidencia parcial.
    indices = buscarPaisesParcial(nombre, paises, True)
    resultados = obtenerResultadosIndice(indices, paises)

    if not resultados:
        print("\t" + f"[X] No se pudo encontrar restultados similares.")
        return

    # Listo la información del país
    print(f"[!] Listando resultados similares...")

    listarPaises(resultados)

def filtrarPaises(): #OPCION 4 DEL MENU
    """ Presenta la información de paises de acuerdo a criterios de selección y ordenamientos a elección """
    paises = obtenerPaises()
    if not paises:
        print("\t" + "[X] No hay paises cargados.")
        return

    paisesResultado = []

    # Elegír criterio de filtrado (criterio filtrado / criterio ordenamiento / ordenamiento)
    while True:
        print("\n" + "[!] Menú de Actualización")
        print("\t" + "1. Continente")
        print("\t" + "2. Rango de Población")
        print("\t" + "3. Rango de Superficie")
        print("\t" + "0. Salir")

        opcion = input("[-] Ingrese una opción: ").strip()
        match opcion:
            case "1":
                paisesResultado = filtrarPorContinente(paises)
                break

            case "2":
                paisesResultado = filtrarPorCantidad(paises, "poblacion")
                break

            case "3":
                paisesResultado = filtrarPorCantidad(paises, "superficie")
                break

            case "0":
                break

            case _:
                print("\t" + "[X] Opción no válida")

    if not paisesResultado:
        print("[!] Sin resultados")
        return

    paisesResultado = ordenarPaises(paisesResultado)

    listarPaises(paisesResultado)

def mostrarEstadisticas(paises): #OPCION 5 DEL MENU
    """ Muestra reporte de estadísticas sobre población, superficie, paises por continentes y promedios """

    if not paises:
        print("\t" + "[X] No hay paises cargados.")
        return

    # Obtener información estadistica sobre los países
    estadisticas = obtenerEstadisticas(paises)

    # Ejecutar reportes
    reporteCotasPoblacion(estadisticas['cotasPoblacion'])
    reportePromedios(estadisticas['promedios'])
    reportePaisesPorContinente(estadisticas['paisesPorContinente'])

def mostrarPaises(paises): #OPCION 6 DEL MENU
    """Lista todos los paises de la lista pasada como parametro. Si no se le pasa una lista,
    obtiene los paises desde el archivo .csv"""

    if not paises:
        print("\t" + "[X] No hay paises cargados.")
        return

    listarPaises(paises)


# ==========================
# Funciones auxiliares
# ==========================

def obtenerResultadosIndice(indices, paises):
    """Retorna una lista de países a partir de una lista de indices
    correspondientes con las posiciones en la lista original."""

    resultados = []

    if not indices:
        return resultados

    # Busca los paises a partir de la lista de coincidencias
    for i in range(len(paises)):
        if i in indices:
            resultados.append(paises[i])

    return resultados

    """ Ordena la lista de paises de acuerdo al criterio deseado en forma ascendente o descendente"""
def ordenarPaises(paises):
    paisesOrdenados = copy.deepcopy(paises)

    # Si viene vacio retorno.
    if not paisesOrdenados:
        return paisesOrdenados

    # Criterio y Tipo de Ordenamiento
    criteriosOrdenamiento = ("nombre", "poblacion", "superficie")
    tiposOrdenamiento     = ("asc", "desc")

    # Mostrar opciones válidas
    criterioOrdenamiento = mostrarMenúOpciones("Ingrese el criterio de ordenamiento:", criteriosOrdenamiento)
    tipoOrdenamiento     = mostrarMenúOpciones("Ingrese el tipo de ordenamiento:", tiposOrdenamiento)

    # Algoritmo de Ordenamiento (Burbuja)
    recorridos = len(paisesOrdenados) - 1

    for recorrido in range(recorridos):
        for i in range(recorridos - recorrido):
            if tipoOrdenamiento.lower() == "asc":
                if paisesOrdenados[i][criterioOrdenamiento] > paisesOrdenados[i + 1][criterioOrdenamiento]:
                    paisesOrdenados[i], paisesOrdenados[i + 1] = paisesOrdenados[i + 1], paisesOrdenados[i]
            else:
                if paisesOrdenados[i][criterioOrdenamiento] < paisesOrdenados[i + 1][criterioOrdenamiento]:
                    paisesOrdenados[i], paisesOrdenados[i + 1] = paisesOrdenados[i + 1], paisesOrdenados[i]

    return paisesOrdenados

    """Retorna en un diccionario las estadísticas solicitadas de población, superficie,
        paises por continente y promedios"""
def obtenerEstadisticas(paises):
    # Diccionario principal con todas las estadistacas, donde la clave del diccionario corresponde a el nombre del "reporte".
    estadisticas = dict()

    cantidadPaises = len(paises)

    # Retorno
    if cantidadPaises == 0:
        print("\t" + "[X] No hay paises cargados.")
        return

    # reporte: Países por Continente
    paisesPorContinente = dict()

    # reporte: Promedio Población - Promedio Superficie
    sumaPoblacion  = 0
    sumaSuperficie = 0

    # reporte: Cotas Población (Países)
    paisMayorPoblacion = paises[0]
    paisMenorPoblacion = paises[0]

    # Bucle estadistico principal
    for i in range(cantidadPaises):
        # ========
        # reporte: Cotas Población (Países)
        # ========

        # Si el mayor país (en poblacion) guardado es mayor al actual, lo actualizo.
        if paises[i]['poblacion'] > paisMayorPoblacion['poblacion']:
            paisMayorPoblacion = paises[i]
        else:
            # Si el menor país (en poblacion) guardado es menor al actual, lo actualizo.
            if paises[i]['poblacion'] < paisMenorPoblacion['poblacion']:
                paisMenorPoblacion = paises[i]

        # ========
        # reporte: Promedio Población - Promedio Superficie
        # ========

        sumaPoblacion  += int(paises[i]['poblacion'])
        sumaSuperficie += int(paises[i]['superficie'])

        # ========
        # reporte: Países por Continente
        # ========

        nombreContinente = paises[i]["continente"]

        # Si el acumulador del continente no existe, lo agrego e inicializo
        if nombreContinente not in paisesPorContinente:
            paisesPorContinente[nombreContinente] = 0

        # Incremento el contador
        paisesPorContinente[nombreContinente] += 1

    # Calculos Post Bucle
    promedios = {
        'superficie': sumaSuperficie / cantidadPaises,
        'poblacion':  sumaPoblacion / cantidadPaises
    }

    # Resultados de Estadísticas
    cotasPoblacion = {
        'paisMayorPoblacion': paisMayorPoblacion,
        'paisMenorPoblacion': paisMenorPoblacion
    }

    # Retorno
    estadisticas = {
        'cotasPoblacion': cotasPoblacion,
        'promedios': promedios,
        'paisesPorContinente': paisesPorContinente
    }

    return estadisticas


# ==========================
# Utilidades
# ==========================

def mostrarMenúOpciones(mensaje, opciones):
    """ Valida el criterio de ordenamiento y el tipo ascendente o descendente en función ordenarPaises """

    print("\n" + f"[!] {mensaje}")
    for i in range(len(opciones)):
        print(f"\t{i + 1}. {opciones[i]}")

    while True:
        opcion = input(f"[-] Ingrese una opción: ").strip()
        if esOpcionValida(opcion, opciones):
            break

    return opciones[int(opcion) - 1]

def crearPais():
    """Crea un País y lo retorna"""

    # Carga de campos para la entidad País
    nombre     = cargarCampoNombre(obtenerPaises())
    poblacion  = cargarCampoPoblacion()
    superficie = cargarCampoSuperficie()
    continente = cargarCampoContinente()

    pais = {
        'nombre': nombre,
        'poblacion': poblacion,
        'superficie': superficie,
        'continente': continente
    }

    return pais

def listarPais(pais, modoLista = False):
    """Lista la información de un país pasado como parámetro"""

    # Permite mostrar la información verticalmente
    if modoLista:
        print(f"[!] Información sobre {pais['nombre'].capitalize()}:")
        print("\t" + "* Población: "  + str(pais['poblacion']))
        print("\t" + "* Superficie: " + str(pais['superficie']))
        print("\t" + "* Continente: " + pais["continente"])
        return

    # Encabezado
    encabezado = f"| {'NOMBRE':<20} |   {'POBLACIÓN':<12} |   {'SUPERFICIE':<12} | {'CONTINENTE':>10} |"
    separador = "-" * len(encabezado)

    print(separador)
    print(encabezado)
    print(separador)

    # Listar Data del País
    print(f"| {pais['nombre']:<20} | {pais['poblacion']:>14,} | {pais['superficie']:>14,} | {pais['continente']:>10} |")
    print(separador)

def listarPaises(paises):
    """Lista la información de todos los paises de una lista pasada como parámetro"""

    # Listar Encabezado
    encabezado = f"{'Nº':>3} | {'NOMBRE':<20} |   {'POBLACIÓN':<12} |   {'SUPERFICIE':<12} | {'CONTINENTE':>10} |"
    print("-" * len(encabezado))
    print(encabezado)
    print("-" * len(encabezado))

    # Listar Data de los Paises
    for i in range(len(paises)):
        print(f"{i + 1:>3} | {paises[i]['nombre']:<20} | {paises[i]['poblacion']:>14,} | {paises[i]['superficie']:>14,} | {paises[i]["continente"]:>10} |")
    print("-" * len(encabezado))

def mostrarOpcion(numero, mensaje):
    """Da formato a las opciones del menú principal al mostrarlas en pantalla"""

    print("\n" + "*" * SEPARADOR)
    print(f"OPCIÓN {numero}: {mensaje}")
    print("*" * SEPARADOR)

def esVacio(campo):
    """Valida que un campo string no sea vacío"""

    if not campo.strip():
        return True
    return False

def buscarPaisesParcial(nombre, paises, empieceCon = False):
    """Busca países por nombre (coincidencia parcial) y retorna una lista con los indices de las coincidencias.
    Si el parametro "empieceCon" es True, buscara solo aquellos cuyo nombre empiecen con el string ingresado"""

    cantidadPaises = len(paises)
    nombreNormalizado = normalizarCampoStr(nombre)

    coincidencias = []

    # Si empieza el país empieza con la coincidencia indicada, retorna una lista con los indices de los paises
    if empieceCon:
        for i in range(cantidadPaises):
            nombrePais = normalizarCampoStr(paises[i]['nombre'])

            if nombrePais.find(nombreNormalizado) == 0:
                coincidencias.append(i)

        return coincidencias

    # Buscada Parcial
    for i in range(cantidadPaises):
        if nombreNormalizado in normalizarCampoStr(paises[i]['nombre']):
            coincidencias.append(i)

    return coincidencias

def buscarPais(nombre, paises):
    """Busca un país por nombre (coincidencia total). Retorna el índice si lo encuentra o -1."""

    nombreNormalizado = normalizarCampoStr(nombre)
    for i in range(len(paises)):
        if normalizarCampoStr(paises[i]['nombre']) == nombreNormalizado:
            return i
    return -1

def normalizarCampoStr(texto):
    """Normaliza el string pasado como parametro: elimina espacios extra y convierte a minúsculas."""

    palabras = str(texto).strip().split()
    resultado = ""

    for palabra in palabras:
        if resultado:
            resultado += " "
        resultado += palabra

    return resultado.lower()

def cargarCampoNombre(paises):
    """ Retorna el nombre de un país válido e inexistente en la lista de paises. """
    while True:
        nombre = input("[-] Ingrese el nombre del pais (máximo 20 caracteres): ").strip()
        if esValidoNombre(nombre, paises):
            break
    return nombre

def cargarCampoPoblacion():
    """ Retorna un valor de población válido (int). """
    while True:
        poblacion = input("\t" + "[-] Población: ").strip()
        if esValidoPoblacion(poblacion):
            break
    return int(poblacion)

def cargarCampoSuperficie():
    """ Retorna un valor de superficie válido (int). """
    while True:
        superficie = input("\t" + "[-] Superficie: ").strip()
        if esValidoSuperficie(superficie):
            break
    return int(superficie)

def cargarCampoContinente():
    """ Retorna un continente válido (Se elige de una tupla). """

    # Tupla de Continentes
    continentes = ("África", "América", "Asia", "Europa", "Oceanía")

    # Mostrar opciones válidas
    print("\n" + f"[!] Ingrese el número de continente:")
    for i in range(len(continentes)):
        print(f"\t{i + 1}. {continentes[i]}")

    while True:
        opcion = input(f"[-] Ingrese una opción: ").strip()
        if esOpcionValida(opcion, continentes):
            break

    continente = continentes[int(opcion) - 1]

    return continente


# ==========================
# Filtros
# ==========================

def filtrarPorContinente(paises):
    """ Solicita ingresar un continente al usuario y filtra los paises de la lista
        por el continente ingresado"""

    paisesFiltrados = []

    # Solicito al usuario el nombre del continente por el cuál filtrar y lo normalizo.
    continente = cargarCampoContinente()
    continenteNormalizado = normalizarCampoStr(continente)

    for pais in paises:
        # Si el continente del país conincde con el del criterio de filtrado, lo agrego a la lista paisesFiltrados.
        if normalizarCampoStr(pais["continente"]) == continenteNormalizado:
            paisesFiltrados.append(pais)

    return paisesFiltrados

def filtrarPorCantidad(paises, criterio):
    """ Filtro por parametro numerico dentro de un rango solicitado al usaurio (para superficies o población).
        Recibe la lista de paises y el criterio por el cúal realizar las comparaciones"""

    paisesFiltrados = []

    # Si no se especifica el campo, retorno
    if not criterio:
        print("\t" + f"[X] Es necesario especificar el criterio por el cuál filtrar (campo)")
        return paisesFiltrados

    # Solicito al usuario que ingrese las cotas inferior y superior.
    print("\n" + "[!] Ingrese la población mínima y máxima para realizar el filtrado: (Incluyendo extremos: [inf; sup])")
    cotaInferior = input("\t" + "[-] Cota inferior: ").strip()
    cotaSuperior = input("\t" + "[-] Cota Superior: ").strip()

    # Valido las cotas
    if not esEnteroPositivo(cotaInferior, "Cota inferior no válida"):
        return paisesFiltrados

    if not esEnteroPositivo(cotaSuperior, "Cota Superior no válida"):
        return paisesFiltrados

    cotaInferior = int(cotaInferior)
    cotaSuperior = int(cotaSuperior)

    if cotaInferior > cotaSuperior:
        print("\t" + f"[X] La cota inferior no puede ser mayor a la cota superior")
        return paisesFiltrados

    # Filtro los paises que cumplan la condición
    for pais in paises:
        cantidad = normalizarCampoStr(pais[criterio])

        cantidad = int(cantidad)

        # Si el campo del país esta dentro del rango de las cotas, lo incluyo a la lista de resultado (paisesFiltrados)
        if cotaSuperior >= cantidad and cantidad >= cotaInferior:
            paisesFiltrados.append(pais)

    return paisesFiltrados


# ==========================
# Validaciones
# ==========================

def esEnteroPositivo(numero, mensajeError = None):
    """Valida que el número pasado como párametro sea un entero positivo,
        opcionalmente imprime un mensaje de error"""

    if not numero.isdigit() or int(numero) >= 10000000000:
        if mensajeError:
            print("\t" + f"[X] {mensajeError}")
        return False
    return True

def esValidoNombre(nombre, paises):
    """Verifica que el nombre ingresado por el usuario sea válido y si ya existe un país con ese nombre
        en la lista de paises"""

    # Campo Vacio
    if esVacio(nombre):
        print("\t" + "[X] El nombre no puede estar vacío")
        return False

    # País ya existente (Mismo nombre)
    if buscarPais(nombre, paises) != -1:
        print("\t" + f"[X] El país '{nombre.capitalize()}' ya existe.")
        return False

    # Longitud de país supera los 20 caracteres (longitud arbitraria para evitar textos largos en el reporte)
    if len(nombre) > 20:
        print("\t" + f"[X] El nombre supera el máximo de 20 caracteres.")
        return False

    return True

def esValidoPoblacion(poblacion):
    """Verifica si el valor de población ingresado por el usuario es válido"""

    return esEnteroPositivo(poblacion, "La población debe ser un número entero positivo y menor a 10 mil millones")

def esValidoSuperficie(superficie):
    """Verifica si el valor de superficie ingresado por el usuario es válido"""

    return esEnteroPositivo(superficie, "La superficie debe ser un número entero positivo y menor a 10 mil millones")

def esOpcionValida(opcion, opciones):
    """Verifica si una opición numerica está incluida en un menú de opciones,
    ambos pasados como parámetros (Opcion >= 1)"""

    if not opcion.isdigit():
        print("\t" + "[X] Opción no válida")
        return False

    opcion = int(opcion)

    # Opción fuera de rango.
    if opcion < 1 or opcion > len(opciones):
        print("\t" + "[X] Opción no válida")
        return False

    return True


# ==========================
# Persistencia
# ==========================

def obtenerPaises():
    """Lee el archivo CSV y retorna una lista de diccionarios.
        Si el archivo no existe, lo crea y retorna lista vacía."""

    paises = []

    if not os.path.exists(NOMBRE_ARCHIVO):
        inicializarArchivo()
        return paises

    with open(NOMBRE_ARCHIVO, newline="", encoding="utf-8-sig") as archivo:
        for fila in csv.DictReader(archivo):
            paises.append({
                "nombre": fila['nombre'],
                "poblacion": int(fila['poblacion']),
                "superficie": int(fila['superficie']),
                "continente": fila["continente"]
            })

    return paises

def guardarPaises(paises):
    """Sobreescribe el archivo con el catálogo completo."""

    with open(NOMBRE_ARCHIVO, "w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS_ARCHIVO)
        escritor.writeheader()
        escritor.writerows(paises)

    print(f"[+] Archivo {NOMBRE_ARCHIVO} guardado exitosamente.")

def inicializarArchivo():
    """Crea el archivo .CSV con el encabezado."""

    with open(NOMBRE_ARCHIVO, "w", newline="", encoding="utf-8-sig") as file:
        csv.DictWriter(file, fieldnames=COLUMNAS_ARCHIVO).writeheader()
    print(f"[+] Se creó el archivo {NOMBRE_ARCHIVO}")


# ==========================
# Reportes
# ==========================

def inicializarReporte(titulo):
    """Genera la estructura básica de un reporte genérico"""

    encabezadoReporte = f"| o Reporte |  {titulo} |"

    print("\n" + ("-" * SEPARADOR) + "\n" + encabezadoReporte)
    print("-" * len(encabezadoReporte) + "\n")

def reporteCotasPoblacion(informacion):
    """Lista un reporte con los paises con mayor y menor población"""

    # Encabezado inicial del reporte
    inicializarReporte("País con Mayor y Menor Población")

    # Obtener resultados
    mayor = informacion["paisMayorPoblacion"]
    menor = informacion["paisMenorPoblacion"]

    # Listar resultados
    print("[1] País con mayor población (cantidad de habitantes): ")
    listarPais(mayor)

    print("\n" + "[2] País con menor población (cantidad de habitantes): ")
    listarPais(menor)

def reportePromedios(informacion):
    """Genera reporte con los promedios solicitados"""

    inicializarReporte("Promedio Superficies y Población")

    # Listar Encabezado
    encabezado = f"| {'Nº':>3} | {'CAMPO':<15} | {'PROMEDIO':<15} |"
    separador = "-" * len(encabezado)

    print(separador)
    print(encabezado)
    print(separador)

    # Recorro claves con un índice manual
    claves = list(informacion.keys())
    i = 0
    while i < len(claves):
        clave = claves[i]
        promedio = informacion[clave]

        print(f"| {i + 1:>3} | {clave:<15} | {round(promedio, 2):<15,} |")

        # Separador entre filas
        if i < len(claves) - 1:
            print(separador)

        i += 1

    print(separador)

def reportePaisesPorContinente(informacion):
    """Genera reporte con cantidad de países por continente."""

    inicializarReporte("Países por Continente")

    # Listar Encabezado
    encabezado = f"| {'Nº':>3} | {'CONTINENTE':<14} | {'PAÍSES':<10} |"
    separador = "-" * len(encabezado)

    print(separador)
    print(encabezado)
    print(separador)

    # Utilizo enumerate para poder agregar un "indice" y no tener que usar una variable contadora
    for i, continente in enumerate(informacion):
        print(f"| {i + 1:>3} | {continente:<14} | {informacion[continente]:<10} |")
    print(separador)


# ==========================
# Inicio de la aplicación
# ==========================

""" Inicialización del Archivo """
if not os.path.exists(NOMBRE_ARCHIVO):
    inicializarArchivo()

mostrarMenu()