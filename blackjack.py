import random


def shuffle_card(cards: list) -> list:
    return random.shuffle(cards)


class Blackjack:
  def __init__(self):
    self.cards: list = ['2','3','4','5','6','7','8','9','10','J','Q','K','A'] * 4
  
  
  
  def play(self) -> list:
    self.cards = shuffle_card(self.cards)
    user_card: list = [random.choice(self.cards) for _ in range(2)]
    diller_card: list = [random.choice(self.cards) for _ in range(2)]
    return user_card and diller_card
  
  def sum_card(self, cards: list) -> int:
    result = 0
    for i in cards:
      if i in ['J','Q','K','A']:
        result += 10
      result += int(i)
    return result
    
      
    
