# Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""

history = ""
abort = ""
prompt = ""
wins = 0
attempts = 0
player_hand =()
dealer_hand = ()
score = "Player won " + str(wins) + " out of " + str(attempts) +" attempts"


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit +  self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos, hide):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        if hide:
            canvas.draw_image(card_back , CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
        else:
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self, is_dealer):
        self.hand=[]
        self.is_dealer = is_dealer

    def __str__(self):
        s = ""
        for x in self.hand:
            s = s + str(x) + " "
        return s

    def hit(self, deck):
        self.add_card(deck.deal_card())
    
    def add_card(self, card):
        self.hand.append(card)

    # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
    def get_value(self):
        ace = 0
        count = 0
        for x in self.hand:
            if x.rank == "A":
                ace = 10
            count = count + VALUES.get(x.rank)
        if count + ace <= 21:
            count = count + ace 
        return count

    def busted(self):
        if self.get_value() > 21:
            return True
        else:
            return False
    
    def draw(self, canvas, p):
        i = 0
        for card in self.hand:
            if self.is_dealer == True:
                if i == 0 and in_play:
                    card.draw(canvas, [p[0] + (i * 80),p[1]], True)
                else:
                    card.draw(canvas, [p[0] + (i * 80),p[1]], False)
            else:
                card.draw(canvas, [p[0] + (i * 80),p[1]], False)
            i = i + 1

# define deck class
class Deck:
    def __init__(self):
        self.inventory = []
        for s in SUITS:
            for r in RANKS:
                self.inventory.append(Card(s,r))
    # add cards back to deck and shuffle
    def shuffle(self):
        random.shuffle(self.inventory)

    def deal_card(self):
        return self.inventory.pop(0)

#define event handlers for buttons
def deal():
    global in_play, player_hand, dealer_hand, deck, attempts, outcome, abort, prompt
    if in_play:
        #aborting a game in progress cause player to lose game
        attempts = attempts + 1
        abort = "Player lost last game because of aborting active game"
    else:
        abort = ""
    prompt = "Hit or Stand?"

    outcome = ""
    deck = Deck()
    deck.shuffle()
    player_hand = Hand(False)
    dealer_hand = Hand(True)
    
    player_hand.hit(deck)
    dealer_hand.hit(deck)
    player_hand.hit(deck)
    dealer_hand.hit(deck)
    
    in_play = True

def hit():
    global in_play, player_hand, dealer_hand, deck, outcome, abort, attempts, prompt
    abort = ""
    # if the hand is in play, hit the player
    if in_play:
        player_hand.hit(deck)
   
        # if busted, assign an message to outcome, update in_play and score
        if player_hand.get_value() > 21:
            in_play = False
            outcome = "Player Busted"
            attempts = attempts + 1
            prompt = "New Deal?"
        
def stand():
    global in_play, player_hand, dealer_hand, deck, wins, attempts, score, outcome, abort, prompt
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    abort = ""
    prompt = ""
    if in_play:
        in_play = False
        while dealer_hand.get_value() < 17:
            dealer_hand.hit(deck)
        attempts = attempts + 1
        if not dealer_hand.busted():
            if player_hand.get_value() > dealer_hand.get_value():
                wins = wins + 1
                # assign a message to outcome, update in_play and score
                history = "Player has", str(player_hand.get_value())," Dealer has:", str(dealer_hand.get_value()) + " So player wina"
                outcome = " Player Wins"
            else:
                history = "Player has", str(player_hand.get_value())," Dealer has:", str(dealer_hand.get_value()) + " So dealer wina"
                outcome = " Dealer Wins"    
        else:
            # player wins hand
            wins = wins + 1
            history = "Player has", str(player_hand.get_value())," Dealer has:", str(dealer_hand.get_value()) + " So player wina"
            outcome = "Dealer busted"
    prompt = "New Deal?"        
            
# draw handler    
def draw(canvas):
    global player_hand, dealer_hand, history, score, aborted, prompt
    
    canvas.draw_text("Blackjack", (200, 50), 40, "Black") 
    score = "Player won " + str(wins) + " out of " + str(attempts) +" attempts"
    canvas.draw_text(score, (200, 80), 12, "Aqua")
    canvas.draw_text(outcome, (190, 125), 30, "White")
    canvas.draw_text(prompt, (130, 180), 20, "White")

    player_hand.draw(canvas, [120, 200])    
    canvas.draw_text("Player:", (10, 250), 20, "White")
    canvas.draw_text("Card count:  " + str(player_hand.get_value()), (10, 280), 12, "White")    
    
    dealer_hand.draw(canvas, [120, 350])

    if not in_play:    
        canvas.draw_text("Card count:  " + str(dealer_hand.get_value()), (10, 430), 12, "White")      
    canvas.draw_text("Dealer:", (10, 400), 20, "White")  
    canvas.draw_text(abort, (15, 550), 20, "Yellow")    
    
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# deal an initial hand

# get things rolling
player_hand = Hand(False)
dealer_hand = Hand(True)

frame.start()


# remember to review the gradic rubric
