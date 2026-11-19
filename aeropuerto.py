
TARIFAS = {
    "E": 85000,
    "J": 210000,
    "P": 450000
}

TASA_AEROPORTUARIA = 12500


def mostrar_menu():
    # Muestra el menu principal
    print("\n===== AEROPUERTO INTERNACIONAL CORDILLERA =====")
    print("1. Registrar vuelo")
    print("2. Vender pasajes")
    print("3. Cambiar estado de vuelo")
    print("4. Mostrar vuelos")
    print("5. Reporte de la jornada")
    print("6. Salir")


def leer_entero(mensaje, minimo, maximo):
    # Pide un numero y valida que este dentro del rango
    while True:
        try:
            numero = int(input(mensaje))
            if numero >= minimo and numero <= maximo:
                return numero
            else:
                print("El numero debe estar entre", minimo, "y", maximo)
        except:
            print("Debes ingresar un numero entero")


def validar_codigo(codigo):
    # Comprueba que el codigo tenga dos letras y cuatro numeros
    if len(codigo) != 6:
        return False

    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numeros = "0123456789"

    for letra in codigo[0:2]:
        if letra not in letras:
            return False

    for numero in codigo[2:6]:
        if numero not in numeros:
            return False

    return True


def buscar_vuelo(vuelos, codigo):
    # Busca un vuelo por su codigo
    for vuelo in vuelos:
        if vuelo["codigo"] == codigo:
            return vuelo

    return None


def registrar_vuelo(vuelos):
    # Registra un nuevo vuelo
    print("\n--- Registrar vuelo ---")

    codigo = input("Ingrese codigo del vuelo: ")

    while validar_codigo(codigo) == False or buscar_vuelo(vuelos, codigo) != None:
        if validar_codigo(codigo) == False:
            print("El codigo debe tener dos letras mayusculas y cuatro numeros")
        else:
            print("Este codigo ya existe")

        codigo = input("Ingrese otro codigo: ")

    destino = ""

    while destino == "":
        destino = input("Ingrese destino: ")
        if destino == "":
            print("El destino es obligatorio")

    capacidad = leer_entero("Ingrese capacidad (50 a 300): ", 50, 300)

    vuelo = {
        "codigo": codigo,
        "destino": destino,
        "capacidad": capacidad,
        "vendidos": 0,
        "estado": "Programado",
        "recaudado": 0
    }

    vuelos.append(vuelo)

    print("Vuelo registrado con exito")


def asientos_disponibles(vuelo):
    # Calcula los asientos que quedan disponibles
    disponibles = vuelo["capacidad"] - vuelo["vendidos"]
    return disponibles


def calcular_ocupacion(vuelo):
    # Calcula el porcentaje de ocupacion del vuelo
    porcentaje = (vuelo["vendidos"] / vuelo["capacidad"]) * 100
    porcentaje = int(porcentaje * 10) / 10
    return porcentaje


def calcular_total_venta(clase, cantidad):
    # Calcula el total de la venta con descuento y tasa
    total_pasajes = TARIFAS[clase] * cantidad

    if cantidad >= 4:
        total_pasajes = total_pasajes * 0.90

    tasa = TASA_AEROPORTUARIA * cantidad
    total = total_pasajes + tasa

    return int(total)


def vender_pasajes(vuelos):
    # Permite vender pasajes para un vuelo
    print("\n--- Vender pasajes ---")

    codigo = input("Ingrese codigo del vuelo: ")
    vuelo = buscar_vuelo(vuelos, codigo)

    if vuelo == None:
        print("El vuelo no existe")
        return

    if vuelo["estado"] != "Programado" and vuelo["estado"] != "Embarcando":
        print("No se pueden vender pasajes para este vuelo")
        return

    print("Asientos disponibles:", asientos_disponibles(vuelo))

    clase = input("Clase (E=Economica, J=Ejecutiva, P=Primera): ")

    if clase == "e":
        clase = "E"
    elif clase == "j":
        clase = "J"
    elif clase == "p":
        clase = "P"

    while clase not in TARIFAS:
        print("La clase ingresada no existe")
        clase = input("Ingrese E, J o P: ")

        if clase == "e":
            clase = "E"
        elif clase == "j":
            clase = "J"
        elif clase == "p":
            clase = "P"

    cantidad = leer_entero("Cantidad de pasajes (1 a 10): ", 1, 10)

    if cantidad > asientos_disponibles(vuelo):
        print("No hay suficientes asientos disponibles")
        return

    total = calcular_total_venta(clase, cantidad)
    tasa = TASA_AEROPORTUARIA * cantidad

    nombres_clases = {
        "E": "Economica",
        "J": "Ejecutiva",
        "P": "Primera"
    }

    print("\n--- Detalle de la venta ---")
    print("Vuelo:", vuelo["codigo"], "-", vuelo["destino"])
    print("Clase:", nombres_clases[clase], "x", cantidad)

    if cantidad >= 4:
        print("Descuento del 10% aplicado sobre los pasajes")

    print("Tasa aeroportuaria:", f"${tasa:,}".replace(",", "."))
    print("TOTAL A PAGAR:", f"${total:,}".replace(",", "."))

    vuelo["vendidos"] = vuelo["vendidos"] + cantidad
    vuelo["recaudado"] = vuelo["recaudado"] + total

    print("Venta realizada con exito")


def cambiar_estado(vuelos):
    # Cambia el estado de un vuelo
    print("\n--- Cambiar estado de vuelo ---")

    codigo = input("Ingrese codigo del vuelo: ")
    vuelo = buscar_vuelo(vuelos, codigo)

    if vuelo == None:
        print("El vuelo no existe")
        return

    if vuelo["estado"] == "Despegado" or vuelo["estado"] == "Cancelado":
        print("Este vuelo ya no puede cambiar de estado")
        return

    print("Estado actual:", vuelo["estado"])

    if vuelo["estado"] == "Programado":
        print("1. Embarcando")
        print("2. Cancelado")

        opcion = leer_entero("Seleccione una opcion: ", 1, 2)

        if opcion == 1:
            vuelo["estado"] = "Embarcando"
        else:
            vuelo["estado"] = "Cancelado"

    elif vuelo["estado"] == "Embarcando":
        print("1. Despegado")
        print("2. Cancelado")

        opcion = leer_entero("Seleccione una opcion: ", 1, 2)

        if opcion == 1:
            vuelo["estado"] = "Despegado"
        else:
            vuelo["estado"] = "Cancelado"

    print("Nuevo estado:", vuelo["estado"])


def mostrar_vuelos(vuelos):
    # Muestra los vuelos registrados
    print("\n--- Lista de vuelos ---")

    if len(vuelos) == 0:
        print("No hay vuelos registrados")
    else:
        for vuelo in vuelos:
            ocupacion = calcular_ocupacion(vuelo)

            print(
                vuelo["codigo"], "-",
                vuelo["destino"], "-",
                vuelo["vendidos"], "/",
                vuelo["capacidad"], "-",
                str(ocupacion) + "% -",
                vuelo["estado"]
            )


def generar_reporte(vuelos):
    # Muestra las estadisticas de la jornada
    print("\n--- Reporte de la jornada ---")

    total_vuelos = len(vuelos)
    pasajeros_totales = 0
    total_recaudado = 0
    vuelos_cancelados = 0
    mayor_ocupacion = None

    for vuelo in vuelos:
        pasajeros_totales = pasajeros_totales + vuelo["vendidos"]
        total_recaudado = total_recaudado + vuelo["recaudado"]

        if vuelo["estado"] == "Cancelado":
            vuelos_cancelados = vuelos_cancelados + 1

        if mayor_ocupacion == None:
            mayor_ocupacion = vuelo
        elif calcular_ocupacion(vuelo) > calcular_ocupacion(mayor_ocupacion):
            mayor_ocupacion = vuelo

    print("Total de vuelos:", total_vuelos)
    print("Pasajeros totales:", pasajeros_totales)
    print("Total recaudado:", f"${total_recaudado:,}".replace(",", "."))
    print("Vuelos cancelados:", vuelos_cancelados)

    if mayor_ocupacion != None:
        print("Vuelo con mayor ocupacion:")
        print(mayor_ocupacion["codigo"], "-", mayor_ocupacion["destino"])
        print("Ocupacion:", str(calcular_ocupacion(mayor_ocupacion)) + "%")
    else:
        print("No hay vuelos registrados")


def main():
    # Inicia el programa con los vuelos entregados
    vuelos = [
        {
            "codigo": "LA1234",
            "destino": "Lima",
            "capacidad": 180,
            "vendidos": 150,
            "estado": "Programado",
            "recaudado": 0
        },
        {
            "codigo": "JA0456",
            "destino": "Buenos Aires",
            "capacidad": 120,
            "vendidos": 118,
            "estado": "Embarcando",
            "recaudado": 0
        },
        {
            "codigo": "SK7890",
            "destino": "Punta Arenas",
            "capacidad": 90,
            "vendidos": 40,
            "estado": "Programado",
            "recaudado": 0
        }
    ]

    while True:
        mostrar_menu()

        opcion = leer_entero("Seleccione una opcion: ", 1, 6)

        if opcion == 1:
            registrar_vuelo(vuelos)
        elif opcion == 2:
            vender_pasajes(vuelos)
        elif opcion == 3:
            cambiar_estado(vuelos)
        elif opcion == 4:
            mostrar_vuelos(vuelos)
        elif opcion == 5:
            generar_reporte(vuelos)
        elif opcion == 6:
            print("adios")
            break


main()
