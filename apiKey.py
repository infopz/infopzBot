
file = open('ApiKeys.txt', 'r')
lines = file.readlines()

def apiBot():
  line = lines[0]
  line = line[0:-1]
  return(line)

def apiMashape():
  line = lines[1]
  line = line[0:-1]
  return(line)
