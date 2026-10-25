import os


def validate_score(score, maximum, label):
    if score < 0:
        raise ValueError(f"{label} score cannot be negative.")
    if score > maximum:
        raise ValueError(f"{label} score cannot be greater than {maximum}.")
    return score


def calculate_final(assignment1, assignment2, exam):
    assignment_part = (assignment1 + assignment2) / 100 * 25
    exam_part = exam / 100 * 75
    return assignment_part + exam_part


def get_grade(final_score):
    if final_score > 90:
        return "A+(Outstanding)"
    elif final_score > 80:
        return "A(Very Good)"
    elif final_score >= 70:
        return "B(Good)"
    else:
        return "Fail"


def save_report(name, assignment1, assignment2, exam, final_score, grade):
    folder = "GradeScores"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{name}.txt")

    with open(path, "w") as file:
        file.write("***Report Card***\n")
        file.write("***Course name: Python for Beginners***\n")
        file.write("=" * 50 + "\n")
        file.write(f" Student Name: {name}\n")
        file.write(f" Assignment-1 Score:{assignment1}\n")
        file.write(f"Assignment-2 Score:{assignment2}\n")
        file.write(f"Exam Score:{exam}\n")
        file.write(f"Final score:{final_score}\n")
        file.write(f"Grade/Remark: {grade}\n")

    return path


try:
    name = input("Enter the student's name: ")
    assignment1 = validate_score(float(input("Assignment-1 score: ")), 50, "Assignment1")
    assignment2 = validate_score(float(input("Assignment-2 score: ")), 50, "Assignment2")
    exam = validate_score(float(input("Exam score: ")), 100, "Final exam")
except ValueError as error:
    print("Error:", error)
    print("Provide the correct input next time!")
else:
    final_score = calculate_final(assignment1, assignment2, exam)
    grade = get_grade(final_score)
    print("Final score:", final_score)
    print("Grade:", grade)

    path = save_report(name, assignment1, assignment2, exam, final_score, grade)
    print("The current working directory:")
    print(os.getcwd())
    print("Get the report card at:")
    print(os.path.join(os.getcwd(), path))