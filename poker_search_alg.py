num_list = [3, 5, 4, 3, 1, 6, 7] # sorted: [3, 3, 4, 5, 6, 6, 7]
suit_list = ['S', 'S', 'S', 'S', 'S', 'D', 'C'] # sorted: [d, h, s, s, s, s, s]
pairs = []
triples = []
flushes = []
straights = []
straight_flushes = []
quartets = []

def binary_search(start, end, arr, target):
    while start <= end:
        mid = start + (end - start) // 2
        if arr[mid] == target:
            return arr[mid]
        elif arr[mid] > target:
            end = mid - 1
        else:
            start = mid + 1

def check_fours(arr):
    index = 0
    while index <= 3:
        count = 0
        for i in range(index+1, len(arr)):
            if arr[i] == arr[i-1]:
                count+=1
            else:
                break
            if count == 3:
                if arr[index] == 1:
                    quartets.append(14)
                else:
                    quartets.append(arr[index])
        index+=1
    return len(quartets)

def check_straight(arr):
    index = 0
    while index <= 2:
        count = 0
        for i in range(index+1, len(arr)):
            if arr[i-1] == 1:
                arr[i-1] = 14
                arr.sort()
                break
            if arr[i]-1 == arr[i-1]:
                count+=1
            else:
                break
            if count == 4:
                straights.append(arr[index])
                straight_flushes.append(suit_list[index])
        index+=1
    return len(straights)

def check_flush(arr):
    index = 0
    while index <= 2:
        count = 0
        for i in range(index+1, len(arr)):
            if arr[i] == arr[i-1]:
                count+=1
            else:
                break
            if count >= 4:
                flushes.append(arr[index])
        index+=1
    return len(flushes)

def check_triple(arr):
    index = 0
    while index <= 4:
        count = 0
        for i in range(index+1, len(arr)):
            if arr[i] == arr[i-1]:
                count+=1
            else:
                break
            if count == 2:
                if arr[index] == 1:
                    triples.append(14)
                else:
                    triples.append(arr[index])
        index+=1
    return len(triples)

def check_pairs(arr):
# Use for loop and nested binary search to search for pairs within the array. O(nlog(n)) time complexity.
    for i in range(len(arr)-1):
        target = arr[i]
        low = i+1
        high = len(arr)-1
        if not binary_search(low, high, arr, target) == 1:
            pairs.append(binary_search(low, high, arr, target))
        else:
            pairs.append(14)
    return len(pairs)

print(f"These are your cards and the community cards: ")
for i in range(len(num_list)):
    print(f"{num_list[i]} of {suit_list[i]}", end=", ")
    if i == len(num_list)-1:
        print('')

num_list.sort()
suit_list.sort()

four_of_kind = check_fours(num_list)
straight = check_straight(num_list)
flush = check_flush(suit_list)
three_of_kind = check_triple(num_list)
doubles = check_pairs(num_list)

if four_of_kind > 0:
    print(f"The best is a four of a kind of {quartets[four_of_kind-1]}\'s")
elif straight > 0:
    for i in range(1, 5):
        straights.append(straights[straight-1]+i)
    straight_flush = check_flush(straights)
    if straight_flush > 0:
        print(f"The best is a straight flush from {straights[straight-1]} to {straights[straight+3]} of the suit {straight_flushes[0]}")
        if straights[straight-1] == 10:
            print(f"Congrats! it\'s a royal flush of the suit {straight_flushes[0]}. That is the rarest hand in all of poker!")
    else:
        print(f"The best is a straight from {straights[straight-1]} to {straights[straight+3]}")
elif flush > 0:
    print(f"You have a flush of the suit {flushes[0]}")
elif three_of_kind > 0:
    print(f"The best is three of a kind of {triples[three_of_kind-1]}\'s")
elif doubles > 0 and pairs[0]:
    if doubles > 1:
        print(f" The best is two-pair of {pairs[doubles-1]}\'s and {pairs[doubles-2]}\'s")
    else:
        print(f"The best is a pair of {pairs[doubles-1]}\'s", end="")
else:
    print(f"Your best is a high card: {num_list[len(num_list)-1]}")