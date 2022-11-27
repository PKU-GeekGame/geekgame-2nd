# https://en.wikipedia.org/wiki/Polydivisible_number

def find_polydivisible(base):
    """Find polydivisible number."""
    numbers = []
    previous = [i for i in range(1, base)]
    new = []
    digits = 2
    while not previous == []:
        numbers.append(previous)
        for n in previous:
            for j in range(0, base):
                number = n * base + j
                if number % digits == 0:
                    new.append(number)
        previous = new
        print(digits,len(new))
        new = []
        digits = digits + 1
    return numbers