numbers = None
answers = None

with open("test_numbers.leo") as file:
    numbers = file.readlines()

with open("test_number_answers.txt") as file:
    answers = file.readlines()

for i in range(len(numbers)):
    print(numbers[i], answers[i])

print(numbers, answers)
print("Done")