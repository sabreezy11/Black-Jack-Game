##Here we will practice importing techniques##
# This file will be used in conjunction with import_test



import random

try:
    import tkinter
except ImportError: # python 2
    import Tkinter as tkinter



###################
###MAIN FUNCTION###
###################

##LOADING CARD IMAGES##
def load_images(card_images):
    # The following is case sensitive since it has to match the .ppm file name.
    suits = ['heart', 'club', 'diamond', 'spade']
    face_cards = ['jack', 'queen', 'king']

    if tkinter.TkVersion >= 8.6:
        extension = 'png'
    else:
        extension = 'ppm'



    ##FOR EACH SUIT, RETRIEVE THE IMAGE FOR THE CARD##
    # Number cards 1 to 10
    for suit in suits:
        for card in range(1, 11):
            name = 'cards_{}/{}_{}.{}'.format(extension, str(card), suit, extension)
            # 'cards' is the subfolder that the images are stored in
            # The rest is the file name format
            image = tkinter.PhotoImage(file=name)
            card_images.append((card, image,))
        # Face card
        for card in face_cards:
            name = 'cards_{}/{}_{}.{}'.format(extension, str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((10, image,))



##DEALING CARDS TO PLAYERS##
def deal_card(frame):
    next_card = deck.pop(0)
    # And add it back to the pack or else you'll eventually run out of cards
    deck.append(next_card)
    # Pop the next card off the top of the deck
    # Pop is a way to retrieve an item from a list and also removes it from the list
    # Pop is the opposite of append
    # Initializing at '0' takes from top of deck
    tkinter.Label(frame, image=next_card[1], relief='raised').pack(side='left')
    # Add the image to a label and display label
    return next_card
    # Return the card's face value



##RETURNS A SCORE IF IT'S GIVEN A LIST OF CARDS##
# Looks at a hand and calculates a score based on that hand
# Only 1 ace can have the value = 11, and this will reduce if the hand busts
def score_hand(hand):
    score = 0 # This is a local variable
    ace = False
    for next_card in hand:
        card_value = next_card[0]
        if card_value == 1 and not ace:
            ace = True
            card_value = 11
        score += card_value
        # If we would bust, check if there is an ace and subtract 10
        if score > 21 and ace:
            score -= 10
            ace = False
    return score



##DEALING CARDS FOR CORRESPONDING BUTTONS##
def deal_dealer(): # Deals card to dealer when 'Dealer' button clicked
    dealer_score = score_hand(dealer_hand)
    while 0 < dealer_score < 17:
        dealer_hand.append(deal_card(dealer_card_frame))
        dealer_score = score_hand(dealer_hand)
        dealer_score_label.set(dealer_score)

    # We now need to check and see if it's game over
    player_score = score_hand(player_hand)
    if player_score > 21:
        result_text.set("Dealer Wins!")
    elif dealer_score > 21 or dealer_score < player_score:
        result_text.set("Player Wins!")
    elif dealer_score > player_score:
        result_text.set("Dealer Wins!")
    else:
        result_text.set("Draw!")


def deal_player(): # Deals card to player when 'Player' button clicked
    player_hand.append(deal_card(player_card_frame))
    player_score = score_hand(player_hand)
    player_score_label.set(player_score)
    if player_score > 21:
        result_text.set("Dealer Wins!")



##NEW GAME##
def new_game():
    global dealer_card_frame # we're going to redefine this global variable
    global player_card_frame # we're going to redefine this global variable
    global dealer_hand # we're going to redefine this global variable
    global player_hand # we're going to redefine this global variable

    # embedded frame to hold the card images  (dealer)
    dealer_card_frame.destroy()
    dealer_card_frame = tkinter.Frame(card_frame, background="green")
    dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)

    # embedded frame to hold the card images (player)
    player_card_frame = tkinter.Frame(card_frame, background="green")
    player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

    result_text.set("")

    # Create the list to store the dealer's and player's hands
    dealer_hand = []  # empty list the cards will be stored in
    player_hand = []  # empty list the cards will be stored in

    deal_player()
    dealer_hand.append(deal_card(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hand)) #this will display dealer score on initial program run
    deal_player()

##DECK SHUFFLE##
def shuffle():
    random.shuffle(deck)

############################################################################
# The following code will be executed if the 'if' statement below holds true
# in the import_test.py file.
# Therefore, when we run import_test, it will run the code but not actually
# start the game.



def play():
    # Deals player and dealer cards when you run program
    deal_player()
    dealer_hand.append(deal_card(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hand)) #this will display dealer score on initial program run
    deal_player()

    mainWindow.mainloop() # this is what officially starts the program


mainWindow = tkinter.Tk() # This should really go after funct. definitions



##SCREEN AND FRAMES FOR DEALER AND PLAYER##
mainWindow.title("Black Jack")
mainWindow.geometry("640x480")
mainWindow.configure(background='green')

result_text = tkinter.StringVar()
result = tkinter.Label(mainWindow, textvariable=result_text)
result.grid(row=0, column=0, columnspan=3)

card_frame = tkinter.Frame(mainWindow, relief="sunken", borderwidth=1, background="green")
card_frame.grid(row=1, column=0, sticky='ew', columnspan=3, rowspan=2)



##EMBEDDED FRAME TO HOLD THE CARD IMAGES##
dealer_score_label = tkinter.IntVar()  # .IntVar() is going to hold the score
tkinter.Label(card_frame, text="Dealer", background="green", fg="white").grid(row=0, column=0)
tkinter.Label(card_frame, textvariable=dealer_score_label, background="green", fg="white").grid(row=1, column=0)

dealer_card_frame = tkinter.Frame(card_frame, background="green")
dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)

player_score_label = tkinter.IntVar() # .IntVar() is going to hold the score

tkinter.Label(card_frame, text="Player", background="green", fg="white").grid(row=2, column=0)
tkinter.Label(card_frame, textvariable=player_score_label, background="green", fg="white").grid(row=3, column=0)

player_card_frame = tkinter.Frame(card_frame, background="green")
player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)



##BUTTONS##
button_frame = tkinter.Frame(mainWindow)
button_frame.grid(row=3, column=0, columnspan=3, sticky='w')

dealer_button = tkinter.Button(button_frame, text="Dealer", command=deal_dealer) #(dealer_card_frame))
dealer_button.grid(row=0, column=0)
player_button = tkinter.Button(button_frame, text="Player", command=deal_player)
player_button.grid(row=0, column=1)

new_game_button = tkinter.Button(button_frame, text="New Game", command=new_game)
new_game_button.grid(row=0, column=2)

shuffle_button = tkinter.Button(button_frame, text="Shuffle", command=shuffle)
shuffle_button.grid(row=0, column=3)

##TESTING THAT IMAGES ARE STORING TO PROPER VALUES##
# Load cards
cards = []
load_images(cards)
print(cards)


# Create a new deck of cards and shuffle them
deck = list(cards) + list(cards) + list(cards)
shuffle()


##DEALER AND PLAYER HAND LIST##
# Create a new deck of cards and shuffle them.
# Create the list to store dealers and players hands
#deck = list(cards) # Creates a new and separate list every time the program runs
dealer_hand = []  # empty list the cards will be stored in
player_hand = []  # empty list the cards will be stored in

if __name__ == "__main__":
    play()






