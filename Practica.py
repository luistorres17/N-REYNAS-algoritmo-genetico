#algoritmo genetico para 10 reynas

# practica 1 algoritmo  genetico para resolver el problema de las n reinas con 8 reinas

#se importan las librerias necesarias
import random
import numpy as np
import matplotlib.pyplot as plt

#se establece el numero de reinas
n = 8

#estructura del tablero que se forma aleatoriamente con posiciones de las reinas igual aleatorias
def generar_tablero(n):
    tablero = []
    for i in range(n):
        tablero.append(random.randint(0,n-1))
    return tablero

#funcion para generar una poblacion inicial con valor predeterminado de 10 individuos
def generar_poblacion_inicial(n):
    poblacion = []
    for i in range(random.randint(10, 100)):
        poblacion.append(generar_tablero(n))
    return poblacion

#funcion para mostrar la poblacion como un vector de individuos
def mostrar_poblacion_vector(poblacion):
    print("Poblacion: ", len(poblacion))
    for i in range(len(poblacion)):
        print(poblacion[i])

#convertir el individuo en un tablero de n reinas
def mostrar_tablero(poblacion, individuo):
    print("Tablero del individuo ", individuo, ":")
    for i in range(n):
        for j in range(n):
            if poblacion[individuo][i] == j:
                print("R", end=" ")
            else:
                print("-", end=" ")
        print()

#genera el tablero de agedrez de 8x8 en matplotlib con diferentes colores y dibuja las reinas en el tablero
def graficar_tablero(poblacion, individuo):
    tablero = np.zeros((n,n))
    for i in range(n):
        tablero[i][poblacion[individuo][i]] = 1
    plt.imshow(tablero, cmap='binary')
    plt.show()
#convirtiendo todos los individuos de la poblacion en tableros de n reinas iguales a la funcion mostrar_tablero
def mostrar_poblacion(poblacion):
    print("Poblacion: ", len(poblacion))
    for i in range(len(poblacion)):
        mostrar_tablero(poblacion, i)


""" apartir de esta parte todas las funciones que se encuentran son para el calculo de el fitness de cada individuo de la poblacion"""
#primera funcion util para el calculo del fitness(cantidad de ataques maximas que puede tener un individuo)
def calmax(n):
    maximo = 0
    for i in range(n):
        for j in range(i+1, n):
            maximo += 1
    return maximo
#segunda funcion util para el calculo del fitness(cantidad de ataques que tiene un individuo horizontal, vertical y diagonalmente)
def calataques(poblacion, individuo):
    #se establece el contador de ataques
    ataques = 0
    #se recorre el tablero del individuo
    for i in range(n):
        #se recorre el tablero del individuo
        for j in range(i+1, n):
            #se verifica si hay una reyna en la misma fila
            if poblacion[individuo][i] == poblacion[individuo][j]:
                ataques += 1
            #se verifica si hay una reyna en la misma columna
            if i - poblacion[individuo][i] == j - poblacion[individuo][j]:
                ataques += 1
            #se verifica si hay una reyna en la misma diagonal
            if i + poblacion[individuo][i] == j + poblacion[individuo][j]:
                ataques += 1
    return ataques

#calculo de ataques de cada individuo de la poblacion
def calcular_ataques_poblacion(poblacion):
    ataques = []
    for i in range(len(poblacion)):
        ataques.append(calataques(poblacion, i))
    return ataques


#se muestran los ataques de cada individuo de la poblacion
def mostrar_ataques_poblacion(poblacion):
    ataques = calcular_ataques_poblacion(poblacion)
    for i in range(len(poblacion)):
        print("Ataques de individuo ", i, ":", ataques[i])


#tercera funcion util para el calculo del fitness(esta funcion devolvera la resta de el maximo de ataques que puede tener un individuo y la cantidad de ataques que tiene el individuo)
def calgen(poblacion, individuo):
    return calmax(n) - calataques(poblacion, individuo)

#cuarta funcion util para el calculo del fitness(usando la funcion calfitness para aplicar el calculo a todos los individuos de la poblacion)
def calcular_genes_poblacion(poblacion):
    gen = []
    for i in range(len(poblacion)):
        gen.append(calgen(poblacion, i))
    return gen

#funcion que busca en calcular_genes_poblacion un numero en especifico
def buscar_genes(gen, numero):
    for i in range(len(gen)):
        if gen[i] == numero:
            return i
    return -1


#suma de todos los genes de la poblacion
def suma_genes(gen):
    suma = 0
    for i in range(len(gen)):
        suma += gen[i]
    return suma


#funcion que reliza la division entre la aptitud de cada individuo y la suma de todas las aptitudes de la poblacion para todos los individuos
def calcular_fitness(gen):
    suma = suma_genes(gen)
    fitness = []
    for i in range(len(gen)):
        fitness.append(gen[i]/suma)
    return fitness

#funcion que multiplica  el fitness de cada individuo por 100 para obtener un valor entero y asi poder usarlo como porcentaje
def calcular_fitness_porcentaje(fitness):
    fitness_porcentaje = []
    for i in range(len(fitness)):
        fitness_porcentaje.append(fitness[i]*100)
    return fitness_porcentaje

"""teminan todas las funciones que sirven para el calculo del fitness"""

#de todos los individuos se eligen 2 aleatoriamente se comparan sus genes y se elige el mejor de los 2 devolviendo su posicion en la poblacion
def seleccionar_padre(poblacion):
    gen = calcular_genes_poblacion(poblacion)
    fitness = calcular_fitness(gen)
    fitness_porcentaje = calcular_fitness_porcentaje(fitness)
    padre1 = random.randint(0, len(poblacion)-1)
    padre2 = random.randint(0, len(poblacion)-1)
    if gen[padre1] > gen[padre2]:
        return padre1
    else:
        return padre2























"""#seleccion de padres con el mayor fitness de la poblacion inicial
def seleccionar_padres(poblacion, fitness):
    padres = []
    for i in range(2):
        maximo = 0
        for j in range(len(fitness)):
            if fitness[j] > maximo:
                maximo = fitness[j]
                indice = j
        padres.append(poblacion[indice])
        fitness[indice] = 0
    return padres"""

#funcion para cruzar los padres con el metodo de un punto de cruce con una probabilidad entre 0.5 y 0.9
def cruzar_padres(padres):
    hijo = []
    probabilidad = random.uniform(0.5, 0.9)
    punto = int(probabilidad*n)
    for i in range(punto):
        hijo.append(padres[0][i])
    for i in range(punto, n):
        hijo.append(padres[1][i])
    return hijo

#funcion para mutar el hijo con una probabilidad entre 0.1 y 0.3
def mutar_hijo(hijo):
    probabilidad = random.uniform(0.1, 0.3)
    if probabilidad < 0.3:
        indice = random.randint(0, n-1)
        hijo[indice] = random.randint(0, n-1)
    return hijo

#introdcir el hijo a la poblacion inicial con el metodo de la sustitucion de peores
def sustituir_peor(poblacion, hijo):
    peor = 0
    for i in range(len(poblacion)):
        if calgen(poblacion, i) < calgen(poblacion, peor):
            peor = i
    poblacion[peor] = hijo
    return poblacion

#funcion para imprimir el tablero del mejor individuo de la poblacion inicial que es el que tiene el fitness igual a 1
def mostrar_mejor(poblacion):
    for i in range(len(poblacion)):
        if calgen(poblacion, i) == calmax(n):
            mostrar_tablero(poblacion, i)
        else:
            print("No hay solucion")
            break






#funcion main
def main():
    #muestra la cantidad de ataques maximas que puede tener un individuo
    #print("Cantidad de ataques maximas: ", calmax(n))
    #se establece la poblacion inicial
    hr = generar_poblacion_inicial(n)
    #mostrar el tamaño de la poblacion inicial
    print("Tamaño de la poblacion inicial: ", len(hr))
    #presionar enter para continuar
    input("Presione enter para continuar")
    #establecer una variable para guardar el numero de  veces que se repite el proceso
    contador = 0

    #se  repite el proceso de seleccionar padres, cruzarlos, mutarlos y sustituir el peor hasta que el valor maximo en genes de la poblacion sea igual a la cantidad de ataques maximas que puede tener un individuo
    while calmax(n) not in calcular_genes_poblacion(hr):
        #se muestra la poblacion inicial como un vector
        #mostrar_poblacion_vector(hr)


        







        #se calculan los ataques de cada individuo de la poblacion inicial
        ataques = calcular_ataques_poblacion(hr)
        #se muestra los ataques de cada individuo de la poblacion inicial
        #mostrar_ataques_poblacion(hr)
        #se calculan los genes de cada individuo de la poblacion inicial usando la funcion calgen que devuelve la resta de el maximo de ataques que puede tener un individuo y la cantidad de ataques que tiene el individuo
        gen = calcular_genes_poblacion(hr)
        #se muestra los genes de cada individuo de la poblacion inicial
        #print("Genes de la poblacion: ", gen)
        #se calcula la suma de todos los genes de la poblacion inicial
        suma = suma_genes(gen)
        #se muestra la suma de todos los genes de la poblacion inicial
        #print("Suma de genes: ", suma)
        #se identifica el primer mejor padre de la poblacion inicial
        padre1 = seleccionar_padre(hr)
        #se muestra el primer mejor padre de la poblacion inicial
        #print("Primer mejor padre: ", hr[padre1])
        #se identifica el segundo mejor padre de la poblacion inicia pero no puede ser el mismo que el primer mejor padre
        padre2 = seleccionar_padre(hr)
        while padre2 == padre1:
            padre2 = seleccionar_padre(hr)
        #se identifica un tercer padre de la poblacion inicial pero no puede ser el mismo que el primer mejor padre ni el segundo mejor padre
        padre3 = seleccionar_padre(hr)
        while padre3 == padre1 or padre3 == padre2:
            padre3 = seleccionar_padre(hr)
        #se indetifica un cuarto padre de la poblacion inicial pero no puede ser el mismo que el primer mejor padre, el segundo mejor padre ni el tercer mejor padre
        padre4 = seleccionar_padre(hr)
        while padre4 == padre1 or padre4 == padre2 or padre4 == padre3:
            padre4 = seleccionar_padre(hr)
        #se muestra el segundo mejor padre de la poblacion inicial
        #print("Segundo mejor padre: ", hr[padre2])
        #se muestra el tercer mejor padre de la poblacion inicial
        #print("Tercer mejor padre: ", hr[padre3])
        #se muestra el cuarto mejor padre de la poblacion inicial
        #print("Cuarto mejor padre: ", hr[padre4])
        #se cruzan los padres para obtener un hijo
        hijo = cruzar_padres([hr[padre1], hr[padre2]])
        #se cruza el 4to mejor padre con el tercer mejor padre para obtener un segundo hijo
        hijo2 = cruzar_padres([hr[padre3], hr[padre4]])
        #se muestra el hijo
        #print("Hijo: ", hijo)
        #se muestra el segundo hijo
        #print("Hijo2: ", hijo2)
        """#se muestra los tableros de los padres y el hijo
        #tableros de los padres
        print("Tableros de los padres")
        mostrar_tablero(hr, padre1)
        mostrar_tablero(hr, padre2)
        #tablero del hijo
        print("Tablero del hijo")
        mostrar_tablero([hijo], 0)"""
        #se muta el hijo
        hijo = mutar_hijo(hijo)
        #se muestra el hijo mutado
        #print("Hijo mutado: ", hijo)
        #se muta el segundo hijo
        hijo2 = mutar_hijo(hijo2)
        #se muestra el segundo hijo mutado
        #print("Hijo2 mutado: ", hijo2)
        #se sustituye el peor individuo de la poblacion inicial por el hijo 1 mutado
        hr = sustituir_peor(hr, hijo)
        #se sustituye el peor individuo de la poblacion inicial por el hijo 2 mutado
        hr = sustituir_peor(hr, hijo2)
        #mostrar_ataques_poblacion(hr)
        print("resolviendo...")
        #se aumenta el contador en 1
        contador += 1
    
    #se busca en en el conjunto de genes de la poblacion inicial el valor maximo que es igual a la cantidad de ataques maximas que puede tener un individuo
    for i in range(len(hr)):
        if calmax(n) == calcular_genes_poblacion(hr)[i]:
            #se muestra el tablero del individuo con el valor maximo de genes
            #mostrar todos los genes de la poblacion
            #se muestra el numero de veces que se repite el proceso
            print("Numero de generaciones que pasaron: ", contador)
            print("Genes de la poblacion: ", calcular_genes_poblacion(hr))
            mostrar_tablero(hr, i),
            #grafica el tablero de ajedrez en matplotlib
            graficar_tablero(hr, i)

            break


        
 

main()
