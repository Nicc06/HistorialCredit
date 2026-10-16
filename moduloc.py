
import os
import time
import pandas as pd # type: ignore

archivo = "credit_risk_dataset (3).csv"

if os.path.exists(archivo):
    df = pd.read_csv(archivo)
    print("Archivo cargado correctamente")
    print("Columnas:", df.columns.tolist())
    print("Cantidad de registros:", len(df))
else:
    print("No se encuentra el archivo")

print("===== SEMANA 6: SISTEMA DE CONSULTAS =====")

# ==========================================
# 1. CARGAR LOS DATOS
# ==========================================

archivo = "credit_risk_dataset (3).csv"

if not os.path.exists(archivo):
    print("Error: No se encontro el archivo CSV.")
    raise SystemExit

df = pd.read_csv(archivo)

# Comprobar que existan las columnas necesarias
columnas = ["person_income", "loan_amnt"]

for columna in columnas:
    if columna not in df.columns:
        print("Falta la columna:", columna)
        raise SystemExit

# Preparar los datos como lista de diccionarios
datos = df.to_dict("records")

print("Datos cargados correctamente.")
print("Cantidad de registros:", len(datos))


# ==========================================
# 2. MERGE SORT
# ==========================================

def merge_sort(lista, columna):

    if len(lista) <= 1:
        return lista

    medio = len(lista) // 2

    izquierda = merge_sort(lista[:medio], columna)
    derecha = merge_sort(lista[medio:], columna)

    resultado = []
    i = 0
    j = 0

    while i < len(izquierda) and j < len(derecha):

        if izquierda[i][columna] <= derecha[j][columna]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1

    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])

    return resultado


# ==========================================
# 3. QUICK SORT
# ==========================================

def quick_sort(lista, columna):

    if len(lista) <= 1:
        return lista

    pivote = lista[len(lista) // 2][columna]

    menores = []
    iguales = []
    mayores = []

    for dato in lista:

        if dato[columna] < pivote:
            menores.append(dato)
        elif dato[columna] == pivote:
            iguales.append(dato)
        else:
            mayores.append(dato)

    return (
        quick_sort(menores, columna)
        + iguales
        + quick_sort(mayores, columna)
    )


# ==========================================
# 4. MOSTRAR REGISTROS
# ==========================================

def mostrar_registros(registros):

    if len(registros) == 0:
        print("No se encontraron registros.")
        return

    print("Cantidad encontrada:", len(registros))

    for dato in registros[:10]:
        print(
            "Ingreso:", dato["person_income"],
            "| Prestamo:", dato["loan_amnt"]
        )

    if len(registros) > 10:
        print("Se muestran solo los primeros 10 registros.")


# ==========================================
# 5. BUSCAR POR INGRESO
# ==========================================

def buscar_ingreso():

    valor = float(input("Ingrese el ingreso que desea buscar: "))

    inicio = time.perf_counter()

    encontrados = [
        dato for dato in datos
        if dato["person_income"] == valor
    ]

    fin = time.perf_counter()

    mostrar_registros(encontrados)
    print("Tiempo de consulta:", fin - inicio, "segundos")


# ==========================================
# 6. BUSCAR POR MONTO DEL PRESTAMO
# ==========================================

def buscar_prestamo():

    valor = float(input("Ingrese el monto del prestamo: "))

    inicio = time.perf_counter()

    encontrados = [
        dato for dato in datos
        if dato["loan_amnt"] == valor
    ]

    fin = time.perf_counter()

    mostrar_registros(encontrados)
    print("Tiempo de consulta:", fin - inicio, "segundos")


# ==========================================
# 7. ORDENAR LOS REGISTROS
# ==========================================

def ordenar_datos():

    print("\n1. Ordenar por ingreso (Merge Sort)")
    print("2. Ordenar por prestamo (Quick Sort)")

    opcion = input("Seleccione una opcion: ")

    if opcion == "1":
        columna = "person_income"
        algoritmo = merge_sort

    elif opcion == "2":
        columna = "loan_amnt"
        algoritmo = quick_sort

    else:
        print("Opcion no valida.")
        return

    print("\n1. Menor a mayor")
    print("2. Mayor a menor")

    orden = input("Seleccione el orden: ")

    if orden not in ("1", "2"):
        print("Opcion no valida.")
        return

    inicio = time.perf_counter()

    resultado = algoritmo(datos, columna)

    if orden == "2":
        resultado = resultado[::-1]

    fin = time.perf_counter()

    mostrar_registros(resultado)

    print("Algoritmo:", algoritmo.__name__)
    print("Tiempo:", fin - inicio, "segundos")


# ==========================================
# 8. FILTRAR POR RANGO DE INGRESOS
# ==========================================

def filtrar_ingresos():

    minimo = float(input("Ingreso minimo: "))
    maximo = float(input("Ingreso maximo: "))

    if minimo > maximo:
        print("El minimo no puede superar al maximo.")
        return

    encontrados = [
        dato for dato in datos
        if minimo <= dato["person_income"] <= maximo
    ]

    mostrar_registros(encontrados)


# ==========================================
# 9. MENU PRINCIPAL
# ==========================================

def menu():

    while True:

        print("\n========== MENU PRINCIPAL ==========")
        print("1. Buscar por ingreso")
        print("2. Buscar por monto del prestamo")
        print("3. Ordenar registros")
        print("4. Filtrar por rango de ingresos")
        print("5. Mostrar cantidad de registros")
        print("0. Salir")

        opcion = input("Seleccione una opcion: ")

        try:

            if opcion == "1":
                buscar_ingreso()

            elif opcion == "2":
                buscar_prestamo()

            elif opcion == "3":
                ordenar_datos()

            elif opcion == "4":
                filtrar_ingresos()

            elif opcion == "5":
                print("Total de registros:", len(datos))

            elif opcion == "0":
                print("Gracias por utilizar el sistema.")
                break

            else:
                print("Opcion no valida.")

        except ValueError:
            print("Error: ingrese un numero valido.")


menu()
