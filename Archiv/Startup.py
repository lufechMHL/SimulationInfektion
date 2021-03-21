msg = "Hello World"
print(msg)

msg.capitalize()
print(msg)

class BauplanKatzenKlasse():
    """ Klasse für das Erstellen von Katzen """

    def __init__(self, rufname, farbe, alter):
        self.rufname = rufname
        self.farbe   = farbe
        self.alter   = alter

    def Ausgabe(self):
        return self.rufname

Wii = BauplanKatzenKlasse("Wii", "braun", 2)

print(Wii.Ausgabe())
