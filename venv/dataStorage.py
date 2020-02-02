import os

def writeData(o):
    try:
        logFile = a'.Uploads/csv.csv'

        csvFile = open(logFile, 'w')

        csvFile.write(str(o))

    except Exception as e:
        print(e)
    finally:
        csvFile.close()
