#####################################################
# Camada Física da Computação
# Carareto
# 11/08/2020
# Aplicação
####################################################


# esta é a camada superior, de aplicação do seu software de comunicação serial UART.
# para acompanhar a execução e identificar erros, construa prints ao longo do código!


import random
from enlace import *
import timeit
import numpy as np
from PIL import Image
from io import BytesIO
from pacote import Pacote, Head, Payload, Mensagem


#   python -m serial.tools.list_ports
serialName = "/dev/cu.usbmodem1412401"

def main():
    try:
        # Declaração de Variáveis:
        com1 = enlace(serialName)
        id_client = b'\x42'
        id_client = b'\x12'
        headByteArray = b''
        payloadByteArray = b''
        mensagem = Mensagem('loss.bmp')
        id_mensagem = int(random.randint(0,255)).to_bytes(1,'big')

        # Ativa comunicacao. Inicia os threads e a comunicação seiral
        com1.enable()
        handshake = generateHandshake()

        # Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print('\n---> A comunicação foi aberta com sucesso!\n')

        # Converter a mensagem em bytes:
        headHandshake_values = {}
        handshake = Pacote()
        lista_payloads = mensagem.construir_payloads()


        

        # Encerra comunicação
        print("-----------------------------")
        print("---> Comunicação encerrada")
        print("-----------------------------")
        com1.disable()


    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()


    # so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
