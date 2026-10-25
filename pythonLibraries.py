# # # # # # # # # import numpy as np

# # # # # # # # # arr = np.array([1, 2, 3, 4, 5])
# # # # # # # # # print(arr)
# # # # # # # # # print(type(arr))

# # # # # # # # from numpy import random
# # # # # # # # import numpy as np

# # # # # # # # x = random.rand()
# # # # # # # # print(x)

# # # # # # # # x = random.choice([3, 5, 7, 9])
# # # # # # # # print(x)

# # # # # # # # prices = np.array([100, 200, 300, 400])
# # # # # # # # print(prices + 50)

# # # # # # # # print(prices * 5)

# # # # # # # # print(prices - 10)

# # # # # # # # print(prices / 2)


# # # # # # # # marks = np.array([60, 70, 80, 90, 100])
# # # # # # # # print(np.mean(marks))
# # # # # # # # print(np.median(marks))
# # # # # # # # print(np.max(marks))

# # # # # # # import pandas as pd

# # # # # # # mydataset = {
# # # # # # #     'cars': ["BMW", "Volvo", "Ford"],
# # # # # # #     'passings': [3, 7, 2]
# # # # # # # }

# # # # # # # myvar = pd.DataFrame(mydataset)

# # # # # # # print(myvar)

# # # # # # try:
# # # # # #     print(x)
# # # # # # except:
# # # # # #     print("an exception occured")

# # # # # # try:
# # # # # #     number1 = 10
# # # # # #     number2 = 0
# # # # # #     result = number1 / number2
# # # # # #     print("Result:", result)
# # # # # # except ZeroDivisionError:
# # # # # #     print("Error: You cannot divide by zero.")

# # # # # # print("Program continues to run")

# # # # # # try:
# # # # # #     age = int(input("Enter you age:"))
# # # # # #     print("Your age is:",  age)
# # # # # # except ValueError:
# # # # # #     print("Invalid input. Please enter a number.")

# # # # # try:
# # # # #     num1 = int(input("Enter your First Number: "))
# # # # #     num2 = int(input("Enter you Second Number: "))
# # # # #     result = num1 / num2
# # # # #     print("Answer is: ", result)
# # # # # except ValueError:
# # # # #     print("Error: Please enter a valid whole number.")
# # # # # except ZeroDivisionError:
# # # # #     print("Error: The second number cannot be zero.")


# # # # try:
# # # #     num1 = int(input("Enter number: "))

# # # # except ValueError:
# # # #     print("Error: Please enter a valid whole number.")

# # # # else:
# # # #     print("Success")
# # # #     print("Your number is: ", num1)

# # # try:
# # #     num1 = int(input("Enter a number: "))
# # #     print("Number is: ", num1)

# # # except ValueError:
# # #     print("Error: Please enter a valid whole number.")

# # # finally:
# # #     print("Thank you for using this program.")

# # def validate_mark(mark):
# #     if mark < 0 or mark > 100:
# #         raise ValueError("Mark must be between 0 and 100.")
# #     return "Mark is valid"

# # try:
# #     print(validate_mark(100))

# # except ValueError as error:
# #     print("Error: ", error)

# def calculate_result():
#     try:
#         name = input("Enter you name: ")
#         marks = float(input("Enter your mark: "))
#         if marks < 0 or marks > 100:
#             raise ValueError("Mark should be between 0 and 100.")
#     except ValueError as error:
#         print(f"Invalid input: {error}")
#     else:
#         print("\nStudent Name: ", name)
#         if marks >= 50:
#             print("Status: Pass")
#         else:
#             print("Status: Fail")

#     finally:
#         print("Thank you for using the result calculator.")

# calculate_result()

# file = open("file.txt", "w")
# file.write("Hello, World!\\n")
# file.write("This is a test file.")
# print("File written successfully.")

with open("file.txt", "w") as file:
    file.write("Hello, World!\n")
    file.write(" This is a test file.")
print("File written successfully.")

# with open("file.txt", "r") as file:
#     first_line = file.readline()
#     second_line = file.readline()
#     print(first_line)
#     print(second_line)

try:
    with open('file.txt', 'r') as file:
        data = file.read()
        print(data)
except FileNotFoundError:
    print("Error: The file 'data.txt' was not found.")
except PermissionError:
    print("Error: You do not have permission to read 'data.txt'.")