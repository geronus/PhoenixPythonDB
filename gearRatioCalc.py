def ratioCalc(current,type,ratio='7/4'):
  w = int(ratio[:ratio.index('/')])
  a = int(ratio[ratio.index('/')+1:])
  if type.lower() == 'armor': return (current*w//a)
  else: return (current*a//w)

# test case of ratioCalc
# testing 700, armor, 7/4
# print(ratioCalc(700,'armor','7/4'))
