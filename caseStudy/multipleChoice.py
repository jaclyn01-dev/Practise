question1 = "What is the value of the expression: 2 * 3 - 4"
question2 = "What is the value of the expression: 1 + (2 * 3) / 4"
question3 = "The set data type can hold duplicate values. The statement is: "

options1 = "(a) 1\n(b) 2\n(c) 3\n(d) None"
options2 = "(a) 1.5\n(b) 3\n(c) 3.5\n(d) None"
options3 = "(a) False\n(b) True\n(c) Partially correct\n(d) None"

correctAnswer1 = "b"
correctAnswer2 = "d"
correctAnswer3 = "a"

# score = 0


# print(f"{question1}\n{options1}")

# prediction1 = str(input("Enter your answer: ")).lower()

# if prediction1 == correctAnswer1:
#     score += 1


# print(f"{question2}\n{options2}")

# prediction2 = str(input("Enter your answer: ")).lower()

# if prediction2 == correctAnswer2:
#     score += 1


# print(f"{question3}\n{options3}")

# prediction3 = str(input("Enter your answer: ")).lower()

# if prediction3 == correctAnswer3:
#     score += 1


# print(f"Your score: {score} out of 3")


quiz = [
    {"question": question1, "options": options1, "answer": correctAnswer1,},
    {"question": question2, "options": options2, "answer": correctAnswer2,},
    {"question": question3, "options": options3, "answer": correctAnswer3,},
]

score = 0

for item in quiz:
    print(item["question"])
    print(item["options"])
    
    prediction = input("Enter your answer: ").lower().strip()
    if prediction == item["answer"]:
        score += 1

print(f"Your score: {score} out of {len(quiz)}")