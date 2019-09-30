import re
import pandas
import matplotlib.pyplot as plt
import calendar


def findMostUsedWord(l):
    d = {}
    for i in l:
        if i in d.keys():
            d[i] = d[i] + 1
        elif i.isalpha():
            d[i] = 1
    max = 0
    key = ''
    for k, v in d.items():
        if v > max:
            max = v
            key = k
    return key.capitalize(), max

#Here ex2 file contains our whatsapp Chat Data
f = open('ex2.txt', encoding='utf8')
l = []
ind = -1
for i in f:
    s = i.rstrip('\n')
    r = re.match(r'[\d]{1,2}/[\d]{1,2}/[\d]{2}, [\d]{2}:[\d]{2} -', s)
    if r:
        l.append(s)
        ind = ind + 1
    else:
        l[ind] = l[ind] + s

f.close()

data = []
li = []
day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
for i in l:
    a = i.strip().split(',')
    a1 = a[0]
    a2, a3, a4 = a[0].strip().split('/')
    a5 = day_names[calendar.weekday(int(a4), int(a2), int(a3))]
    a6 = a[1].strip().split('-')
    a7, a8 = a6[0].split(':')
    c = a6[1].split(':')
    a9 = ''
    a10 = ''
    if len(c) >= 2 and 'changed' not in c[0]:
        a9 = c[0]
        a10 = c[1]
    else:
        a9 = 'N/A'
        a10 = c[0]
    r = re.split(r'\W+', a10.lower())
    li.extend(r)
    a11 = len(a10)
    # appending to data list for dataframe
    data.append([a1, a3, a2, a4, a5, a6, a7, a8, a9, a10, a11])

df = pandas.DataFrame(data,
                      columns=['Date', 'Day', 'Month', 'Year', 'Day_Name', 'Time', 'TimeH', 'TimeM', 'User', 'Message',
                               'MessageSize'])
print(df)

d = df.groupby(['User']).count()
#print(d)
d.plot.bar(y='Message', title='Number of Messages by Each User')
d1 = df.groupby(['Month']).count()
d1.plot.bar(y='Message', title='Number of Messages in each Month')

d2 = df.groupby(['TimeH']).count()
d2.plot.bar(y='Message', title='Number of Messages in each Hour')
#print(d2)
d3 = df.groupby(['Year']).count()
d3.plot.bar(y='Message', title='Number of Messages in each Year')

d4 = df.groupby(['Day_Name']).count()
d4.plot.barh(y='Message', title='Number of Messages according to day_wise ')

print('Longest Message is:', df['MessageSize'].max(), 'characters')
muw, muwt = findMostUsedWord(li)
print('The Most Used Word is:' + muw + '-> used ' + str(muwt) + ' times')
plt.show()