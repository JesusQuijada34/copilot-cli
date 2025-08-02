#!/usr/bin/env python
import os
import json
import subprocess
import time
import sys

# 🎨 ANSI Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

CONFIG_FILE = "zorin_setup.json"

QUESTIONS = [
    "¿Tienes instalado GitHub CLI (gh)?",
    "¿Has iniciado sesión con 'gh auth login'?",
    "¿Instalaste la extensión Copilot CLI con 'gh extension install github/gh-copilot'?",
    "¿Puedes ejecutar 'gh copilot suggest' sin errores?",
    "¿Copilot CLI responde con sugerencias útiles?",
    "¿Has probado 'gh copilot explain'?",
    "¿El comando 'gh copilot' aparece en la ayuda de 'gh'?",
    "¿Copilot CLI está en tu PATH?",
    "¿Has actualizado gh y Copilot recientemente?",
    "¿Confirmas que Copilot CLI está funcionando correctamente?"
]

# 🧪 Check if a command exists
def is_installed(command):
    return subprocess.call(f"type {command}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

# 🧪 Check if Copilot CLI is functional
def copilot_is_ready():
    try:
        result = subprocess.run(["gh", "copilot", "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except Exception:
        return False

# 💬 Ask questions and save answers
def ask_questions():
    answers = {}
    print(f"{CYAN}🧠 Verificación interactiva de Copilot CLI en Zorin OS{RESET}\n")
    for q in QUESTIONS:
        while True:
            ans = input(f"{YELLOW}{q} (y/n): {RESET}").strip().lower()
            if ans in ["y", "n"]:
                answers[q] = "sí" if ans == "y" else "no"
                break
            else:
                print(f"{RED}❌ Respuesta inválida. Escribe 'y' para sí o 'n' para no.{RESET}")
    with open(CONFIG_FILE, "w") as f:
        json.dump(answers, f, indent=4)
    return answers

# 📖 Load previous answers
def load_answers():
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

# 🛠️ Attempt to repair installation
def repair_installation():
    print(f"{MAGENTA}🔧 Reparando instalación de Copilot CLI...{RESET}")
    if not is_installed("gh"):
        print(f"{YELLOW}📦 Instalando GitHub CLI...{RESET}")
        os.system("sudo apt update && sudo apt install -y gh")
    print(f"{YELLOW}🔐 Ejecuta 'gh auth login' si no lo has hecho.{RESET}")
    print(f"{YELLOW}📦 Instalando extensión Copilot CLI...{RESET}")
    os.system("gh extension install github/gh-copilot")

# ✅ Update JSON to reflect successful installation
def mark_installed():
    answers = load_answers() or {}
    for q in QUESTIONS:
        answers[q] = "sí"
    with open(CONFIG_FILE, "w") as f:
        json.dump(answers, f, indent=4)

# 🚀 Mostrar ejemplos si Copilot está instalado
def show_examples():
    print(f"\n{GREEN}✅ Copilot CLI detectado. Aquí tienes algunos ejemplos:{RESET}")
    print(f"{CYAN}$ gh copilot suggest 'crear un script bash para hacer backup'{RESET}")
    print(f"{CYAN}$ gh copilot explain 'sudo apt update && sudo apt upgrade'{RESET}")
    print(f"{CYAN}$ gh copilot suggest 'listar procesos que consumen más CPU'{RESET}")
    print(f"\n{MAGENTA}✨ Usa estos comandos directamente en tu terminal Zorin para experimentar con Copilot CLI.{RESET}")

# 🧩 Lógica principal
def main():
    answers = load_answers()
    if answers and answers.get(QUESTIONS[-1]) == "sí" and copilot_is_ready():
        show_examples()
    else:
        print(f"{YELLOW}🔍 Verificando estado de Copilot CLI...{RESET}")
        if not copilot_is_ready():
            repair_installation()
            if copilot_is_ready():
                print(f"{GREEN}✅ Reparación exitosa. Copilot CLI está listo.{RESET}")
                mark_installed()
                show_examples()
            else:
                print(f"{RED}❌ No se pudo verificar la instalación de Copilot CLI.{RESET}")
                ask_questions()
        else:
            mark_installed()
            show_examples()

if __name__ == "__main__":
    main()

