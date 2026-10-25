# def double(n):
#     return n * 2

# print(double(4))     # 8
# x = double(10)       # x holds 20

# def celsius_to_fahrenheit(c):
#     return c * 9 / 5 + 32

# print(celsius_to_fahrenheit(0))

# x = celsius_to_fahrenheit(100)
# print(x)

# def area_of_rectangle(width, height):
#     return width * height

# area = area_of_rectangle(3, 5)
# print(area)

# scores = [78, 65, 89, 86, 55, 91, 64, 89]

# highest_score = scores[0]

# for score in scores:
#     if score > highest_score:
#         highest_score = score

# print(highest_score)

scores = [78, 65, 89, 86, 55, 91, 64, 89]

def highest(scores):

    highest_score = scores[0]

    for score in scores:
        if score > highest_score:
            highest_score = score

    return highest_score

result = highest(scores)
print(result)

def lowest(scores):

    lowest_score = scores[0]

    for score in scores:
        if score < lowest_score:
            lowest_score = score

    return lowest_score

lowest_result = lowest(scores)
print(lowest_result)

def average(scores):

    total = 0

    for score in scores:
        total += score

    return total / len(scores)


# def average(scores):
#     return sum(scores) / len(scores)

average_result = average(scores)
print(average_result)

def count_above_average(scores):

    above_average = 0

    avg = average(scores)

    for score in scores:
        if score > avg:
            above_average += 1

    return above_average

above_average_result = count_above_average(scores)
print(above_average_result)