from threading import Thread, Semaphore
import random
import time

NUM_ALUMNOS = 5
NUM_SILLAS = 3
TTEMPO_ESPERA = 0.3
buffer = []

mut_buffer = Semaphore(1)
despertar = Semaphore(0)

multiplexAlu =Semaphore(NUM_SILLAS)

def alumno(id):
    numPreg = random.randint(1,5)
    while numPreg > 0:
        
        time.sleep(TTEMPO_ESPERA)
        print('El alumno %d ha entrado al cubículo y tiene %d preguntas' %(id,numPreg))

        with mut_buffer:
            buffer.append([id,numPreg])
        despertar.release()
        numPreg -= 1
    print('\t\tSaliendo alumno %d \n' %id)

def profesor():
    while True:
        print('Entrando al profe')
         #Despertando al profe
        despertar.acquire()


        #Sección crítica para obtener preguntas
        mut_buffer.acquire()
        if len(buffer) == 0:
            print('\t\tNo hay preguntas en la cola, me voy a dormi')
            mut_buffer.release()
            continue
        #Extrayendo al alumno con su id y el numero de pregunta
        infoPreg = buffer.pop(0)
        contPreg=infoPreg[1]
        mut_buffer.release()

        while contPreg > 0:
            mut_buffer.acquire()
            print('Respondiendo la pregunta %d del alumno %d ' % (contPreg, infoPreg[0]))
            contPreg-=1
            mut_buffer.release()

#Por medio de un multiplex generamos la restricción de solo NUM_SILLAS dentro del cúbiculo 
def llamada(id,multiplexAlu):
    multiplexAlu.acquire()
    alumno(id)
    multiplexAlu.release()

Thread(target=profesor,args=[]).start()

for i in range(NUM_ALUMNOS):
    Thread(target=llamada,args=[i,multiplexAlu]).start()