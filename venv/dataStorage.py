import os

def writeData(o):
    try:
        logFile = r'.Uploads/csv.csv'

        csvFile = open(logFile, 'a')

        csvFile.write(str(o))

    except Exception as e:
        print(e)
    finally:
        csvFile.close()
