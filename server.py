import socket
import threading
import time
import random

# Configurații server
HOST = '127.0.0.1'  # Adresa IP locală (localhost)
PORT = 65432        # Portul pe care ascultă serverul

# Funcția de producător, care trimite date către clienți și salvează în fișier
def producator(conn, addr):
    print(f"Conectat la: {addr}")
    with open("log_mesaje.txt", "a") as log_file:  # Deschidem fișierul în modul 'append'
        while True:
            try:
                item = random.randint(1, 100)  # Producem un element aleator
                mesaj = f"Produs: {item}\n"
                conn.sendall(mesaj.encode('utf-8'))  # Trimitem datele către client
                print(f"Trimis: {mesaj.strip()} către {addr}")
                
                # Scriem mesajul în fișierul de log
                log_file.write(f"{mesaj.strip()} de la {addr}\n")
                log_file.flush()  # Asigurăm scrierea imediată în fișier
                
                time.sleep(random.uniform(1, 3))  # Întârziere aleatorie între produse
            except ConnectionResetError:
                print(f"Conexiunea cu {addr} a fost întreruptă.")
                break
    conn.close()

if __name__ == "__main__":
    # Cream un socket de server TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))  # Asociem adresa și portul cu serverul
        s.listen()  # Serverul ascultă conexiuni
        print(f"Serverul ascultă pe {HOST}:{PORT}")
        while True:
            # Acceptăm conexiuni noi
            conn, addr = s.accept()
            # Pentru fiecare client, rulăm un fir de execuție separat
            t = threading.Thread(target=producator, args=(conn, addr))
            t.start()
