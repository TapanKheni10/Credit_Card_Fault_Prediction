from pymongo.mongo_client import MongoClient
import pandas as pd 
import os
import json

## uniform resource indentifier
url = f"mongodb+srv://tapankheni:tapankheni@cluster0.blfohxj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

## create a connection to the MongoDB
client = MongoClient(url)

## send a ping to the server to confirm the connection
try:
    client.admin.command('ping')
    print('MongoDB connection: You are successfully connected to the MongoDB!')
except Exception as e:
    print(e)

## create a database and a collection
DATABASE_NAME = 'credit_card_fault_detection'
COLLECTION_NAME = ['fraudulent_transactions_data', 'default_credit_card_data']

file_paths = ["/Users/tapankheni/Data_Science/Data Science Projects/Credit_Card_Fault_Prediction/data/creditcard_2023.csv",
              "/Users/tapankheni/Data_Science/Data Science Projects/Credit_Card_Fault_Prediction/data/UCI_Credit_Card.csv"]

for i in range(2):

    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME[i]]
    
    data = pd.read_csv(file_paths[i])
    data.drop(columns=[data.columns[0]], axis=1, inplace=True)
    
    data_dict = data.to_dict(orient='records')

    collection.insert_many(data_dict)
    
    print(f"Data inserted into the collection: {COLLECTION_NAME[i]}")
    
client.close()
