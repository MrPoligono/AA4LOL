import psutil, requests, websocket, json, base64, ssl, threading 
from controler import LCUcontroler
import traceback
stop = threading.Event()

def getLCU():
    for proces in psutil.process_iter(['name']):
        if proces.info['name'] in  ('LeagueClientUx.exe', 'LeagueClientUx'):
            try:
                args = dict(arg.lstrip('-').split('=', 1) for arg in proces.cmdline() if '=' in arg)
                if 'app-port' in args and 'remoting-auth-token' in args:
                    return args['app-port'], args['remoting-auth-token']
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                continue
    return None

def waitLCU():
    global controler
    while not stop.is_set():
        info = getLCU()
        if info:
            controler = LCUcontroler(info)
            return info
        stop.wait(1.0)

def onOpen(ws):
    print("open")
    ws.send(json.dumps([5, "OnJsonApiEvent"]))

def onMessage(ws, message):
    global controler
    if not message:
        return
    try:
        _, _, payload = json.loads(message)
        handlerMetod = controler.HANDLERS.get(payload["uri"])
        if handlerMetod:
            handlerMetod(payload)
    except Exception as e:
        print(f"error en handler {handlerMetod.__name__}: {e}")
        traceback.print_exception

def onError(ws, err):
    if isinstance(err, KeyboardInterrupt):
        stop.set()
    print(err)

def onClose(ws, statusCode, reason):
    print("Conexion terminada")


def run():
    while not stop.is_set():
        port, token = waitLCU()
        print(f"https//127.0.0.1:{port}", f"riot:{token}")
        auth = base64.b64encode(f"riot:{token}".encode()).decode()
        ws = websocket.WebSocketApp(
            f"wss://127.0.0.1:{port}",
            header=[f"Authorization: Basic {auth}"],
            on_open=onOpen,
            on_message=onMessage,
            on_error=onError,
            on_close=onClose
        )
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        if stop.wait(1.0):
            break

run()
