import os
import boto3
# os.environ['AWS_DEFAULT_REGION'] = 'eu-central-1'

# Document
documentName = "a.jpg"

# Read document content
with open(documentName, 'rb') as document:
    imageBytes = bytearray(document.read())

# Amazon Textract client
textract = boto3.client('textract', region_name='eu-west-1')

# Call Amazon Textract
response = textract.detect_document_text(Document={'Bytes': imageBytes})

#print(response)

detected_lines = []
# Print detected text
for item in response["Blocks"]:
    if item["BlockType"] == "LINE":
        loc_variable = '\033[94m' + item["Text"] + '\033[0m'
        print(loc_variable)
        detected_lines.append(loc_variable)
        
print(len(detected_lines))
