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
        self.head_container = [self.msg_type, self.cli_id, self.serv_id,
                               self.msg_id, self.pkgs_qty, self.pkg_id, self.payload_size, b'', b'', b'']

        # Inicializando atributo de EOP
        self.EOP = b'\x4C\x4F\x56\x55'

        # Inicializando atributos de apoio
        self.file_type = ''
        self.pkg_size = int(128).to_bytes(1, 'big')
        self.pkg_counter = 0
        self.eop_size = 4
        self.eop = b''
        self.head_size = 10
        self.head = b''
        self.msg_id_list = []
        self.pkgs_qty_list = []
        self.pkg_id_list = []

        self.payload = b''
        self.msg_type_dict = {'handshake': b'\x01',
                              'handshake-response': b'\x02',
                              'data': b'\x03',
                              'data-ok': b'\x04',
                              'timeout': b'\x05',
                              'error': b'\x06'}
        self.FLAGS = {'ENABLED': False,
                      'GOT_HEAD': False,
                      'GOT_FILE_TYPE': False,
                      'GOT_HEAD_INFO': False,
                      'SENT_HS_RESPONSE': False,  
                      'HS_PAYLOAD': False,
                      'ERROR': False,
                      'GOT_PAYLOAD': False,
                      'GOT_EOP': False,
                      'END_OF_MSG': False}
        self.STATUS = {'activate_com_ok': '', 'activate_com_!ok': '',
                       'disable_com': '',
                       'read_pkg': '',
                       'read_head_ok': '', 'read_head_!ok': '',
                       'get_head_1': '', 'hs': '', 'get_head_2': '', 'get_head_!ok': '',
                       '': ''}

    def status(self, msg):
        print(f'---> {self.STATUS[msg]}!')

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
        else:
            return 'error'

        if self.FLAGS['GOT_HEAD']:
            self.get_head_infos()
        if self.FLAGS['GOT_HEAD_INFO']:
            self.read_payload()
        if self.FLAGS['GOT_PAYLOAD']:
            self.check_eop()
        if self.FLAGS['END_OF_MSG']:
            self.disable_comunications()
            return 'END'

    def read_head(self):
        self.head = self.com1.getData(self.head_size)[0]
        for i in arange(self.head_size):
            self.head_container[i] = self.head[i]
        self.msg_id_list.append(self.msg_id)
        self.pkgs_qty_list.append(self.pkgs_qty)
        self.pkg_id_list.append(self.pkg_id)
        self.pkg_counter = int.to_bytes(self.pkgs_qty, 'big')
        self.status(2)
        self.FLAGS['GOT_HEAD'] = True

    def get_head_infos(self):
        if self.msg_type == b'\x01' and not self.FLAGS['SENT_HS_RESPONSE']:
            head_response_list = [self.msg_type_dict['handshake-response'], self.cli_id, self.serv_id,
                                  self.msg_id, self.pkgs_qty, self.pkg_id, self.payload_size, b'\x00\x00\x00']
            head_response = b''.join(head_response_list)
            self.status(3)
            self.com1.sendData(head_response)
            self.status(5)
            self.FLAGS['SENT_HS_RESPONSE'] = True
            self.FLAGS['GOT_HEAD_INFO'] = True
            self.FLAGS['HS_PAYLOAD'] = True
        elif self.msg_type == b'\x03' and self.FLAGS['SENT_HS_RESPONSE']:
            self.status(3)
        else:
            
            pass

    def read_payload(self):
        if self.FLAGS['HS_PAYLOAD']:
            self.com1.getData(self.payload_size)[0]
            self.FLAGS['HS_PAYLOAD'] = False
        elif int.to_bytes(self.pkg_id, 'big') == 0:
            self.file_type = self.com1.getData(self.payload_size)[
                0].decode('ascii')
            self.FLAGS['GOT_FILE_TYPE'] = True
        else:
            self.payload += self.com1.getData(self.payload_size)[0]
        self.FLAGS['GOT_PAYLOAD'] = True
        self.status(6)

    def check_eop(self):
        self.eop = self.com1.getData(self.eop_size)
        self.FLAGS['GOT_EOP'] = True
        if self.eop == self.EOP:
            self.pkg_counter -= 1
            if self.pkg_counter == 0:
                self.FLAGS['END_OF_MSG'] = True


def main():
    ans = ''
    try:
        server = Server()
        server.activate_comunication()
        while (ans != 'END' or ans != 'error'):
            ans = server.read_pkg()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        server.disable()


if __name__ == "__main__":
    main()
