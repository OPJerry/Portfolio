__name__ = "GraUno.py"
__author__ = "Jeremiasz Talik"
__system__ = "Windows"
__status__ = "work in progress"
"""_requirements_
to be able to run the program correctly, type in terminal:
pip install mysql-connector-python
"""

from dataclasses import dataclass, field
import random
from random import shuffle
from time import sleep
import os
import re
import mysql.connector

@dataclass
class UnoCard:
    """_summary_
    UnoCard class is the basic element of the game
    """
    name: str
    color: str

    def __str__(self) -> str:
        card = f'<({self.name}) [{self.color}]>'
        return card
    
    def __lt__(self, other):
        """_summary_
        color comparison method. implemented to create a clearer view during gameplay
        """
        if self.color != other.color:
            return self.color < other.color
        return self.name < other.name

@dataclass
class UnoCardSpecial:
    """_summary_
    UnoCardSpecial class is one of elements of the game, which has an additional impact on the gameplay
    """
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
            """_summary_
            Method that adds two additional cards from the deck to the opponent
            """
            for _ in range(2):
                if len(fulldeck) > 0:
                    card = fulldeck[0]
                    przeciwnik.reka.eq.append(card)
                    fulldeck.remove(card)
   
@dataclass
class UnoCardWild:
    """_summary_
    UnoCardWild class is one of elements of the game, which has an additional impact on the gameplay
    - stronger then UnoCardSpecial
    This type of card have unique color, that matches all others colors

    After playing this card, the player will change color of this card to the one of 4 that he choose
    """
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
            valid_number = ("1","2","3","4")
            new_color = input("[1] Blue\n[2] Red\n[3] Green\n[4] Yellow\n Jaki ma być nowy kolor ? ")
            if new_color in valid_number:
                if new_color =="1": 
                    new_color="Blue"
                if new_color =="2": 
                    new_color="Red"
                if new_color =="3": 
                    new_color="Green"
                if new_color =="4": 
                    new_color="Yellow"
                barowa_lada.karty_na_stole[-1].color = new_color
            else:
                print("Nieprawidłowy wybór")
        if self.name == "+4":
            for _ in range(4):
                if len(fulldeck) > 0:
                    card = fulldeck[0]
                    przeciwnik.reka.eq.append(card)
                    fulldeck.remove(card)
                else:
                    print("Brak kart do pobrania z talii.")
                    break
            valid_number = ("1","2","3","4")
            new_color = input("[1] Blue\n[2] Red\n[3] Green\n[4] Yellow\n Jaki ma być nowy kolor ? ")
            if new_color in valid_number:
                if new_color =="1": 
                    new_color="Blue"
                if new_color =="2": 
                    new_color="Red"
                if new_color =="3": 
                    new_color="Green"
                if new_color =="4": 
                    new_color="Yellow"
                barowa_lada.karty_na_stole[-1].color = new_color
            else:
                print("Nieprawidłowy wybór")

@dataclass
class Hand:
    """_summary_
    structure for entities, gives the opportunity to have cards.
    In other words, it stores card information in a cache.
    """
    eq: list = field(default_factory=list)
    x = 0
    def numbered_cards(self) -> str:
        """_summary_
        numbers the cards in numerical order, making them easier to recall during the game.

        Returns:
            str: 1. 2. 3. etc...
        """
        cards_with_numbers = [f"{x + 1}. {card}" for x , card in enumerate(self.eq)]
        return "\n".join(cards_with_numbers)

    def __str__(self) -> str:
        return self.numbered_cards()

@dataclass
class Player:
    """_summary_
    The class used by players allows them to make moves
    """
    name: str
    reka: Hand = field(default_factory=Hand)

    def deal_initial_hand(self, type_of_deck, number_of_initial_cards=6):
            """_summary_
            Deals the initial hand of cards, defaults 6 cards
            """
            for _ in range(number_of_initial_cards):
                card = type_of_deck[0]
                self.reka.eq.append(card)
                type_of_deck.remove(card)
            self.reka.eq = sorted(self.reka.eq, key=lambda card: (card.color, card.name))

    def draw_card(self, podmiot):
            """_summary_
            allows a player to draw one card when he is not able to play any card in his hand
            """
            for _ in range(1):
                if len(fulldeck) > 0:
                    card = fulldeck[0]
                    print(f'Wylosowano {card}')
                    podmiot.reka.eq.append(card)
                    fulldeck.remove(card)
                else:
                    print("Brak kart do pobrania z talii.")
                    break

    def __str__(self) -> str:
        return "{name}"
    
    def play_card(self):
        """_summary_
        Allows a player to play a card he choose, when the card meets the play requirements.
        If card have any special properties, they will be activated.
        """
        try:
            while True:
                choice = input("Którą kartę chcesz zagrać? ")
                try:
                    int_choice = int(choice.strip())
                    break
                except ValueError:
                    print("@@@ Nieprawidłowy wybór. Wpisuj tylko liczby całkowite @@@")
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
    """_summary_
    The field on which the game takes place. Defaults should have one card.
    unlike other entities, it always displays the single card most recently added to the stack
    """
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
    """_summary_
    Basic "Rock, paper, scissors" game.
    A method designed to determine who starts the game

    Returns: int(2) if player is the winner or the game ended by draw. OR int(1) otherwise
    """
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
        print(f"Ty wybrałeś {wybor_gracza1} a ja {wybor_gracza2}")
        sleep(1)
        print('Ok, zaczynaj.')
        print("")
        return wynik
    elif wynik == 1:
        os.system('cls')
        print(f"Ty wybrałeś {wybor_gracza1} a ja {wybor_gracza2}")
        sleep(2)
        print("")
        print('HA! Wygrałem czyli zaczynam!')
        return wynik
    
def is_int(zmienna):
    """_summary_

    method that checks whether the value of a variable is an integer

    Returns: integer
    """
    wzór = r'^\d+$'
    spr = re.match(wzór, zmienna)
    if spr:
        return (int(spr.group()))
    else:
        return None

def ranking():
    print("")
    print("   TOP 5 SCORE")
    sql = "SELECT user_name, user_scoring FROM users ORDER BY user_scoring DESC LIMIT 5"
    cursor.execute(sql)
    results_of_cursor = cursor.fetchall()
    x = 1
    for row in results_of_cursor:
        print(f"{x}. {row}")
        x += 1

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

MySQL = mysql.connector.connect(
  host="sql8.freesqldatabase.com",
  user="sql8674916",
  password="D7CCT9FHFN",
  database="sql8674916")

cursor = MySQL.cursor()
print("")
print("Witaj w Jaskini Jerrego!")
print(f"(⁠☞⁠ ͡⁠°⁠ ͜⁠ʖ⁠ ͡⁠°⁠)⁠☞ ~Najlepsze trunki, magia w powietrzu i niezapomniane gry w UNO~\n")
print("[1] Nowa gra")
print("[2] Ranking zwycięzców")
while True:
    startodp = input("Wybierz opcje: ")
    if startodp == '1':
        os.system('cls')
        print("Witaj podróżniku!")
        sleep(1)
        print("Mam na imię Jerry i jestem tutaj barmanem.")
        sleep(1.5)
        print('zagrajmy w tutejszą odmianę "Uno"')
        sleep(1)
        print("Jak masz na imię: ")
        print("")
        gracz = Player(name=input("-> na imię mi: ").strip().capitalize())
        graczname = gracz.name
        print(f'Witaj {gracz.name}, pozwól że rozdam nam karty')
        sleep(2)
        print("")
        print(f'Zazwyczaj mamy tu więcej osób ale dziś gramy sami.')
        sleep(1.5)
        break
    if startodp == '2':
        ranking()
        print("")
        print("[1] Nowa gra")
        print("[2] Ranking zwycięzców")
    else:
        print("Nieprawidłowy wybór")


def new_game_AI(graczmove):
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
                    print(f"Jerry miał {len(przeciwnik.reka.eq)} kart.")
                    print()
                    print(f"Ale zagrał kartę: {card_to_play}")
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
                                    break                              
                        if card_to_play.name == "+2":
                            for _ in range(2):
                                if len(fulldeck) > 0:
                                    card = fulldeck[0]
                                    gracz.reka.eq.append(card)
                                    print(f"dobrałeś kartę {card}")
                                    fulldeck.remove(card)
                                else:
                                    print("Brak kart do pobrania z talii.")
                                    break
                            
                    przeciwnik.reka.eq.remove(card_to_play)
                    
                else:
                    print(f"Jerry miał {len(przeciwnik.reka.eq)} kart.")
                    print()
                    print("Ale dobrał kartę")
                    card = fulldeck[0]
                    przeciwnik.reka.eq.append(card)
                    fulldeck.remove(card)
                    
                graczmove += 1


            if len(gracz.reka.eq) == 0:
                print("koniec gry, wygrałeś")
                x = len(barowa_lada.karty_na_stole)
                y = len(przeciwnik.reka.eq)
                z = x + y + y
                user_name = graczname
                user_scoring = z
                sql = "INSERT INTO users (user_name, user_scoring) VALUES (%s, %s)"
                val = (user_name, user_scoring)

                cursor.execute(sql, val)
                MySQL.commit()
                print(f"dodano cie do rankingu z wynikiem: {user_scoring}.")
                break
            if len(przeciwnik.reka.eq) == 0:
                print("koniec gry, przegrałeś")
                break
    else:
        print("Mamy Remis !")
        print("udało się wyczerpać wszystkie karty na stosie, i nie można już rozstrzygnąć kto wygrał te partię.")

odp = 1
while odp == 1:
    fulldeck = deck_of_normal_cards + deck_of_special_cards + deck_of_Wild_cards
    shuffle(fulldeck)
    gracz = Player(name=graczname)
    przeciwnik = Player(name="Jerry")
    barowa_lada = Table()
    print("")
    print("[Jerry tasuje karty i rozdaje wam początkowe rozdanie]")
    gracz.deal_initial_hand(fulldeck)
    przeciwnik.deal_initial_hand(fulldeck)
    barowa_lada.deal_initial_Table()
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
        answer = input('-> Wpisz "Y" lub "N": ')
        if answer.lower() in {'y', 'n'}:
            break
    if answer.lower() == 'y':
        print("Zasady są proste:")
        print("W grze chodzi o to aby pozbyć się wszystkich kart z ręki zanim zrobi to przeciwnik")
        print("na stole zawsze jest jakaś karta z talii, w jednej turze możesz umieścić jedną kartę z twojej ręki")
        print("ale tylko pod warunkiem że karta ma taki sam kolor, lub numer jak karta która jest na szczycie stołu.")
        print('Niektóre karty zamiast zwykłego koloru mają kolor "Wild". Wild jest kolorem uniwersalnym i pasuej do każdego')
        print("Jeżeli nie możesz położyć na stół żadnej karty, musisz dobrać dodatkową kartę z talii - w ramach kary.")
        print("W talii z której będziemy dobierać karty znajduja się też karty specialne które wprowadzają pewne zmiany ale to już zrozumiesz w trakcie gry...")
        print("")
        print("W trakcie rozgrywki posługujemy się tylko liczbami całkowitymi, przypisanymi do odpowiedzi")
        print('Oraz tylko w niektrych przypadkach literami "Y" lub "N"')
        print('Zawsze udzielamy jednej odpowiedzi jednocześnie, potwierdzając ją klawiszem "enter"')
    elif answer.lower() == 'n':
        print("No to gramy!!!")
    
    print("")
    print('Pierwsze ustalmy kto będzie zaczynał, zagramy w "Papier, Kamien i Nożyce"')
    print("")
    sleep(2)
    print("Jeśli wygram, to zacznę.")
    graczmove = papierkamiennozyce()
    try:
        new_game_AI(graczmove)
    except IndexError:
        print("")
        print("Jerry: brakło kart do dobrania. Wygląda na to że mamy remis :)")
    print("Czy chcesz zagrać jeszcze raz ?")
    odp = input("wpisz [Y] lub [N]: ")
    odp = odp.capitalize().strip()
    if odp != "Y":
        break
        
print("do zobaczenia podróżniku :)!")