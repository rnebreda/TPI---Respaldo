# Trabajo Práctico Integrador — Programación 1
## Gestión de Datos de Países en Python
### Descripción general
Este proyecto implementa una aplicación en **Python 3** que permite gestionar información de países, almacenada en un archivo **CSV**.
El sistema permite realizar operaciones de **búsqueda, filtrado, ordenamiento y generación de estadísticas**, aplicando estructuras de datos (listas y diccionarios) y técnicas de modularización mediante funciones.

El objetivo del trabajo es afianzar los conceptos fundamentales de la programación estructurada y la manipulación de datos en Python.

---
### Funcionalidades principales
El programa presenta un menú interactivo en consola con las siguientes opciones:

```
******************************************************************************************
1. Agregar Países
2. Actualizar País
3. Buscar País
4. Filtrar Países
5. Mostrar Estadísticas
6. Mostrar Países
0. Salir
******************************************************************************************
[-] Ingrese una opción
```
---
> Menú principal
### Estructura del proyecto

```
📂
├── TrabajoPractico.py   # Código fuente principal
├── paises.csv           # Dataset base (generado automáticamente)
├── README.md            # Documento descriptivo
```
### Estructuras y conceptos aplicados
- **Listas:** para almacenar colecciones de países.
- **Diccionarios:** para representar cada país y sus campos (`nombre`, `poblacion`, `superficie`, `continente`).
- **Funciones:** cada acción principal se encuentra modularizada.
- **Condicionales y bucles:** control de flujo y validaciones de entradas.
- **Archivos CSV:** persistencia de datos.
- **Ordenamiento (Burbuja):** permite ordenar ascendente o descendente por diferentes criterios.
- **Filtrado:** permite obtener subconjuntos de datos según condiciones específicas (continente o rangos numéricos).
- **Estadísticas:** cálculo de promedios y análisis de máximos/mínimos.
---
### Instrucciones de ejecución

1. Clonar o descargar el repositorio:
```bash
git clone https://github.com/valentinryma/TP-Integrador-Programacion-I
````

2. Ejecutar programa:
```bash
python TrabajoPractico.py
```

****
### Ejemplo de uso:

#### 1 Agregar País

```bash
******************************************************************************************
1. Agregar Países
2. Actualizar País
3. Buscar País
4. Filtrar Países
5. Mostrar Estadísticas
6. Mostrar Países
0. Salir
******************************************************************************************
[-] Ingrese una opción: 1

******************************************************************************************
OPCIÓN 1: Agregar Países
******************************************************************************************
[-] Ingrese el nombre del pais: Perí
        [-] Población: 3457000
        [-] Superficie: 580

[!] Ingrese el número de continente:
        1. África
        2. América
        3. Asia
        4. Europa
        5. Oceanía
[-] Ingrese una opción: 2
[-] Presione 'S' para agregar el siguiente: x
[!] Volviendo al menú...
[+] Archivo paises.csv guardado exitosamente.

******************************************************************************************
```

Si el país ya existe en el archivo, notifica al usuario y vuelve a solicitarle el nombre del país a cargar:
```
******************************************************************************************
OPCIÓN 1: Agregar Países
******************************************************************************************
[-] Ingrese el nombre del pais: Perú
    [X] El país 'Perú' ya existe.

******************************************************************************************
```

#### 5. Estadísticas (Módulo de Reportes)
```
******************************************************************************************
1. Agregar Países
2. Actualizar País
3. Buscar País
4. Filtrar Países
5. Mostrar Estadísticas
6. Mostrar Países
0. Salir
******************************************************************************************
[-] Ingrese una opción: 5

******************************************************************************************
OPCIÓN 5: Mostrar Estadísticas
******************************************************************************************
```
> Menú Principal: Opción 5 seleccionada

```
------------------------------------------------------------------------------------------
| o Reporte |  País con Mayor y Menor Población |
-------------------------------------------------

[1] País con mayor población: India, 1440000000 habitantes.
------------------------------------------------------------------------
| NOMBRE               |    POBLACIÓN |   SUPERFICIE |      CONTINENTE |
------------------------------------------------------------------------
| India                |   1440000000 |      3287263 |            Asia |
------------------------------------------------------------------------
```

```
[2] País con menor población: Republica de Córdoba, 3457000 habitantes.
------------------------------------------------------------------------
| NOMBRE               |    POBLACIÓN |   SUPERFICIE |      CONTINENTE |
------------------------------------------------------------------------
| Republica de Córdoba |      3457000 |          580 |         América |
------------------------------------------------------------------------
```

```
------------------------------------------------------------------------------------------
| o Reporte |  Promedio Superficies y Población |
-------------------------------------------------

-------------------------------------------
|  Nº | CAMPO           | PROMEDIO        |
-------------------------------------------
|   1 | superficie      | 1979615.5       |
-------------------------------------------
|   2 | poblacion       | 128709884.62    |
-------------------------------------------
```

```
------------------------------------------------------------------------------------------
| o Reporte |  Países por Continente |
--------------------------------------

-------------------------------------
|  Nº | CONTINENTE     | PAÍSES     |
-------------------------------------
|   1 | Europa         | 14         |
|   2 | África         | 10         |
|   3 | Asia           | 15         |
|   4 | América        | 12         |
|   5 | Oceanía        | 1          |
-------------------------------------

******************************************************************************************
```
