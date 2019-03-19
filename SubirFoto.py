def remove_char(s):
    return s[ :len(s) - 1]

i = 0
cadena = "P"
print(cadena)
for j in range(0, 10):
    cadena += j.__str__()
    print(cadena)
    cadena = remove_char(cadena)
