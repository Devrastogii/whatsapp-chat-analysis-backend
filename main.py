import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, request
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'], supports_credentials=True)

file_content_dict = {}

@app.route("/")
def hello_world():
    return "hi"

@app.route('/file-data', methods=['POST'])
def fileData():
    file = request.files['file']    
    file_content = file.read().decode('utf-8')

    # file_content_dict['file_content'] = file_content

    df = getData(file_content)
    words = countWords(df)
    msg = countMsg(df)
    
    return {'file':file_content, 'words': words, 'msg': msg}

def getData(file_content):

    # Data Processing

    date_pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    message = re.split(date_pattern, file_content)[6:]
    df = pd.DataFrame(data=message, columns=['Message'])

    df['Name'] = df['Message'].apply(lambda x: x.split(':')[0])
    df['Message'] = df['Message'].apply(lambda x: "".join(x.split(':')[1:]))
    df['Message'] = df['Message'].apply(lambda x: x.replace('\n', ''))

    dateTime = re.findall(date_pattern, file_content)[5:]

    df['Name'] = df['Name'].apply(lambda x: x.strip())
    df['Message'] = df['Message'].apply(lambda x: x.strip())
    
    df['DateTime'] = dateTime    
    df['Date'] = df['DateTime'].apply(lambda x: x.split(',')[0])
    df['Time'] = df['DateTime'].apply(lambda x: x.split(',')[1].replace('-', ''))
    df['Date'] = pd.to_datetime(df['Date'])

    df['Day'] = df['Date'].dt.day_name()
    df['Month'] = df['Date'].dt.month_name()
    df['Year'] = df['Date'].dt.year
    df['Date'] = df['Date'].dt.day

    df['Time'] = df['Time'].apply(lambda x: x.strip())    
    df['Time'] = pd.to_datetime(df['Time'])
    df['Hour'] = df['Time'].dt.hour
    df['Minute'] = df['Time'].dt.minute

    df = df[['Date', 'Day', 'Month', 'Year', 'Hour', 'Minute', 'Name', 'Message']]

    return df

def countWords(df):
    words = 0

    for i in df['Message']:
        words += len(i)

    return words

def countMsg(df):
    return df.shape[0]


app.run(debug=True)