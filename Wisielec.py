import random
from dataclasses import dataclass

@dataclass
class Letter:
    character: str
    is_hidden: bool = True

    def __str__(self) -> str:
        if self.is_hidden:
            return "_"
        else:
            return self.character

class Word:
    def __init__(self, slowodozgadniecia: str) -> None:
        self.letters = []
        for letter in slowodozgadniecia:
            self.letters.append(Letter(letter))

    def __str__(self) -> str:
        word = [str(letter) for letter in self.letters]
        return "".join(word)
    
    def __contains__(self, proba_letter: str) -> bool:
        return proba_letter in [letter.character for letter in self.letters]
    
    def __iter__(self):
        return iter(self.letters)
    
    def wszystkieodkryte(self) -> bool:
        return not any([letter.is_hidden for letter in self.letters])
wynik = 0
listofwords = ["koala", "jeleń", "foka", "kameleon", "kogut", "tygrys", "gepard", "słoń", "delfin", "kangur",
"mrówkojad", "pingwin", "żyrafa", "zebra", "panda", "lis", "kruk", "hipopotam", "goryl", "wiewiórka",
"żółw", "sowa", "gepard", "sęp", "karp", "bóbr", "dąb", "koń", "lis", "krab", "szczur",
"puma", "łoś", "wąż", "borsuk", "krowa", "tygrys", "gepard", "koń", "lama", "fretka", "lama",
"kozioł", "wilk", "kaczka", "gepard", "kruk", "lisek", "kangur", "surykatka", "sokół", "struś",
"zebra", "salamandra", "papuga", "pająk", "koza", "lama", "żaba", "struś", "gepard", "kuna",
"zając", "słoń", "żubr", "zyrafa", "bizon", "ryś", "koziorożec", "kaczka", "flaming", "panda",
"kameleon", "jeż", "mrówka", "kot", "tygrys", "krowa", "kozioł", "świnka morska", "gepard", "gazela",
"pawian", "słoń", "jednorożec", "wydra", "gepard", "zyrafa", "orka", "sokół", "leniwiec", "kuna"
]

class Wygrałeś(Exception):
    pass


class Game:
    def __init__(self, zycia: int, word: Word, nazwa_gracza: str) -> None:
        self.zycia = zycia
        self.word = word
        self.nazwa_gracza = nazwa_gracza

    def start(self):
        print("")
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(f'@@@ Witaj {self.nazwa_gracza} zagrajmy! @@@')
        print("Kategoria: Zwierzęta")
        print("")
        listofanserws = []
        while self.zycia > 0:
            print("")
            print(f'masz {self.zycia} szans.')
            print(self.word)


            if self.word.wszystkieodkryte():
                raise Wygrałeś
            print(f'próbowałeś już {listofanserws}')
            proba = input('Podaj Literę: ')
            probalower = proba.lower()
            
            
            if probalower in self.word:
                for letter in self.word:
                    if probalower == letter.character:
                        letter.is_hidden = False
            else:
                print("nie udany strzał")
                listofanserws.append(probalower)
                print(f'próbowałeś już {listofanserws}')
                self.zycia -= 1
                if self.zycia == 0:
                    print("Tym razem się nie udało i przegrałeś...")
                    print(f"Słowo którego szukałeś to {zadanie}")
                    print(f'twój wynik to {wynik}')


gracz = input("Podaj swoje imie: ").capitalize().strip()
play_again = ''

while play_again == '':
    try:
        zadanie = random.choice(listofwords)
        game = Game(zycia=10, word=Word(zadanie), nazwa_gracza=gracz)
        game.start()
    except Wygrałeś:
        print("Wygrałeś grę !")
        wynik += 1
        print(f'twój wynik to {wynik}')
   
    play_again = input('Naciśnij enter by zagrać jeszcze raz ')