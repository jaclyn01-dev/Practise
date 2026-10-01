student_scores = {'Harry': 85, 'Ron': 77, 'Hermione': 97, 'Draco': 73, 'Neville': 43 }

student_grades = {}

for student, score in student_scores.items():
    if score > 90:
        student_grades[student] = 'Outstanding'
    elif score > 80:
        student_grades[student] = 'Exceeds Expectations'
    elif score > 70:
        student_grades[student] = 'Acceptable'
    else:
        student_grades[student] = 'Fail'

print(student_grades)