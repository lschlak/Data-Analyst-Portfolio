
########################################################################################################
# Code to Extract Tables from PDFs Using AWS Textract + the AWS Python SDK
# Luke Schlake
# May 2024
#########################################################################################################

from textractor.visualizers.entitylist import EntityList
from textractor.data.constants import TextractFeatures, Direction, DirectionalFinderType
import boto3
from trp import Document
from botocore.config import Config
from textractprettyprinter.t_pretty_print import convert_table_to_list
import os
import pandas as pd
import json
import numpy as np
from textractprettyprinter import get_layout_csv_from_trp2
import csv
from trp.trp2 import TDocument, TDocumentSchema

directory = "Define input directory here"
output = "Define output directory here"

# Initialize Amazon Textract client
textract = boto3.client('textract')

for filename in os.listdir(directory):
    try:
        f = os.path.join(directory, filename)
        print(f)
        if os.path.isfile(f):
            # Call Amazon Textract
            with open(f, "rb") as document:
                response = textract.analyze_document(
                    Document={
                        'Bytes': document.read(),
                    },
                    FeatureTypes=["TABLES","LAYOUT"]
                )
            doc = Document(response)
        
            #RETURNS THE TABLE 

            #Added the ticker = 1 AND the ticker = ticker +1 

            for page in doc.pages:
                # Print tables
                ticker = 1
                filename = filename[:-3]
                for table in page.tables:
                    dfs = list()
                    dfs.append(pd.DataFrame(convert_table_to_list(trp_table=table)))
                    data = dfs[0]
                    file_path = output +"\\" + filename + "Table" + str(ticker)+ ".csv"
                    ticker= ticker +1
                    data.to_csv(file_path)

            #RETURNS THE LAYOUT
            filename_csv = filename +"csv"

            #Save the json:
            with open(filename, "w") as outfile: 
                json.dump(response, outfile)

            #Open it and read it to create the data:
            with open(filename) as input_fp:
                trp2_doc: TDocument = TDocumentSchema().load(json.load(input_fp))
                layout_csv = get_layout_csv_from_trp2(trp2_doc)

            with open(filename_csv, 'w', newline='') as file:
                writer = csv.writer(file)
                for page in layout_csv:
                    writer.writerows(page)

            f = filename_csv
            df = pd.read_csv(f, encoding='unicode_escape')
            df1 = df.iloc[:, [1, 2]].T
            df1['file'] = filename
            file_path2 =  output +"\\" + filename + "Layout" + ".csv"
            df1.to_csv(file_path2)
            
        else: 
            print("no")
    except Exception as error:
        print("Error:", error)