import threading
import time
import logging
import random
from queue import Queue

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s',)

# Dimensiunea maximă a cozii (buffer)
BUF_SIZE = 10
q = Queue(BUF_SIZE)

# Firul producător
class ProducerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if not q.full():
                item = random.randint(1, 10)
                q.put(item)
                logging.debug(f'Putting {item} : {q.qsize()} items in queue')
                time.sleep(random.random())

# Firul consumator
class ConsumerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if not q.empty():
                item = q.get()
                logging.debug(f'Getting {item} : {q.qsize()} items in queue')
                time.sleep(random.random())

if __name__ == "__main__":
    # Inițializăm și rulăm firele de producător și consumator
    producer = ProducerThread()
    consumer = ConsumerThread()

    producer.start()
    time.sleep(2)  # Dăm un mic timp pentru a umple coada
    consumer.start()
