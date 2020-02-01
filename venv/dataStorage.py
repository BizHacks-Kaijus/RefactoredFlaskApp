import os

def writeData(o):
    try:
        logFile = r'C:/Users/chess/OneDrive/Documents/Ben/Projects/BizHacks/Flask/venv/Uploads/csv.txt'

        csvFile = open(logFile, 'w')

        csvFile.write(str(o))

    except Exception as e:
        csvFile.write("Error.")
        print(e)
    finally:
        csvFile.close()
