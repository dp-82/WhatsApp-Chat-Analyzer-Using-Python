import re
import pandas
import matplotlib.pyplot as plt
import calendar


def findMostUsedWord():
    d = {}
    for i in words_list:
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

def findTopFiveUsers():
    d = []
    for i in df_user.iterrows():
        d.append([i[1][0], i[0]])
    d.sort(reverse=True)
    top5_names = []
    top5_no_of_msgs = []
    c = 0
    for i in d:
        if i[1] != 'N/A':
            top5_no_of_msgs.append(i[0])
            top5_names.append(i[1])
            c += 1
        if c == 5: break
    return top5_no_of_msgs,top5_names

# Here ex2 file contains our whatsapp Chat Data
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
words_list = []
day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
               'November', 'December'];
for i in l:
    a = i.strip().split(',')
    a1 = a[0]
    a2, a3, a4 = a[0].strip().split('/')
    a5 = day_names[calendar.weekday(int(a4), int(a2), int(a3))]
    a6 = a[1].strip().split('-')
    a7= a6[0].split(':')[0]
    c = a6[1].split(':')
    a8 = ''
    a9 = ''
    if len(c) >= 2 and 'changed' not in c[0]:
        a8 = c[0].strip()
        a9 = c[1]
    else:
        a8 = 'N/A'
        a9 = c[0]
    r = re.split(r'\W+', a9.lower())
    words_list.extend(r)
    a10 = len(a9)
    data.append([a1, a3, month_names[int(a2) - 1], '20' + a4, a5, a6[0], a7, a8, a9, a10])

df = pandas.DataFrame(data,
                      columns=['Date', 'Day', 'Month', 'Year', 'Day_Name', 'Time', 'Time_H', 'User', 'Message',
                               'MessageSize'])
print(df)

df_user = df.groupby(['User']).count()
df_user.plot.bar(y='Message', title='Number of Messages by Each User')
plt.show()

df_month = df.groupby(['Month']).count()
df_month.plot.bar(y='Message', title='Number of Messages in each Month')
plt.show()

df_timeh = df.groupby(['Time_H']).count()
df_timeh.plot.bar(y='Message', title='Number of Messages in each Hour')
plt.show()

df_year = df.groupby(['Year']).count()
df_year.plot.bar(y='Message', title='Number of Messages in each Year')
plt.show()

df_dayname = df.groupby(['Day_Name']).count()
df_dayname.plot.barh(y='Message', title='Number of Messages according to day_wise ')
plt.show()

print('Longest Message is:', df['MessageSize'].max(), 'characters')
muw, muwt = findMostUsedWord()
print('The Most Used Word is:' + muw + '-> used ' + str(muwt) + ' times')

# for top 5 users
top5=findTopFiveUsers()
plt.pie(top5[0], labels=top5[1])
plt.title('Top 5 Users')
plt.show()

'''
    2/8/00, 08:02 - Dharmaraju: hello
    a1=Whole Date as a String(ex:2/8/00)
    a2=Month(ex:2)
    a3=Day(ex:8)
    a4=Year(ex:00)
    a5=Day_Name(ex:Wednesday)
    a6[0]=Whole Time(ex->08:02)
    a7=Only Hour (ex:08)
    a8=UserName(ex:'Dharmaraju')
    a9=UserMessage(ex:'hello')
    a10=MessageSize(ex:5)
    words_list[]=It contains all words used in all messages
    l[]=It contains lines which follows the pattern
    data[]=contains list of values which is to be stored in df
    df=original dataframe
    df_user=dataframe grouped by user
    and so on
    '''