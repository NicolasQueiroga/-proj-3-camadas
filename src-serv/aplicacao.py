#####################################################
# Camada Física da Computação
# Carareto
# 11/08/2020
# Aplicação
####################################################


from enlace import *
import timeit
from numpy import arange
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
        self.cli_id = b''
        self.serv_id = b''
        self.msg_id = b''
        self.pkgs_qty = b''
        self.pkg_id = b''
        self.payload_size = b''
        self.head_container = [self.msg_type, self.cli_id, self.serv_id, self.msg_id, self.pkgs_qty, self.pkg_id, self.payload_size]

        # Inicializando atributo de EOP
        self.EOP = b'\x4C\x4F\x56\x55'

        # Inicializando atributos de apoio
        self.rx_buffer = b''
        self.pkg_size = int(128).to_bytes(1, 'big')
        self.head_size = 10
        self.head = b''
        self.msg_id_list = []
        self.pkgs_qty_list = []
        self.pkgs_id_list = []

        self.payload = b''
        self.msg_type_dict = {'handshake': b'\x01',
                              'handshake-response': b'\x02',
                              'data': b'\x03',
                              'data-ok': b'\x04',
                              'timeout': b'\x05',
                              'error': b'\x06'}
        self.ACTIVE_ACTION = ''
        self.FLAGS = {'ENABLED': False,
                      'GOT_HEAD': False,
                      'GOT_HEAD_INFO': False,
                      'SENT_HS_RESPONSE': False,
                      'ERROR': False,
                      'GOT_PKG': False,
                      'GOT_EOP': False}
        self.STATUS = ['Comunicação Iniciada com sucesso', 'Comunicação Terminada com sucesso', 'Head Lida com sucesso', 'Informações do Head extraídas com sucesso', 'Check do head feito', 'Envio da resposta do HANDSHAKE Enviada com sucesso', ]

    def status(self, step):
        print(f'---> {self.STATUS[step]}!')

    def activate_comunication(self):
        self.com1.enable()
        self.status(0)
        self.FLAGS['ENABLED'] = True
    
    def disable_comunications(self):
        self.com1.disable()
        self.status(1)
        self.FLAGS['ENABLED'] = False


    def read_pkg(self):
        if self.FLAGS['ENABLED']:
            self.read_head()
        if self.FLAGS['GOT_HEAD']:
            self.get_head_infos()

    def read_head(self):
        self.head = self.com1.getData(self.head_size)[0]
        for i in arange(len(self.head_container)):
            self.head_container[i] = self.head[i]
        self.status(2)
        self.FLAGS['GOT_HEAD'] = True
    
    def get_head_infos(self):
        if self.msg_type == b'\x01' and not self.FLAGS['SENT_HS_RESPONSE']:
            head_response_list = [self.msg_type_dict['handshake-response'], self.cli_id, self.serv_id, self.msg_id, self.pkgs_qty, self.pkg_id, self.payload_size, b'\x00\x00\x00']
            head_response = b''.join(head_response_list)
            self.status(3)
            self.com1.sendData(head_response)
            self.status(5)
            self.FLAGS['SENT_HS_RESPONSE'] = True
            self.FLAGS['GOT_HEAD'] = False
            self.FLAGS['GOT_HEAD_INFO'] = False
            self.read_pkg()
        if self.msg_type == b'\x03' and self.FLAGS['SENT_HS_RESPONSE']:
            self.status(3)



    def read_payload(self):
        if self.FLAGS['ENABLED']:
            self.rx_buffer = self.com1.getData(self.pkg_size)[0]
            self.FLAGS['GOT_PKG'] = True
        else:
            self.status()



def main():
    try:
        server = Server()
        server.activate_comunication()
        server.read_pkg()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        server.disable()


if __name__ == "__main__":
    main()
