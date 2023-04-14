from threading import Thread, Semaphore
import random
import time

NUM_ALUMNOS = 5
NUM_SILLAS = 3
TTEMPO_ESPERA = 0.3
PREGUNTAS = 5
buffer = []

mut_buffer = Semaphore(1)
señal = Semaphore(1)
despertar = Semaphore(0)
impreSem = Semaphore(1)
multiplexAlu =Semaphore(NUM_SILLAS)

def alumno(id):
    numPreg = random.randint(1,PREGUNTAS)
    var = 1
    while var <= numPreg:
        with impreSem:
            print('El alumno %d ha entrado al cubículo y tiene %d preguntas' %(id,numPreg))
        señal.acquire()

        with mut_buffer:
            buffer.append([id,var])
        despertar.release()
        var += 1
        time.sleep(TTEMPO_ESPERA)

    with impreSem:
        print('\t\t\tSaliendo alumno %d \n' %id)

def profesor():
    while True:
        #Despertando al profe
        print('\tProfe despierto')
        despertar.acquire()

        with mut_buffer:
            infoPreg = buffer.pop(0)
            contPreg=infoPreg[1]
            print('Respondiendo la pregunta %d del alumno %d ' % (contPreg, infoPreg[0]))
        señal.release()

#Por medio de un multiplex generamos la restricción de solo NUM_SILLAS dentro del cúbiculo 
def llamada(id,multiplexAlu):
    multiplexAlu.acquire()
    alumno(id)
    multiplexAlu.release()

Thread(target=profesor,args=[]).start()

for i in range(NUM_ALUMNOS):
    Thread(target=llamada,args=[i,multiplexAlu]).start()

