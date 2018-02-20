fr = open("map1.txt", "r")
values = fr.readlines()
fr.close()
width = str(len(values[0])-1)
height = str(len(values))
print(width + " boxes wide")

print(height + " boxes tall")
