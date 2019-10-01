import re
import pandas
import matplotlib.pyplot as plt


def barChart(xValues, yValues, bTitle, xLable, yLable):
    plt.bar(xValues, yValues)
    plt.title(bTitle)
    plt.xlabel(xLable)
    plt.ylabel(yLable)
    plt.show()


def pieChart(pValues, pLables, pTitle):
    plt.pie(pValues, labels=pLables)
    plt.title(pTitle)
    plt.show()


def tableChart(row_lables, col_lables, data, location='center'):
    plt.table(rowLabels=row_lables, colLabels=col_lables, cellText=data, loc=location)
    plt.show()


def checkAndInsertIntoDict(dict_name, key):
    if key in dict_name.keys():
        dict_name[key] = dict_name[key] + 1
    else:
        dict_name[key] = 1


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

datedict = {}
timedict = {'00': 0, '01': 0, '02': 0, '03': 0, '04': 0, '05': 0, '06': 0, '07': 0, '08': 0, '09': 0, '10': 0, '11': 0,
            '12': 0, '13': 0, '14': 0, '15': 0, '16': 0, '17': 0, '18': 0, '19': 0, '20': 0, '21': 0, '22': 0, '23': 0}
userdict = {}
yeardict = {}
monthdict = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, '10': 0, '11': 0, '12': 0}

data = []
for i in l:
    a = i.strip().split(',')
    b = a[1].strip().split('-')
    c = b[1].strip().split(':')
    y = a[0].split('/')
    # year
    checkAndInsertIntoDict(yeardict, y[2].strip())
    # month
    checkAndInsertIntoDict(monthdict, y[0].strip())
    # date
    checkAndInsertIntoDict(datedict, a[0].strip())
    # for time
    checkAndInsertIntoDict(timedict, b[0].split(':')[0])

    str_user_name = ''
    msg = ''
    # for finding username
    if len(c) >= 2:
        str_user_name = c[0]
        msg = c[1]
    else:
        str_user_name = 'N/A'
        msg = c[0]
    # appending to data list for dataframe
    data.append([a[0], b[0], str_user_name, msg])
    # for userdictionary
    checkAndInsertIntoDict(userdict, str_user_name)

df = pandas.DataFrame(data, columns=['Date', 'Time', 'User', 'Message'])
print(df)

# bar chart for time vs number of messages
barChart(timedict.keys(), timedict.values(), 'Time Vs NumberOfMessages', 'Time', 'Number Of Messages')
# bar chart for date vs number of messages
barChart(datedict.keys(), datedict.values(), 'Date Vs NumberOfMessages', 'Date', 'Number Of Messages')
# pie chart for top 5 users
udk = list(userdict.keys())
for i in range(len(udk)):
    for j in range(i + 1, len(udk)):
        if userdict[udk[i]] < userdict[udk[j]]:
            udk[i], udk[j] = udk[j], udk[i]
udk.append('N/A')
udk.remove('N/A')
udv = []
for i in range(5):
    udv.append(userdict[udk[i]])

pieChart(udv, udk[:5], 'Top 5 Users')
# plotting tables for users vs number of messages
table_data = []
for k, v in userdict.items():
    table_data.append([k, v])
tableChart(list(range(len(userdict))), ['User', 'NumberOfMessages'], table_data, 'center')
# year vs number of messages
barChart(yeardict.keys(), yeardict.values(), 'Year Vs NumberOfMessages', 'Year', 'Number Of Messages')
# month vs number of messages in all years
barChart(monthdict.keys(), monthdict.values(), 'Month vs NumberOfMessages In All Years', 'Month', 'Number Of Messages')
