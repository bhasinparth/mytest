#importing the required libraries
import pandas as pd
import numpy as np

#reading csv file from desktop folder in my pc
data = pd.read_csv("C:/Users/parth/Desktop/data.csv")

#extracting bank name from column "number"
data['Bank'] =   pd.np.where(data.number.str.contains("ICICI"), "ICICI Bank",
                 pd.np.where(data.number.str.contains("HDFC"), "HDFC Bank",
                 pd.np.where(data.number.str.contains("PNB"), "Punjab National Bank",
                 pd.np.where(data.number.str.contains("YES"), "YES Bank",
                 pd.np.where(data.number.str.contains("SBI"), "State Bank of India",
                 pd.np.where(data.number.str.contains("BOI"), "Bank of India",
                 pd.np.where(data.number.str.contains("AXIS"), "Axis Bank","-")))))))

#seperating the Available balance and transaction amounts
values = pd.DataFrame(data.body.str.split('bal|Bal',1).tolist(),
                                   columns = ['Transaction','Balance'])

#performing regex to extract the amount
values['checker']=~values.Transaction.str.contains('OTP|due|Due|Please pay|Monthly|& save|at branches|month')
values['Balance']=values.Balance.str.extract('(?i)(?:(?:RS|INR|MRP)\.?\s?)(\d+(:?\,\d+)?(\,\d+)?(\.\d{1,2})?)')[0]
values['Transaction']=values.Transaction.str.extract('(?i)(?:(?:RS|INR|MRP)\.?\s?)(\d+(:?\,\d+)?(\,\d+)?(\.\d{1,2})?)')[0]
values=values.fillna(0)
values.loc[values['checker'] == 0, 'Transaction'] = 0
values.loc[values['checker'] == 0, 'Balance'] = 0
del values['checker']

#converting from datatype object to float
values['Transaction'] = values['Transaction'].astype('str')
values['Transaction'] = values['Transaction'].str.replace(',', '')
values['Transaction'] = pd.to_numeric(values['Transaction'], errors='coerce')

#converting from datatype object to float
values['Balance'] = values['Balance'].astype('str')
values['Balance'] = values['Balance'].str.replace(',', '')
values['Balance'] = pd.to_numeric(values['Balance'], errors='coerce')

data['Balance']=values['Balance']
data['Transaction']=values['Transaction']

#groupby operation to fetch sum of total transactions(credit+debit)
trans=data.groupby('Bank')["Transaction"].sum().reset_index(name ='Total Transactions')

#groupby to fetch the available balance from latest row
bal=data.groupby('Bank')['Balance'].agg('last').reset_index(name ='Available Balance')
bal=bal.replace(0,'-')

#fetching the result table
result=pd.merge(trans, bal, on="Bank")

#saving the result in new csv file in my pc
result.to_csv("C:/Users/parth/Desktop/result.csv")