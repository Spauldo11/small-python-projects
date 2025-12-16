def binary_search(start, end, arr, target):
    while start <= end:
        mid = start + (end - start) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] > target:
            end = mid - 1
        else:
            start = mid + 1
arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 23, 25, 26, 34, 456, 56534]
x = 23
ans = binary_search(0, len(arr) - 1, arr, x)
print(ans)