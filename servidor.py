#!/usr/bin/env phython3
import socket

#soket é um IP + porta
HOST = '127.0.0.1'
PORT = 30000

#criar um soket(familia de protocolo-IPv4, protocolo UDP)
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

s.bind((HOST,PORT))

#teste
print('Aguardando conexão de um cliente')

#trocar mensagens
while True:
	#tamanho maximo de dados para receber (40 bytes por msg)
	msg, ender = s.recvfrom(40)
	msg = msg.decode()
	print('RECEBIDO: ',msg)
	
	#testar formato da mensagem recebida (faixa de representação)
	if int(msg[0:5])>0 and int(msg[0:5])<11 and msg[5:6] == '0' and msg[6:10].isdigit(): 
		
		#mudar de ping para pong
		new_msg = msg[:5] + '1' + msg[6:]
		print('ENVIADO: ',new_msg)
					
		#enviar dados de volta ao cliente
		s.sendto(new_msg.encode(),ender)