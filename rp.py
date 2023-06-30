import csv
# from underthesea import word_tokenize
path = 'E:\\code\python\chatbot\PDT-Chatbot\chatapp\data\\raw_data\\tuyen_sinh'
name = 'tuyen_sinh'

Q = []
A = []
I = []

# a = open('E:\code\python\chatbot\\abcd.txt', "r")
# s = a.read()
# print(s)

count = []
for i in range(21):
    count.append(0)

for i in range(61):
    num = '0' if i < 10 else ''
    f = open(path + '\\' + name + num + str(i) + '.txt', "r", encoding='utf-8')
    QAI = f.read()
    string = QAI.split('#')
    Q.append(string[0])
    A.append(string[1])
    I.append(int(string[2]))
    count[int(string[2]) - 1] += 1

print(len(I))

for i in range(len(count)):
    print(f'{i+1}: {count[i]}')

with open('QAI.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Q", "A", "I"])

    for i in range(len(I)):
        writer.writerow([Q[i], A[i], I[i]])

file.close()


# print(Q)
# print(A)
# print(I)
