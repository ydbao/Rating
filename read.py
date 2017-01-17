f1 = open('xxx.txt', 'r')
f2 = open('new_ratings.txt', 'r')
f3 = open('imgname.txt', 'r')
f4 = open('predict_ratings.txt', 'w')

l1 = []
for s in f1.readlines():
    import re
    mark = re.findall(r"0\.\d+", s)
    if len(mark) != 0 :
        i = float(mark[-1]) * 100
        l1.append(i)
    else:
        l1.append(0)

l2= []
for s in f2.readlines():
    l2.append(s)

count = 0
l3 = []
for s in f3.readlines():
    if len(l1) >= count:
        if l1[count] != 0:
            n = abs(int(l1[count]) - int(l2[count]))
            l3.append(n)
            f4.writelines(s + '   difference : '+ str(n) + '   xiaobing : ' + str(l2[count]) + '    huazhong : ' + str(l1[count]) + '\n')
    count += 1

f1.close()
f2.close()
f3.close()
f4.close()

l5 = 0
l10 = 0
l15 = 0
l20 = 0
l25 = 0
l30 = 0
l40 = 0
print(len(l3))
for m in l3:
    if m <= 5:
        l5 += 1
    if m <= 10:
        l10 += 1
    if m <= 15:
        l15 += 1
    if m <= 20:
        l20 += 1
    if m <= 25:
        l25 += 1
    if m <= 30:
        l30 += 1
    if m > 30:
        l40 += 1

print(l5)
print(l10)
print(l15)
print(l20)
print(l25)
print(l30)
print(l40)