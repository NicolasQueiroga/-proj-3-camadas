TIPO_MENSAGEM = {'handshake':b'\x01','handshake-response':b'\x02','data':b'\x03','data-ok':b'\x04','timeout':b'\x05','error':b'\x06'}
EOP = b'\x4C\x4F\x56\x55'


def generateHandshake(id_Client,id_Server,id_Msg):
    tipo_mensagem = TIPO_MENSAGEM['handshake']
    list_handshake = [tipo_mensagem, id_Client, id_Server, id_Msg,  b'\x00\x00\x00\x00\x00\x00', b'\x4C\x4F\x56\x55']
    handshake = b''.join(list_handshake)
    #print(handshake)
    return handshake

def generateFirstPkg(id_Client,id_Server,id_Msg,number_of_pkgs,file_name):
    tipo_mensagem = TIPO_MENSAGEM['data']
    bytes_first_pkg_payload = file_name.encode()
    #print(f'\nbytes payload: {bytes_first_pkg_payload}\n')
    list_first_pkg_head = [tipo_mensagem, id_Client, id_Server, id_Msg, number_of_pkgs, b'\x00', len(bytes_first_pkg_payload).to_bytes(1,'big'),b'\x00\x00\x00']
    first_pkg_head = b''.join(list_first_pkg_head)
    first_pkg = first_pkg_head + bytes_first_pkg_payload + EOP
    return first_pkg

def generatePkg(id_Client,id_Server,id_Msg,number_of_pkgs,pkg_id,lista_payloads):
    tipo_mensagem = TIPO_MENSAGEM['data']
    payload = lista_payloads[pkg_id-1]
    #print(payload)
    list_pkg_head = [tipo_mensagem, id_Client, id_Server, id_Msg, number_of_pkgs, int(pkg_id).to_bytes(1,'big'), len(payload).to_bytes(1,'big'),b'\x00\x00\x00']
    pkg_head = b''.join(list_pkg_head)
    #print(pkg_head)
    pkg = pkg_head + payload + EOP
    #print(f'\nPACOTE: {pkg}\n')
    return pkg