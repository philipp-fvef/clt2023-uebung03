from nltk.grammar import Nonterminal, CFG
from collections import deque


'''Hinweis:
Eine Schema-basierte Implementierung der Parser benötigt im Kern 2 Dinge:
- eine Repräsentation der Items
- eine Implementierung der möglichen Operationen

Items werden dann zur Chart und zur Agenda hinzugefügt. Die Chart sammelt alle
möglichen Items, die Agenda gibt vor, in welcher Reihenfolge die Items
abgearbeitet werden. Weder die Chart noch die Agenda soll Items doppelt
behandeln.

Die Chart ist als Python-Menge von Items implementiert. An jeder Position i in
der Chart befindet sich eine Menge (=ein Set) von Items.
Damit man ein Objekt o als Element in ein Set m eintragen kann (mit m.add(o)),
muss dieses Objekt eine Methode namens __hash__ haben.
Andernfalls bekommt man einen TypeError: TypeError: unhashable type: 'list'
--> Die primitiven Datentypen wie String und Integer haben diese Methode
    implementiert, wie Sie in der Python-Shell mit der dir()-Funktion und
    einem beliebigen Wert ausprobieren können (z.B. dir(5)).

Die Items des Earley-Parsers sind als Klasse implementiert.
Ein Earley-Item sieht so aus (s. Folie 21): [i, A → α • β, k], die einzelnen
Elemente finden Sie in der __init__-Methode der EarleyItem-Klasse. Die Klasse
implementiert auch eine __hash__-Methode, so dass die EarleyItem-Objekte in
Sets hinzugefügt werden können.

Alternativ könnte man ein Item als Tupel implementieren. Tupel sind
unveränderliche Listen. Tupel haben eine __hash__-Methode und können deshalb
als Elemente von Sets verwendet werden. Viele Listenoperationen kann man auch
auf Tupel anwenden, z.B. Konkatenation (+) und Slice-Operationen.

Die drei möglichen Operationen des Earley-Parsers, predict, scan und complete,
werden von der parse()-Methode aufgerufen.
'''


class EarleyItem:
    def __init__(self, production, dot_in_production, start, dot):
        self.production = production
        self.dot_in_production = dot_in_production
        self.start = start
        self.dot = dot

    # das Symbol nach dem Punkt
    def next_symbol(self):
        if self.dot_in_production < len(self.production.rhs()):
            return self.production.rhs()[self.dot_in_production]
        else:
            return None

    def __repr__(self):
        """Mit dieser Methode weiß Python, wie es eine Liste mit Item-Objekten
        ausgeben soll."""
        return self.__dotted_rule()

    def __dotted_rule(self):
        """Gibt eine String-Repraesentation des Items zurück"""
        item = "[{0}, {1} ->".format(self.start, self.production.lhs())
        for i in range(len(self.production.rhs())):
            if i == self.dot_in_production:
                item = "{0} *".format(item)
            item = "{0} {1}".format(item, self.production.rhs()[i])
        if self.dot_in_production == len(self.production.rhs()):
            item = "{0} *".format(item)
        return "{0}, {1}]".format(item, self.dot)

    # __eq__ und __hash__ sind wichtig, damit EarlyItem-Objekte korrekt
    # in Sets eingetragen werden
    def __eq__(self, other):
        return (self.production == other.production
                and self.dot_in_production == other.dot_in_production
                and self.start == other.start
                )

    def __hash__(self):
        return hash((self.production, self.dot_in_production, self.start))


class EarleyParser:

    def __init__(self):
        self.items = []           # items[i] = S_{i+1} aus der Vorlesung.
        self.agenda = deque()     # die Agenda (eine Queue von Items)

    # Traegt ein Item in die Chart und die Agenda ein, falls es noch nicht
    # schon vorher in der Chart war
    def enqueue(self, item):
        index = item.dot
        if item not in self.items[index]:
            print("   enqueue: ", item)
            self.items[index].add(item)
            self.agenda.append(item)

    # Parst den angegebenen Satz mit der Grammatik
    def parse(self, grammar, words):
        # Chart wird auf lauter leere Item-Mengen initialisiert
        for i in range(len(words)+1):
            self.items.append(set())

        # Start-Items in dieser Implementierung: alle Produktionen, in denen
        # das Startsymbol auf der linken Seite steht
        for prod in grammar.productions(lhs=grammar.start()):
            self.enqueue(EarleyItem(prod, 0, 0, 0))

        # so lange die Agenda nicht leer ist:
        while len(self.agenda) > 0:
            # Items von der Agenda nehmen
            item = self.agenda.popleft()
            index = item.dot
            print("\npop:", item)

            # unterscheide je nach Item, welche Regel angewendet werden soll
            if item.dot_in_production < len(item.production.rhs()):
                next = item.next_symbol()
                if isinstance(next, Nonterminal):
                    # predict
                    print("Predict!")
                    for prod in grammar.productions(lhs=next):
                        self.enqueue(EarleyItem(prod, 0, index, index))
                else:
                    # scan
                    print("Scan!")
                    if index < len(words) and words[index] == next:
                        self.enqueue(EarleyItem(item.production,
                                                item.dot_in_production+1,
                                                item.start,
                                                index+1
                                                ))
            else:
                # complete
                print("Complete!")
                for old_item in self.items[item.start]:
                    if old_item.next_symbol() == item.production.lhs():
                        # TODO - besser indizieren
                        self.enqueue(EarleyItem(old_item.production,
                                                old_item.dot_in_production+1,
                                                old_item.start,
                                                index
                                                ))

    def print_chart(self):
        for i in range(len(self.items)):
            print(i, self.items[i])


if __name__ == "__main__":
    grammar = CFG.fromstring("""
    S -> NP VP
    PP -> P NP
    NP -> Det N | Det N | 'I'
    VP -> V NP | VP PP
    Det -> 'an' | 'my'
    N -> 'elephant' | 'pajamas'
    V -> 'shot'
    P -> 'in'
    """)

    parser = EarleyParser()
    parse = parser.parse(grammar,
                         ["I", "shot", "an", "elephant", "in", "my", "pajamas"]
                         )
    print(parse)
    parser.print_chart()
