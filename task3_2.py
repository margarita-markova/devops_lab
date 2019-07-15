def is_dividing_number(num):
    n = num
    while n > 0:
        d = n % 10
        if (d == 0) or (num % d != 0):
            return False
        n = n // 10
    return True


def create_list(left, right):
    result = []
    for num in range(left, right + 1):
        if is_dividing_number(num):
            result.append(num)
    return result


if __name__ == '__main__':
    left = 0
    right = 0
    while (1 >= left >= right) or (right >= 10000):
        left = int(input())
        right = int(input())
    print(create_list(left, right))
