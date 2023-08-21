print("hola mundo")
# mi_tupla = ('cadena de texto', 15, 2.8, 'otro dato', 25)
# print(mi_tupla[1])
# mi_diccionario = {
#     'clave1':'hola',
#     'clave2':'chau',
#     'clave3':'haupei',
# }
# print(mi_diccionario['clave1'])
#
# anio = 2001
# # while anio <= 2012:
# #     print("Informes del Año " + str(anio))
# #     anio += 1
#
#
# # while True:
# #     nombre = input("Por favor, ingresa tu nombre: ")
# #     if nombre:
# #         break
#
# for anio in range(2001, 2013):
#     print("Informes del Año", str(anio))
def recorrer_parametros_arbitrarios(parametro_fijo, *arbitrarios, **kwords):
    print(parametro_fijo)
    for argumento in arbitrarios:
        print(argumento)
# Los argumentos arbitrarios tipo clave, se recorren como los diccionarios
    for clave in kwords:
        print("El valor de", clave, "es", kwords[clave])
recorrer_parametros_arbitrarios("Fixed", "arbitrario 1", "arbitrario 2",
                                "arbitrario 3", clave1="valor uno", clave2="valor dos")