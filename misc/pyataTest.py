import os

def send2Pd(message=''):
    os.system("echo '" + message + "' | pdsend 3000")

def on():
    message = '0 42'
    send2Pd(message)
