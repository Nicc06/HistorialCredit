
import os
import random
import math
import pandas as pd # type: ignore

print("===== SEMANA 7: OPTIMIZACION CREDITICIA =====")

# ==========================================
# 1. CARGAR LOS DATOS
# ==========================================

archivo = "credit_risk_dataset (3).csv"

if not os.path.exists(archivo):
    print("Error: no se encuentra el archivo CSV.")
    raise SystemExit

df = pd.read_csv(archivo)

# Comprobar las columnas necesarias
columnas = [
    "loan_amnt",
    "loan_int_rate",
    "loan_status"
]

for columna in columnas:
    if columna not in df.columns:
        print("Falta la columna:", columna)
        raise SystemExit

# Utilizar solo registros con datos válidos
df = df.dropna(subset=columnas).copy()

# Tomar una muestra de hasta 100 clientes
df = df.head(100).reset_index(drop=True)

# Crear un identificador para cada fila
df["cliente_id"] = range(1, len(df) + 1)

print("Clientes evaluados:", len(df))


# ==========================================
# 2. PREPARAR BENEFICIO Y RIESGO
# ==========================================

# El interés se utiliza como indicador de beneficio bruto.
# Se calcula proporcionalmente al monto solicitado.
df["beneficio_estimado"] = (
    df["loan_amnt"] * df["loan_int_rate"] / 100
)

# loan_status = 1 representa incumplimiento histórico
df["riesgo_historico"] = df["loan_status"].astype(int)

# Penalización académica por incumplimiento histórico.
# Es un supuesto del ejercicio, no una pérdida real.
df["penalizacion_riesgo"] = (
    df["beneficio_estimado"] * df["riesgo_historico"]
)

# Puntuación individual
df["puntuacion"] = (
    df["beneficio_estimado"] - df["penalizacion_riesgo"]
)

clientes = df.to_dict("records")


# ==========================================
# 3. DEFINIR LA FUNCION DE EVALUACION
# ==========================================

def evaluar(solucion, clientes, presupuesto):
    """
    Una solución es una lista de 0 y 1.
    1 = cliente seleccionado.
    0 = cliente no seleccionado.

    Devuelve una puntuación para la selección.
    """

    monto_total = 0
    puntuacion_total = 0

    for i in range(len(solucion)):

        if solucion[i] == 1:

            cliente = clientes[i]

            monto_total += cliente["loan_amnt"]
            puntuacion_total += cliente["puntuacion"]

    # No permitimos superar el presupuesto
    if monto_total > presupuesto:
        return -1

    return puntuacion_total


# ==========================================
# 4. CREAR UNA SOLUCION INICIAL
# ==========================================

def crear_solucion_inicial(clientes, presupuesto):

    solucion = [0] * len(clientes)
    indices = list(range(len(clientes)))

    random.shuffle(indices)

    monto_actual = 0

    for i in indices:

        monto = clientes[i]["loan_amnt"]

        if monto_actual + monto <= presupuesto:

            solucion[i] = 1
            monto_actual += monto

    return solucion


# ==========================================
# 5. GENERAR UNA SOLUCION VECINA
# ==========================================

def generar_vecino(solucion):

    vecino = solucion.copy()

    # Elegir un cliente al azar
    i = random.randrange(len(vecino))

    # Si estaba seleccionado, se quita.
    # Si no estaba seleccionado, se agrega.
    vecino[i] = 1 - vecino[i]

    return vecino


# ==========================================
# 6. SIMULATED ANNEALING
# ==========================================

def simulated_annealing(
    clientes,
    presupuesto,
    temperatura_inicial=1000,
    enfriamiento=0.995,
    iteraciones=10000
):

    actual = crear_solucion_inicial(
        clientes, presupuesto
    )

    puntuacion_actual = evaluar(
        actual, clientes, presupuesto
    )

    mejor = actual.copy()
    mejor_puntuacion = puntuacion_actual

    temperatura = temperatura_inicial

    for _ in range(iteraciones):

        vecino = generar_vecino(actual)

        puntuacion_vecino = evaluar(
            vecino, clientes, presupuesto
        )

        diferencia = (
            puntuacion_vecino - puntuacion_actual
        )

        # Aceptar si mejora o si se cumple
        # la probabilidad de aceptar una solución peor
        if puntuacion_vecino >= 0 and (
            diferencia > 0
            or random.random() < math.exp(
                min(diferencia / max(temperatura, 1e-10), 0)
            )
        ):

            actual = vecino
            puntuacion_actual = puntuacion_vecino

        # Guardar la mejor solución encontrada
        if puntuacion_actual > mejor_puntuacion:

            mejor = actual.copy()
            mejor_puntuacion = puntuacion_actual

        # Reducir la temperatura
        temperatura *= enfriamiento

    return mejor, mejor_puntuacion


# ==========================================
# 7. EJECUTAR LA OPTIMIZACION
# ==========================================

presupuesto = float(
    input("Ingrese el presupuesto disponible: ")
)

if presupuesto <= 0:
    print("El presupuesto debe ser mayor que cero.")
    raise SystemExit

# Fijar una semilla permite repetir la prueba
random.seed(42)

mejor_solucion, mejor_puntuacion = simulated_annealing(
    clientes,
    presupuesto
)


# ==========================================
# 8. MOSTRAR LOS RESULTADOS
# ==========================================

seleccionados = []

for i in range(len(mejor_solucion)):

    if mejor_solucion[i] == 1:
        seleccionados.append(clientes[i])

monto_total = sum(
    cliente["loan_amnt"]
    for cliente in seleccionados
)

beneficio_total = sum(
    cliente["beneficio_estimado"]
    for cliente in seleccionados
)

penalizacion_total = sum(
    cliente["penalizacion_riesgo"]
    for cliente in seleccionados
)

print("\n===== RESULTADOS DE OPTIMIZACION =====")
print("Presupuesto:", presupuesto)
print("Clientes seleccionados:", len(seleccionados))
print("Monto total asignado:", round(monto_total, 2))
print("Presupuesto restante:", round(presupuesto - monto_total, 2))
print("Beneficio bruto estimado:", round(beneficio_total, 2))
print("Penalizacion por riesgo:", round(penalizacion_total, 2))
print("Puntuacion final:", round(mejor_puntuacion, 2))

print("\n===== CLIENTES SELECCIONADOS =====")

if len(seleccionados) == 0:
    print("No se seleccionaron clientes.")
else:
    for cliente in seleccionados:
        print(
            "Cliente:", cliente["cliente_id"],
            "| Prestamo:", cliente["loan_amnt"],
            "| Tasa:", cliente["loan_int_rate"],
            "| Incumplimiento historico:",
            cliente["loan_status"],
            "| Puntuacion:", round(cliente["puntuacion"], 2)
        )

print("\nSemana 7 terminada.")
