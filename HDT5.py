'''***********************************************************************************************************
Universidad del Valle de Guatemala
Algoritmos y Estructura de Datos
Seccion 30
Mario Galvez, 10113
Jose Alejandro Rivera, 14213
Hoja de Trabajo 5 - 26/08/2015
***********************************************************************************************************'''
import random
import simpy

numero_instrucciones= 0

def source(env, procesos, intervalo, espacioMemoria, instruccionesCPU, colaCPU, lista):#genera numeros aleatorios
     for i in range(procesos):
        numMemoria = random.randint(1,10) #genera un numero de 1 a 10 de memoria
        numInstrucciones = random.randint(1,10) #genera un numero de 1 a 10 de cantidad de instrucciones
        num = i +1
        env.process(memoria(env, espacioMemoria, numMemoria, 'Proceso %d' %num,instruccionesCPU, "ESPERANDO", colaCPU, numInstrucciones, lista))
        t = random.expovariate(1.0 / intervalo)
        yield env.timeout(t)
        
#env, 'Proceso %d' % i, i, CpuProc, memoria, numIns, numWait

def memoria(env, espacioMemoria, numMemoria, nombre, instruccionesCPU, estado, colaCPU, numInstrucciones, lista): #define si hay espacio suficiente en memoria para realizar los procesos
     yield espacioMemoria.get(numMemoria)
     print('%s tiene asignado memoria.' % (nombre))
     env.process(proceso(env, nombre, colaCPU, instruccionesCPU, numInstrucciones, estado, numMemoria, lista))

def proceso(env, nombre, colaCPU, instruccionesCPU, numInstrucciones, estado, numMemoria, lista):
     with colaCPU.request() as req:
         yield req
         print('%s esta iniciando' % (nombre))
         if numInstrucciones >= instruccionesCPU:
              yield env.timeout(instruccionesCPU)
         else:
              pass #si las instrucciones son menos de 3, el CPU se libera
         numInstrucciones = numInstrucciones - instruccionesCPU
         if numInstrucciones < 0:
              pendientes = 0
         else:
              pendientes = numInstrucciones
         print('%s ha realizado 3 instrucciones' % (nombre))
         print('%s tiene %d instrucciones pendientes' % (nombre, pendientes))
         if numInstrucciones < 0:
              estado = "TERMINADO"
              print ('%s esta %s' % (nombre, estado))
              lista.append(env.now)
              yield espacioMemoria.put(numMemoria)
         else:
              numRandom = random.randint(1,2)
              if numRandom ==1:
                   estado = "ESPERANDO"
                   print('%s esta %s' % (nombre, estado))
                   with colaEspera.request() as req2:
                        yield req2
                        yield env.timeout(instruccionesCPU)
                        print('%s esta realizando operaciones' % (nombre))
                   env.process(proceso(env, nombre, colaCPU, instruccionesCPU, numInstrucciones, estado, numMemoria, lista))

              else:
                   estado = "LISTO"
                   print('%s esta %s' % (nombre, estado))
                   env.process(proceso(env, nombre, colaCPU, instruccionesCPU, numInstrucciones, estado, numMemoria, lista))


env = simpy.Environment() #esto genera el ambiente
espacioMemoria = simpy.Container(env, init = 100, capacity= 100) #esto genera la cola de memoria (de tamano 100)
colaCPU = simpy.Resource(env, capacity = 1) #esto genera la cola de CPU (con capacidad de 1)
colaEspera = simpy.Resource(env, capacity = 1) #esto genera la cola de espera (con capacidad de 1)
procesos = 150
 #esta es la cantidad de procesos que se desea realizar
lista = []
tiempoFinal = 0.0

instruccionesCPU = 6
intervalo= 10.0 #funcion exponencial con intervalo 10
random_seed= 42 
random.seed(42)
env.process(source(env, procesos, intervalo, espacioMemoria, instruccionesCPU, colaCPU, lista)) #con esto se empieza a realizar el programa

env.run() #corre el programa
for i in range(procesos):
     tiempoFinal = tiempoFinal + lista[i]
print('El tiempo final es: %f' % (tiempoFinal))
