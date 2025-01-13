import time
import threading
from rich.live import Live
from modules.bot import TwitchBot
from modules.interface import console, update_interface
from modules.logger import setup_logging

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

    # Criar todos os bots primeiro
    for i, (token, proxy) in enumerate(zip(tokens, proxies), 1):
        bot = TwitchBot(token, channels, messages, proxy)
        bots.append(bot)

    # Iniciar interface imediatamente
    with Live(console=console, refresh_per_second=1) as live:
        # Iniciar threads em background
        for i, bot in enumerate(bots, 1):
            thread = threading.Thread(
                target=bot.connect_and_send,
                name=f"Bot-{i}",
                daemon=True
            )
            threads.append(thread)
            thread.start()

        # Loop da interface
        while True:
            update_interface(bots, tokens, channels)
            time.sleep(1)

if __name__ == '__main__':
    run_bot_manager()
