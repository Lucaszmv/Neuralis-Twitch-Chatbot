from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.box import SQUARE
from rich.align import Align
from datetime import datetime

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

def create_status_table(bots):
    table = Table(
        box=SQUARE,
        border_style="magenta",
        width=90,
        padding=(0, 2),
        show_lines=True,
        header_style="white"
    )
    
    table.add_column("BOT", style="white", width=5, justify="center")
    table.add_column("STATUS", style="white", width=20, justify="center")
    table.add_column("CHANNEL", style="white", width=14, justify="center")
    table.add_column("USER IP", style="white", width=20, justify="center")
    table.add_column("UPTIME", style="white", width=15, justify="center")
    
    for i, bot in enumerate(bots, 1):
        # Definir cores para cada status
        status_colors = {
            "STARTING": "cyan",
            "CONNECTING": "blue",
            "AUTHENTICATED": "blue",
            "SENT": "green",
            "WAITING": "yellow",
            "ERROR": "red"
        }
        
        status_translations = {
            "Iniciando": "STARTING",
            "Conectando": "CONNECTING",
            "Autenticado": "AUTHENTICATED",
            "Mensagem Enviada": "SENT",
            "Aguardando": "WAITING",
            "Erro": "ERROR"
        }
        
        current_status = status_translations.get(bot.status, bot.status.upper())
        status_color = status_colors.get(current_status, "white")
        status_symbol = "●" if bot.status != "Erro" else "○"
        
        table.add_row(
            f"{i:02d}",
            f"[{status_color}]{status_symbol} {current_status}[/{status_color}]",
            bot.current_channel or "Waiting...",
            bot.proxy.split(':')[0] or "Waiting IP...",
            format_elapsed_time(bot.start_time)
        )
    
    return table

def update_interface(bots, tokens, channels):
    console.clear()
    display_header()
    
    stats_table = create_stats_table(bots, channels)
    status_table = create_status_table(bots)
    
    console.print(Align.center(stats_table))
    console.print(Align.center(status_table))
    console.print("")  # Mantendo apenas uma linha em branco no final 