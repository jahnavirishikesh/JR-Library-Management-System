# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 16:41:44 2020

@author: Jahnavi Rishikesh
Library Application
Jahnavi Rishikesh
Standard XII A

"""
from datetime import date
import pandas as pd
import os

# Function Name : printMainScreen
# Function Description: Prints the main menu
# Input parameters: None
# Output parameters:Returns the chosen menu option
def printMainScreen ():
    
    print ("\n\nWELCOME TO JAHNAVI's LIBRARY")
    print ("*********************************")
    
    print ("1. Books Maintenance")
    print ("2. Customer Maintenance")
    print ("3. Library functions")
    print ("4. Show all books")
    print ("5. Show all customers")
    print ("0. Exit")
    choice = int(input ("Enter your choice: "))
    
    return choice

# Function Name : bookMaintenanceMenu
# Function Description: Prints the Book maintenance menu options
# Input parameters: None
# Output parameters:Returns the chosen menu option
def bookMaintenanceMenu ():
    
    print ("\n\nWELCOME TO JAHNAVI's LIBRARY - BOOK MAINTENANCE OPTIONS")
    print ("*********************************")
    
    print ("1. Add new Books to Library")
    print ("2. Search for books by ISBN")
    print ("3. Search for books by Author")
    print ("4. Search for books by Title")
    print ("0. Exit to previous menu")
    choice = int(input ("Enter your choice: "))
    
    return choice

# Function Name : customerMaintenanceMenu
# Function Description: Prints the Customer maintenance menu options
# Input parameters: None
# Output parameters:Returns the chosen menu option
def customerMaintenanceMenu ():
    
    print ("\n\nWELCOME TO JAHNAVI's LIBRARY - CUSTOMER MAINTENANCE OPTIONS")
    print ("*********************************")
    
    print ("1. Add New Customer account")
    print ("2. Search for customer account by account number")
    print ("3. Search for customer account by name")
    print ("0. Exit to previous menu")
    choice = int(input ("Enter your choice: "))
    
    return choice

# Function Name : libraryMenu
# Function Description: Prints the common librarby functions menu options
# Input parameters: None
# Output parameters:Returns the chosen menu option
def libraryMenu() :
    
    print ("\n\nWELCOME TO JAHNAVI's LIBRARY - LIBRARY OPTIONS")
    print ("*********************************")
    
    print ("1. Issue a book")
    print ("2. Return a book")
    print ("3. List all books issued by customer")
    print ("0. Exit to previous menu")
    choice = int(input ("Enter your choice: "))
    
    return choice

# Function Name : searchBy
# Function Description: Generalised search function - searches for a given value in a given dataframe
#                        returns True if the value is found in the dataframe under the given index/column name
# Input parameters: searchOf -> "books","customer"
#                   usingParam -> the actual index under which to search eg. ACCOUNT_ID, ISBN, TITLE etc
#                   myval -> The value being searched for
# Output parameters:Returns the chosen menu option
def searchBy(searchOf, usingParam,myval):
    mydf = pd.DataFrame()
    # Trim leading zeros for number
    #print ("Searching for  ",searchOf," using ", usingParam," equal to ", myval)
    if (searchOf == "book"):
        mydf = booksdf
    else:
        if (searchOf == "customer"):
            mydf = customersdf
    if (mydf.empty):
        return False
    
    #print (type(myval))
        
    if (usingParam == "ACCOUNT_NUMBER" or usingParam == "ISBN"):
        #print ("Restricted search")
        #print ("Length was:", str(len(mydf)))
        if (len(mydf) >= int(myval)):
             #print ("In here myval", myval)
             result = mydf.loc[int(myval)]
        else:
             result = pd.DataFrame()
    else:
        #print ("My string :",mydf[usingParam])
        result = mydf.loc[mydf[usingParam].str.contains(myval)]
        
    if (result.empty) :
        return False
    else:
        return True
    
    return False


# Function Name : addBook
# Function Description: Function to add a book to the library
#                       If book already exists - allows to add additional copies
#                       If new book can enter details and add the book 
# Input parameters: None
# Output parameters:None. 
# Database updates: Updates booksdf dataframe and BOOKS table in the database
def addBook():
    global booksdf
    
    print("Add book functionality")
    print ("**********************")
    
    # check if book already exists. If yes then ask if additional copies are to be added
    isbn= input ("Enter the ISBN number: ")
    isFound = searchBy("book","ISBN",isbn)
    if (isFound):
        print ("Found this book in the database. You can add more copies for the same book. ")
        result = booksdf.loc[int(isbn)]
        print (result['TITLE'], " by ", result['AUTHOR_FNAME'],result['AUTHOR_LNAME'])
        addcopies = int(input ("Enter number of additional copies:"))
        num_copies = int(result['NUMBER_OF_COPIES'])
        num_copies = num_copies + addcopies
        booksdf.at[int(isbn),'NUMBER_OF_COPIES'] = str(num_copies)
        num_issued = int(result['ISSUED_COPIES'])
        print("Successfully added copies of the book. Number of copies in the library is now : ",num_copies)
    else:
        
        title= input ("Enter the title: ") 
        author_fname= input ("Enter the author's first name: ")
        author_lname= input ("Enter the author's last name: ")
        genre= input ("Enter the genre: ")
        num_copies = int(input("Enter the number of copies in library: "))
        num_issued = 0
    
        val = (title,author_fname,author_lname,genre, str(num_copies),str(num_issued))
        # add to the dataframe that is in memory
        myBooksIndexList = list(["TITLE", "AUTHOR_FNAME", "AUTHOR_LNAME", "GENRE", "NUMBER_OF_COPIES", "ISSUED_COPIES"])
        myBooksRow = pd.Series(val,index=myBooksIndexList,name=int(isbn))
        booksdf = booksdf.append(myBooksRow)
        
        print ("Index is ",booksdf.index.name)
    #input ("Press ENTER to continue.")
    return 


# Function Name : issueBook
# Function Description: Function to issue a book from the library
#                       Checks for customer details and validity
#                       For a valid customer takes details of ISBN number to be issued.
#                       if ISBN not known can search by TITLE or AUTHOR and select correct ISBN
#                       If book copies are not available informs the customer
#                       If copies are available issues the book to the customer
# Input parameters: None
# Output parameters:None. 
# Database updates: Updates booksdf dataframe and BOOKS table in the database - reduces available copies by 1
#                   Updates transactiondf dataframe and TRANSACTIONS table in the database - creates a new transaction for the book issued with current date
#                   STATUS set as ISSUED shows its an open transaction.
def issueBook():
    print("Issue book functionality")
    print ("************************")
    global transactionsdf
    
    account_number= input ("Enter your customer account number: ")
    #check whether customer exists
    customerIsFound = searchBy("customer","ACCOUNT_NUMBER", account_number)
    if (customerIsFound) :
        customerResult = customersdf.loc[int(account_number)]
        idxCustomer = int(account_number)
        print ("Welcome", customerResult['CUSTOMER_FNAME'],customerResult['CUSTOMER_LNAME'],"!")
        issued_isbn = input("If you know the ISBN, enter it : ")
        isISBNFound = False
        if (issued_isbn.strip() == "") :
            issued_title = input("Enter the book's title: ")
            if (issued_title.strip() == ""):
                issued_author_lname = input("Enter the author's last name: ")
                if (issued_author_lname.strip() == ""):
                    print ("You need to enter atleast one of these parameters to issue a book.")
                    #input("Press ENTER to continue.")
                    return
                else:
                    #author known
                    #print ("Author is known.")
                    # search for list by Author. Ask customer to type ISBN from list
                    isFound= searchBy("book", "AUTHOR_LNAME", issued_author_lname)
                    if (isFound==False):
                        print ("Invalid author or we do not have any books from this author..")
                        input ("Press ENTER to continue.")
                        return
                    booksList = booksdf.loc[booksdf['AUTHOR_LNAME'].str.contains(issued_author_lname)]
                    print ("Here are the books from the author you requested:")
                    print ("ISBN          TITLE                  AUTHOR NAME")
                    for ind,row in booksList.iterrows():
                        print (ind," ",row['TITLE']," by ", row['AUTHOR_FNAME'],row['AUTHOR_LNAME'])
                    
                    #print (booksList)
                    issued_isbn = input("Kindly choose your ISBN from the given list: ")
                    isISBNFound = True
            else:
                #   title known
                #print("Title is known.")
                # searchBy Title. Show list of books. Ask customer to type ISBN again from list
                isFound= searchBy("book", "TITLE", issued_title)
                if (isFound == False):
                    print ("We do not have any such book in our library.. ")
                    input ("Press ENTER to continue.")
                    return
                booksList = booksdf.loc[booksdf['TITLE'].str.contains(issued_title)]
                print ("Here are the books with the given title: ")
                print ("ISBN          TITLE                  AUTHOR NAME")
                for ind,row in booksList.iterrows():
                    print (ind," ",row['TITLE']," by ", row['AUTHOR_FNAME'],row['AUTHOR_LNAME'])
                    
                issued_isbn = input ("Kindly choose your ISBN from the given list: ")
                isISBNFound = True
        else:
            # ISBN known
            #print("ISBN is known.")
            isISBNFound = True
        
    else:
        # customer was not found
        print ("Invalid customer. Recheck your customer account number")
        return
        
    if (isISBNFound):
        #do functionality of issuing the book
        # here we know the customer acccount number is valid
        # we also know issued ISBN is valid
        #print ("Going into isFound with issued_isbn",str(issued_isbn))
        isFound = searchBy("book",'ISBN', issued_isbn)
        if (isFound == False):
            print("Something is wrong. Invalid ISBN has been entered or we do not have this book in our library.")
            #input("Press ENTER to continue.")
            return
        bookResult = booksdf.loc[int(issued_isbn)]
        idxBook = int(issued_isbn)
        print ("The book to be issued is", bookResult['TITLE'], " by ",  bookResult['AUTHOR_FNAME'], bookResult['AUTHOR_LNAME'], ".")
        print ("No of copies:" ,bookResult['NUMBER_OF_COPIES'])
        
        print ("Issued copies:" ,bookResult['ISSUED_COPIES'])
        availableBooks = int(bookResult['NUMBER_OF_COPIES']) - int(bookResult['ISSUED_COPIES'])
        if (availableBooks <= 0) :
            print ("Book is out of stock. Please try later.")
            return
        numIssuedCopies = int(bookResult['ISSUED_COPIES']) +1
        booksdf.at[idxBook,'ISSUED_COPIES'] = str(numIssuedCopies)
        
        #Update Transaction DF 
        if (transactionsdf.empty):
            #doing for first time no transactions exist
            transactionID = 1
        else:
            lastTransactionID = getMaxValue()
            transactionID = lastTransactionID + 1
        print ("TransactionId for issuing the book is:  ", transactionID)
        date_issued = date.today() 
        
        status = "ISSUED"
                
        myTransactionsIndexList = list(['ACCOUNT_NUMBER', 'ISBN', 'DATE_ISSUED', 'DATE_RETURNED', 'STATUS'])
        val = (int(account_number),int(issued_isbn),str(date_issued),'',status)
        myrow = pd.Series(val,index=myTransactionsIndexList,name=int(transactionID))
        transactionsdf = transactionsdf.append(myrow)
        print ("*************************")   
        print ("The book is successfully issued!")
        print ("Transaction ID :" , transactionID)
        print ("Customer account:",account_number)
        print ("Book issued ISBN",issued_isbn)
        print ("Book title:",booksdf.at[idxBook,'TITLE'])
        print ("Book author:",booksdf.at[idxBook,'AUTHOR_FNAME'],booksdf.at[idxBook,'AUTHOR_LNAME'])
        print ("Issued on:" , date_issued)
        print ("*************************")
        availableBooks = int(bookResult['NUMBER_OF_COPIES']) - int(bookResult['ISSUED_COPIES'])
        print ("Note to librarian : Available copies of this book in the library are:",availableBooks)
    else:
        print ("None of the parameters were satisfied.")
        
    #input ("Enter any key to continue...")    
    return


# Function Name : returnBook
# Function Description: Function to return a book back to the library
#                       Checks for customer details and validity
#                       For a valid customer shows list of books he has issued
#                       takes details of ISBN number to be returned.
#                       Returns the book by updating RETURN date, setting STATUS as 0 to show its returned 
#                       updating stock of available books by reducing issued copies count
# Input parameters: None
# Output parameters:None. 
# Database updates: Updates booksdf dataframe and BOOKS table in the database - reduces issued copies by 1
#                   Updates transactiondf dataframe and TRANSACTIONS table in the database - 
#                   updates return date for book with current date
#                   STATUS set as ISSUED shows its an open transaction.
def returnBook():
    print("Return book")
    print ("*************")
    global transactionsdf
        #acc number
    account_number = input("Enter customer's account number: ") 
    #validate acc num
    customerIsFound = searchBy("customer", "ACCOUNT_NUMBER", account_number)
    if (customerIsFound):
        customerResult = customersdf.loc[int(account_number)]
        
        transactionResult = transactionsdf.loc[transactionsdf.ACCOUNT_NUMBER == int(account_number)]
        if (transactionResult.empty):
            transactionResult = transactionsdf.loc[transactionsdf.ACCOUNT_NUMBER == (account_number)]
       
        if (transactionResult.empty) :
            print ("Customer has not issued any books.")
            return
        transactionResult = transactionResult.loc[(transactionResult['STATUS'] == "ISSUED")]
        
        if (transactionResult.empty) :
            print ("Customer has not issued any books.")
            return
        print ("Following books are issued to this customer with account id \n", str(account_number))
        print ("TRANSACTION ID   , ISBN,        ISSUED ON")
        for ind,row in transactionResult.iterrows():
            print (str(ind),"              ",row["ISBN"],row['DATE_ISSUED'])
        issued_isbn = input("PLease enter the isbn of the book to be returned: ")
        transactionResult = transactionResult.loc[(transactionResult['ISBN'] == int(issued_isbn))]
        if (transactionResult.empty):
            print("No records to be returned")
            return
        
        idxTransaction = transactionResult.index[0]
        
        bookResult = booksdf.loc[int(issued_isbn)]
        idxBook = int(issued_isbn)
        numIssuedCopies = int(booksdf.at[idxBook,'ISSUED_COPIES'])
        numIssuedCopies = numIssuedCopies - 1
        booksdf.at[idxBook,'ISSUED_COPIES'] = numIssuedCopies
        
        
        #print ("Updated issued copies.")
        date_returned = date.today()
        status = ""
        transactionsdf.at[idxTransaction,'STATUS'] = status
        #transactionId = transactionResult.at[idxTransaction, 'TRANSACTION_ID']
        transactionId = idxTransaction
        #print ("TRANASCTION ID FOR THIS ISSUE IS ", str(idxTransaction))
        #print("Updated status as returned")
        transactionsdf.at[int(idxTransaction),'DATE_RETURNED'] = date_returned
        #print ("Updated date returned")
        #
        
        print ("Return was successful")
        print ("*********************")
        print ("Updated record below #",transactionId)
        print ("Customer Account No :",account_number )
        print ("ISBN:", transactionsdf.at[idxTransaction,'ISBN'])
        print ("Date returned:", transactionsdf.at[idxTransaction,'DATE_RETURNED'])
        print ("**********************")
        numIssuedCopies = int(booksdf.at[idxBook,'ISSUED_COPIES'])
        availableCopies = int(booksdf.at[idxBook,'NUMBER_OF_COPIES']) - numIssuedCopies
        print ("Note to librarian: Available copies of this book are now ",availableCopies)
               #transactionsdf.at[idxTransaction,'ACCOUNT_ID'],transactionsdf.at[idxTransaction,'ISBN'],transactionsdf.at[idxTransaction,'DATE_ISSUED'],transactionsdf.at[idxTransaction,'DATE_RETURNED'],transactionsdf.at[idxTransaction,'STATUS'])
    else:
        print("Customer was not found. Please check given account number.")
        return
    return

# Function Name : addCustomer
# Function Description: Function to add a new customer
#                       Gets customer details and creates a new customer account number
# Input parameters: None
# Output parameters:None. 
# Database updates: Inserts a new record in customersdf dataframe and CUSTOMERS table in the database
def addCustomer():
    global customersdf
    print("Add Customer functionality")
    print ("***************************")
    if (customersdf.empty):
       # print ("Description is none")
        print ("First time no records in database yet")
        lastcustomer = 0
    else:
        lastcustomer = int(getLastCustomer())
    #print ("Got last customer as ", str(lastcustomer))    
    account_number = lastcustomer + 1
    customer_fname = input("Enter customer's first name: ")
    customer_lname = input("Enter customer's last name: ")
    customer_mobile_number = input("Enter customer's mobile number: ")
    customer_mobile_number  = customer_mobile_number [:10]
    #print ("Substring is now :",customer_mobile_number)
    address_line = input("Enter customer's address: ")
    address_city = input("Enter customer's city: ")
    address_state = input("Enter customer's state: ")
    address_pincode = input("Enter customer's pincode: ")
    address_pincode  = address_pincode [:6]

    customer_since = date.today()
        # add to the dataframe that is in memory
    
    val = (customer_fname,customer_lname,customer_mobile_number,address_line,address_city,address_state,address_pincode,str(customer_since))
    global myCustomerIndexList
    #print (myCustomerIndexList[1:])
    #print (val)
    
    myCustomerRow = pd.Series(val,index = myCustomerIndexList[1:],name=int(account_number) )
    #print ("Series")
    #print (myCustomerRow)
    customersdf = customersdf.append(myCustomerRow)
    print ("New customer created")
    print("************************")
    
    print (customer_fname," ",customer_lname, ": Your new account number is :", account_number)
    return
    
# Function Name : listAllBooksByCustomer
# Function Description: Function to get customer account number and show all issued books
# Input parameters: None
# Output parameters:None. 
def listAllBooksByCustomer():
    global transactionsdf
   
    print ("List of books issued")
    print ("********************")
    if (transactionsdf.empty):
        print ("No transactions in this library yet")
        return
    #print ("Came here with transactionsdf")
    #print (transactionsdf)
    
    account_number = input ("Enter customer account number: ")
    issuedBooksdf = transactionsdf.loc[transactionsdf.ACCOUNT_NUMBER == int(account_number)]
    if (issuedBooksdf.empty):
        issuedBooksdf = transactionsdf.loc[transactionsdf.ACCOUNT_NUMBER == (account_number)]
       
    print ("Books issued are below")
    print ("***********************")
    print (issuedBooksdf)
    return
# Function Name : reportBooks
# Function Description: Function to show all books available 
# Input parameters: None
# Output parameters:None. 
def reportBooks():
    global booksdf
    global myBooksIndexList
    
    header = ""
    if (booksdf.empty):
        print ("Library is empty - no available books")
        return
        
    print ("LIST OF BOOKS IN LIBRARY")
    print ("****************************")
    for t in myBooksIndexList:
        header = header + str(t) + "\t"
    print (header)
        
    for ind, row in booksdf.iterrows():
        #print (ind)
        #print (row)
        nextbookline = "" + str(ind) +"\t"
        for t in myBooksIndexList[1:]:
            nextbookline = nextbookline + str(row[t])+ "\t"
        print(nextbookline)

    return

# Function Name : reportCustomers
# Function Description: Function to show all customers available 
# Input parameters: None
# Output parameters:None.
def reportCustomers():
    global customersdf
    global myCustomerIndexList
    
    header = ""
    if (customersdf.empty):
        print ("Library is empty - no available customers")
        return
        
    print ("LIST OF ALL CUSTOMERS IN LIBRARY")
    print ("****************************")
    for t in myCustomerIndexList:
        header = header + str(t) + "\t"
    print (header)    
    for ind, row in customersdf.iterrows():
        nextline = "" + str(ind) + "\t"
        for t in myCustomerIndexList[1:]:
            nextline = nextline + str(row[t])+ "\t"
        print(nextline)

    return
    
# Function Name : updateDataToCSV
# Function Description: Function to write given dataframe to csv file
# Input parameters: mydata - dataframe, fileName - name of the file to be written
# Output parameters:None. 
def updateDataToCSV(mydata,fileName,myIndex):
    if (mydata.empty):
        print ("Empty data nothing to write in "+ fileName)
    else:
        datafilepath = os.getcwd()+"\\DATA FILES\\" + fileName
        mydata.to_csv(datafilepath,index_label=myIndex)
        
    return

# Function Name : getDataFrameFromCSV
# Function Description: Function to read from CSV and return a dataframe
# Input parameters: mydata - dataframe, fileName - name of the file to be read
# Output parameters:Returns a dataframe. 
def getDataFrameFromCSV(fileName,myindex):
    datafilepath = os.getcwd()+"\\DATA FILES\\" + fileName
    mydata = pd.DataFrame()
    # check if file exists. First time run there is no file
    if os.path.isfile(datafilepath):
        print ("Reading ",datafilepath)
        mydata = pd.read_csv(datafilepath)
        #print ("My index",myindex)
        #print (mydata)
        if (mydata.empty):
            print ("Data empty")
        else:
            mydata = mydata.set_index(myindex)
            #print (mydata)
    #mydata.reindex(index = mydata[0])
    return mydata
   


# Function Name : getMaxValue
# Function Description: Function to get last transaction id. TID in database is number but in dataframe treated as string 
#                       Hence it is not in sorted order. This function iterates and returns max value
# Input parameters: None
# Output parameters:Returns an integer which is the last transaction id. 
def getMaxValue():
    # function written to get max of transaction id
    maxValue = 0
    #print (transactionsdf)
    for ind,row in transactionsdf.iterrows():
        if int (ind) > maxValue:
            maxValue = int (ind)
    
    return maxValue

    
def getLastCustomer():

    maxValue = 0
    #print (transactionsdf)
    for ind,row in customersdf.iterrows():
        if int(ind) > maxValue:
            maxValue = int (ind)
    
    return maxValue


#Start of main program
#***************************
try:    
    myBooksIndexList = list(["ISBN", "TITLE", "AUTHOR_FNAME", "AUTHOR_LNAME", "GENRE", "NUMBER_OF_COPIES", "ISSUED_COPIES"])
    myCustomerIndexList = list(['ACCOUNT_NUMBER','CUSTOMER_FNAME',    'CUSTOMER_LNAME','CUSTOMER_MOBILE_NUMBER','ADDRESS_LINE','ADDRESS_CITY',    'ADDRESS_STATE','ADDRESS_PINCODE','CUSTOMER_SINCE'])
    myTransactionsIndexList = list(['TRANSACTION_ID', 'ACCOUNT_NUMBER', 'ISBN', 'DATE_ISSUED', 'DATE_RETURNED', 'STATUS'])
       
    # loading local panda dataframes with the database records for faster search
    booksdf = pd.DataFrame()
    customersdf = pd.DataFrame()
    transactionsdf = pd.DataFrame()
    #datafilepath = os.getcwd()
    
    booksdf = getDataFrameFromCSV("books.csv","ISBN")
    customersdf = getDataFrameFromCSV("customers.csv","ACCOUNT_NUMBER")
    transactionsdf = getDataFrameFromCSV("transactions.csv","TRANSACTION_ID")
    if (transactionsdf.empty):
        print ()
    else:
        transactionsdf["ISBN"].astype(int)
        transactionsdf["ACCOUNT_NUMBER"].astype(int)
        #print ("After conversion: ",transactionsdf["ISBN"].dtype)
        
    choice = printMainScreen()
    
    #loop to continue in program until option to Exit is chosen    
    while (choice != 0):
        newchoice = 1
        # Choice of book maintenance
        if (choice == 1):
            while (newchoice != 0):
                newchoice = bookMaintenanceMenu()
                if (newchoice == 1):
                    addBook()
                    
                    newchoice = 0
                    input("Press enter to continue...")
                if (newchoice == 2):
                    myval = input("Enter the ISBN number:")
                    isFound = searchBy("book","ISBN",myval)
                    if (isFound):
                        bookResult = booksdf.loc[int(myval)]
                        idxBook = int(myval)
                        print ("Book with given ISBN is: ", bookResult['TITLE'], " by ", bookResult['AUTHOR_FNAME'], bookResult['AUTHOR_LNAME'])
                    else:
                        print ("Sorry did not find this book in the library.")
                    newchoice = 0
                    input("Press enter to continue...")
                if (newchoice == 3):
                    myval = input("Enter the Author's Last Name:")
                    isFound = searchBy("book","AUTHOR_LNAME",myval)
                    
                    if (isFound):
                        print ("Found the following books by this author:")
                        bookResult = booksdf.loc[booksdf['AUTHOR_LNAME'].str.contains(myval)]
                        for ind,row in bookResult.iterrows():
                            print (row['TITLE'])
                    else:
                        print ("Sorry did not any books by this author in the library.")
                    newchoice = 0
                    input("Press enter to continue...")
                if (newchoice == 4):
                    myval = input("Enter the Title:")
                    isFound=searchBy("book","TITLE",myval)
                    if (isFound):
                        print ("Found the following books with similar titles")
                        bookResult = booksdf.loc[booksdf['TITLE'].str.contains(myval)]
                        for ind,row in bookResult.iterrows():
                            print (row['TITLE'] , " by ", row['AUTHOR_FNAME'],row['AUTHOR_LNAME'])
                    else:
                        print ("Sorry did not find any similar titles in the library")
                    newchoice = 0
                    input("Press enter to continue...")
                    
                    
        # Choice of customer maintenance        
        if (choice == 2):
            while (newchoice != 0):
                newchoice =  customerMaintenanceMenu()
                if (newchoice == 1):
                    addCustomer()
                    newchoice = 0
                    input("Press enter to continue...")
                if (newchoice == 2):
                    myval = input("Enter the account number:")
                    isFound = searchBy("customer","ACCOUNT_NUMBER",myval)
                    if (isFound):
                        customerResult = customersdf.loc[int(myval)]
                        #idxCustomer = customerResult.index[0]
                        print ("Customer found is: ", customerResult['CUSTOMER_FNAME'],customerResult['CUSTOMER_LNAME'] )
                    else:
                        print ("Sorry did not find this customer account in the library.")
                    newchoice = 0
                    input("Press enter to continue...")
                if (newchoice == 3):
                    myval = input("Enter the customer's last name:")
                    isFound = searchBy("customer","CUSTOMER_LNAME",myval)
                    if (isFound):
                        customerResult = customersdf.loc[customersdf['CUSTOMER_LNAME'].str.contains(myval)]
                        print ("ACCOUNT NUMBER        CUSTOMER NAME        CITY      MOBILE NUMBER")
                        for ind,row in customerResult.iterrows():
                            print (str(ind),"\t",row['CUSTOMER_FNAME'],"\t",row['CUSTOMER_LNAME'],"\t", row['ADDRESS_PINCODE'], "\t",row ['CUSTOMER_MOBILE_NUMBER'] )
                    else:
                        print ("Sorry did not find this customer account in the library.")
                    newchoice = 0
                    input("Press enter to continue...")
                

        # Choice of library functions  
        if (choice == 3):
            while (newchoice != 0):
                newchoice = libraryMenu()
                if (newchoice == 1):
                    issueBook()
                    newchoice = 0
                    input("Press enter to continue...")
                if (newchoice == 2):
                    returnBook()
                    newchoice = 0
                    input("Press enter to continue...")
                if (newchoice == 3):
                    listAllBooksByCustomer()
                    newchoice = 0
                    input("Press enter to continue...")
                if (newchoice == 4):
                    newchoice = 0    
                    input("Press enter to continue...")
        # Choice of reports
        if (choice == 4):
            reportBooks()
            input("Press enter to continue...")
        if (choice == 5):
            reportCustomers()
            input("Press enter to continue...")
            
        choice = printMainScreen()   
    #print ("Out of main menu .. going to write the csv now")
    # Before leaving the program write the records to the csv file   
    updateDataToCSV(booksdf,"books.csv","ISBN")
    updateDataToCSV(customersdf,"customers.csv","ACCOUNT_NUMBER")
    updateDataToCSV(transactionsdf,"transactions.csv","TRANSACTION_ID")
    print ("Thank you for using Jahnavi's Library App. See you soon !!!")
except:
    print ("Something went wrong. Please contact the administrator")
    