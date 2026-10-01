scores = [78, 65, 89, 86, 55, 91, 64, 89]

highest_score = scores[0]

for score in scores:
    if score > highest_score:
        highest_score = score

print(f"The highest score in the class is: {highest_score}")