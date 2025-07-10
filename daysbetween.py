import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, timedelta
import holidays

try:
    from tkcalendar import DateEntry
except ImportError:
    raise ImportError("Bitte installiere tkcalendar: pip install tkcalendar")

def get_german_states():
    return [
        'Baden-Württemberg', 'Bayern', 'Berlin', 'Brandenburg', 'Bremen',
        'Hamburg', 'Hessen', 'Mecklenburg-Vorpommern', 'Niedersachsen',
        'Nordrhein-Westfalen', 'Rheinland-Pfalz', 'Saarland', 'Sachsen',
        'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen'
    ]

def insert_current_date(event):
    today = date.today()
    event.widget.set_date(today)

def calculate_days():
    global last_holiday_list
    start = start_date_entry.get_date()
    end = end_date_entry.get_date()
    include_end = enddate_var.get()
    count_saturday = saturday_var.get()
    selected_state = state_combobox.get()

    if start > end or (start == end and not include_end):
        messagebox.showerror("Fehler", "Das Startdatum muss vor dem Enddatum liegen.")
        return

    if not selected_state or selected_state not in get_german_states():
        messagebox.showerror("Fehler", "Bitte ein gültiges Bundesland wählen.")
        return

    state_holidays = holidays.Germany(prov=selected_state)
    delta_days = (end - start).days + (1 if include_end else 0)
    workdays = 0
    feiertage_liste = []
    for i in range(delta_days):
        current = start + timedelta(days=i)
        weekday = current.weekday()
        is_workday = (weekday < 5) or (count_saturday and weekday == 5)
        if is_workday:
            if current in state_holidays:
                feiertage_liste.append(f"{current.strftime('%d.%m.%Y')}: {state_holidays.get(current)}")
            else:
                workdays += 1

    last_holiday_list = feiertage_liste

    result_text = (
        f"Zeitraum: {start.strftime('%d.%m.%Y')} bis {end.strftime('%d.%m.%Y')} "
        f"({'inklusive' if include_end else 'exklusive'} Enddatum)\n"
        f"Bundesland: {selected_state}\n"
        f"Gesamtzahl der Tage: {delta_days}\n"
        f"Arbeitstage{' (inkl. Samstag)' if count_saturday else ''}: {workdays}\n"
        f"Anzahl der Feiertage: {len(feiertage_liste)}"
    )
    result_label.config(state=tk.NORMAL)
    result_label.delete("1.0", tk.END)
    result_label.insert(tk.END, result_text)
    result_label.config(state=tk.DISABLED)

def show_holidays():
    if not last_holiday_list:
        messagebox.showinfo("Feiertage", "Keine Feiertage im gewählten Zeitraum.")
        return
    holidays_window = tk.Toplevel(root)
    holidays_window.title("Berücksichtigte Feiertage")
    holidays_window.geometry("400x400")
    frame = ttk.Frame(holidays_window, padding=10)
    frame.pack(fill=tk.BOTH, expand=True)
    scroll = tk.Scrollbar(frame)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    holidays_text = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scroll.set)
    holidays_text.pack(expand=True, fill=tk.BOTH)
    holidays_text.insert(tk.END, "\n".join(last_holiday_list))
    holidays_text.config(state=tk.DISABLED)
    scroll.config(command=holidays_text.yview)

def show_info():
    info_text = (
        "Tage-Rechner\n\n"
        "Dieses Programm berechnet die Anzahl der gesamten Tage und der Arbeitstage "
        "zwischen zwei Daten. Optionen:\n"
        "• Kalenderauswahl für Start- und Enddatum\n"
        "• Enddatum optional inklusive\n"
        "• Samstage als Arbeitstage wählbar\n"
        "• Feiertage werden angezeigt (nur über den Button)\n"
        "• Ergebnis kann kopiert werden\n"
        "• Doppelklick auf ein Datumsfeld trägt das heutige Datum ein\n\n"
        "Erstellt von Dieter Eckstein 2025"
    )
    messagebox.showinfo("Information", info_text)

def copy_result():
    root.clipboard_clear()
    root.clipboard_append(result_label.get("1.0", tk.END).strip())
    messagebox.showinfo("Kopiert", "Das Ergebnis wurde in die Zwischenablage kopiert.")

# --- GUI Erstellung ---
root = tk.Tk()
root.title("Tage-Rechner")
root.geometry("520x420")
root.minsize(520, 420)    # Mindestgröße, damit nichts verschwindet
root.resizable(False, True)

main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)

# Eingabebereich
input_frame = ttk.Frame(main_frame)
input_frame.pack(fill=tk.X, pady=(0, 10))

ttk.Label(input_frame, text="Startdatum:").grid(row=0, column=0, sticky=tk.W, pady=5)
start_date_entry = DateEntry(input_frame, date_pattern="dd.MM.yyyy")
start_date_entry.grid(row=0, column=1, sticky=tk.EW, padx=(10, 0))
start_date_entry.bind("<Double-Button-1>", insert_current_date)

ttk.Label(input_frame, text="Enddatum:").grid(row=1, column=0, sticky=tk.W, pady=5)
end_date_entry = DateEntry(input_frame, date_pattern="dd.MM.yyyy")
end_date_entry.grid(row=1, column=1, sticky=tk.EW, padx=(10, 0))
end_date_entry.bind("<Double-Button-1>", insert_current_date)

ttk.Label(input_frame, text="Bundesland:").grid(row=2, column=0, sticky=tk.W, pady=5)
state_combobox = ttk.Combobox(input_frame, values=get_german_states(), state="readonly")
state_combobox.grid(row=2, column=1, sticky=tk.EW, padx=(10, 0))
state_combobox.set("Saarland")

input_frame.columnconfigure(1, weight=1)

# Optionen
options_frame = ttk.LabelFrame(main_frame, text="Optionen", padding="10")
options_frame.pack(fill=tk.X, pady=(0, 10))

enddate_var = tk.BooleanVar(value=False)
saturday_var = tk.BooleanVar(value=False)
ttk.Checkbutton(options_frame, text="Enddatum inklusive", variable=enddate_var).pack(anchor="w", pady=2)
ttk.Checkbutton(options_frame, text="Samstage als Arbeitstage zählen", variable=saturday_var).pack(anchor="w", pady=2)

# Ausgabebereich (Textfeld mit 6 Zeilen)
result_frame = ttk.LabelFrame(main_frame, text="Ergebnis", padding="10")
result_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 10))

result_label = tk.Text(result_frame, height=2, font=("Helvetica", 10), wrap=tk.WORD)
result_label.pack(anchor="nw", fill=tk.BOTH, expand=True)
result_label.config(state=tk.DISABLED)

# Button-Bereich mit Unicode-Symbolen
button_frame = ttk.Frame(main_frame)
button_frame.pack(fill=tk.X, pady=(10, 0))

ttk.Button(button_frame, text="▶️ Ausführen", command=calculate_days).pack(side=tk.LEFT, expand=True, padx=5)
ttk.Button(button_frame, text="📅 Feiertage", command=show_holidays).pack(side=tk.LEFT, expand=True, padx=5)
ttk.Button(button_frame, text="📋 Kopieren", command=copy_result).pack(side=tk.LEFT, expand=True, padx=5)
ttk.Button(button_frame, text="ℹ️ Info", command=show_info).pack(side=tk.LEFT, expand=True, padx=5)
ttk.Button(button_frame, text="❌ Beenden", command=root.quit).pack(side=tk.LEFT, expand=True, padx=5)

last_holiday_list = []
root.mainloop()
