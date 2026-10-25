print("=" * 52)
print("This is a simple calculator.")
print(f"It supports the following operations:\ni)   Addition\nii)  Subtraction\niii) Multiplication\niv)  Division")
print("=" * 52)

firstNumber = float(input("Enter the first number: "))
secondNumber = float(input("Enter the second number: "))
operator = input("Enter an operator(+, -, *, /): ")

answer = None

if operator == "+":
    answer = firstNumber + secondNumber
elif operator == "-":
    answer = firstNumber - secondNumber
elif operator == "*":
    answer = firstNumber * secondNumber
elif operator == "/":
    answer = firstNumber / secondNumber
else:
    print("Invalid operator. Cannot compute result.")

if answer is not None:
    print(f"The final result is: {answer}")