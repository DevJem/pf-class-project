# Jeremy DeHay
# Security Scripting w/ Python
# CYBR-260-40
# python 3.5


import socket
import flowplayer_dance
# import requests
import sys
# import threading


def server(host):
    # serving = threading.Thread(target=run_server)
    # serving.start()
    # serving.join(timeout=5)
    # if serving.is_alive():
    #     print("Encoding callbacks took too long...")
    print(socket.gethostbyname(socket.gethostname()))
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print(flowplayer_dance.get_ip())
        s.bind(("0.0.0.0", 80))
        s.listen(10)

        print("listening")
        conn, addr = s.accept()
        print("1")
        data = conn.recv(20480)
        print("2")
        if data:
            print(data)
            conn.close()
            # if token == 'pythonisthegreatest':
        print("3")
        conn.close()
        print("4")
    except:
        e = sys.exc_info()
        print(e)
    print("exited server")
