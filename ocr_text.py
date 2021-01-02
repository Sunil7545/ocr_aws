import os
import boto3
import itertools
import argparse
import tempfile
import numpy as np
import matplotlib.image as mpimg

def extract_text(file_name):

    # configure S3

    # s3 = boto3.resource('s3', region_name='eu-west-1')
    # bucket = s3.Bucket(file_name)
    # object = bucket.Object('a.jpg')
    # tmp = tempfile.NamedTemporaryFile()
    # print(tmp.name)
    # Read document content
    with open(file_name, 'rb') as document:
        image_bytes = bytearray(document.read())

    # Amazon Textract client
    print(np.array(image_bytes).shape)
    text_extract = boto3.client('textract', region_name='eu-west-1')

    # Call Amazon Text-ract
    response = text_extract.detect_document_text(Document={'Bytes': image_bytes})

    detected_lines = []
    # Print detected text
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            # loc_variable = '\033[94m' + item["Text"] + '\033[0m'
            loc_variable = item["Text"].split(" ")
            # print(loc_variable)
            detected_lines.append(loc_variable)

    detected_lines = list(itertools.chain(*detected_lines))
    # print(detected_lines)
    return detected_lines


# Document
# document_name = "a.jpg"
# input folder name, which has data
parser = argparse.ArgumentParser()
parser.add_argument("image", help="select the input image for text extraction", type=str)
parser.add_argument("key_word", help="to check in the document", type=str)
args = parser.parse_args()
document_name = args.image
key_name = args.key_word
text_extracted = extract_text(document_name)
s3 = boto3.resource('s3', region_name='eu-west-1')
# s3 = boto3.client('s3')
bucket = s3.Bucket('textract-data-sky')
object = bucket.Object('a.jpg')
tmp = tempfile.NamedTemporaryFile()
with open(tmp.name, 'wb') as f:
    object.download_fileobj(f)
    img = mpimg.imread(tmp.name)
    # img = bytearray(f.read())
    print(np.array(img).shape)
print(text_extracted.count(key_name))



