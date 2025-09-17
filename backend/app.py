# backend/app.py
direction = None
client_ip = None
if src == SERVER_IP and dst != SERVER_IP:
direction = 'out'
client_ip = dst
elif dst == SERVER_IP and src != SERVER_IP:
direction = 'in'
client_ip = src
else:
return
proto = detect_protocol(pkt)
window_ts = int(time.time() // WINDOW_SIZE * WINDOW_SIZE)
with lock:
if not windows or windows[-1]['start'] != window_ts:
windows.append(new_window(window_ts))
win = windows[-1]
entry = win['data'][client_ip]
entry[direction] += total_len
entry['protocols'][proto] += total_len
except Exception as e:
# tratar erro porém não travar
print('process_packet error', e)


# inicia sniffer — só se scapy estiver disponível
def start_sniffer():
if sniff is None:
print('scapy não disponível — desabilitando sniffer. Instale scapy para captura ao vivo.')
return
bpf = f'host {SERVER_IP}'
# store=False para não guardar pacotes em memória
sniff(prn=process_packet, filter=bpf, store=False)


# endpoints
@app.get('/api/windows/latest')
async def get_latest_window():
with lock:
if not windows:
raise HTTPException(status_code=404, detail='No windows yet')
w = windows[-1]
clients = {}
for ip, v in w['data'].items():
clients[ip] = {"in": v['in'], "out": v['out'], "protocols": dict(v['protocols'])}
return {"start": w['start'], "clients": clients}


@app.get('/api/windows/history')
async def get_history(n: int = 10):
with lock:
res = []
for w in list(windows)[-n:]:
clients = {ip: {"in": v['in'], "out": v['out']} for ip,v in w['data'].items()}
res.append({"start": w['start'], "clients": clients})
return res


@app.get('/api/drilldown')
async def drilldown(start: int, client: str):
with lock:
for w in windows:
if w['start'] == start:
if client in w['data']:
return {"start": start, "client": client, "protocols": dict(w['data'][client]['protocols'])}
raise HTTPException(status_code=404, detail='Client not found in window')
raise HTTPException(status_code=404, detail='Window not found')


# start background threads
threading.Thread(target=window_rotator, daemon=True).start()
threading.Thread(target=start_sniffer, daemon=True).start()


# observação: execute com uvicorn: uvicorn backend.app:app --host 0.0.0.0 --port 8000