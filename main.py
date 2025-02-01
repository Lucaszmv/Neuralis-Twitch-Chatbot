import time
import threading
from rich.live import Live
import questionary
from questionary import Style as QuestionaryStyle
import os
from modules.bot import TwitchBot
from modules.interface import console, update_interface, bot_logo
from modules.logger import setup_logging

# Estilo personalizado para o questionary
custom_style = QuestionaryStyle([
    ('qmark', 'fg:#ff00ff'),  # Magenta para o [BOT]
    ('question', 'fg:#ffffff nobold'),  # Branco para o texto
    ('answer', 'fg:#ffffff nobold'),
    ('pointer', 'fg:#ff00ff nobold'),  # Magenta
    ('highlighted', 'fg:#ff00ff nobold'),
    ('selected', 'fg:#ff00ff nobold'),
    ('text', 'fg:#ffffff nobold'),
    ('instruction', 'fg:#ffffff nobold')
])

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def select_channels():
    with open('configs/channels.txt', 'r', encoding='utf-8') as f:
        available_channels = [line.strip() for line in f if line.strip()]
    
    if not available_channels:
        console.print(f"[magenta][BOT][/magenta] Nenhum canal disponível em configs/channels.txt")
        return []
    
    console.print(f"\n[magenta][BOT][/magenta] Canais disponíveis:\n")
    for idx, channel in enumerate(available_channels, 1):
        console.print(f"[magenta][{idx}][/magenta] {channel}")
    
    while True:
        selection = questionary.text(
            "\n[BOT] Digite os números dos canais que deseja usar (ex: 1,3,5) ou 'all' para usar todos: ",
            style=custom_style,
            qmark=""
        ).ask()
        
        if selection.lower() == 'all':
            return available_channels
        
        try:
            selected_indices = [int(idx.strip()) - 1 for idx in selection.split(',')]
            
            if any(idx < 0 or idx >= len(available_channels) for idx in selected_indices):
                console.print(f"[magenta][BOT][/magenta] Número inválido! Use números entre 1 e {len(available_channels)}")
                continue
                
            return [available_channels[idx] for idx in selected_indices]
            
        except ValueError:
            console.print(f"[magenta][BOT][/magenta] Formato inválido! Use números separados por vírgula (ex: 1,3,5)")
            continue

def run_bot_manager():
    setup_logging()
    clear_screen()
    bot_logo()
    
    # Seleção de canais
    selected_channels = select_channels()
    if not selected_channels:
        console.print("[magenta][BOT][/magenta] Nenhum canal selecionado. Encerrando...")
        return
    
    # Carregar outras configurações
    with open('configs/tokens.txt', 'r', encoding='utf-8') as f:
        tokens = [line.strip() for line in f if line.strip()]
    
    with open('configs/messages.txt', 'r', encoding='utf-8') as f:
        messages = [line.strip() for line in f if line.strip()]
        
    with open('configs/proxy.txt', 'r', encoding='utf-8') as f:
        proxies = [line.strip() for line in f if line.strip()]

    bots = []
    threads = []

    # Criar bots
    for i, (token, proxy) in enumerate(zip(tokens, proxies), 1):
        bot = TwitchBot(token, selected_channels, messages, proxy)
        bots.append(bot)

    clear_screen()
    # Iniciar interface
    with Live(console=console, refresh_per_second=1) as live:
        for i, bot in enumerate(bots, 1):
            thread = threading.Thread(
                target=bot.connect_and_send,
                name=f"Bot-{i}",
                daemon=True
            )
            threads.append(thread)
            thread.start()

        while True:
            update_interface(bots, tokens, selected_channels)
            time.sleep(1)

if __name__ == '__main__':
    run_bot_manager()
