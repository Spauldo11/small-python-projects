import numpy as np
arr1 = [[1, 2], [1, 3]]
arr2 = [21, 26]
arr3 = np.linalg.inv(arr1) * arr2
print(np.linalg.inv(arr1))
for i in range(len(arr3)):
    print(arr3[i])