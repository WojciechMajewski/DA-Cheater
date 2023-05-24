import numpy as np
from player import Player

class DzialoMajewski(Player):
    first_player = None
    known_pile = []
    ever_seen = set()

    def putCard(self, declared_card):
        if self.first_player == None:
            self.first_player = True
            #print(self.name, " First? ", str(self.first_player))

        hand = sorted(self.cards)
        if declared_card == None:
            declared_card = (8, 0)
        
        for card in hand:
            if card not in self.ever_seen:
                self.ever_seen.add(card)
        
        ### seen cards that are not in my hand nor on the pile must be in opponent's hand
        opponents_hand = [card for card in self.ever_seen if card not in hand and card not in self.known_pile]
        
        if len(hand) == 1:
            if hand[-1][0] < declared_card[0]:
                return "draw" ### Forced rule


        ### check if I have to lie:
        if hand[-1][0] < declared_card[0]:          ### Need to remember cards drawn by the opponent, to not declare a card that they have in hand!!!
            self.known_pile.append(hand[0])
            for v in range(6):
                value = 14 - v

                ### If all legal cards are in opponent's hand, just declare an Ace
                if value < declared_card[0]:
                    return hand[0], (14, 3)
                
                for c in range(4):
                    color = 3 - c
                    ### If there is a legal card that is, to my knowledge, not in opponent's hand, declare it while placing my weakest card.
                    if (value, color) not in opponents_hand:
                        return hand[0], (value, color)
            return hand[0], (14, 3) ### (14, 3) will always be the last card in my hand when I sort it
        
        ### else, tell the truth:
        for card in hand:
            if card[0] >= declared_card[0]:
                self.known_pile.append(card)
                return card, card

        return "draw"
    
    def checkCard(self, opponent_declaration):
        if self.first_player == None:
            self.first_player = False
            #print(self.name, " First? ", str(self.first_player))

        self.known_pile.append((-1, -1)) ### Unknown card played by opponent, might be drawn instantly if I check.

        ### If they declare a card I have in hand, they are lying!
        if opponent_declaration in self.cards:
            return True
        
        ### If I remember that I've put the declared card on the pile and it is still there, they are lying!
        if opponent_declaration in self.known_pile:
            return True

        ### If they declare an Ace and I don't have one, I will need it for my last move so I check. Perhaps they were lying, even better for me!
        if opponent_declaration[0] == 14 and sorted(self.cards)[-1][0] < 14:
            return True
        
        return False

    ### Reiplemented to get extra information
    def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=True):

        ### Remove all drawn cards from the memory pile
        if checked and noTakenCards != None:
            for c in range(noTakenCards): self.known_pile.pop()
        
        ### Remember ever revealed cards
        if revealedCard != None and revealedCard not in self.ever_seen:
            self.ever_seen.add(revealedCard)

        if log: 
            print("Feedback = " + self.name + " : checked this turn = " + str(checked) +
              "; I checked = " + str(iChecked) + "; I drew cards = " + 
                      str(iDrewCards) + "; revealed card = " + 
                      str(revealedCard) + "; number of taken cards = " + str(noTakenCards))
