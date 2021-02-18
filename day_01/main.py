numbers = []

with open('./input.txt', 'r') as file:
    numbers = [int(number) for number in file.readlines()]

array_length = len(numbers)

for i in range(array_length):
    for j in range(array_length):
        for k in range(array_length):
            if numbers[i] + numbers[j] + numbers[k] == 2020:
                print(numbers[i] * numbers[j] * numbers[k])

