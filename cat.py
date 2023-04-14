from threading import Thread, Semaphore
import random
import time

NUM_SILLAS = 3
TTEMPO_ESPERA = 0.3
buffer = []

mut_buffer = Semaphore(1)
señaliza = Semaphore(0)
despertar = Semaphore(0)
respEspera = Semaphore(1)
multiplexAlu =Semaphore(5)

s = Semaphore(3)

def catorrazos(id):
	cant = random.randint(1,5)
	for i in range(cant):
		print('Soy %d: y daré %d !!!' %(id,cant))
		time.sleep(random.random())

def catorrea(id,s):
	s.acquire()
	catorrazos(id)
	s.release()

for i in range(10):
	Thread(target=catorrea, args=[i,s]).start()

