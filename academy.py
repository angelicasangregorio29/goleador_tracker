import json
import os
from datetime import datetime

DATA_FILE = "goleador_data.json"


# ------------------------------
# Persistenza dati
# ------------------------------

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"courses": [], "participants": [], "awards": []}

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"courses": [], "participants": [], "awards": []}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# ------------------------------
# Utility
# ------------------------------

def get_full_name(first, last):
    return f"{first.strip()} {last.strip()}"


def find_participant(data, first_name, last_name, course_name=None):
    for p in data["participants"]:
        if (
            p["first_name"].lower() == first_name.lower()
            and p["last_name"].lower() == last_name.lower()
        ):
            if course_name:
                if p["course"].lower() == course_name.lower():
                    return p
            else:
                return p
    return None


# ------------------------------
# Funzioni dedicate al salvataggio
# ------------------------------

def save_course(data, course_name):
    """Aggiunge un corso se non esiste già."""
    if any(c.lower() == course_name.lower() for c in data["courses"]):
        print(f"⚠️ Il corso '{course_name}' esiste già.")
        return False

    data["courses"].append(course_name)
    save_data(data)
    print(f"✅ Corso '{course_name}' salvato con successo!")
    return True


def save_participant(data, first_name, last_name, course_name):
    """Aggiunge una partecipante se non esiste già nello stesso corso."""
    if not any(c.lower() == course_name.lower() for c in data["courses"]):
        print(f"⚠️ Il corso '{course_name}' non esiste.")
        return False

    if find_participant(data, first_name, last_name, course_name):
        print(f"⚠️ {first_name} {last_name} è già iscritta al corso '{course_name}'.")
        return False

    participant = {
        "first_name": first_name,
        "last_name": last_name,
        "course": course_name
    }

    data["participants"].append(participant)
    save_data(data)
    print(f"🎉 Partecipante {first_name} {last_name} iscritta a '{course_name}'!")
    return True


# ------------------------------
# Gestione Corsi
# ------------------------------

def add_course(data):
    name = input("Nome del nuovo corso: ").strip()
    if not name:
        print("⚠️ Nome non valido.")
        return

    save_course(data, name)


def list_courses(data):
    if not data["courses"]:
        print("Nessun corso presente.")
        return

    print("\nCorsi disponibili:")
    for c in data["courses"]:
        print(f"- {c}")
    print()


# ------------------------------
# Gestione Partecipanti
# ------------------------------

def add_participant(data):
    if not data["courses"]:
        print("⚠️ Nessun corso disponibile. Creane uno prima.")
        return

    first = input("Nome: ").strip()
    last = input("Cognome: ").strip()

    list_courses(data)
    course = input("Corso di iscrizione: ").strip()

    save_participant(data, first, last, course)


def list_participants(data):
    if not data["participants"]:
        print("Nessuna partecipante registrata.")
        return

    print("\nPartecipanti:")
    for p in data["participants"]:
        print(f"- {p['first_name']} {p['last_name']} ({p['course']})")
    print()


# ------------------------------
# Assegnazione Goleador
# ------------------------------

def assign_goleador(data):
    first = input("Nome partecipante: ").strip()
    last = input("Cognome partecipante: ").strip()

    p = find_participant(data, first, last)
    if not p:
        print("⚠️ Partecipante non trovata.")
        return

    try:
        qty = int(input("Quante Goleador assegnare? "))
        if qty <= 0:
            raise ValueError
    except ValueError:
        print("⚠️ Numero non valido.")
        return

    award = {
        "participant_full_name": get_full_name(first, last),
        "course": p["course"],
        "goleador": qty,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    data["awards"].append(award)
    save_data(data)

    print(f"🍬 Assegnate {qty} Goleador a {award['participant_full_name']}!")


# ------------------------------
# Statistiche
# ------------------------------

def total_goleador_per_course(data):
    totals = {}

    for a in data["awards"]:
        totals[a["course"]] = totals.get(a["course"], 0) + a["goleador"]

    if not totals:
        print("Nessuna assegnazione registrata.")
        return

    print("\nTotale Goleador per corso:")
    for course, total in totals.items():
        print(f"- {course}: {total}")
    print()


def top_scorer(data):
    scores = {}

    for a in data["awards"]:
        scores[a["participant_full_name"]] = scores.get(a["participant_full_name"], 0) + a["goleador"]

    if not scores:
        print("Nessuna assegnazione registrata.")
        return

    top = max(scores, key=scores.get)
    print(f"\n🏆 Top Scorer: {top} con {scores[top]} Goleador!\n")


# ------------------------------
# Menu
# ------------------------------

def print_menu():
    print("\n===== GOLEADOR ACADEMY =====")
    print("1. Aggiungi corso")
    print("2. Iscrivi partecipante")
    print("3. Assegna Goleador")
    print("4. Lista corsi")
    print("5. Lista partecipanti")
    print("6. Totale Goleador per corso")
    print("7. Top Scorer")
    print("0. Esci")


def run_app():
    data = load_data()

    while True:
        print_menu()
        choice = input("Scelta: ").strip()

        if choice == "1":
            add_course(data)
        elif choice == "2":
            add_participant(data)
        elif choice == "3":
            assign_goleador(data)
        elif choice == "4":
            list_courses(data)
        elif choice == "5":
            list_participants(data)
        elif choice == "6":
            total_goleador_per_course(data)
        elif choice == "7":
            top_scorer(data)
        elif choice == "0":
            print("Arrivederci dalla Goleador Academy!")
            break
        else:
            print("Scelta non valida.")

        input("\nPremi INVIO per continuare...")