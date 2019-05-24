from math import *

def sign(value):
  sig = 1
  if value < 0: sig = -1
  return sig

def radian(d, m, s):
  sig = sign(d)
  deg = abs(d)
  return (deg + m/60.0 + s/3600.0) * pi / 180.0 * sig
  
class Angle():

  def __init__(self, rad):
    self.rad = rad
    self.sign = sign(self.rad)
    rad = abs(self.rad)
    ang = rad * 180.0 / pi
    deg = floor(ang)
    mins = (ang - deg) * 60.0
    minute = floor(mins)
    secs = (mins - minute) * 60.0
    self.decdeg = rad * 180.0 / pi  
    self.degree = deg * self.sign
    self.minute = minute
    self.second = round(secs, 2)

  