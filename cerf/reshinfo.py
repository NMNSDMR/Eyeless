from itertools import product
i = 0
def generate_combinations (letters, length) :
    for combo in product (letters, repeat=length) :
        yield ''.join (combo)
letters = input ("Введите буквы без пробелов: ") 
length = int (input ("Введите длину комбинации: "))|
wewe = input("Введите слово которое нужно найти")
for combo in generate_combinations (letters, length) :
    i += 1
    print (combo)
    if combo == wewe:
        print (i)
        break