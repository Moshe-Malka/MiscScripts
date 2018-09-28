#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Native Imports
from datetime import datetime
from time import sleep
import sys
import os
import re
import random
# 3rd Party  Imports
try:
    from openpyxl import load_workbook
    import pandas as pd
    import mysql.connector as mc
    import progressbar
except ImportError as ie:
    print ie
    print "#"*80    
    print "Need to install packages:"
    print "pip install mysql-connector-python"
    print "pip install openpyxl"
    print "pip install pandas"
    print "pip install progressbar"
    print "#"*80
    sys.exit(1)

def getStoreName(store_id):
    # Setting up connection to aurora DB.
    try:
        cnx = mc.connect(user='mmalka', password='MosheIsTheUFCChampion', host='reader-db.wiser.com', database='wp_data_prod')
    except Exception as e:
        print "Error connecting to DB"
        print e
    query = """ select s.store_name 
                from stores as s
                where s.id = {0}
            """.format(store_id)
    try:
        df = pd.read_sql(query, cnx)
        if df.empty:
            print "One of the DataFrames is empty (query result is empty). storeID {} - exiting program...".format(store_id)
            sys.exit(1)
        cnx.close()
        return str(df.iat[0, 0])
    except Exception as e:
        print "Error running query"
        print e
        sys.exit(1)

def getData(store_id):
    print "✓ Started Query for store number: {0} <{1}>".format(store_id, datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    try:
        cnx = mc.connect(user='mmalka', password='MosheIsTheUFCChampion', host='reader-db.wiser.com', database='wp_data_prod')
    except Exception as e:
        print "Error connecting to DB"
        print e
    query = """       
        SELECT
                p.url "url",
                p.last_update "extraction_date",              
                pps.sku "sku",
                pps.name "product_name",
                prod.upc "upc",
                prod.mpn "mpn",              
                s.store_name "competitor_name",
                s.store_url "source_url",
                p.source "source"
        FROM pricing p
        JOIN products_per_store as pps ON pps.product_id = p.product_id
        JOIN stores as s ON s.id = p.store_id
        JOIN products as prod ON prod.id = p.product_id
        JOIN compete_settings as cs ON cs.store_id = pps.store_id AND cs.compete_id = p.store_id
        WHERE pps.store_id = {0}
            AND cs.enabled = 1
        ORDER BY p.product_id, s.store_name
        ;
    """.format(store_id)
    try:
        df = pd.read_sql(query, cnx)
        print "✓ Finished Query for store number: {0} <{1}>".format(store_id, datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        if df.empty:
            print "One of the DataFrames is empty (query result is empty). storeID {} - exiting program...".format(store_id)
            sys.exit(1)
        cnx.close()
        return df
    except Exception as e:
        print "Error running query"
        print e
        sys.exit(1)

def parseSource(source):
    try:
        sourceMapping = { 8: 'SM', 24: 'PHP Legacy', 2: 'Google Shopping', 5: 'Amazon', 25: 'PHPH Legacy', 9: "M2" }
        val = sourceMapping[source]
        return val
    except KeyError as ke:
        # print "Parsing Source Error : " + ke
        return source
     
def createDirectory(storeNamesPath):
    try:    # add directory handeling for each report.        
        if not os.path.isdir(getBasePath() + '/' + storeNamesPath):
            os.makedirs(getBasePath() + '/' + storeNamesPath)
            print "✓ Created directory for output: {0}".format(getBasePath() + '/' + storeNamesPath)
    except OSError as ose:
        print "Error while trying to create directory:"
        print ose
        sys.exit(1)

def handleArgs(args):    
    if len(args) != 2:
        print "Error: not enough arguments (2) !"
        print "Usage: python v3-report.py <old store id> <new store id>"
        sys.exit(1)
    try:
        for arg in args:
            assert arg.isdigit()
        return args
    except Exception as e:
        print e
        print "Error: argument is not a number"
        sys.exit(1)

def getOutputFileName(path):
    return "{0}/{1}/CompetitorReport-{2}.xlsx".format(getBasePath(), path, datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))

def getBasePath():
    return os.path.dirname(os.path.abspath(__file__))

def getStoreNamesPath(args):
    return re.sub(r'\s', '-' , '_'.join([getStoreName(x) for x in args]))

def saveDataToExcel(args, mainOutputDF, diffDF, statsDF):
    storeNamesPath = getStoreNamesPath(args)           #re.sub(r'\s', '-' , '_'.join([getStoreName(x) for x in args]))
    writer = pd.ExcelWriter(path= getOutputFileName(storeNamesPath) , engine='openpyxl')
    
    if not mainOutputDF.empty:
        try:
            mainOutputDF.to_excel(writer, sheet_name='M2 Grater Then M1', index=False)
            print "✓ Finished Writing 'M2 gt M1' <{0}>".format(startTime.strftime('%Y-%m-%d_%H-%M-%S'))
        except Exception as mainException:
            print "Failed to write 'M2 Grater Then M1' to excel"
            print mainException
    
    if not diffDF.empty:
        try:
            diffDF.to_excel(writer, sheet_name='Difference', index=False)
            print "✓ Finished Writing 'Difference' <{0}>".format(startTime.strftime('%Y-%m-%d_%H-%M-%S'))
        except Exception as diffException:
            print "Failed to write 'Difference' to excel"
            print diffException 

    if not statsDF.empty:
        try:
            statsDF.to_excel(writer, sheet_name='Statistics', index=False)
            print "✓ Finished Writing 'Statistics' <{0}>".format(startTime.strftime('%Y-%m-%d_%H-%M-%S'))
        except Exception as statException:
            print "Failed to write 'Statistics' to excel"
            print statException    

    try:
        writer.save()
    except Exception as e:
        print "Error saving file : {0}".format(e)
        sys.exit(1)

if __name__ == '__main__':
    reload(sys)  
    sys.setdefaultencoding('utf8')
    startTime = datetime.now()
    print "✓ Started Main <{0}>".format(startTime.strftime('%Y-%m-%d_%H-%M-%S'))    
    bar = progressbar.ProgressBar(maxval=100, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

    # args = handleArgs(sys.argv[1:])

    ################### Keep For Testing Porpuses #############################
    args = ['1198893219', '1201711444']

    createDirectory(getStoreNamesPath(args))

    old_df = getData(str(args[0]))
    new_df = getData(str(args[1]))

    old_store_skus = [str(x) for x in list(old_df.sku.unique())]
    new_store_skus = [str(x) for x in list(new_df.sku.unique())]

    # Initializing DF's
    mainOutputDF = pd.DataFrame(columns=
                    ["Product_Name", "SKU", "MPN", "UPC", "Competitors Count {0}".format(str(args[0])),
                    "Competitors Count {0}".format(str(args[1])),
                    "Difference","Sellers", "Source", "Source_URL", "URL", "Extraction_Date"])
    diffDF = pd.DataFrame(columns=
                    ["Product_Name", "SKU", "MPN", "UPC", "Competitors Count {0}".format(str(args[0])),
                    "Competitors Count {0}".format(str(args[1])),
                    "Difference","Sellers", "Source", "Source_URL", "URL", "Extraction_Date"])
    statsDF = pd.DataFrame(columns= ["Store", "Total Skus", "Total Competitores"] )
    
    newStoreCompCount = 0
    oldStoreCompCount = 0

    start = 1
    bar.start()
    sleep(2)
    for sku in old_store_skus:
        current =  ( start / float(len(old_store_skus)) )* 100
        bar.update( current )
        start += 1
        
        newStoreComps = list(new_df.loc[new_df['sku'] == sku].competitor_name)
        oldStoreComps = list(old_df.loc[old_df['sku'] == sku].competitor_name)
         
        newStoreCompCount += len(newStoreComps)
        oldStoreCompCount += len(oldStoreComps)

        diff = [x.encode('utf-8') for x in oldStoreComps if x not in newStoreComps]
        if len(diff) > 0:        # there are competitors that are in the old store BUT not on the new store.   
            # print diff
            firstRowDiff = True
            for comp in diff:
                diffdata = old_df.loc[(old_df['sku'] == sku) & (old_df['competitor_name'] == comp)]
                mainOutputDF = mainOutputDF.append({
                                "Product_Name": str(diffdata.product_name.values[0].encode('utf-8')) if firstRowDiff else None,
                                "SKU": sku if firstRowDiff else None,
                                "MPN": str(diffdata.mpn.values[0]) if firstRowDiff else None,
                                "UPC": str(diffdata.upc.values[0]) if firstRowDiff else None,
                                "Competitors Count {0}".format(args[0]): len(oldStoreComps) if firstRowDiff else None,
                                "Competitors Count {0}".format(args[1]): len(newStoreComps) if firstRowDiff else None,
                                "Difference": len(diff) if firstRowDiff else None,
                                "Sellers": comp.replace('*','').encode('utf-8'),
                                "Source": parseSource(int(diffdata.source.values[0])),
                                "Source_URL": str(diffdata.source_url.values[0]),
                                "URL": str(diffdata.url.values[0]),
                                "Extraction_Date": str(diffdata.extraction_date.values[0]).split(".")[0]
                                }, ignore_index=True)
                firstRowDiff = False 
            firstRow = True
            # for comp in oldStoreComps:
            #     data = old_df.loc[(old_df['sku'] == sku) & (old_df['competitor_name'] == comp)]
            #     mainOutputDF = mainOutputDF.append({
            #                     "Product_Name": str(data.product_name.values[0].encode('utf-8')) if firstRow else None,
            #                     "SKU": sku if firstRow else None,
            #                     "MPN": str(data.mpn.values[0]) if firstRow else None,
            #                     "UPC": str(data.upc.values[0]) if firstRow else None,
            #                     "Competitors Count {0}".format(args[0]): len(oldStoreComps) if firstRow else None,
            #                     "Competitors Count {0}".format(args[1]): len(newStoreComps) if firstRow else None,
            #                     "Difference": len(diff) if firstRow else None,
            #                     "Sellers": comp.encode('utf-8'),
            #                     "Source": parseSource(int(data.source.values[0])),
            #                     "Source_URL": str(data.source_url.values[0]),
            #                     "URL": str(data.url.values[0]),
            #                     "Extraction_Date": str(data.extraction_date.values[0]).split(".")[0]
            #                     }, ignore_index=True)
            #     firstRow = False
        # else: # => all competitors that are in the old store are also in the new store.
            
    # Set-up stats data
    data = {
            "Store 1": [
                "Store {0}".format(args[0]),    # Store
                len(old_store_skus),    # Total Skus
                oldStoreCompCount,  # Total Competitores
                ]
                ,
            "Store 2": [
                "Store {0}".format(args[1]),    # Store
                len(new_store_skus),    # Total Skus
                newStoreCompCount,  # Total Competitores
                ]
        }
    statsDF = pd.DataFrame.from_dict(data ,orient='index', columns = ["Store", "Total Skus", "Total Competitores"])
    # Finish progress bar
    bar.finish()

    saveDataToExcel(args, mainOutputDF, diffDF, statsDF)

    print "✓ Finished Main <{0}>".format(startTime.strftime('%Y-%m-%d_%H-%M-%S'))
    timeTook = ' '.join([ ''.join(x) for x in zip(str(datetime.now() - startTime).split(".")[0].split(":"),[' Hour/s', ' Minute/s', ' Second/s'])])
    print "✓ Script took : [ {0} ]".format(timeTook)