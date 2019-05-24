from inventory.models import *
from django.db import connection

class Point():

  def __init__(self, x, y):
    self.x = x
    self.y = y 

  def toString(self):
    return '{0} {1}'.format(self.x, self.y)
