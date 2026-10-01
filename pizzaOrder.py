size = input("What size pizza do you want? S, M, or L: ").upper()
add_pepperoni = input("Do you want pepperoni? Y or N: ").upper()
add_extraCheese = input("Do you want extra cheese? Y or N: ").upper()

bill = 0

if size == "S":
    bill = 15

elif size == "M":
    bill = 20

elif size == "L":
    bill = 25

if add_pepperoni == "Y":
    if size == "S":
        bill += 2
    else:
        bill += 3

if add_extraCheese == "Y":
    bill += 1

print(f"Your final bill is: R{bill}")