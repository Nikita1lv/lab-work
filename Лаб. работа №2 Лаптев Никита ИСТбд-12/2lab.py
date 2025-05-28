import re
D = {'0': 'ноль', '1': 'один', '2': 'два', '3': 'три', '4': 'четыре', '5': 'пять', '6': 'шесть', '7': 'семь', '8': 'восемь', '9': 'девять'}
nums = []

with open('1lab.txt') as f:
    pattern = re.compile(r'^[0123]+3[0123]$')
    while (line := f.readline()):
        for n in line.split():
            if not all(c in '0123' for c in n):
                continue
            if pattern.match(n) and int(n, 4) <= 1023:
                if (filtered := n.replace('3', '')):
                 if filtered and not all(c == '0' for c in filtered):
                    nums.append(filtered)
if nums:
    avg = (min(int(n, 4) for n in nums) + max(int(n, 4) for n in nums)) // 2
    print(*nums, '\nСреднее:', ' '.join(D[d] for d in str(avg)))
