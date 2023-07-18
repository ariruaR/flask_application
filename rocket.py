from random import randint,choice

class Rocket:
  def __init__(self,bid):
    self.bid = bid
  
  def play(self):
    self.COEF = [0.00,0.01,0.03,0.07,0.13,0.25,0.33,0.47,0.56,0.75,1.0,1.15,1.45,2.0,2.5,3.65,15]
    # self.int_coef = randint(0,7)
    # self.float_coef = randint(0,9) / 10
    # self.result_coef = (float(self.int_coef) + self.float_coef)
    self.result_coef = choice(self.COEF)
    return self.result_coef
  def get_bid(self):
    self.finally_bid = self.result_coef * float(self.bid)
    return round(self.finally_bid,2)

  @staticmethod
  def start(bid):
    return Rocket(bid).play()