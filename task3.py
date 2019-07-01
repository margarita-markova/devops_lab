def isDividingNumber(num):
    n = num
    while n > 0:
        d = n % 10
        if (d == 0) or (num % d != 0):
            return False
        n = n // 10
    return True


if __name__ == '__main__':
    left = 0
    right = 0
    while (1 >= left >= right) or (right >= 10000):
        left = int(input())
        right = int(input())
    result = []
    for num in range(left, right + 1):
        if isDividingNumber(num):
            result.append(num)
    print(result)
