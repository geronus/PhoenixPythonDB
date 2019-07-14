# convert arabic numbers to roman numerals and vice-versa:

RA = ["CM", "CD", "XC", "XL", "IX", "IV", "M", "D", "C", "L", "X", "V", "I"]
RtoA = {
  "CM": 900,
  "CD": 400,
  "XC": 90,
  "XL": 40,
  "IX": 9,
  "IV": 4,
  "M": 1000,
  "D": 500,
  "C": 100,
  "L": 50,
  "X": 10,
  "V": 5,
  "I": 1
}

AR = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
AtoR = {
  1000: "M",
  900: "CM",
  500: "D",
  400: "CD",
  100: "C",
  90: "XC",
  50: "L",
  40: "XL",
  10: "X",
  9: "IX",
  5: "V",
  4: "IV",
  1: "I"
}

def converts(num):
  if type(num) == type(100):
    ## new code, keeps it in the correct order

    if num == 0:
      result = '0'
    else:
      result = ''
      for x in AR:
        while num >= x:
          result += AtoR[x]
          num -= x

    ## old code, wasn't working correctly
    # for a in AtoR:
    #   # print(a)
    #   while num >= a:
    #     # print('{} is > {}'.format(num, a))
    #     result += AtoR[a]
    #     num -= a

  else:
    result = 0
    ## new code, keeps it in the correct order
    counter = len(num)
    while counter > 0:
      for y in RA:
        if y in num:
          result += RtoA[y]
          num = num.replace(y, '', 1)
        counter = len(num)

    ## old code, wasn't working correctly
    # for r in RtoA:
    #   counter = len(num)
    #   while counter > 0:
    #     if r in num:
    #       result += RtoA[r]
    #       num = num.replace(r, '', 1)
    #     counter -= 1

  return result

# # test cases
# # test    45  ,     2948    , 100
# # expect 'XLV', 'MMCMXLVIII', 'C'
# print(converts(45))
# print(converts(2948))
# print(converts(100))
# # test the other functionality
# # test 'MCMXCIX', 'XXXVII', 'MCMXXIV'
# # expect 1999   ,    37   ,   1924
# print(converts('MCMXCIX'))
# print(converts('XXXVII'))
# print(converts('MCMXXIV'))