import collections

if __name__ == '__main__':
    n = int(input())
    in_list = []
    while len(in_list) < n:
        i = int(input())
        if 0 <= i <= 100:
            in_list.append(i)

    a = collections.Counter(in_list).most_common(1)
    print('The most frequently element: ')
    print(a[0][0])
