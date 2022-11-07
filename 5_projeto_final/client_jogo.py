import os
import socket

# Número máximo de bytes que podem ser enviados
# de uma vez só com o UDP
MAX_BYTES = 65535
MAX_PLAYERS = 3


def client(port):
    curr_players = 0
    player_id = -1

    # Criando um socket
    # AF_INET: utilizando a pilha de protocolos da Internet
    # SOCK_DGRAM: selecionando o protocolo UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    text = input('Insira sua GamerTag:\n')
    # Preparamos os dados da solicitação
    data = text.encode('ascii')

    # Enviamos os dados para o endereço do servidor
    # na porta adequada (default = 1060)
    sock.sendto(data, ('127.0.0.1', port))

    while curr_players != 3:
        data, address = sock.recvfrom(MAX_BYTES)

        text = data.decode('ascii')
        for i, j in enumerate(text.split('|')):
            if (len(j) == 0):
                continue
            if (i == 0):
                os.system('cls' if os.name == 'nt' else 'clear')
            j = j.split('#')
            curr_players = i + 1
            print("Jogador {}:".format(i + 1))
            print("Gamertag: {}\nEndereço: {}:{}\n\n".format(j[0], j[1], j[2]))
        if player_id == -1:
            player_id = curr_players

    print("\n*********************************")
    print("Bem vindo ao jogo de Adivinhação!")
    print("*********************************\n")

    if player_id == 1:
        print("Defina o nível de dificuldade")
        level = input("(1)Fácil (2)Médio (3)Difícil\n")
        data = level.encode('ascii')
        sock.sendto(data, ('127.0.0.1', port))
    else:
        print('O jogador 1 esta escolhendo a dificuldade. Aguarde...')

    data, address = sock.recvfrom(MAX_BYTES)
    text = data.decode('ascii')
    text = text.split("#")
    if text[1] == "OK":
        print("Dificuldade escolhida: {}".format(text[0]))

    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        if int(data.decode('ascii')) == player_id:
            guess = input('Qual seu chute? (Entre 1 e 100):')
            data = guess.encode('ascii')
            sock.sendto(data, ('127.0.0.1', port))

        data, address = sock.recvfrom(MAX_BYTES)
        text = data.decode('ascii')
        text = text.split('#')

        if text[0] == 'G':
            print('O jogador {} ganhou! (Numero: {})'.format(text[1], text[2]))
            print('Pontuaçao:')
            for i in range(len(text) - 3):
                print('Jogador {}: {} pontos'.format(i, text[3 + i]))
            break
        elif text[0] == 'B':
            print('O jogador {} chutou a cima. (Chute: {})'.format(
                text[1], text[2]))
        else:
            print('O jogador {} chutou baixo . (Chute: {})'.format(
                text[1], text[2]))


if __name__ == '__main__':
    # Execução da função com a porta do nosso servidor
    client(1060)
