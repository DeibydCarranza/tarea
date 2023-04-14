from threading import Thread, Semaphore
import random
import time

NUM_ALUMNOS = 5
NUM_SILLAS = 3
TTEMPO_ESPERA = 0.3
buffer = []

mut_buffer = Semaphore(1)
señaliza = Semaphore(0)
despertar = Semaphore(0)

respEspera = Semaphore(1)

multiplexAlu =Semaphore(NUM_SILLAS)

def alumno(id):
    numPreg = random.randint(1,5)
    while numPreg > 0:
        
        time.sleep(TTEMPO_ESPERA)
        #respEspera.release() ############ Último hilo creado
        print('El alumno %d ha entrado al cubículo y tiene %d preguntas' %(id,numPreg))
        multiplexAlu.acquire()
        with mut_buffer:
            buffer.append([id,numPreg])
        despertar.release()
        #señaliza.release()
        numPreg -= 1
        print('sadd')



def profesor():
    while True:
        print('Entrando al profe')
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

        multiplexAlu.release()
        while contPreg > 0:
            mut_buffer.acquire()
            print('Respondiendo la pregunta %d del alumno %d ' % (contPreg, infoPreg[0]))
            contPreg-=1
            mut_buffer.release()

            #respEspera.acquire()  ######## Último hilo creado



Thread(target=profesor,args=[]).start()

for i in range(NUM_ALUMNOS):
    Thread(target=alumno,args=[i]).start()