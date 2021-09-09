from pacote import Pacote, Mensagem
from ..config.config import *

def generateHandshake(id_Client,id_Server):
    byte_handshake_head = b''
    handshake = Pacote()
    return handshake