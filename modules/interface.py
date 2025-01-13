from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.box import SQUARE
from datetime import datetime

console = Console()

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

def update_interface(bots, tokens, channels):
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