people = int(input("How many ways are you splitting the cost of this hangout?"))
places = int(input("How many places are you going to spend moneya at during your hangout?"))
total_bill = 0

for i in range(1, places+1):
    add = int(input("How much did you spend at place #" + str(i)) + ' ')
    total_bill += add

split_bill = total_bill / people
print("Each person will have to pay $" + str(split_bill))