import os, sys
import re
import csv

# vollständiger Pfad zum Script. card-database.csv muss im selben Verzeichnis liegen.
real_path = os.path.dirname(os.path.realpath(__file__))

mode = "attack" # gibt an, welcher Wert zurückgeliefert werden soll (1. Kommandoparameter)
argument = ""   # soll den Parameterteil nach dem Kommando enthalten

# unify_name
# Funktion wandelt mit Leerzeichen getrennten Text in Kurznamen ohne Leer-, Sonderzeichen und Zahlen um
def unify_name(cardname):
    # in Kleinbuchstaben umwandeln:
    unified = str(cardname).lower()
    # alle Zeichen entfernen, die nicht "a" bis "z", oder "ß" sind u
    unified = re.sub(r'[^a-zß]', '', unified)
    return unified

# Kommandozeilenparameter verarbeiten. Der an Position 0 (der erste) ist der Name des Scripts und wird entfernt.
# An Position 1 (zweite Stelle) befindet sich der Modus, der z.B. "attack" (Angriffswert) oder
# "name" (Kartenname) sein kann. 
# Alle folgenden werden in shortcut-Format ohne Leer-,Sonderzeichen und Zahlen
# umgewandelt
if (len(sys.argv) > 2):
    # Modus für Rückgabewert:
    mode = sys.argv[1].strip()
    # alle Befehlsargumente aneinanderreihen und in Kleinbuchstaben umwandeln:
    argument = ''.join(sys.argv[2:])
    # alle Zeichen entfernen, die nicht "a" bis "z", oder "ß" sind:
    argument = unify_name(argument)
else:
    print("Error: arguments missing")

# Datenbank laden
cards = {}
# names soll alternative Kurznamen basierend auf dem Langnamen enthalten, z.B.
# soll statt "rotauge" auch "rotaugendrache" funktionieren ("rotaugen drache" funktioniert genauso)
names = {}
with open(os.path.join(real_path, 'card-database.csv'), mode='r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    # alle Zeilen der CSV-Datei durchlaufen
    for row in reader:
        if (len(row) >= 3):
            shortcut = unify_name(row[0])
            cardname = row[1].strip()
            attackpower = row[2].strip()
            # sicherstellen, dass attackpower wirklich eine Ganzzahl ist, ansonsten auf 0 setzens:
            attackpower = int(attackpower) if attackpower.isdigit() else 0
        cards[shortcut] = {"name": cardname, "attack": attackpower}
        alt_shortcut = unify_name(cardname)
        names[alt_shortcut] = shortcut

result = "not_found" # Standardrückgabewert
if (argument in names):
    argument = names[argument]  # in wirklichen Shortcut umwandeln

if (argument in cards):
    formatstr = "{attack}"  # Angriffswert
    if (mode == "name"):    # Kartenname
        formatstr = "{name}"
    if (mode == "attack_name"): # Angriffswert und Kartenname, durch Komma getrennt
        formatstr = "{attack},{name}"
    # weitere Modi können hier ergänzt werden.
    
    result = formatstr.format(**cards[argument])
    
print(result)