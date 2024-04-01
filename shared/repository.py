import pandas as pd
import pyodbc
import xml.etree.ElementTree as ET

from pyodbc import Row
from shared.customer import Person

def getAllProducts():
    with getConn() as conn:
        df = pd.read_sql("SELECT ProductId, Name, ProductNumber FROM SalesLT.Product", conn)
        return df
    
def getCustomers():
    with getConn() as conn:
        df = pd.read_sql(""" 
            SELECT C.CustomerID, CompanyName = C.CompanyName + ' (' + A.City + ', ' + A.StateProvince + ' - ' + A.CountryRegion + ')' 
            FROM SalesLT.Customer C
            INNER JOIN SalesLT.CustomerAddress CA ON C.CustomerID = CA.CustomerID
            INNER JOIN SalesLT.Address A ON CA.AddressId = A.AddressId
            ORDER BY C.CompanyName
        """, conn)
        return df
    
def getAddress(customerId):
    with getConn() as conn:
        df = pd.read_sql(""" 
            SELECT A.AddressID, A.AddressLine1, A.AddressLine2, A.City, A.StateProvince, A.CountryRegion, A.PostalCode,
                   FullAddress = A.AddressLine1 + ', ' + A.City + ' ' + A.StateProvince + ' ' + A.CountryRegion + ' ' + A.PostalCode
            FROM SalesLT.CustomerAddress CA
            INNER JOIN SalesLT.[Address] A ON CA.AddressID = A.AddressID
            WHERE CA.CustomerID = ?
        """,params=[customerId], con=conn)
        return df
    
def getProduct(productNumber):  
    product = Row
    with getConn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM SalesLT.Product WHERE ProductNumber = ?", productNumber)

        product = cursor.fetchone()

        return product
    
def saveSalesTransaction(purchases, customer:Person):  
    product = Row

    with getConn() as conn:
        sql = 'exec SalesLT.SavePurchase ?, ?, ?'
        params = (customer.id, customer.addressId, purchases)
        cursor = conn.cursor()
        cursor.execute(sql, params)

def getConn():
    server = 'adventureworks-svr.database.windows.net'
    database = 'AdventureWorks'
    username = 'adm'
    password = 'P@ssw0rd'
    driver= '{ODBC Driver 17 for SQL Server}'

    conn = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

    return conn