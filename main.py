import json
import os
from datetime import datetime

DATA_FILE = "goleador_data.json"


# ------------------------------
# Funzioni di persistenza dati
# ------------------------------

def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "courses": [],
            "participants": [],
            "awards": []
        }

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # Se il file è corrotto o vuoto, riparti pulito
            return {
                "courses": [],
                "participants": [],
                "awards": []
            }


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# ------------------------------
# Funzioni di utilità
# ------------------------------

def get_participant_full_name(participant):
    return f"{participant['first_name'].strip()} {participant['last_name'].strip()}"


def find_participant(data, first_name, last_name, course_name=None):
    first_name = first_name.strip()
    last_name = last_name.strip()

    for p in data["participants"]:
        if (
            p["first_name"].strip().lower() == first_name.lower()
            and p["last_name"].strip().lower() == last_name.lower()
        ):
            if course_name:
                if p["course"].strip().lower() == course_name.strip().lower():
                    return p
            else:
                return p
    return None


# ------------------------------
# Gestione Corsi
# ------------------------------

def add_course(data):
    course_name = input("Inserisci il nome del nuovo corso: ").strip()
    if not course_name:
        print("Il nome del corso non può essere vuoto.")
        return

    # Evita duplicati (case-insensitive)
    if any(c.lower() == course_name.lower() for c in data["courses"]):
        print(f"Il corso '{course_name}' esiste già.")
        return

    data["courses"].append(course_name)
    save_data(data)
    print(f"Corso '{course_name}' creato con successo!")


def list_courses(data):
    if not data["courses"]:
        print("Nessun corso presente.")
        return

    print("\nCorsi attivi:")
    for idx, c in enumerate(data["courses"], start=1):
        print(f"{idx}. {c}")
    print()


# ------------------------------
# Gestione Partecipanti
# ------------------------------

def add_participant(data):
    if not data["courses"]:
        print("Non ci sono corsi disponibili. Crea prima un corso.")
        return

    first_name = input("Nome partecipante: ").strip()
    last_name = input("Cognome partecipante: ").strip()
    if not first_name or not last_name:
        print("Nome e cognome non possono essere vuoti.")
        return

    list_courses(data)
    course_name = input("Inserisci il nome del corso a cui iscrivere la partecipante: ").strip()

    # Verifica che il corso esista
    if not any(c.lower() == course_name.lower() for c in data["courses"]):
        print(f"Il corso '{course_name}' non esiste. Operazione annullata.")
        return

    # Evita di iscrivere due volte la stessa persona allo stesso corso
    existing = find_participant(data, first_name, last_name, course_name)
    if existing:
        print(f"La partecipante {first_name} {last_name} è già iscritta al corso '{course_name}'.")
        return

    participant = {
        "first_name": first_name,
        "last_name": last_name,
        "course": course_name
    }
    data["participants"].append(participant)
    save_data(data)
    print(f"Partecipante {first_name} {last_name} iscritta al corso '{course_name}' con successo!")


def list_participants(data):
    if not data["participants"]:
        print("Nessuna partecipante iscritta.")
        return

    print("\nPartecipanti:")
    for idx, p in enumerate(data["participants"], start=1):
        full_name = get_participant_full_name(p)
        print(f"{idx}. {full_name} - Corso: {p['course']}")
    print()


# ------------------------------
# Assegnazione Goleador
# ------------------------------

def assign_goleador(data):
    if not data["participants"]:
        print("Non ci sono partecipanti registrate. Aggiungi una partecipante prima.")
        return

    first_name = input("Nome della partecipante: ").strip()
    last_name = input("Cognome della partecipante: ").strip()

    participant = find_participant(data, first_name, last_name)
    if not participant:
        print("Partecipante non trovata. Verifica nome e cognome.")
        return

    # Richiedi quante Goleador
    try:
        goleador_won = int(input("Quante Goleador ha vinto? "))
        if goleador_won <= 0:
            print("Il numero di Goleador deve essere positivo.")
            return
    except ValueError:
        print("Inserisci un numero valido.")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    award = {
        "participant_full_name": get_participant_full_name(participant),
        "course": participant["course"],
        "goleador": goleador_won,
        "timestamp": timestamp
    }

    data["awards"].append(award)
    save_data(data)
    print(
        f"Assegnate {goleador_won} Goleador a {award['participant_full_name']} "
        f"nel corso '{award['course']}' in data {timestamp}."
    )


# ------------------------------
# Analytics & Statistiche
# ------------------------------

def total_goleador_per_course(data):
    if not data["awards"]:
        print("Non ci sono ancora assegnazioni di Goleador.")
        return

    totals = {}
    for award in data["awards"]:
        course = award["course"]
        totals[course] = totals.get(course, 0) + award["goleador"]

    print("\nTotale Goleador per corso:")
    for course, total in totals.items():
        print(f"- {course}: {total} Goleador")
    print()


def top_scorer(data):
    if not data["awards"]:
        print("Non ci sono ancora assegnazioni di Goleador.")
        return

    scores = {}
    for award in data["awards"]:
        name = award["participant_full_name"]
        scores[name] = scores.get(name, 0) + award["goleador"]

    # Trova la top scorer
    top_name = max(scores, key=scores.get)
    top_score = scores[top_name]

    print("\nTop Scorer della Goleador Academy:")
    print(f"- {top_name} con {top_score} Goleador totali!")
    print()


# ------------------------------
# (Opzionale) Stub per AI commento motivazionale
# ------------------------------

def motivational_comment_stub(data):
    """
    Questa funzione è solo uno stub: qui potresti integrare Gemini
    o un'altra AI per generare un commento motivazionale.
    Per ora restituisce solo un messaggio statico.
    """
    total_awards = sum(a["goleador"] for a in data["awards"])
    participants_count = len(data["participants"])

    if participants_count == 0:
        print("Nessuna partecipante registrata, ma è il momento perfetto per iniziare a costruire la squadra!")
        return

    avg = total_awards / participants_count if participants_count > 0 else 0

    if avg == 0:
        msg = (
            "La classe è appena partita: nessuna Goleador assegnata (ancora!). "
            "Ogni grande goleador inizia dal primo tiro a porta."
        )
    elif avg < 5:
        msg = (
            "La classe sta scaldando i motori: le Goleador iniziano ad arrivare. "
            "Continuate così, la prossima ondata di premi è vicina!"
        )
    else:
        msg = (
            "La classe è in piena forma: le Goleador fioccano come gol in finale! "
            "Continuate a mantenere questo ritmo leggendario."
        )

    print("\nCommento motivazionale:")
    print(msg)
    print()


# ------------------------------
# Menu principale
# ------------------------------

def print_menu():
    print("===== Goleador Academy Tracker =====")
    print("1. Aggiungi nuovo corso")
    print("2. Iscrivi una partecipante a un corso")
    print("3. Assegna Goleador a una partecipante")
    print("4. Mostra tutti i corsi")
    print("5. Mostra tutte le partecipanti")
    print("6. Totale Goleador per corso")
    print("7. Top Scorer")
    print("8. Commento motivazionale (stub AI)")
    print("0. Esci")


def main():
    data = load_data()

    while True:
        print_menu()
        choice = input("Seleziona un'opzione: ").strip()

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
        elif choice == "8":
            motivational_comment_stub(data)
        elif choice == "0":
            print("Uscita dal Goleador Academy Tracker. A presto!")
            break
        else:
            print("Scelta non valida, riprova.")

        input("\nPremi INVIO per continuare...")


if __name__ == "__main__":
    main()