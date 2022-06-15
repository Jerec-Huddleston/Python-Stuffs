'''
Black Jack
'''
from random import shuffle

class Deck():
    '''
    Deck of Cards
    '''
    Suits = ["Hearts", "Clubs", "Diamonds", "Spades"]
    Values = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]

    def __init__(self):
        self.shuffled_deck = []

    def shuffle(self):
        '''
        fills shuffled_deck list with cards then random.shuffle()
        '''
        for suit in self.Suits:
            for value in self.Values:
                self.shuffled_deck.append((value, suit))
        shuffle(self.shuffled_deck)

    def draw(self):
        '''
        OUTPUT = shuffled_deck.pop()
        if shuffled_deck is empty call self.shuffle() then output
        '''
        while True:
            try:
                return self.shuffled_deck.pop()
            except:
                self.shuffle()


class Player():
    '''
    Black Jack player
    '''

    def __init__(self, name = "Player"):
        self.cards = [[], []]
        self.at_table = True
        self.money = 1000
        self.bet = []
        self.name = name
        self.has_special = False
        self.has_stood = [False, False]
        self.has_bust = [False, False]

    def hand_total(self, hand = 0):
        '''
        INPUT = List of tuples ("Card Value", "Card Suit")
        OUTPUT = Numerical value of all cards
        aces are counted as 11 unless over 21
        '''
        total = 0
        count_of_aces = 0
        for value, _ in self.cards[hand]:
            if value in ["Jack", "Queen", "King"]:
                total += 10
            elif value in ["2", "3", "4", "5", "6", "7", "8", "9", "10"]:
                total += int(value)
            else: count_of_aces += 1
        #don't add aces untill after all other cards
        for ace in range(count_of_aces):
            if total + 11 > 21:
                total += 1
            else:
                total += 11
        return total

    def betting(self):
        while True:
            #make sure bet is valid
            try:
                player_bet = int(input(f"\nYou currently have ${self.money}\n{self.name} place your bet! "))
            except:
                print("That's not a valid bet. Try again!")
                continue
            if player_bet <= 0:
                print("Nice try, but you can't bet zero or negative numbers!")
                continue
            elif player_bet > self.money:
                print("You don't have enough money to make that bet")
                continue
            else:
                self.bet.append(player_bet)
                break

    def hit(self, deck, hand = 0, dealer = False):
        card = deck.draw()
        self.cards[hand].append(card)
        if dealer == False:
            print(f"{self.name} drew: {card[0]} of {card[1]}")
        return deck

    def stand(self, hand = 0):
        self.has_stood[hand] = True
        print(f"{self.name} stood")

    def split(self, deck):
        self.cards[1].append(self.cards[0].pop())
        self.has_special = True
        self.bet.append(self.bet[0])
        print(f"{self.name} split")
        for i in range(len(self.cards)):
            print(f"Hit for hand {i + 1}")
            deck = self.hit(deck, i)
            print(f"Total: {self.hand_total(i)}")
        return deck

    def double_down(self, deck):
        print(f"{self.name} doubled down!")
        deck = self.hit(deck)
        self.stand()
        self.bet[0] *= 2
        self.has_special = True
        return deck

    def can_special_moves(self):
        split_check = False
        double_down_check = False
        tens = ["10", "Jack", "Queen", "King"]
        if self.money >= self.bet[0] * 2:
            if self.cards[0][0][0] == self.cards[0][1][0]:
                split_check = True
            elif self.cards[0][0][0] in tens and self.cards[0][1][0] in tens:
                split_check = True
            double_down_check = True
        return split_check, double_down_check

    def print_cards(self, hand = 0):
        output = ""
        for i, _ in enumerate(self.cards[hand]):
            output += self.cards[hand][i][0] + " of " + self.cards[hand][i][1]
            if i + 1 < len(self.cards[hand]):
                output+= ", "
        return output

    def bust_check(self, hand = 0):
        total = self.hand_total(hand)
        if total > 21:
            self.has_bust[hand] = True
            print(f"{self.name} bust with {total}!")
        else:
            print(f"{self.name}'s cards are {self.print_cards(hand)}\n" \
                  f"Total: {total}")
        return self.has_bust[hand]

    def second_hand_check(self):
        if len(self.cards[1]) > 0:
            second_hand = 2
        else:
            second_hand = 1
        return second_hand

    def bet_result(self, result, total):
        print(f"{self.name} has {result} this hand with {total}")
        if result == "lost":
            print(f"lost ${self.bet[0]}")
            self.money -= self.bet[0]
        elif result == "won":
            print(f"gained ${self.bet[0]}")
            self.money += self.bet[0]
        self.bet.pop(0)
        
            

#game logic
def black_jack_start():
    #game logic
    player_list = player_setup()
    deck = Deck()
    dealer = Player("The dealer")
    new_round(player_list, deck, dealer)

def player_setup():
    '''
    asks for how many players there are and asks for names for each of them
    initializes a player class for each player and dealer
    '''
    while True:
        try:    
            player_no = int(input("How many players are there? 1-4 "))
        except:
            print("\nThat's not a valid input.")
            continue
        if 0 < player_no < 5:
            break
        else:
            print("\nThere must be 1-4 players.")
            continue
    #create a list with and instance of Player() class for each player, final instance will always be Dealer
    player_list = []
    for i in range(player_no):
        player_name = input(f"\nPlayer {i + 1} please input your name ")
        player_list.append(Player(player_name))
    return player_list

def new_round(player_list, deck, dealer):
    #ask player if they want to leave the table and also check if their money = 0
    index = 0
    index_list = []
    for player in player_list:
        if player.money <= 0:
            player.at_table = False
            print(f"\n{player.name} has no money left")
        while player.at_table == True:
            leave_table = input(f"\n{player.name} would you like to bet or leave the table? bet/leave ").lower()
            if leave_table == "bet":
                break
            elif leave_table == "leave":
                player.at_table = False
            else:
                print("\nThat's not a valid response try again")
                continue
        if player.at_table == True:
            player.betting()
            index += 1
        else:
            print(f"\n{player.name} has left the table.")
            index_list.append(index)
    for i in index_list:
        player_list.pop(i)
    if len(player_list) > 0:
        player_turn(player_list, deck, dealer)
    else:
        no_players()

def player_turn(player_list, deck, dealer):
    #deal first two cards to players and dealer
    for player in player_list:
        player, deck = initial_deal(player, deck)
    dealer, deck = initial_deal(dealer, deck, True)
    print("\nCards have been dealt")
    for player in player_list:
        print(f"{player.name}'s deal {player.print_cards()}")
    #players declare move
    dealer_card =  dealer.cards[0][0]
    turn = 1
    hands_playing = len(player_list)
    while hands_playing > 0:
        for player in player_list:
            second_hand = player.second_hand_check()
            for i in range(second_hand):
                if player.has_bust[i] == True or player.has_stood[i] == True:
                    continue
                total = player.hand_total(i)
                if total == 21:
                    print(f"{player.name} has 21!")
                    player.stand(i)
                    input("Hit enter to continue: ")
                    print("\n")
                    hands_playing -= 1
                    continue
                print(f"\n{dealer.name}'s shown card is {dealer_card[0]} of {dealer_card[1]}")
                if i >= 1:
                    print(f"{player.name}'s second hand")
                move_list = ["hit", "stand"]
                #add special moves on turn 1
                if turn == 1 and player.has_special == False:
                    split_check, double_down_check = player.can_special_moves()
                    if split_check == True:
                        move_list.append("split")
                    if double_down_check == True:
                        move_list.append("double down")
                #check if move is valid
                while True:
                    print(f"Your cards: {player.print_cards(i)}\n" \
                          f"Total: {total}\n" \
                          f"Available moves: {move_list}")
                    move = input(f"{player.name} declare your move ").lower()
                    #do the move that has been input and break
                    if move in move_list:
                        if move == "hit":
                            deck = player.hit(deck, i)
                        elif move == "stand":
                            player.stand(i)
                            hands_playing -= 1
                        elif move == "double down":
                            deck = player.double_down(deck)
                            hands_playing -= 1
                        elif move == "split":
                            deck = player.split(deck)
                            hands_playing += 1
                        print("\n")
                        break
                    else:
                        print("\nThat's not a valid move!")
                        continue
                #check if hand has bust
                if player.bust_check(i):
                    hands_playing -= 1
                input("Hit enter to continue: ")
                print("\n")
        turn += 1
    dealer_turn(player_list, deck, dealer)

def initial_deal(player, deck, dealer = False):
    '''
    draws the first two cards for each player and dealer
    '''
    for i in range(2):
        deck = player.hit(deck, 0, dealer)
    return player, deck

def dealer_turn(player_list, deck, dealer):
    print(f"It's the dealer's play")
    while True:
        dealer_total = dealer.hand_total()
        if dealer_total >= 17:
            dealer.stand()
            print(f"The dealer's total is {dealer.hand_total()}")
            input("Hit enter to continue: ")
            print("\n")
            break
        else:
            deck = dealer.hit(deck)
            print("\n")
            if dealer.bust_check():
                break
    resolve_winners(player_list, deck, dealer, dealer_total)

def resolve_winners(player_list, deck, dealer, dealer_total):
    for player in player_list:
        second_hand = player.second_hand_check()
        for i in range(second_hand):
            if i >= 1:
                print(f"{player.name}'s second hand")
            total = player.hand_total(i)
            player_won = "lost"
            if player.has_bust[i] == False and total > dealer_total:
                player_won = "won"
            elif player.has_bust[i] == False and dealer.has_bust[0] == True:
                player_won = "won"
            elif total == dealer_total:
                player_won = "tied"
            player.bet_result(player_won, total)
            input("Hit enter to continue: ")
            print("\n")
    reset_game(player_list, deck, dealer)

def reset_game(player_list, deck, dealer):
    for player in player_list:
        player.cards = [[], []]
        player.bet = []
        player.has_special = False
        player.has_stood = [False, False]
        player.has_bust = [False, False]
    dealer.cards = [[], []]
    dealer.bet = []
    dealer.has_special = False
    dealer.has_stood = [False, False]
    dealer.has_bust = [False, False]
    print("Starting a new round")
    new_round(player_list, deck, dealer)

def no_players():
    print("There are no players left at the table.")
    
black_jack_start()