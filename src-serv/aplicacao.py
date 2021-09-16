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
                      'CHECK_HEAD': False,
                      'SENT_HS_RESPONSE': False,
                      'HS_PAYLOAD': False,
                      'ERROR': False,
                      'GOT_PAYLOAD': False,
                      'GOT_EOP': False,
                      'END_OF_MSG': False,
                      'GOT_SIZE': False,
                      'FIRST_RUN': True}

        self.STATUS = {'activate_com_ok': 'Comunication activated', 'activate_com_!ok': 'Comunication NOT activated',
                       'disable_com': 'Comunication disabled',
                       'read_pkg': 'Reading package',
                       'read_head_ok': 'Head ok', 'read_head_!ok': 'Head NOT ok',
                       'got_hs': 'Handshake received', 'sent_hs': 'Handshake response sent', 'got_data': 'Data received', 'sent_dataOK': 'Sent data received confirmation', 'check_head_!ok': 'Problem with head',
                       'got_pl': 'Payload received', 'got_filetype': 'Filetype received', 'read_payload_!ok': 'Payload NOT received', 'no_pl': 'No payload from HS',
                       'eop_error': 'EOP error'}

    def status(self, msg):
        print(f'---> {self.STATUS[msg]}!')

    def activate_comunication(self):
        self.com1.enable()
        self.status('activate_com_ok')
        self.FLAGS['ENABLED'] = True

    def disable_comunications(self):
        self.com1.disable()
        self.status('disable_com')
        self.FLAGS['ENABLED'] = False

    def init(self):
        self.FLAGS['GOT_HEAD'] = False
        self.FLAGS['CHECK_HEAD'] = False
        self.FLAGS['GOT_PAYLOAD'] = False
        self.FLAGS['END_OF_MSG'] = False
        self.FLAGS['GOT_EOP'] = False

    def read_pkg(self):
        self.com1.rx.clearBuffer()
        self.init()
        self.status('read_pkg')

        if self.FLAGS['ENABLED'] and not self.FLAGS['ERROR']:
            self.read_head()
        else:
            return False

        if self.FLAGS['GOT_HEAD'] and not self.FLAGS['ERROR']:
            self.read_payload()
        else:
            return False

        if self.FLAGS['GOT_PAYLOAD'] and not self.FLAGS['ERROR']:
            self.check_eop()
        else:
            return False

        if self.FLAGS['GOT_EOP'] and not self.FLAGS['ERROR']:
            self.ans()
        else:
            return False

        if self.FLAGS['END_OF_MSG'] and not self.FLAGS['ERROR']:
            self.disable_comunications()
            return False
        else:
            return True

    def read_head(self):
        try:
            self.head = self.com1.getData(self.head_size)[0]
            self.msg_type = self.head[0].to_bytes(1, 'big')
            self.cli_id = self.head[1].to_bytes(1, 'big')
            self.serv_id = self.head[2].to_bytes(1, 'big')
            self.msg_id = self.head[3].to_bytes(1, 'big')
            self.pkgs_qty = self.head[4].to_bytes(1, 'big')
            self.pkg_id = self.head[5].to_bytes(1, 'big')
            self.payload_size = self.head[6]

            # mudar para dicio {pkg_id: {}}
            self.msg_id_list.append(self.msg_id)
            self.pkgs_qty_list.append(self.pkgs_qty)
            self.pkg_id_list.append(self.pkg_id)
            if self.FLAGS['GOT_SIZE']:
                self.pkg_counter = int.from_bytes(self.pkgs_qty, 'big')

            if self.msg_type == b'\x01' and self.FLAGS['FIRST_RUN']:
                self.pkg_counter += 2
                self.FLAGS['HS_PAYLOAD'] = True

            self.status('read_head_ok')
            self.FLAGS['GOT_HEAD'] = True
        except Exception as erro:
            self.FLAGS['ERROR'] = True

    def read_payload(self):
        try:
            if self.FLAGS['HS_PAYLOAD']:
                self.status('no_pl')
                self.FLAGS['GOT_SIZE'] = True
                self.FLAGS['FIRST_RUN'] = False
            elif self.pkg_id == b'\x00' and not self.FLAGS['GOT_FILE_TYPE']:
                self.file_type = self.com1.getData(self.payload_size)[
                    0].decode('ascii')
                self.FLAGS['GOT_FILE_TYPE'] = True
                self.FLAGS['GOT_SIZE'] = False
                self.status('got_filetype')
            else:
                self.payload += self.com1.getData(self.payload_size)[0]
                self.status('got_pl')
            self.FLAGS['GOT_PAYLOAD'] = True
        except Exception as erro:
            self.status('read_payload_!ok')
            self.FLAGS['ERROR'] = True

    def save_file(self):
        file = self.file_type
        with open("resources/" + file, "wb") as bin_file:
            bin_file.write(self.payload)

    def check_eop(self):
        try:
            self.eop = self.com1.getData(self.eop_size)[0]
            self.FLAGS['GOT_EOP'] = True
            if self.eop == self.EOP:

                self.pkg_counter -= 1
                if self.pkg_counter == 0:
                    self.FLAGS['END_OF_MSG'] = True
                    self.save_file()
        except Exception as erro:
            self.status('eop_error')
            self.FLAGS['ERROR'] = True

    def ans(self):
        try:
            if self.msg_type == b'\x01' and not self.FLAGS['SENT_HS_RESPONSE']:
                self.status('got_hs')
                head_response_list = [self.msg_type_dict['handshake-response'],
                                      self.cli_id, self.serv_id, self.msg_id, b'\x00\x00\x00\x00\x00\x00']
                head_response = b''.join(head_response_list)

                self.com1.sendData(head_response)
                self.status('sent_hs')
                self.FLAGS['HS_PAYLOAD'] = False
                self.FLAGS['SENT_HS_RESPONSE'] = True
            elif self.msg_type == b'\x03' and self.FLAGS['SENT_HS_RESPONSE']:
                self.status('got_data')
                dataOK_response_list = [self.msg_type_dict['data-ok'], self.cli_id,
                                        self.serv_id, self.msg_id, b'\x00\x00\x00\x00\x00\x00']
                dataOK_response = b''.join(dataOK_response_list)
                self.com1.sendData(dataOK_response)
                self.status('sent_dataOK')
        except Exception as erro:
            self.status('check_head_!ok')
            self.FLAGS['ERROR'] = True


def main():
    ans = ''
    try:
        server = Server()
        server.activate_comunication()
        while (server.read_pkg()):
            print('---> pkg OK!\n\n')

        if ans == 'error':
            print('ERROOOOO')

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        server.disable()


if __name__ == "__main__":
    main()
