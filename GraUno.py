from dataclasses import dataclass, field
import random
from random import shuffle
from time import sleep
import os
import re

@dataclass
class UnoCard:
    name: str
    color: str

    def __str__(self) -> str:
        card = f'<({self.name}) [{self.color}]>'
        return card
    
    def __lt__(self, other):
        if self.color != other.color:
            return self.color < other.color
        return self.name < other.name

@dataclass
class UnoCardSpecial:
    name: str
    color: str
    card_function: str

    def __str__(self) -> str:
        card = f'<({self.name}) [{self.color}]> {self.card_function}'
        return card
    
    def __lt__(self, other):
        if self.color != other.color:
            return self.color < other.color
        return self.name < other.name
    
    def power(self):
        if self.name == "Pułapka":
            pass
        if self.name == "+2":
            for _ in range(2):
                if len(fulldeck) > 0:
                    card = fulldeck[0]
                    przeciwnik.reka.eq.append(card)
                    fulldeck.remove(card)
   
@dataclass
class UnoCardWild:
    name: str
    card_function: str
    color: str 

    def __str__(self) -> str:
        card = f'<({self.name}) [{self.color}]> {self.card_function}'
        return card 
    
    def __lt__(self, other):
        if self.color != other.color:
            return self.color < other.color
        return self.name < other.name
    
    def power(self):
        if self.name == "ChangeColor":
            new_color = input("Jaki ma być nowy kolor ? ")
            barowa_lada.karty_na_stole[-1].color = new_color
        if self.name == "+4":
            for _ in range(4):
                if len(fulldeck) > 0:
                    card = fulldeck[0]
                    przeciwnik.reka.eq.append(card)
                    fulldeck.remove(card)
                else:
                    print("Brak kart do pobrania z talii.")
            new_color = input("Jaki ma być nowy kolor ? ")
            barowa_lada.karty_na_stole[-1].color = new_color
@dataclass
class Hand:
    eq: list = field(default_factory=list)
    x = 0
    def numbered_cards(self) -> str:
        cards_with_numbers = [f"{x + 1}. {card}" for x , card in enumerate(self.eq)]
        return "\n".join(cards_with_numbers)

    def __str__(self) -> str:
        return self.numbered_cards()

@dataclass
class Player:
    name: str
    reka: Hand = field(default_factory=Hand)

    def deal_initial_hand(self, type_of_deck, number_of_initial_cards=6):
            for _ in range(number_of_initial_cards):
                card = type_of_deck[0]
                self.reka.eq.append(card)
                type_of_deck.remove(card)
            self.reka.eq = sorted(self.reka.eq, key=lambda card: (card.color, card.name))

    def draw_card(self, podmiot):
            for _ in range(1):
                if len(fulldeck) > 0:
                    card = fulldeck[0]
                    print(f'Wylosowano {card}')
                    podmiot.reka.eq.append(card)
                    fulldeck.remove(card)
                else:
                    print("Brak kart do pobrania z talii.")

    def __str__(self) -> str:
        return "{name}"
    
    def play_card(self):
        try:
            choice = input("Którą kartę chcesz zagrać? ")
            int_choice = int(choice)
            int_choice -= 1
            card = self.reka.eq[int_choice]

            last_card = barowa_lada.karty_na_stole[-1]
            if card.color == last_card.color or card.name == last_card.name or card.color == ".Wild":
                
                barowa_lada.karty_na_stole.append(card)
                
                if isinstance(card, (UnoCardSpecial, UnoCardWild)):
                    card.power()
                # Usuń kartę z ręki gracza
                self.reka.eq.remove(card)
                
                print(f"Gracz {self.name} zagrał kartę: {card}")
            else:
                print("Nie możesz zagrać tej karty!")
        except IndexError:
            print("Nie masz aż tylu kart")
            return

@dataclass
class Table:
    karty_na_stole: Hand = field(default_factory=list)

    def __str__ (self) -> str:
        return f"Ilość kart na stole: {len(self.karty_na_stole)} \n Karta na szczycie: {self.karty_na_stole[-1]}"
    
    def deal_initial_Table(self, number_of_initial_cards=1):
            for _ in range(number_of_initial_cards):
                card = random.choice(deck_of_normal_cards)
                self.karty_na_stole.append(card)
                deck_of_normal_cards.remove(card)

    def display_last_card(self) -> str:
        card = self.karty_na_stole[-1]
        print(f' Karta na szczycie: <({card.name}) [{card.color}]>')

def papierkamiennozyce():
    opcje = [1, 2, 3]

    def pobierz_wybor(gracz):
        while True:
            print("wybierz jedną z opcji: \n[1] Kamień \n[2] Papier \n[3] Nożyce")
            wybor_gracza = input(f'podaj swoj wybór: ')
            if int(wybor_gracza) in opcje:
                return int(wybor_gracza)

    def sprawdz_wynik(wybor_gracza1, wybor_gracza2):
        if wybor_gracza1 == wybor_gracza2:
            print('Remis, ty zaczynaj ')
            print("")
            return 2

        elif (wybor_gracza1 == 1 and wybor_gracza2 == 3) or \
             (wybor_gracza1 == 2 and wybor_gracza2 == 1) or \
             (wybor_gracza1 == 3 and wybor_gracza2 == 2):
            return 2

        else:
            return 1

    wybor_gracza1 = pobierz_wybor('Gracz1')
    wybor_gracza2 = random.choice(opcje)
    wynik = sprawdz_wynik(wybor_gracza1, wybor_gracza2)

    if wybor_gracza2 ==1: 
        wybor_gracza2="Kamień"
    if wybor_gracza2 ==2: 
        wybor_gracza2="Papier"
    if wybor_gracza2 ==3: 
        wybor_gracza2="Nożyce"
    if wybor_gracza1 ==1: 
        wybor_gracza1="Kamień"
    if wybor_gracza1 ==2: 
        wybor_gracza1="Papier"
    if wybor_gracza1 ==3: 
        wybor_gracza1="Nożyce"

    if wynik == 2:
        os.system('cls')
        print(f"Ja wybrałem {wybor_gracza2} a ty {wybor_gracza1}")
        sleep(1)
        print('Wygrałeś, zaczynasz.')
        print("")
        return wynik
    elif wynik == 1:
        os.system('cls')
        print(f"Ja wybrałem {wybor_gracza2} a ty {wybor_gracza1}")
        sleep(2)
        print("")
        print('HA! wygrałem czyli zaczynam!')
        return wynik
    
def new_game_multiplayer():
   list_of_players = []
   how_many_players = int(input("Ilu będzie graczy ?: "))
   for x in range(how_many_players):
       y = Player(input(f"podaj nazwę gracza {x+1}: "))
       list_of_players.append(y)
       if x >= len(list_of_players):
           return list_of_players
   x = [player.name for player in list_of_players]
   print(f'Witamy graczy {", ".join(x)} przy stoliku')

def is_int(zmienna):
    wzór = r'^\d+$'
    spr = re.match(wzór, zmienna)
    if spr:
        return (int(spr.group()))
    else:
        return None
    
deck = [str(i) for i in range(10)]
colors = ['Blue', 'Red', 'Green', 'Yellow']
deck_of_normal_cards = []
deck_of_special_cards = []
deck_of_Wild_cards = []

# Tutaj tworzę zwykłe karty
for x in range(2):
    for color in colors:
        for number in deck:
            card = UnoCard(name=str(number), color=color)
            deck_of_normal_cards.append(card)

# Tutaj tworzę karty specialne
specialdeck = list(range(2))
card_function = ["Pułapka", "+2"]

for number in specialdeck:
    for color in colors:
        specialcard = UnoCardSpecial(name=card_function[0], card_function="Karta która nic nie robi ale za to utrudnia", color=color)
        specialcard2 = UnoCardSpecial(name=card_function[1], card_function="zmusza następnego gracza do dobrania dwóch kart", color=color)
        deck_of_special_cards.append(specialcard)
        deck_of_special_cards.append(specialcard2)

# Tutaj tworzę dzikie karty
for x in range(4):
    wild1 = UnoCardWild(name= "ChangeColor", card_function= "zmienia kolor na stosie", color= ".Wild")
    wild2 = UnoCardWild(name= "+4", card_function= "Zmusza przeciwnika do dobrania 4 kart i zmienia kolor stosu", color=".Wild")
    deck_of_Wild_cards.append(wild1)
    deck_of_Wild_cards.append(wild2)

fulldeck = deck_of_Wild_cards + deck_of_special_cards + deck_of_normal_cards
shuffle(fulldeck)

print("Witaj podróżniku!")
sleep(1)
print("Mam na imię Jerry i jestem tutaj barmanem.")
sleep(1.5)
print('zagrajmy w tutejszą odmianę "Uno"')
sleep(1)
print("Jak masz na imię: ")
print("")
gracz = Player(name=input("-> na imię mi: ").strip().capitalize())
przeciwnik = Player(name="Jerry")
sleep(0.5)
print(f'Witaj {gracz.name}, pozwól że rozdam nam karty')
sleep(2)
print(f'Zazwyczaj mamy tu więcej osób ale dziś gramy sami.')
barowa_lada = Table()
gracz.deal_initial_hand(fulldeck)
przeciwnik.deal_initial_hand(fulldeck)
barowa_lada.deal_initial_Table()
sleep(3)
print("")
print("[Jerry tasuje karty i rozdaje wam początkowe rozdanie]")
print("")
sleep(4)
print("oto twoje karty, przeglądnij je ale mi nie pokazuj.")
print("")
sleep(2)
print(gracz.reka)
sleep(2)
print("")
print("Wyjaśnić ci zasady?")
while True:
    answer = input('-> Wpisz "T" lub "N": ')
    if answer.lower() in {'t', 'n'}:
        break
print("")   
if answer.lower() == 't':
    print("Zasady są proste:")
    print("W grze chodzi o to aby pozbyć się wszystkich kart z ręki zanim zrobi to przeciwnik")
    print("na stole zawsze jest jakaś karta z talii, w jednej turze możesz umieścić jedną kartę z twojej ręki")
    print("ale tylko pod warunkiem że karta ma taki sam kolor, lub numer jak karta która jest na szczycie stołu.")
    print('Niektóre karty zamiast zwykłego koloru mają kolor "Wild". Wild jest kolorem uniwersalnym i pasuej do każdego')
    print("Jeżeli nie możesz położyć na stół żadnej karty, musisz dobrać dodatkową kartę z talii - w ramach kary.")
    print("W talii z której będziemy dobierać karty znajduja się też karty specialne które wprowadzają pewne zmiany ale to już zrozumiesz w trakcie gry...")
elif answer.lower() == 'n':
    print("No to gramy!!!")
print("")
print('Pierwsze ustalmy kto będzie zaczynał, zagramy w "Papier, Kamien i Nożyce"')
print("")
sleep(2)
print("Jeśli wygram, to ja zacznę")
graczmove = papierkamiennozyce()

if len(fulldeck) > 0:
    while len(gracz.reka.eq) > 0 or len(przeciwnik.reka.eq) > 0:   
        if graczmove % 2 == 0:
            print("")
            print("ręka gracza:")
            print(gracz.reka)
            print("")
            print("")
            barowa_lada.display_last_card()
            print(f" twój przeciwnik ma {len(przeciwnik.reka.eq)} kart w ręce.")
            print("")
            print("co byś chciał zrobić ?")
            while True:
                move = input("[1] Zagrać kartę \n[2] Dobrać kartę\n Wybieram: ")
                imove = is_int(move)
                is_int(move)
                break
            if imove == 1:    
                gracz.play_card()
                graczmove += 1
                os.system('cls')
            if imove == 2:
                os.system('cls')
                gracz.draw_card(gracz)
                graczmove += 1            
        else:
            card_to_play = None
            last_card = barowa_lada.karty_na_stole[-1]
            for card in przeciwnik.reka.eq:
                if card.color == last_card.color or card.name == last_card.name or card.color == ".Wild":
                    card_to_play = card
                    break
            
            if card_to_play:
                barowa_lada.karty_na_stole.append(card_to_play)
                
                if isinstance(card_to_play, (UnoCardSpecial, UnoCardWild)):
                    if card_to_play.name == "ChangeColor":
                        new_color = random.choice(colors)
                        barowa_lada.karty_na_stole[-1].color = new_color
                    if card_to_play.name == "+4":
                        for _ in range(4):
                            if len(fulldeck) > 0:
                                card = fulldeck[0]
                                gracz.reka.eq.append(card)
                                print(f"dobrałeś kartę {card}")
                                fulldeck.remove(card)
                                new_color = random.choice(colors)
                                barowa_lada.karty_na_stole[-1].color = new_color
                            else:
                                print("Brak kart do pobrania z talii.")
                    if card_to_play.name == "+2":
                        for _ in range(2):
                            if len(fulldeck) > 0:
                                card = fulldeck[0]
                                gracz.reka.eq.append(card)
                                print(f"dobrałeś kartę {card}")
                                fulldeck.remove(card)
                            else:
                                print("Brak kart do pobrania z talii.")
                        
                przeciwnik.reka.eq.remove(card_to_play)
                
                print(f"Jerry zagrał kartę: {card_to_play}")
            else:
                card = fulldeck[0]
                przeciwnik.reka.eq.append(card)
                fulldeck.remove(card)
                print("Jerry dobrał kartę")

            graczmove += 1


        if len(gracz.reka.eq) == 0:
            print("koniec gry, wygrałeś")
            break
        if len(przeciwnik.reka.eq) == 0:
            print("koniec gry, przegrałeś")
            break
else:
    print("Mamy Remis !")
    print("udało się wyczerpać wszystkie karty na stosie, i nie można już rozstrzygnąć kto wygrał te partię.")