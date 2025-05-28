D = {'0': 'ноль', '1': 'один', '2': 'два', '3': 'три', '4': 'четыре', '5': 'пять', '6': 'шесть', '7': 'семь', '8': 'восемь', '9': 'девять'}
nums = []
with open('1lab.txt') as f:
    while (line := f.readline()):
        for n in line.split():
            if len(n) > 1 and n[-2] == '3' and all(c in '0123' for c in n) and int(n, 4) <= 1023 and int(n[-1]) % 2:
                if (filtered := n.replace('3', '')):
                    nums.append(filtered)
if nums:
    avg = (min(int(n, 4) for n in nums) + max(int(n, 4) for n in nums)) // 2
    print(*nums, '\nСреднее:', ' '.join(D[d] for d in str(avg)))
