#####################################################
# Camada Física da Computação
# Carareto
# 11/08/2020
# Aplicação
####################################################


# esta é a camada superior, de aplicação do seu software de comunicação serial UART.
# para acompanhar a execução e identificar erros, construa prints ao longo do código!


from enlace import *
import timeit
import numpy as np
from PIL import Image
from io import BytesIO


# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)


def main():
    try:
        # declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        # para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)

        # Ativa comunicacao. Inicia os threads e a comunicação seiral
        com1.enable()
        t1 = timeit.default_timer()

        # Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print('\n---> A comunicação foi aberta com sucesso!')
        # aqui você deverá gerar os dados a serem transmitidos.
        # seus dados a serem transmitidos são uma lista de bytes a serem transmitidos. Gere esta lista com o
        # nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        with open('resources/img.bmp', 'rb') as image:
            f = image.read()
            txBuffer = bytearray(f)

        # faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
        img_size = len(f)
        print(f'---> Tamanho da imagem: {img_size} bytes')

        # finalmente vamos transmitir os tados. Para isso usamos a funçao sendData que é um método da camada enlace.
        # faça um print para avisar que a transmissão vai começar.
        # tente entender como o método send funciona!
        # Cuidado! Apenas trasmitimos arrays de bytes! Nao listas!

        txBuffer = np.array(txBuffer)
        com1.sendData(np.asarray(txBuffer))

        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # Tente entender como esse método funciona e o que ele retorna
        txSize = com1.tx.getStatus()
        # Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        # Observe o que faz a rotina dentro do thread RX
        # print um aviso de que a recepção vai começar.
        print('\n---> A recepção vai começar!')
        # Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        # Veja o que faz a funcao do enlaceRX  getBufferLen
        buffer_size = com1.tx.getBufferLen()
        print(f'---> Tamanho do buffer: {buffer_size} bytes')
        print(
            f'\n---> Tamanho da imagem = Tamanho do buffer? {buffer_size == img_size}')

        # acesso aos bytes recebidos
        txLen = len(txBuffer)
        rxBuffer, nRx = com1.getData(txLen)
        print("\nRecebido:\n {}\n" .format(rxBuffer))

        output_image = Image.open(BytesIO(rxBuffer))
        output_image.save('resources/out.bmp')

        # Encerra comunicação
        print("-----------------------------")
        print("---> Comunicação encerrada")
        com1.disable()

        t2 = timeit.default_timer()
        print(f'---> process took {t2 - t1} seconds')
        print("-----------------------------")

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()


    # so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
