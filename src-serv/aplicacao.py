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
        self.msg_type = b''
        self.cli_id = int(42).to_bytes(1, 'big')
        self.serv_id = int(21).to_bytes(1, 'big')
        self.msg_id = b''
        self.pkgs_qty = b''
        self.pkg_id = b''
        self.payload_size = b''

        # Inicializando atributo de EOP
        self.EOP = b'\x4C\x4F\x56\x55'

        # Inicializando atributos de apoio
        self.rx_buffer = b''
        self.head_size = 10
        self.head = b''
        self.payload = b''
        self.TIPO_MENSAGEM = {'handshake': b'\x01',
                              'handshake-response': b'\x02',
                              'data': b'\x03',
                              'data-ok': b'\x04',
                              'timeout': b'\x05',
                              'error': b'\x06'}
        self.FLAGS = {'ENABLED': False,
                      'ERROR': False,
                      'GOT_PKG': False,
                      'GOT_HEAD': False,
                      'GOT_PKG_INFO': False,
                      'GOT_EOP': False}

    def status(self, step):
        msgs = ['A comunicação foi iniciada com sucesso!',
                'A comunicação não foi ativada, utilize o método "activate_comunication"']
        print(f'---> {msgs[step]}')

    def activate_comunication(self):
        self.com1.enable()
        self.FLAGS['ENABLED'] = True

    def read_pkg(self):
        if self.FLAGS['ENABLED']:
            self.rx_buffer = self.com1.getData()[0]
        else:
            self.status(1)

    def read_head(self):
        self.head = self.com1.getData(self.head_size)[0]
        self.msg_type = self.head[0]

    def read_payload(self):
        pass


def main():
    try:
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
