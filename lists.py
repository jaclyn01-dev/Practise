myList = ["banana", "cherry", "apple", "mango", "cherry"]

list2 = [1, 2, 3, 5, 5]

list3 = [True, False, False]

list4 = ["abc", 5, True, 40, "Male"]

# for items in list4:
#     print(items)

# myList[1:2] = ["berries", "watermelon"]

# myList.append("orange")

# for fruit in myList:
#     print(fruit)

# myList.extend(list2)

# for fruit in myList:
#     print(fruit)

# while "cherry" in myList:
#     myList.remove("cherry")

# for fruit in myList:
#     print(fruit)

# myTuple = ("banana", "cherry", "apple", "mango", "cherry")
# print(myTuple)

# thisset = {"apple", "banana", "cherry", "mango", "cherry", "banana"}
# print(thisset)

myDictionary = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

# print(myDictionary)

# for key, value in myDictionary.items():
#     print(f"{key}: {value}")

car = {
    "brand": "Ford",
    "colours": ["red", "blue"],               # the value is a list
    "owner": {"name": "Sam", "age": 30}       # the value is another dictionary
}

print(car["colours"])        # red
print(car["owner"])     # Sam