import boto3
import json
import string

s3 = boto3.client('s3')
max_labels = 10
min_confidence = 90
rekog = boto3.client('rekognition', region_name='us-east-1')


# analyze(path-to-image, description-of-product)
def analyze(img): 
	upload(img)
	current_catagory = ""
	current_conf = 0
	for label in detect_labels(img):
		#print("{Name} - {Confidence}%".format(**label))
		if do_mapping(label['Name']) != "empty" and label['Confidence'] > current_conf:
			current_catagory = do_mapping(label['Name'])
			current_conf = label['Confidence']
	#print("Conclusion " + current_catagory)
	return {"cat": current_catagory, "conf": current_conf}

def upload(img):
    documentKey = img
    bucketName = "bizhacks2020"
    outputName = documentKey
    s3.upload_file(documentKey, bucketName, outputName)

def detect_labels(img):
    response = rekog.detect_labels(
        Image = {
            "S3Object": {
                "Bucket": "bizhacks2020",
                "Name": img
            }
        }
    )
    MaxLabels = max_labels
    MinConfidence=min_confidence
    return response['Labels']

def do_mapping(str):
	if str == "Pc" or str == "Computer":
		return "Computers"
	elif str == "Cell Phone" or str == "Phone" or str == "Mobile Phone" or str == "Iphone":
		return "Phones"
	elif str == "Camera" or str == "Digital Camera":
		return "Cameras"
	elif str == "Headset" or str == "Headphones":
		return "Headphones"
	elif str == "Screen" or str == "Display" or str == "Monitor" or str == "LCD Screen":
		return "TVs"
	else:
		return "empty"