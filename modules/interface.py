from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.box import SQUARE
from rich.align import Align
from datetime import datetime
from collections import Counter

console = Console()

def format_elapsed_time(start_time):
    delta = datetime.now() - start_time
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    seconds = delta.seconds % 60
    return f"{hours:02d}h {minutes:02d}m {seconds:02d}s"

def display_header():
    # Logo centralizado
    logo = """
[white bold]                          NEURALIS[/white bold]
      [magenta]────────────────────────────────────────────────[/magenta]
[white]            Made by: [bold]Velbots[/bold] │ Version: 1.0.0[/white]
      [magenta]────────────────────────────────────────────────[/magenta]"""
    console.print(Align.center(logo))

def create_stats_table(bots, channels):
    runtime = format_elapsed_time(bots[0].start_time if bots else datetime.now())
    
    # Ler o número de proxies do arquivo
    try:
        with open('configs/proxy.txt', 'r', encoding='utf-8') as f:
            proxies_count = sum(1 for line in f if line.strip())
    except:
        proxies_count = 0
    
    stats = Table(
        box=SQUARE,
        border_style="magenta",
        width=60,
        padding=(0, 2),
        show_header=True,
        header_style="white"
    )
    
    stats.add_column("CHANNELS", justify="center", style="white", width=5)
    stats.add_column("THREADS", justify="center", style="white", width=5)
    stats.add_column("RUNTIME", justify="center", style="white", width=8)
    stats.add_column("PROXIES", justify="center", style="white", width=5)
    
    stats.add_row(
        str(len(channels)),
        str(len(bots)),
        runtime,
        str(proxies_count)  # Usando o número real de proxies
    )
    
    return stats

def create_status_summary_table(bots):
    table = Table(
        box=SQUARE,
        border_style="magenta",
        width=90,
        padding=(0, 2),
        show_lines=True,
        header_style="white"
    )
    
    table.add_column("STATUS", style="white", width=20, justify="center")
    table.add_column("BOTS", style="white", width=15, justify="center")
    table.add_column("ÚLTIMO CANAL", style="white", width=20, justify="center")
    table.add_column("MENSAGENS ENVIADAS", style="white", width=20, justify="center")
    
    # Contar bots por status
    status_count = Counter(bot.status for bot in bots)
    total_messages = sum(bot.messages_sent for bot in bots)
    last_channel = next((bot.current_channel for bot in bots if bot.current_channel), "Nenhum")
    
    # Pegar o status mais relevante para mostrar
    priority_order = ["Erro", "Mensagem Enviada", "Autenticado", "Conectando", "Aguardando", "Iniciando"]
    current_status = None
    for status in priority_order:
        if status in status_count:
            current_status = status
            break
    
    if current_status:
        status_translations = {
            "Iniciando": ("STARTING", "cyan"),
            "Conectando": ("CONNECTING", "blue"),
            "Autenticado": ("AUTHENTICATED", "blue"),
            "Mensagem Enviada": ("SENT", "green"),
            "Aguardando": ("WAITING", "yellow"),
            "Erro": ("ERROR", "red")
        }
        
        translated_status, color = status_translations.get(current_status, (current_status.upper(), "white"))
        status_symbol = "●" if current_status != "Erro" else "○"
        
        table.add_row(
            f"[{color}]{status_symbol} {translated_status}[/{color}]",
            str(len(bots)),  # Total de bots
            last_channel,
            str(total_messages)
        )
    
    return table

def update_interface(bots, tokens, channels):
    console.clear()
    display_header()
    
    stats_table = create_stats_table(bots, channels)
    status_table = create_status_summary_table(bots)  # Usando a nova função
    
    console.print(Align.center(stats_table))
    console.print(Align.center(status_table))
    console.print("")

def bot_logo():
    logo = """
[white bold]                          NEURALIS[/white bold]
      [magenta]────────────────────────────────────────────────[/magenta]
[white]            Made by: [bold]Velbots[/bold] │ Version: 1.0.0[/white]
      [magenta]────────────────────────────────────────────────[/magenta]"""
    console.print(Align.center(logo))