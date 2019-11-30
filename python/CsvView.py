import csv, datetime, pytz


def writeCsv(targetList, uniqueString):
    # utf_8_sigにしないとExcelで化ける
    with open(makePathToDirectory() + makeName(uniqueString), 'w', encoding='utf_8_sig') as f:
        writer = csv.writer(f)

        for line in targetList:
            writer.writerow(line)


def makeName(uniqueString):
    now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

    date = [now.year, now.month, now.day, now.hour, now.minute]
    dateStr = ''

    for el in date:
        dateStr += str(el) + '_'

    fileName = dateStr + uniqueString + '.csv'

    return fileName


def makePathToDirectory():
    path = "exportCsv/"
    return path