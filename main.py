import socket
import random
import time
import threading
import logging
import os
import socks
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.box import SQUARE
from datetime import datetime

# Setup console
console = Console()

# Setup logging com formato mais organizado
def setup_logging():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Criar novo arquivo de log para cada execução
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f'logs/bot_{timestamp}.log'
    
    logging.basicConfig(
        filename=log_file,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )

def create_box_line(width, left, middle, right):
    return f"{left}{middle * (width-2)}{right}"

def display_header(tokens, channels):
    console.clear()
    
    # Título centralizado
    title_panel = Panel(
        "[white]TWITCH CHAT BOT MANAGER[/white]",
        border_style="red",
        width=80,
        padding=(0, 2)
    )
    console.print(title_panel, justify="center")
    
    # Info table
    info_table = Table(
        show_header=False,
        border_style="red",
        width=80,
        padding=0
    )
    
    info_table.add_column("Info", style="white", width=20)
    info_table.add_column("Valor", style="white", width=60)
    
    info_table.add_row("Bots Ativos", f"{len(tokens)}")
    info_table.add_row("Canais", f"{', '.join(channels)}")
    info_table.add_row("Status", "Sistema Online")
    info_table.add_row("Iniciado", datetime.now().strftime("%H:%M:%S"))
    
    console.print(info_table, justify="center")

def create_status_table():
    table = Table(
        title="Status dos Bots",
        border_style="red",
        header_style="white bold",
        width=80,
        padding=0,
        show_lines=True,
        show_edge=True,
        box=SQUARE
    )
    
    # Configurar colunas sem quebra de linha
    table.add_column("ID", style="white", width=4, no_wrap=True, justify="center")
    table.add_column("Status", style="white", width=10, no_wrap=True, justify="left")
    table.add_column("Proxy", style="white", width=20, no_wrap=True, justify="left")
    table.add_column("Mensagem", style="white", width=25, no_wrap=True, justify="left")
    table.add_column("Canal", style="white", width=15, no_wrap=True, justify="left")
    table.add_column("Delay", style="white", width=6, no_wrap=True, justify="center")
    
    return table

def format_status(status):
    status_styles = {
        "Iniciando": "[yellow]INIT[/yellow]",
        "Conectando": "[blue]CONN[/blue]",
        "Autenticado": "[green]AUTH[/green]",
        "Mensagem Enviada": "[green]SENT[/green]",
        "Aguardando": "[yellow]WAIT[/yellow]",
        "Erro": "[red]ERR[/red]"
    }
    return status_styles.get(status, status)

class TwitchBot:
    def __init__(self, token, channels, messages, proxy):
        self.token = token
        self.channels = channels
        self.messages = messages
        self.proxy = proxy
        self.server = "irc.chat.twitch.tv"
        self.port = 6667
        self.running = True
        self.status = "Iniciando"
        self.last_message = ""
        self.current_channel = ""
        self.delay_time = 0  # Tempo de espera atual
        self.next_message_time = 0  # Timestamp da próxima mensagem
        self.start_time = datetime.now()
        self.messages_sent = 0

    def update_status(self, status, message="", channel=""):
        self.status = status
        if message:
            self.last_message = message
            self.messages_sent += 1
            # Define próximo delay e timestamp
            self.delay_time = random.randint(30, 120)
            self.next_message_time = time.time() + self.delay_time
        if channel:
            self.current_channel = channel

    def get_remaining_delay(self):
        """Retorna o tempo restante até a próxima mensagem"""
        if self.next_message_time > time.time():
            return int(self.next_message_time - time.time())
        return 0

    def connect_and_send(self):
        while self.running:
            try:
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
                
                delay = random.randint(30, 120)
                self.update_status("Aguardando")
                time.sleep(delay)

            except Exception as e:
                self.update_status("Erro", str(e))
                logging.error(f"Bot {self.token[:8]} - Erro: {str(e)}")
                time.sleep(5)
                continue

def run_bot_manager():
    setup_logging()
    
    # Carregar configurações
    with open('configs/tokens.txt', 'r', encoding='utf-8') as f:
        tokens = [line.strip() for line in f if line.strip()]
    
    with open('configs/channels.txt', 'r', encoding='utf-8') as f:
        channels = [line.strip() for line in f if line.strip()]
    
    with open('configs/messages.txt', 'r', encoding='utf-8') as f:
        messages = [line.strip() for line in f if line.strip()]
        
    with open('configs/proxy.txt', 'r', encoding='utf-8') as f:
        proxies = [line.strip() for line in f if line.strip()]

    bots = []
    threads = []

    # Mostrar interface imediatamente
    display_header(tokens, channels)
    table = create_status_table()
    
    # Criar todos os bots primeiro
    for i, (token, proxy) in enumerate(zip(tokens, proxies), 1):
        bot = TwitchBot(token, channels, messages, proxy)
        bots.append(bot)
        table.add_row(
            f"{i}",
            format_status("Iniciando"),
            proxy.split(':')[0],
            "",
            "",
            "0s"
        )
    
    console.print(table, justify="center")

    # Iniciar threads em background
    for i, bot in enumerate(bots, 1):
        thread = threading.Thread(
            target=bot.connect_and_send,
            name=f"Bot-{i}",
            daemon=True
        )
        threads.append(thread)
        thread.start()
        time.sleep(1)  # Reduzido para 1 segundo

    # Interface em tempo real
    with Live(console=console, refresh_per_second=1) as live:
        while True:
            console.clear()
            display_header(tokens, channels)
            table = create_status_table()
            
            for i, bot in enumerate(bots, 1):
                message = bot.last_message
                if len(message) > 22:
                    message = message[:19] + "..."
                
                channel = bot.current_channel
                if len(channel) > 12:
                    channel = channel[:9] + "..."
                
                table.add_row(
                    f"{i}",
                    format_status(bot.status),
                    bot.proxy.split(':')[0],
                    message,
                    channel,
                    f"{bot.get_remaining_delay()}s"
                )
            
            console.print(table, justify="center")
            time.sleep(1)

if __name__ == '__main__':
    run_bot_manager()
