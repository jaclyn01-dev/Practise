import random

a = random.randint(1, 9)
b = random.randint(1, 9)
c = random.randint(1, 9)
d = random.randint(1, 9)

# # a = 4
# # b = 3
# # c = 5
# # d = 2

expression = f"{a} + ({b} * {c}) / {d}"
correct = a + (b * c) / d

# a = random.randint(2, 20)
# b = random.randint(2, 20)
# c = random.randint(2, 9)

# expression = f"{a} * {b} % {c}"
# correct = a * b % c

print("Predict the value of the following expression: " + expression)

prediction = float(input("Enter your answer: "))

if round(prediction, 2) == round(correct, 2):
    print("Your answer is correct.")

else:
    print("Your answer is incorrect.")
    print("The correct answer is: " + str(round(correct, 2)))