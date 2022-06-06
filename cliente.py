#!/usr/bin/env phython3

import socket
import time
import math
import statistics 

#variáveis para lidar com a representação do tempo
unidade = 1000000
retorno = 1000

# Endereço IP do servidor
HOST = '127.0.0.1'
# a porta que o servidor está
PORT =  30000

# criar um soket(familia de protocolo-IPv4, protocolo UDP)
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

#deve enviar 10 mensagens no formato:
total = 10
# 5 Bytes : Numero de identificação
# 1 Byte : 0 - Ping / 1 - Pong 
ping = '0'
# 4 Bytes : Timestamp (unidades de milisegundos)
#tempo máximo de espera 1 seg (fixo)
s.settimeout(1)
#lista com tupla (mensagem,tempo de chegada) para mensagens que exederem o tempo máximo
lista_atrasados = []
# 30 Bytes : Mensagem do pacote
mensagem = 'trabalho_de_redes_Juliana';  
#verificar se está no tamanho padrão (por segurança)
if len(mensagem) > 30 :
    print('mensagem fora do formato ping')

#Obs.: para as estatísticas de pacotes perdidos: considerar que todos 
#foram perdidos e decrementar o valor com a chegada de cada um no cliente
perdidos = total
#tempo em mili 
tempo_inicial = time.time()*1000
#lista de rtts
rtts = []

for i in range(total):
    #numero da mensagem em 5 Bytes
    numero = '{:05d}'.format(i+1)
    #medir o tempo (4 dígitos menos significativos)
    tempo_saida = ((math.trunc(time.time()*unidade))%10000)  

    # juntar as informações
    msg_final = str(numero) + ping + str(tempo_saida) + mensagem
    print('ENVIADA: ', msg_final)

    #enviar a mensagem através do socket criado
    s.sendto(msg_final.encode(),(HOST,PORT))

    try:
        while True:
            #receber o retorno do servidor
            msg_servidor,ender = s.recvfrom(40)
            tempo_chegada = ((math.trunc(time.time()*unidade))%10000)
            #se a mensagem for de uma rodada anterior, armazena  
            #para depois verificar o formato e colocar nas estatísticas
            msg_servidor = msg_servidor.decode()
            if int(msg_servidor[0:5]) < (i+1):
                perdidos-=1
                lista_atrasados.append((msg_servidor,tempo_chegada)) 
            elif int(msg_servidor[0:5]) == (i+1) :
                perdidos-=1
                break;               

    except:
        #esgotou o tempo de espera para receber a msg do servidor
        print('Exedeu o tempo de espera do pacote ', numero)

    else:        

        #testar formato da mensagem recebida (igual a enviada, porém com pong) - obs.: numero já testado
        if msg_servidor[5:6] == '1' and msg_servidor[6:10] == str(tempo_saida) and msg_servidor[10:] == mensagem: 

            #dentro do formato -> imprime a mensagem de ping
            rtts.append((tempo_chegada - tempo_saida)/retorno)
            print('40 bytes from ',HOST,': icmp_seq=',int(numero),'time=',(tempo_chegada-tempo_saida)/retorno)
            print('RECEBIDA: ',msg_servidor)

        else:
            #tem erro
            print('A mensagem recebida foi corrompida')

#apos os 10 pings estabelecer as estatísticas
tempo_final = time.time()*1000

#primeiro, verificar se as mensagens recebidas com atraso estão no padrão para entrar nas estatísticas
for msg, tempo in lista_atrasados:
    if int(msg[0:5])>0 and msg[5:6] == '1' and msg[6:10].isdigit() and msg[10:]==mensagem:
        #mensagem no padrão - contabiliza o tempo
        rtts.append((tempo-int(msg[6:10]))/retorno)
        print('40 bytes from ',HOST,': icmp_seq=',int(msg[0:5]),'time=',((tempo-int(msg[6:10]))/retorno))

#tempos convertidos para milissegundos
print(total,' pocotes transmitidos, ',
      total-perdidos,' recebidos, ',
      perdidos/total*100,'% pacotes perdidos,time ', 
      '{:.3f}'.format(tempo_final - tempo_inicial), 
      'ms rtt min/avg/max/mdev = ', '{:.3f}'.format(min(rtts)),'/',
      '{:.3f}'.format(sum(rtts)/len(rtts)),'/',
      '{:.3f}'.format(max(rtts)),'/','{:.3f}'.format(statistics.stdev(rtts)))

