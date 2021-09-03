#####################################################
# Camada Física da Computação
# Carareto
# 11/08/2020
# Aplicação
####################################################


from enlace import *
import timeit
import numpy as np
from PIL import Image
from io import BytesIO


class Server:

    def __init__(self) -> None:
        '''

        '''

        # Inicializando objeto "com1"
        self.serial_number = "/dev/ttyACM0"
        self.com1 = enlace(self.serial_number)

        # Inicializando atributos de "head"
        self.cli_id = int(42).to_bytes(1, 'big')
        self.serv_id = int(69).to_bytes(1, 'big')
        self.msg_id = b''
        self.packs_qty = b''
        self.pack_id = 0
        self.payload_size = b''

        # Inicializando atributos de apoio
        self.FLAGS = {'ENABLED': False}

    def activate_comunication(self):
        self.com1.enable()
        self.FLAGS['ENABLED'] = True

    def read_payload(self):
        if self.FLAGS['ENABLED']:
            pass
        else:
            print('---> A comunicação não foi ativada, utilize o método "activate_comunication"')


serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)


def main():
    try:
        com1 = enlace(serialName)
        com1.enable()
        print('\n---> A comunicação foi aberta com sucesso!')

        t1 = timeit.default_timer()

        t2 = timeit.default_timer()

        print("-----------------------------")
        print("---> Comunicação encerrada")
        com1.disable()

        print(f'---> process took {t2 - t1} seconds')
        print("-----------------------------")

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()


if __name__ == "__main__":
    main()
