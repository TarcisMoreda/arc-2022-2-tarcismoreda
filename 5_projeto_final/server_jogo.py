import random
import socket

# Número máximo de bytes que podem ser enviados
# de uma vez só com o UDP
MAX_BYTES = 65535
MAX_PLAYERS = 3


def server(port):
    jogadores = {'gamertag': [], 'address': [], 'points': []}
    setup = False

    # Criando o socket
    # AF_INET: utilizando a pilha de protocolos da Internet
    # SOCK_DGRAM: selecionando o protocolo UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Ligando o socket ao endereço de localhost
    # e à porta indicada pelo usuário (default = 1060)
    sock.bind(('127.0.0.1', port))

    # Loop aguardando as solicitações dos clientes
    while not setup:
        # A função recvfrom fica aguardando a chegada
        # da socilitação do cliente
        # Além dos dados enviados pelo cliente, também
        # conseguimos acessar o endereço IP do cliente
        data, address = sock.recvfrom(MAX_BYTES)

        # Decodificamos os dados para ascii e apresentamos
        # na sáida padrão
        text = data.decode('ascii')

        jogadores['address'].append(address)
        jogadores['gamertag'].append(text)
        jogadores['points'].append(1000)

        text = ''
        for i in range(len(jogadores['address'])):
            text += '{}#{}#{}|'.format(jogadores['gamertag'][i],
                                       jogadores['address'][i][0],
                                       jogadores['address'][i][1])

        data = text.encode('ascii')
        for ad in jogadores['address']:
            sock.sendto(data, ad)

        if len(jogadores['address']) == MAX_PLAYERS:
            setup = True

    level = -1
    data, address = sock.recvfrom(MAX_BYTES)
    text = data.decode('ascii')
    level = int(text)

    text = "{}#{}".format(level, "OK")
    data = text.encode("ascii")
    for ad in jogadores['address']:
        sock.sendto(data, ad)

    num_secreto = random.randrange(1, 101)
    tent = 0
    if level == 1:
        tent = 20
    elif level == 2:
        tent = 10
    else:
        tent = 5

    for i in range(tent):
        for j in range(MAX_PLAYERS):
            text = str(j + 1)
            data = text.encode('ascii')
            for ad in jogadores['address']:
                sock.sendto(data, ad)

            data, address = sock.recvfrom(MAX_BYTES)
            text = data.decode('ascii')

            guess = int(text)
            correct = guess == num_secreto
            bigger = guess > num_secreto
            smaller = guess < num_secreto

            if correct:
                jogadores['points'][j] += (tent - i) * level
                text = 'G#{}#{}'.format(j + 1, guess)
                for i in range(MAX_PLAYERS):
                    text += '#{}'.format(jogadores['points'][i])
                data = text.encode('ascii')
                for ad in jogadores['address']:
                    sock.sendto(data, ad)

                break

            else:
                if bigger:
                    text = 'B#{}#{}'.format(j + 1, guess)
                    data = text.encode('ascii')
                    for ad in jogadores['address']:
                        sock.sendto(data, ad)
                elif smaller:
                    text = 'S#{}#{}'.format(j + 1, guess)
                    data = text.encode('ascii')
                    for ad in jogadores['address']:
                        sock.sendto(data, ad)


if __name__ == '__main__':
    # Execução função com a porta do nosso servidor
    server(1060)
