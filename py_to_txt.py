import os

path = "."
# for root, d_names, f_names in os.walk(path):
#     print(root, d_names, f_names)

exclude = set(['venv', '.idea', '.venv', 'dist'])
lst = []
for root, d_names, f_names in os.walk(path):
    d_names[:] = [d for d in d_names if d not in exclude]
    if len(d_names) != 0:
        for i in range(len(f_names)):
            if os.path.splitext(f_names[i])[1] == '.py':
                lst.append(os.path.join(root, f_names[i]))
print(lst)

with open('AllCode.txt', 'w+', encoding="UTF-8") as fw:
    for i in lst:
        with open(i, 'r', encoding="UTF-8") as fr:
            name = i.replace('.\\', '').replace('\\', '/')
            fw.write('-' * 5 + f' {name} ' + '-' * 5)
            fw.write('\n')
            arr = fr.read().split('\n')
            s = ''
            for i in arr:
                if '#' not in i:
                    s += i + '\n'
            fw.write(s)
            fw.write('\n')
