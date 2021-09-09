from numpy import arange

class Pacote:
    def __init__(self, byteArrayHead, byteArrayPayload):
        self.head = Head(byteArrayHead)
        self.payload = Payload(byteArrayPayload)
        self.EOP = b'/x4C/x4F/x56/x55'
        
    def build_pacote(self):
        pacote = b''
        pacote += self.head.byteHead + self.payload.bytePayload + self.EOP
        return pacote

class Mensagem():
    def __init__(self, data_path):
        with open(data_path, "rb") as image:
            f = image.read()
            self.mensagem = bytearray(f)
            print('\n---> Imagem convertida em bytes\n')

    def construir_payloads(self):
        lista_payloads=[]
        payload = b''
        FLAG = 100
        for byte in self.mensagem:
            if FLAG >= 100:
                if payload != b'':
                    lista_payloads.append(payload)
                FLAG = 0
                payload = byte
            else:
                payload += byte
                FLAG += 1
        return lista_payloads