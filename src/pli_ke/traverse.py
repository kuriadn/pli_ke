from math import *
from pli_ke.angle import *

def distance(dx, dy):
  return sqrt(dx ** 2 + dy ** 2)

def bearing(dx, dy):
  ang = atan(dx / dy)
  if dx < 0 and dy > 0: ang += 2 * pi 
  if dx < 0 and dy < 0: ang += pi
  if dx > 0 and dy < 0: ang += pi 
  ang = Angle(ang)
  dsgn = u'\N{DEGREE SIGN}'
  dstr = str(ang.degree) + dsgn + ' ' + str(ang.minute) + "'" + ' ' + str(ang.second) + '"'
  return dstr
