import random
import simpy

# el carro se conduce un tiempo y tiene que llegar a cargarse de energia
# luego puede continuar conduciendo
# Debe hacer cola (FIFO) en el cargador

# name: identificacion del carro
# bcs:  cargador de bateria
# driving_time: tiempo que conduce antes de necesitar carga
# charge_duration: tiempo que toma cargar la bateria

def car(env, name, bcs, driving_time, charge_duration):
    global totalGasStation
    # Simulate driving to the BCS
    yield env.timeout(driving_time)

    # Request one of its charging spots
    print('%s arriving at %d' % (name, env.now))
    llegada = env.now #llegada a la estacion de servicio
    with bcs.request() as req:  #pedimos conectarnos al cargador de bateria
        yield req

        # Charge the battery
        print('%s starting to charge at %s' % (name, env.now))
        yield env.timeout(charge_duration)
        print('%s leaving the bcs at %s' % (name, env.now))
        # se hizo release automatico del cargador bcs
        tiempoTotal= env.now - llegada
        totalGasStation = totalGasStation + tiempoTotal 
        print('%s leaving gas station at %s' % (name, tiempoTotal))

#
env = simpy.Environment()  #crear ambiente de simulacion
bcs = simpy.Resource(env, capacity=2) #el cargador de bateria soporta 2 carros
                                      #a la vez
totalGasStation = 0.0
numCarros = 10
RANDOM_SEED = 42 #para generar la misma serie de random
random.seed(RANDOM_SEED)
interval = 10

# crear los carros
for i in range(numCarros):
    t = random.expovariate(1.0 / interval)
    env.process(car(env, 'Car %d' % i, bcs, t, 5))

# correr la simulacion
env.run()
    
promedioGasStation = totalGasStation / numCarros
print "el promedio fue: " , promedioGasStation
