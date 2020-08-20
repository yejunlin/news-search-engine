from operator import itemgetter

f = open("data/res.csv", "r")

table = []
for line in f:
    col = line.split(',')
    table.append(col)

table_sorted = sorted(table, key=itemgetter(3), reverse=True)#对时间特征进行1.0偏重排序

for row in table_sorted:                    #遍历读取排序后的嵌套列表
    row = [str(x) for x in row]             #转换为字符串格式，好写入文本
    print(row[2])
f.close()