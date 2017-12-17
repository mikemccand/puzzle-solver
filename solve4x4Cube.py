'''
This brue-force script solves thie 4x4x4 3D printed cube puzzle at:

   https://www.thingiverse.com/thing:2308116
   
'''

def setPixel(block, x, y, z):
  if inBounds(x) == False:
    raise RuntimeError('x=%s is out of bounds' % x)
  if inBounds(y) == False:
    raise RuntimeError('y=%s is out of bounds' % y)
  if inBounds(z) == False:
    raise RuntimeError('z=%s is out of bounds' % z)
  if block[16 * x + 4 * y + z] != 0:
    raise RuntimeError('same pixel set!')
  block[16 * x + 4 * y + z] = 1

def getPixel(block, x, y, z):
  if inBounds(x) == False:
    raise RuntimeError('x=%s is out of bounds' % x)
  if inBounds(y) == False:
    raise RuntimeError('y=%s is out of bounds' % y)
  if inBounds(z) == False:
    raise RuntimeError('z=%s is out of bounds' % z)
  return block[16 * x + 4 * y + z]

def inBounds(x):
  return 0 <= x < 4

def checkBlock(block):
  for x in range(4):
    for y in range(4):
      for z in range(4):
        if getPixel(block, x, y, z):
          found = False
          for xd in (-1, 1):
            newX = x + xd
            if inBounds(newX):
              if getPixel(block, newX, y, z):
                found = True
          for yd in (-1, 1):
            newY = y + yd
            if inBounds(newY):
              if getPixel(block, x, newY, z):
                found = True
          for zd in (-1, 1):
            newZ = z + zd
            if inBounds(newZ):
              if getPixel(block, x, y, newZ):
                found = True
          if not found:
            raise RuntimeError('disconnected pixel %s, %s, %s' % (x, y, z))

def createNewBlock():
  return [0] * 64

def translate(block, xDelta, yDelta, zDelta):
  block2 = createNewBlock()
  for x in range(4):
    for y in range(4):
      for z in range(4):
        if getPixel(block, x, y, z):
          newX = x + xDelta
          newY = y + yDelta
          newZ = z + zDelta
          if not inBounds(newX) or not inBounds(newY) or not inBounds(newZ):
            return None
          setPixel(block2, newX, newY, newZ)
  return block2

def rotate90XAndTranslate(block, xDelta, yDelta, zDelta):
  block2 = createNewBlock()
  for x in range(4):
    for y in range(4):
      for z in range(4):
        if getPixel(block, x, y, z):
          newX = x + xDelta
          newY = -z + yDelta
          newZ = y + zDelta
          if not inBounds(newX) or not inBounds(newY) or not inBounds(newZ):
            return None
          setPixel(block2, newX, newY, newZ)
  return block2

def rotate90YAndTranslate(block, xDelta, yDelta, zDelta):
  block2 = createNewBlock()
  for x in range(4):
    for y in range(4):
      for z in range(4):
        if getPixel(block, x, y, z):
          newX = z + xDelta
          newY = y + yDelta
          newZ = -x + zDelta
          if not inBounds(newX) or not inBounds(newY) or not inBounds(newZ):
            return None
          else:
            setPixel(block2, newX, newY, newZ)
  return block2

def rotate90ZAndTranslate(block, xDelta, yDelta, zDelta):
  block2 = createNewBlock()
  for x in range(4):
    for y in range(4):
      for z in range(4):
        if getPixel(block, x, y, z):
          newX = y + xDelta
          newY = -x + yDelta
          newZ = z + zDelta
          if not inBounds(newX) or not inBounds(newY) or not inBounds(newZ):
            return None
          setPixel(block2, newX, newY, newZ)
  return block2

def rotate90X(block):
  for xDelta in range(-4, 5):
    for yDelta in range(-4, 5):
      for zDelta in range(-4, 5):
        newBlock = rotate90XAndTranslate(block, xDelta, yDelta, zDelta)
        if newBlock is not None:
          return newBlock
  raise RuntimeError('found no X rotation')

def rotate90Y(block):
  for xDelta in range(-4, 5):
    for yDelta in range(-4, 5):
      for zDelta in range(-4, 5):
        newBlock = rotate90YAndTranslate(block, xDelta, yDelta, zDelta)
        if newBlock is not None:
          return newBlock
  raise RuntimeError('found no Y rotation')

def rotate90Z(block):
  for xDelta in range(-4, 5):
    for yDelta in range(-4, 5):
      for zDelta in range(-4, 5):
        newBlock = rotate90ZAndTranslate(block, xDelta, yDelta, zDelta)
        if newBlock is not None:
          return newBlock
  raise RuntimeError('found no Z rotation')

if False:
  def allRotations(part):
    l = [(part, None)]
    block = part
    for i in range(3):
      block = rotate90X(block)
      l.append((block, '%dX' % (90 * (i+1))))
    block = rotate90X(block)
    if block != part:
      raise RuntimeError('part was not the same after rotating by 90X 4 times!')

    block = part
    for i in range(3):
      block = rotate90Y(block)
      l.append((block, '%dY' % (90 * (i+1))))
    block = rotate90Y(block)
    if block != part:
      raise RuntimeError('part was not the same after rotating by 90Y 4 times!')

    block = part
    for i in range(3):
      block = rotate90Z(block)
      l.append((block, '%dZ' % (90 * (i+1))))
    block = rotate90Z(block)
    if block != part:
      raise RuntimeError('part was not the same after rotating by 90Z 4 times!')
    return l
else:
  def allRotations(part):
    l = []
    partx = part
    for x in range(4):
      party = partx
      for y in range(4):
        partz = party
        for z in range(4):
          l.append((partz, 'x%s,y%s,z%s' % (90*x, 90*y, 90*z)))
          partz = rotate90Z(partz)
        party = rotate90Y(party)
      partx = rotate90X(partx)
    return l

def allTranslations(part):
  for xDelta in range(-4, 5):
    for yDelta in range(-4, 5):
      for zDelta in range(-4, 5):
        newPart = translate(part, xDelta, yDelta, zDelta)
        if newPart is not None:
          yield newPart, (xDelta, yDelta, zDelta)

def mergeParts(part1, part2):
  part = createNewBlock()
  for i in range(64):
    sum = part1[i] + part2[i]
    if sum == 2:
      return None
    elif sum in (0, 1):
      part[i] = sum
    else:
      raise RuntimeError('fail!  sum=%s' % sum)
  return part

def countPixels(part):
  return sum(part)

def draw(part):
  s = 'z=0:\n%s' % drawLayer(part, 0)
  s += 'z=1:\n%s' % drawLayer(part, 1)
  s += 'z=2:\n%s' % drawLayer(part, 2)
  s += 'z=3:\n%s' % drawLayer(part, 3)
  return s

def drawLayer(part, z):
  s = ''
  for y in (3, 2, 1, 0):
    for x in (0, 1, 2, 3):
      if getPixel(part, x, y, z):
        s += '*'
      else:
        s += ' '
    s += '\n'
  return s

def rotateAndTranslate(part):
  checkBlock(part)
  s = set()
  l = []
  for part0, part0Rotate in allRotations(part):
    for part0a, part0Delta in allTranslations(part0):
      tup = tuple(part0a)
      if tup not in s:
        s.add(tup)
        l.append((tup, part0Rotate, part0Delta))
  return l

part1 = createNewBlock()
setPixel(part1, 0, 0, 0)
setPixel(part1, 0, 0, 1)
setPixel(part1, 0, 0, 2)
setPixel(part1, 0, 1, 0)
setPixel(part1, 1, 1, 0)
setPixel(part1, 1, 2, 0)
setPixel(part1, 1, 3, 0)
setPixel(part1, 1, 3, 1)
setPixel(part1, 1, 3, 2)
setPixel(part1, 2, 1, 0)
setPixel(part1, 3, 1, 0)
setPixel(part1, 3, 0, 0)
setPixel(part1, 3, 0, 1)

part2 = createNewBlock()
setPixel(part2, 0, 0, 0)
setPixel(part2, 0, 1, 0)
setPixel(part2, 1, 0, 0)
setPixel(part2, 1, 1, 0)
setPixel(part2, 1, 2, 0)
setPixel(part2, 0, 0, 1)
setPixel(part2, 0, 1, 1)
setPixel(part2, 1, 1, 1)
setPixel(part2, 0, 0, 2)

part3 = createNewBlock()
setPixel(part3, 0, 0, 0)
setPixel(part3, 0, 1, 0)
setPixel(part3, 0, 2, 0)
setPixel(part3, 0, 3, 0)
setPixel(part3, 1, 0, 0)
setPixel(part3, 1, 3, 0)
setPixel(part3, 1, 0, 1)
setPixel(part3, 1, 0, 2)

part4 = createNewBlock()
setPixel(part4, 0, 0, 0)
setPixel(part4, 0, 1, 0)
setPixel(part4, 0, 2, 0)
setPixel(part4, 1, 0, 0)
setPixel(part4, 2, 0, 0)
setPixel(part4, 2, 1, 0)
setPixel(part4, 0, 0, 1)
setPixel(part4, 0, 1, 1)

part5 = createNewBlock()
setPixel(part5, 0, 0, 0)
setPixel(part5, 0, 1, 0)
setPixel(part5, 1, 1, 0)
setPixel(part5, 1, 1, 1)
setPixel(part5, 2, 1, 1)
setPixel(part5, 2, 2, 1)

part6 = createNewBlock()
setPixel(part6, 0, 0, 0)
setPixel(part6, 0, 1, 0)
setPixel(part6, 0, 2, 0)
setPixel(part6, 0, 3, 0)
setPixel(part6, 1, 2, 0)
setPixel(part6, 0, 1, 1)

part7 = createNewBlock()
setPixel(part7, 0, 0, 0)
setPixel(part7, 0, 1, 0)
setPixel(part7, 1, 0, 0)
setPixel(part7, 2, 0, 0)
setPixel(part7, 2, 0, 1)

part8 = createNewBlock()
setPixel(part8, 0, 0, 0)
setPixel(part8, 0, 1, 0)
setPixel(part8, 0, 1, 1)
setPixel(part8, 1, 0, 0)
setPixel(part8, 1, 0, 1)

part9 = createNewBlock()
setPixel(part9, 0, 0, 0)
setPixel(part9, 1, 0, 0)
setPixel(part9, 0, 1, 0)
setPixel(part9, 0, 1, 1)

totPixels = 0
all = set()
sumAll = 0
for i in range(1, 10):
  totPixels += countPixels(locals()['part%d' % i])
  locals()['allPart%s' % i] = rotateAndTranslate(locals()['part%d' % i])
  print('part %d has %d variants' % (i, len(locals()['allPart%s' % i])))
  print('%s' % draw(locals()['part%d' % i]))
  sumAll += len(locals()['allPart%s' % i])
  for partx, partXRotate, partXDelta in locals()['allPart%s' % i]:
    all.add(tuple(partx))
print('TOT pixels %s' % totPixels)
if totPixels != 64:
  raise RuntimeError('pixel total is not 64')
print('TOT unique parts %s vs %s' % (len(all), sumAll))
if len(all) != sumAll:
  raise RuntimeError('parts are somehow not unique?')

allPart1 = []
for part1a, part1Delta in allTranslations(part1):
  allPart1.append((part1a, None, part1Delta))

for part1a, part1Rotate, part1Delta in allPart1:
  #print('try another part1 (%s, %s):\n%s' % (part1Rotate, part1Delta, draw(part1a)))
  block1 = mergeParts(createNewBlock(), part1a)
  #print('    part1 matched:\n%s' % draw(block1))
  for part2a, part2Rotate, part2Delta in allPart2:
    #print('  try another part2 (%s, %s):\n%s' % (part2Rotate, part2Delta, draw(part2a)))
    newBlock = mergeParts(block1, part2a)
    if newBlock is None:
      continue
    #print('    part2 matched:\n%s' % draw(newBlock))
    block12 = newBlock
    for part3a, part3Rotate, part3Delta in allPart3:
      #print('    try another part3 (%s, %s):\n%s' % (part3Rotate, part3Delta, draw(part3a)))
      newBlock = mergeParts(block12, part3a)
      if newBlock is None:
        continue
      #print('    part3 matched:\n%s' % draw(newBlock))
      block123 = newBlock
      for part4a, part4Rotate, part4Delta in allPart4:
        #print('    try another part4 (%s, %s):\n%s' % (part4Rotate, part4Delta, draw(part4a)))
        newBlock = mergeParts(block123, part4a)
        if newBlock is None:
          continue
        #print('    part4 matched:\n%s' % draw(newBlock))
        block1234 = newBlock
        for part5a, part5Rotate, part5Delta in allPart5:
          #print('    try another part5 (%s, %s):\n%s' % (part5Rotate, part5Delta, draw(part5a)))
          newBlock = mergeParts(block1234, part5a)
          if newBlock is None:
            continue
          #print('    part5 matched:\n%s' % draw(newBlock))
          block12345 = newBlock
          for part6a, part6Rotate, part6Delta in allPart6:
            #print('    try another part6 (%s, %s):\n%s' % (part6Rotate, part6Delta, draw(part6a)))
            newBlock = mergeParts(block12345, part6a)
            if newBlock is None:
              continue
            #print('    part6 matched:\n%s' % draw(newBlock))
            block123456 = newBlock
            for part7a, part7Rotate, part7Delta in allPart7:
              #print('    try another part7 (%s, %s):\n%s' % (part7Rotate, part7Delta, draw(part7a)))
              newBlock = mergeParts(block123456, part7a)
              if newBlock is None:
                continue
              #print('    part7 matched:\n%s' % draw(newBlock))
              block1234567 = newBlock
              for part8a, part8Rotate, part8Delta in allPart8:
                #print('    try another part8 (%s, %s):\n%s' % (part8Rotate, part8Delta, draw(part8a)))
                newBlock = mergeParts(block1234567, part8a)
                if newBlock is None:
                  continue
                #print('    part8 matched:\n%s' % draw(newBlock))
                block12345678 = newBlock
                for part9a, part9Rotate, part9Delta in allPart9:
                  #print('    try another part9 (%s, %s):\n%s' % (part9Rotate, part9Delta, draw(part9a)))
                  newBlock = mergeParts(block12345678, part9a)
                  if newBlock is None:
                    continue
                  print('SOLUTION!!!\n%s' % draw(newBlock))
                  for i in range(1, 10):
                    print('  part%s:' % i)
                    print('    rotate: %s' % str(locals()['part%dRotate' % i]))
                    print('    translate: %s' % str(locals()['part%dDelta' % i]))
                    print('%s' % draw(locals()['part%sa' % i]))
