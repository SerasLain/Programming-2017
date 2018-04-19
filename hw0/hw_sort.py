def find_max():
    arr = list(map(int, input().strip().split(' ')))
    print(arr)
    max_1 = 0
    max_2 = 0
    max_3 = 0
    for i in range(len(arr)):
        if arr[i] > max_1:
            max_1 = arr[i]
            continue
        if arr[i] <= max_1 & arr[i] > max_2:
            max_2 = arr[i]
            continue
        if arr[i] <= max_2 & arr[i] > max_3:
            max_3 = arr[i]
            continue
            print(max_1, max_2, max_3)
    return max_1, max_2, max_3

def main():
    print(find_max())

if __name__ == "__main__":
    main()
