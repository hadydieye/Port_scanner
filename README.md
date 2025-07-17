# 🔎 Port Scanner Python – CLI Multithreadé

Un scanner de ports en ligne de commande (CLI) rapide, coloré, et multithreadé, idéal pour apprendre la cybersécurité en Python.

---

## 🚀 Fonctionnalités

- Scanner n'importe quelle adresse IP ou nom d’hôte.
- Multithreading configurable (par défaut : 100 threads).
- Timeout personnalisable (par défaut : 1s).
- Mode verbeux pour afficher les ports fermés.
- Affichage en couleur (vert pour ouvert, rouge pour fermé).
- Export des résultats dans un fichier `.txt`.
- Respecte les bonnes pratiques (PEP 8), code bien structuré.

---

## ⚠️ Avertissement

Ce script est à but **éducatif uniquement**. N’utilisez **jamais** ce scanner sur un réseau ou système sans autorisation préalable.

---

## 📦 Installation

### ✅ Étapes recommandées pour tous les systèmes (avec environnement virtuel)

```bash
# Clone du projet
git clone https://github.com/hadydieye/Port_scanner.git
cd Port_scanner

# Création d'un environnement virtuel (recommandé sur Ubuntu/Debian)
python3 -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate

# Installation des dépendances dans l'environnement isolé
pip install -r requirements.txt
```

### ❗ Si vous voyez une erreur `externally-managed-environment`

Cela signifie que votre environnement système est protégé (ex. : Ubuntu avec Python 3.12+). La solution recommandée est d’utiliser un environnement virtuel comme ci-dessus.

Plus d'infos : [https://peps.python.org/pep-0668/](https://peps.python.org/pep-0668/)

---

## 🛠️ Utilisation

```bash
python port_scanner.py -t <hôte> -p <plage> [--timeout <secondes>] [--threads <n>] [-o <fichier>] [-v]
```

### Exemples :

```bash
python port_scanner.py -t 192.168.1.1 -p 1-1000
python port_scanner.py -t scanme.nmap.org -p 20-90 --threads 50 --timeout 0.5 -v
python port_scanner.py -t example.com -p 21,22,80,443 -o resultats.txt
```

---

## 🧪 Tests

- Testé sur Python 3.8+ (Linux, macOS, Windows)
- Fonctionne avec des cibles locales (`127.0.0.1`) ou distantes
- Gère les erreurs réseau et interruptions (Ctrl+C)

---

## 📂 Structure du projet

```
port_scanner/
├── port_scanner.py       # Script principal
├── requirements.txt      # Dépendance (colorama)
├── README.md             # Documentation
└── tests/                # (Optionnel) Dossier de tests
```

---

## 📈 Evolutions possibles

- Scan UDP
- Interface graphique (Tkinter / PyQt)
- Détection de version de service (bannières)
- Export JSON / HTML

---

## 👨‍💻 Auteur

Projet développé avec ❤️ par **Scriptseinsei**

Licence : MIT

