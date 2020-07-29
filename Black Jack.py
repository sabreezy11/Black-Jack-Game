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
        # Pop the next card off the top of the deck
        # Pop is a way to retrieve an item from a list and also removes it from the list
        # Pop is the opposite of append
        # Initializing at '0' takes from top of deck
    deck.append(next_card)
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

    # global player_score # Use the global versions of this variable, and not try to create a local variable
    # global player_ace # Use the global versions of this variable, and not try to create a local variable
    # card_value = deal_card(player_card_frame)[0]
    # if card_value == 1 and not player_ace:
    #     player_ace = True
    #     card_value = 11 # if player already has ace in hand (ace = 1), the second ace will = 11
    # player_score += card_value
    #
    # # if we would bust, check if there is an ace and subract 10
    # # player_ace is always the same value
    # # player_score is always being assigned a new value
    # if player_score > 21 and player_ace:
    #     player_score -= 10
    #     player_ace = False
    # player_score_label.set(player_score)
    # if player_score > 21:
    #     result_text.set("Dealer Wins!")
    #
    # print(locals()) # prints a list of all local variables



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
    # The command function that you assign has to be the function that executes when
    # the button is clicked. You don't want to call the function instead of assigning
    # the command.
dealer_button.grid(row=0, column=0)
player_button = tkinter.Button(button_frame, text="Player", command=deal_player)
player_button.grid(row=0, column=1)



##TESTING THAT IMAGES ARE STORING TO PROPER VALUES##
# Load cards
cards = []
load_images(cards)
print(cards)



##DEALER AND PLAYER HAND LIST##
# Create a new deck of cards and shuffle them.
# Create the list to store dealers and players hands
deck = list(cards) # Creates a new and separate list every time the program runs
random.shuffle(deck)

dealer_hand = []  # empty list the cards will be stored in
player_hand = []  # empty list the cards will be stored in



##DEALS PLAYER AND DEALER CARDS WHEN YOU RUN PROGRAM##
deal_player()
dealer_hand.append(deal_card(dealer_card_frame))
dealer_score_label.set(score_hand(dealer_hand)) #this will display dealer score on initial program run
deal_player()




##CALCULATE DEALER/PLAYER SCORE##




mainWindow.mainloop()



##  NOTES ON CALCULATING DEALER/PLAYER SCORES ## (see deal_dealer and deal_player func.)
################################################
#The face value of a card can be pbtained from the tuple returned by the deal_card
#function, so that can be used to update the player's total. The code also has to
#deal with the two values that an Ace can represent. In Black Jack, no matter how many
#aces a player has, only one of them at most can have the value 11, or of course the
#player will bust since the max score is 21. The technique here is to give the first ace
#a value of 11 and add any subsequent ones the value of 1. If the player busts by
#holding at least one ace, then ten is subtracted from the total and a check for being bust
#is performed again. That way it will give the player the option to treat an ace as 1 instead
#of 11.
#To do all this, we need 2 more variables: one to store the player's total, and another
#to track whether or not the player holds an ace that has the value 11.
#
#
#player_score = 0 added to ##EMBEDDED FRAME TO HOLD THE CARD IMAGES##
#player_ace = False added to ##EMBEDDED FRAME TO HOLD THE CARD IMAGES##
#modified deal_player function with checking for ace values
#
#