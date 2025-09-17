# backend/capture.py
import threading
import time
import random
from collections import defaultdict, deque

WINDOW_SIZE = 5  # segundos
KEEP_WINDOWS = 60

# Estrutura de janelas de tráfego
lock = threading.Lock()
windows = deque(maxlen=KEEP_WINDOWS)

def new_window(start_ts):
    return {
        "start": start_ts,
        "data": defaultdict(lambda: {"in": 0, "out": 0, "protocols": defaultdict(int)})
    }

# Inicializa primeira janela
with lock:
    now = int(time.time())
    windows.append(new_window(int(now // WINDOW_SIZE * WINDOW_SIZE)))

# Rotator de janelas
def window_rotator():
    cur_start = windows[-1]['start']
    while True:
        time.sleep(0.5)
        now = int(time.time())
        expected_start = int(now // WINDOW_SIZE * WINDOW_SIZE)
        if expected_start != cur_start:
            cur_start = expected_start
            with lock:
                windows.append(new_window(cur_start))

# Função que gera tráfego falso
def fake_traffic_generator(server_ip):
    clients = ["192.168.0.10", "192.168.0.11", "192.168.0.12", "192.168.0.13", "192.168.0.14"]
    protocols = ["HTTP", "HTTPS", "FTP", "TCP", "UDP", "ICMP"]
    while True:
        time.sleep(1)
        client = random.choice(clients)
        direction = random.choice(["in", "out"])
        proto = random.choice(protocols)
        size = random.randint(200, 5000)  # bytes
        window_ts = int(time.time() // WINDOW_SIZE * WINDOW_SIZE)
        with lock:
            if not windows or windows[-1]['start'] != window_ts:
                windows.append(new_window(window_ts))
            entry = windows[-1]['data'][client]
            entry[direction] += size
            entry['protocols'][proto] += size

# Função para iniciar a captura (simulada)
def start_capture(server_ip):
    # Inicia thread para gerar tráfego falso
    threading.Thread(target=fake_traffic_generator, args=(server_ip,), daemon=True).start()
    # Inicia thread para rotacionar janelas
    threading.Thread(target=window_rotator, daemon=True).start()
