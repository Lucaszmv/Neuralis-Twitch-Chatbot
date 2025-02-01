import socket
import random
import time
import logging
import socks
from datetime import datetime

class TwitchBot:
    def __init__(self, token, channels, messages, proxy, semaphore):
        self.token = token
        self.channels = channels
        self.messages = messages
        self.proxy = proxy
        self.semaphore = semaphore
        self.server = "irc.chat.twitch.tv"
        self.port = 6667
        self.running = True
        self.status = "Iniciando"
        self.last_message = ""
        self.current_channel = ""
        self.delay_time = 0
        self.next_message_time = 0
        self.start_time = datetime.now()
        self.messages_sent = 0

    def update_status(self, status, message="", channel=""):
        self.status = status
        if message:
            self.last_message = message
            self.messages_sent += 1
            self.delay_time = random.randint(400, 500)
            self.next_message_time = time.time() + self.delay_time
        if channel:
            self.current_channel = channel

    def get_remaining_delay(self):
        if self.next_message_time > time.time():
            return int(self.next_message_time - time.time())
        return 0

    def connect_and_send(self):
        while self.running:
            try:
                # Adquirir semáforo antes de enviar mensagens
                with self.semaphore:
                    # Configurar proxy
                    proxy_parts = self.proxy.split(':')
                    proxy_host = proxy_parts[0]
                    proxy_port = int(proxy_parts[1])
                    proxy_user = proxy_parts[2]
                    proxy_pass = proxy_parts[3]

                    self.update_status("Conectando")

                    # Criar socket com proxy
                    irc = socks.socksocket()
                    irc.set_proxy(
                        proxy_type=socks.SOCKS5,
                        addr=proxy_host,
                        port=proxy_port,
                        username=proxy_user,
                        password=proxy_pass
                    )
                    
                    irc.connect((self.server, self.port))
                    
                    # Autenticar
                    irc.send(f"PASS oauth:{self.token}\n".encode("utf-8"))
                    irc.send(f"NICK bot\n".encode("utf-8"))
                    
                    response = irc.recv(2048).decode("utf-8")
                    self.update_status("Autenticado")
                    
                    # Entrar no canal e enviar mensagem
                    for channel in self.channels:
                        irc.send(f"JOIN #{channel}\n".encode("utf-8"))
                        time.sleep(1)
                        
                        message = random.choice(self.messages)
                        irc.send(f"PRIVMSG #{channel} :{message}\n".encode("utf-8"))
                        
                        self.update_status("Mensagem Enviada", message, channel)
                        logging.info(f"Bot {self.token[:8]} enviou via {proxy_host} em #{channel}: {message}")
                    
                    irc.close()
                    
                    # Aguardar entre 20-40 segundos antes de liberar o semáforo para o próximo token
                    delay_between_tokens = random.randint(20, 40)
                    self.update_status(f"Aguardando Próximo Token ({delay_between_tokens}s)")
                    time.sleep(delay_between_tokens)

                # Delay fora do semáforo para o próprio bot
                delay = random.randint(400, 500)
                self.update_status("Aguardando")
                time.sleep(delay)

            except Exception as e:
                self.update_status("Erro", str(e))
                logging.error(f"Bot {self.token[:8]} - Erro: {str(e)}")
                time.sleep(5)
                continue 