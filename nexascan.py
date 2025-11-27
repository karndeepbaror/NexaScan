#!/usr/bin/env python3

import os
import subprocess
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

console = Console()

# ----------------------------------------
# Banner (Tool Intro)
# ----------------------------------------
def banner():
    console.print(Panel.fit(
        "[bold green]NexaScan - Network Scanner Tool[/bold green]\n"
        "[cyan]Developer: Karndeep Baror[/cyan]\n"
        "[cyan]GitHub: github.com/karndeepbaror[/cyan]",
        title="[bold magenta]NEXA SCAN - Nmap Automater Script[/bold magenta]",
        border_style="bright_magenta"
    ))


# Small loading animation for smooth UI
def loading(txt="Processing"):
    for i in range(3):
        console.print(f"[yellow]{txt}{'.' * (i+1)}[/yellow]", end="\r")
        time.sleep(0.4)
    console.print(" " * 40, end="\r")


# ----------------------------------------
# Target input
# ----------------------------------------
def get_target():
    return Prompt.ask("[bold cyan]Enter Target (IP / Domain)[/bold cyan]")


# ----------------------------------------
# Scan Categories
# ----------------------------------------

# Basic scans — commonly used
BASIC = {
    "1": ("Normal Scan", "-sV"),
    "2": ("Ping Scan", "-sn"),
    "3": ("Detect OS", "-O"),
    "4": ("Aggressive Scan", "-A"),
    "5": ("Service Version", "-sV"),
    "6": ("Traceroute", "--traceroute"),
}

# Advanced / Stealth scans
ADVANCED = {
    "1": ("SYN Stealth Scan", "-sS"),
    "2": ("TCP Connect Scan", "-sT"),
    "3": ("FIN Scan", "-sF"),
    "4": ("NULL Scan", "-sN"),
    "5": ("XMAS Scan", "-sX"),
    "6": ("Idle Scan", "-sl"),
    "7": ("Fragment Scan", "-f"),
    "8": ("Decoy Scan", "-D RND:10"),
    "9": ("Spoofed Source", "-S 1.2.3.4"),
}

# Port-based / intense modes
PORTS = {
    "1": ("Top Ports", "--top-ports 100"),
    "2": ("Full Port Scan", "-p-"),
    "3": ("TCP Only", "-sT"),
    "4": ("UDP Only", "-sU"),
    "5": ("Fast Scan", "-F"),
    "6": ("Intense Scan", "-T4 -A -v"),
    "7": ("No DNS", "-n"),
    "8": ("IPv6 Scan", "-6"),
}

# NSE script categories
SCRIPTS = {
    "1": ("Default Scripts", "--script default"),
    "2": ("Safe Scripts", "--script safe"),
    "3": ("Vulnerability Scan", "--script vuln"),
    "4": ("Malware Check", "--script malware"),
    "5": ("Auth Scripts", "--script auth"),
    "6": ("Brute Force", "--script brute"),
    "7": ("HTTP Scripts", "--script http*"),
    "8": ("SSL/TLS Scripts", "--script ssl*"),
    "9": ("FTP Scripts", "--script ftp*"),
    "10": ("DNS Enumeration", "--script dns-*"),
    "11": ("SMB Enumeration", "--script smb*"),
    "12": ("Banner Grab", "--script banner"),
    "13": ("Complete Vulnerability + Default", "--script default,vuln"),
}


# ----------------------------------------
# Menu printer (reusable)
# ----------------------------------------
def print_menu(title, items):
    table = Table(title=title, border_style="magenta")
    table.add_column("ID", style="cyan", width=5)
    table.add_column("Scan Type", style="green")

    for key, (name, _) in items.items():
        table.add_row(key, name)

    console.print(table)
    choice = Prompt.ask("[bold yellow]Select ID[/bold yellow]", choices=items.keys())
    return items[choice]


# ----------------------------------------
# Execute scan
# ----------------------------------------
def run_scan(flags, target):
    console.print(Panel(
        f"[green]Running scan on [bold]{target}[/bold]...[/green]",
        border_style="green"
    ))
    loading("Scanning")

    try:
        result = subprocess.check_output(
            ["nmap"] + flags.split() + [target],
            stderr=subprocess.STDOUT,
            text=True
        )
        return result
    except Exception as e:
        return str(e)


# ----------------------------------------
# Main menu controller
# ----------------------------------------
def main():
    while True:
        os.system("clear")
        banner()

        console.print("""
[bold magenta]MAIN MENU[/bold magenta]

[cyan]1.[/cyan] BASIC SCANS  
[cyan]2.[/cyan] ADVANCED / STEALTH SCANS  
[cyan]3.[/cyan] PORT & INTENSE SCANS  
[cyan]4.[/cyan] NSE SCRIPT SCANS  
[cyan]5.[/cyan] Exit  
        """)

        choice = Prompt.ask(
            "[bold yellow]Select Category[/bold yellow]",
            choices=["1", "2", "3", "4", "5"]
        )

        if choice == "5":
            console.print("[green]Exiting...[/green]")
            break

        target = get_target()

        if choice == "1":
            scan_name, flags = print_menu("BASIC SCANS", BASIC)
        elif choice == "2":
            scan_name, flags = print_menu("ADVANCED / STEALTH SCANS", ADVANCED)
        elif choice == "3":
            scan_name, flags = print_menu("PORT & INTENSE", PORTS)
        else:
            scan_name, flags = print_menu("NSE SCRIPT SCANS", SCRIPTS)

        console.print(Panel(
            f"[bold cyan]Scan Selected:[/bold cyan] {scan_name}\n"
            f"[bold cyan]Target:[/bold cyan] {target}",
            border_style="cyan"
        ))

        output = run_scan(flags, target)

        console.print(Panel(
            f"[white]{output}[/white]",
            title="[bold green]SCAN RESULT[/bold green]",
            border_style="green"
        ))

        input("\n[bold yellow]Press Enter to return to menu...[/bold yellow]")


if __name__ == "__main__":
    main()
