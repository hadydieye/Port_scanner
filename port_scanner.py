#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading
import argparse
import time
import sys
from colorama import Fore, Style, init

# Initialisation de colorama (Windows compatible)
init(autoreset=True)

# Port -> Service mapping de base
COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 3306: "MySQL", 3389: "RDP",
    8080: "HTTP-ALT", 5900: "VNC", 6379: "Redis"
}

# Résultats globaux
open_ports = []
lock = threading.Lock()

def get_service(port):
    return COMMON_PORTS.get(port, "UNKNOWN")

def scan_port(target, port, timeout, verbose):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target, port))
            with lock:
                if result == 0:
                    service = get_service(port)
                    print(f"{Fore.GREEN}[{port}] - OPEN - {service}")
                    open_ports.append((port, service))
                elif verbose:
                    print(f"{Fore.RED}[{port}] - CLOSED")
    except socket.gaierror:
        print(f"{Fore.RED}Impossible de résoudre l'hôte : {target}")
        sys.exit(1)
    except socket.error:
        print(f"{Fore.RED}Erreur de connexion à {target}")
        sys.exit(1)

def thread_worker(target, port_list, timeout, verbose):
    for port in port_list:
        scan_port(target, port, timeout, verbose)

def chunkify(lst, n):
    return [lst[i::n] for i in range(n)]

def main():
    parser = argparse.ArgumentParser(description="🛡️ Scanner de ports Python (multithreadé)")
    parser.add_argument("-t", "--target", required=True, help="Adresse IP ou nom d'hôte")
    parser.add_argument("-p", "--ports", default="1-1024", help="Plage de ports (ex: 1-1024)")
    parser.add_argument("-o", "--output", help="Fichier de sortie pour les ports ouverts")
    parser.add_argument("-v", "--verbose", action="store_true", help="Afficher les ports fermés")
    parser.add_argument("--timeout", type=float, default=1.0, help="Timeout (s) par port (défaut: 1.0)")
    parser.add_argument("--threads", type=int, default=100, help="Nombre de threads max (défaut: 100)")

    args = parser.parse_args()

    print(Fore.CYAN + "\n⚠️  Utilisation éthique uniquement. Ne scannez pas des hôtes sans autorisation.\n")

    try:
        target_ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print(f"{Fore.RED}Erreur : Nom d'hôte invalide.")
        sys.exit(1)

    # Parsing de la plage de ports
    try:
        if "-" in args.ports:
            start, end = map(int, args.ports.split("-"))
            port_range = list(range(start, end + 1))
        else:
            port_range = [int(p) for p in args.ports.split(",")]
    except ValueError:
        print(f"{Fore.RED}Erreur : Plage de ports invalide.")
        sys.exit(1)

    print(f"{Style.BRIGHT}🔍 Cible : {args.target} ({target_ip})")
    print(f"{Style.BRIGHT}🔢 Plage de ports : {args.ports}")
    print(f"{Style.BRIGHT}🚀 Threads : {args.threads}")
    print(f"{Style.BRIGHT}⏱️ Timeout : {args.timeout}s\n")

    start_time = time.time()

    # Préparation des threads
    chunks = chunkify(port_range, args.threads)
    threads = []

    for chunk in chunks:
        t = threading.Thread(target=thread_worker, args=(target_ip, chunk, args.timeout, args.verbose))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Résumé final
    duration = time.time() - start_time
    print(f"\n📊 {Style.BRIGHT}Scan terminé en {duration:.2f} secondes.")
    print(f"📂 Ports ouverts trouvés : {len(open_ports)}\n")

    for port, service in sorted(open_ports):
        print(f"{Fore.GREEN}[{port}] - OPEN - {service}")

    # Export
    if args.output:
        try:
            with open(args.output, "w") as f:
                f.write("Port\tEtat\tService\n")
                for port, service in sorted(open_ports):
                    f.write(f"{port}\tOPEN\t{service}\n")
            print(f"\n💾 Résultats enregistrés dans : {args.output}")
        except IOError:
            print(f"{Fore.RED}Erreur d'écriture dans le fichier {args.output}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Interruption utilisateur (Ctrl+C). Fin du scan.")
        sys.exit(0)
