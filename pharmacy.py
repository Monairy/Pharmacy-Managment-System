from openpyxl import Workbook,load_workbook
from tkinter import *
from tkinter import messagebox
import os
import datetime
from tkdocviewer import DocViewer

Path = ("MedicineDatabase.xlsx") #Path Of DataBase
Path2 = ("OrderDatabase.xlsx")
"""
Notes:
   for writing in cell; column=letter, row=number(starting with 1)
   save is a must after writing
"""
class Database:
  def GetRowIndex(self): #index of row to write in
       return self.sheet.max_row+1
  def SaveDatabase(self):
      self.workbook.save(filename=self.DataBaseFile)
      
####################################
########_Medicine_Database##########
####################################
class MedicineDatabase(Database):
  DataBaseFile=Path
  workbook = load_workbook(filename=DataBaseFile) #Write
  sheet= workbook.active #Write
  
  def SearchMedicineByName(self,MedicineName): # Find Medicine in Database with it's name and return dictionary of data
      DictOfData={}
      found = 0
      for row in range(1,self.sheet.max_row+1):# loop over rows
             if(str(self.sheet["A"+str(row)].value).lower()==MedicineName.lower()):
                 DictOfData["barcode"]= self.sheet["B"+str(row)].value
                 DictOfData["quantity"]= self.sheet["C"+str(row)].value
                 DictOfData["expire"]= self.sheet["D"+str(row)].value
                 DictOfData["price"]= self.sheet["E"+str(row)].value
                 found = 1
      if (found == 1):
        return DictOfData
      else:
         DictOfData["barcode"] = "Not Found"
         DictOfData["quantity"]= "Not Found"
         DictOfData["expire"]  = "Not Found"
         DictOfData["price"]   = "Not Found"
         ShowError("Medicine Not Found")
         return DictOfData

  def EditMedicineBarcode(self,MedicineName,NewBarcode):
    for row in range(1,self.sheet.max_row+1): # loop over rows
       if(str(self.sheet["A"+str(row)].value).lower()==MedicineName.lower()):
            self.sheet["B"+str(row)]= NewBarcode #update barcode
            self.SaveDatabase()
  def EditMedicineQuantity(self,MedicineName,NewQuantity):
    for row in range(1,self.sheet.max_row+1): # loop over rows
       if(str(self.sheet["A"+str(row)].value).lower()==MedicineName.lower()):
            self.sheet["C"+str(row)]= NewQuantity #update quantity
            self.SaveDatabase()
  def EditMedicineExpire(self,MedicineName,NewExpire):
    for row in range(1,self.sheet.max_row+1): # loop over rows
       if(str(self.sheet["A"+str(row)].value).lower()==MedicineName.lower()):
            self.sheet["D"+str(row)]= NewExpire #update expire
            self.SaveDatabase()            
  def EditMedicinePrice(self,MedicineName,NewPrice):
    for row in range(1,self.sheet.max_row+1): # loop over rows
       if(str(self.sheet["A"+str(row)].value).lower()==MedicineName.lower()):
            self.sheet["E"+str(row)]= NewPrice #update price
            self.SaveDatabase()
  def AddMedicineToDataBase(self,medicine):
    RowIndex=str(self.GetRowIndex())
    if (medicine.name!=""): # To Avoid storing empty objects
     self.sheet["A"+RowIndex]= medicine.name
     self.sheet["B"+RowIndex]= medicine.barcode
     self.sheet["C"+RowIndex]= medicine.quantity
     self.sheet["D"+RowIndex]= medicine.expire
     self.sheet["E"+RowIndex]= medicine.price
     self.SaveDatabase()
     
####################################
#########_Order_Database_###########
#################################### 
class OrderDatabase(Database):
  DataBaseFile=Path2
  workbook = load_workbook(filename=DataBaseFile) #Write
  sheet= workbook.active #Write

  def NextReceiptNo(self):
    return self.sheet.max_row
  
  def AddOrderToDataBase(self,order):
    RowIndex=str(self.GetRowIndex())
    self.sheet["A"+RowIndex]= order.receiptnum # OrderID
    self.sheet["B"+RowIndex]="" #initial value to avoid none
    for i in range(0,len(order.items)): #Products 
      self.sheet["B"+RowIndex]=str(self.sheet["B"+RowIndex].value) + order.items[i] + ","
    self.sheet["C"+RowIndex]="" #initial value to avoid none  
    for i in range(0,len(order.items)): #quantities 
      self.sheet["C"+RowIndex]=str(self.sheet["C"+RowIndex].value) + order.quantities[i] + ","
    self.sheet["D"+RowIndex]= order.CalcSum() #total price 
    self.sheet["E"+RowIndex]= order.PaymentType #Payment Type Cash or Visa
    self.sheet["F"+RowIndex]= order.date #Date
    self.SaveDatabase()
    self.DeductQuantityFromMedicineDataBase(order)

  def DeductQuantityFromMedicineDataBase(self,order): #after successful order
     DB=MedicineDatabase()
     for i in range(0, len(order.items)):
       MedicineName=order.items[i]
       SoldQuantity=int(order.quantities[i])
       AvailableQuantity=int(DB.SearchMedicineByName(MedicineName)["quantity"])
       DB.EditMedicineQuantity(MedicineName,AvailableQuantity-SoldQuantity)

  def DailyProfit(self):
    RowIndex = self.GetRowIndex()
    today = datetime.date.today()
    today =str(today).split()
    DailyProfit=0
    for i in range(1, RowIndex):
        OrderDate =str(self.sheet["F"+str(i)].value).split()

        if OrderDate[0] == today[0]:
            DailyProfit = DailyProfit+int(self.sheet["D"+str(i)].value)
    return DailyProfit
  def MonthlyProfit(self):
    RowIndex = self.GetRowIndex()
    today = datetime.date.today()
    ourmonth = str(today)[0:7]
    MonthlyProfit = 0
    for i in range(1, RowIndex):
        OrderDate = str(self.sheet["F" + str(i)].value)[0:7]

        if (OrderDate == ourmonth):
              MonthlyProfit = MonthlyProfit + int(self.sheet["D" + str(i)].value)
    return MonthlyProfit
  
####################################
##########_Clients_DB_############
####################################
class ClientDatabase(Database):#####################################################
 pass


####################################
#########_Medicine_Class_###########
####################################
class Medicine:
 name="null"
 barcode="null"
 quantity="null"
 expire="null"
 price="null"
 def SetName(self,Name):
    self.name=Name.lower()
 def SetBarcode(self,Barcode):
    self.barcode=Barcode
 def SetQuantity(self,Quantity):
    self.quantity=Quantity    
 def SetExpire(self,Expire):
    self.expire=Expire    
 def SetPrice(self,Price):
    self.price=Price    
 def AddToDataBase(self):
    DB=MedicineDatabase()
    DB.AddMedicineToDataBase(self)

    
####################################
#########_Receipt_Class_############
####################################   
class Receipt(): # 3 lists items:quantities:prices
  receiptnum=0
  OrderType="In Store" #store or delivery
  PaymentType="Cash"
  DeliveryAddress="N/A"
  date=str(datetime.datetime.now())[:16]
  items=[]
  quantities=[]
  prices=[]
  def AddItem(self,item,quantity,price):
    self.items.append(item)
    self.quantities.append(quantity)
    self.prices.append(price)
    self.SetReceiptNum()
  def SetReceiptNum(self):
     DB=OrderDatabase()
     self.receiptnum=DB.NextReceiptNo()
  def SetPaymentType(self,paymenttype):
    self.PaymentType=paymenttype    
  def SetType(self,Type):
     self.OrderType=Type   
  def SetDeliveryAddress(self,Address):
     self.DeliveryAddress=Address
  def CalcSum(self): # returns string of total order price
    total=0
    for i in range (0,len(self.prices)):
      total = total+int(self.quantities[i])*int(self.prices[i])
    return str(total)
  def AddToDataBase(self):
     DB=OrderDatabase()
     DB.AddOrderToDataBase(self)  
  def printrec(self):
    print (self.items)
    print (self.quantities)
    print (self.prices)

####################################
##########_Client_Class_############
####################################
class Client(): ################################################
  address="null"
  number="0"
  ID="0"


####################################
########_USEFUL_FUNCTIONS_##########
#################################### 
    
def ShowError(error):
  errorbox = Tk()
  errorbox.withdraw()
  messagebox.showinfo("Error", error)
  
def space(word,numofspaces):
   space = ""
   for i in range (0,numofspaces-len(word)):
     space = space + " "
   return space
  
####################################
#######_Add_New_Medicine_###########
####################################
def AddMedicineUI():
    global label1,label2,label3,label4,label5,entry1,entry2,entry3,entry4,entry5,ButtonAdd
    DestroyAll()

    label1= Label(GUI,text="name",    bg="LightBlue",fg="white",font=("Times", 20),width=7,relief="ridge")
    label1.place(x=0,y=120)
    label2= Label(GUI,text="barcode", bg="LightBlue",fg="white",font=("Times", 20),width=7,relief="ridge")
    label2.place(x=0,y=160)
    label3= Label(GUI,text="quantity",bg="LightBlue",fg="white",font=("Times", 20),width=7,relief="ridge")
    label3.place(x=0,y=200)
    label4= Label(GUI,text="expire",  bg="LightBlue",fg="white",font=("Times", 20),width=7,relief="ridge")
    label4.place(x=0,y=240)
    label5= Label(GUI,text="price",   bg="LightBlue",fg="white",font=("Times", 20),width=7,relief="ridge")
    label5.place(x=0,y=280)
    
    entry1=Entry(GUI , font=("Times", 20))
    entry1.place(x=150,y=120)
    entry2=Entry(GUI , font=("Times", 20))
    entry2.place(x=150,y=160)
    entry3=Entry(GUI , font=("Times", 20))
    entry3.place(x=150,y=200)
    entry4=Entry(GUI , font=("Times", 20))
    entry4.place(x=150,y=240)
    entry5=Entry(GUI , font=("Times", 20))
    entry5.place(x=150,y=280)

    ButtonAdd = Button(GUI, text ="Add",font=("Arial", 14),command = lambda : NewMedicine())
    ButtonAdd.configure(height=1,width=10)
    ButtonAdd.place(x=100,y=320)
    
    
def NewMedicine():
  Med=Medicine()
  Med.SetName(entry1.get())
  Med.SetBarcode(entry2.get())
  Med.SetQuantity(entry3.get())   
  Med.SetExpire(entry4.get())   
  Med.SetPrice(entry5.get())
  Med.AddToDataBase()
  labeldone= Label(GUI,text="Medicine Added Successfuly",bg="GREY",fg="RED",font=("Times", 20)) 
  labeldone.place(x=0,y=360)
  GUI.after(2000,lambda:labeldone.destroy()) # done label appear and disappear after time

####################################
########_Edit_Medicine_#############
####################################  
def EditExistingMedicineUI(): # enter name, click search then show result of search by: showDataUI()
    DestroyAll()       
    global label6,entry6,ButtonSearch
    label6= Label(GUI,text="Enter Medicine Name: ",bg="LightBlue",fg="white",font=("Times", 20),width=20,relief="ridge")
    label6.place(x=200,y=120)
    
    entry6=Entry(GUI , font=("Times", 20),width=20)
    entry6.place(x=210,y=160)

    
    ButtonSearch = Button(GUI, text ="Search",font=("Arial", 14),command = lambda : ShowDataUI())
    ButtonSearch.configure(height=1,width=10)
    ButtonSearch.place(x=290,y=200)


def ShowDataUI(): #After Search
   global entry7,entry8,entry9,entry10,ButtonBarcode,ButtonQuantity,ButtonExpire,ButtonPrice     
   if (entry6.get()!=""):
     DB = MedicineDatabase()
     MedicineData = DB.SearchMedicineByName(entry6.get())  #dictionary of medicine data from database

     entry7 = Entry(GUI, font=("Times", 15),width=15) # entry for barcode
     entry7.insert(0,MedicineData.get("barcode"))
     entry7.place(x=200,y=320)

     ButtonBarcode = Button(GUI, text ="Edit Barcode",font=("Arial", 12),command=lambda:EditMedicine(1))
     ButtonBarcode.configure(height=1,width=15)
     ButtonBarcode.place(x=205,y=360)
####################################
     entry8 = Entry(GUI, font=("Times", 15),width=15) # entry for quantity
     entry8.insert(0,MedicineData.get("quantity"))
     entry8.place(x=400,y=320)

     ButtonQuantity = Button(GUI, text ="Edit Quantity",font=("Arial", 12),command=lambda:EditMedicine(2))
     ButtonQuantity.configure(height=1,width=15)
     ButtonQuantity.place(x=405,y=360)
####################################
     entry9 = Entry(GUI, font=("Times", 15),width=15) # entry for expire
     entry9.insert(0,MedicineData.get("expire"))
     entry9.place(x=600,y=320)

     ButtonExpire = Button(GUI, text ="Edit Expire",font=("Arial", 12),command=lambda:EditMedicine(3))
     ButtonExpire.configure(height=1,width=15)
     ButtonExpire.place(x=605,y=360)
####################################
     entry10 = Entry(GUI, font=("Times", 15),width=15) # entry for price
     entry10.insert(0,MedicineData.get("price"))
     entry10.place(x=800,y=320)

     ButtonPrice = Button(GUI, text ="Edit Price",font=("Arial", 12),command=lambda:EditMedicine(4))
     ButtonPrice.configure(height=1,width=15)
     ButtonPrice.place(x=805,y=360)

     
def EditMedicine(arg): # execute action depending on arg, 1:barcode, 2:quantity, 3:expire, 4:price
    DB = MedicineDatabase()
    MedicineData = DB.SearchMedicineByName(entry6.get())  #search in db and get dictionary of medicine data from database

    if (arg==1):
      DB.EditMedicineBarcode(entry6.get(),entry7.get()) # EditMedicineBarcode(name,barcode)

      label= Label(GUI,text="Barcode Modified Successfuly",bg="GREY",fg="RED",font=("Times", 15))
      label.place(x=200,y=400)
      GUI.after(2000,lambda:label.destroy())     # label appear and disappear after time

    if (arg==2):
      DB.EditMedicineQuantity(entry6.get(),entry8.get()) # EditMedicineQuantity(name,quantity)

      label= Label(GUI,text="Quantity Modified Successfuly",bg="GREY",fg="RED",font=("Times", 15))
      label.place(x=400,y=400)
      GUI.after(2000,lambda:label.destroy())    

    if (arg==3):
      DB.EditMedicineExpire(entry6.get(),entry9.get()) # EditMedicineExpire(name,expire)

      label= Label(GUI,text="Expire Modified Successfuly",bg="GREY",fg="RED",font=("Times", 15))
      label.place(x=600,y=400)
      GUI.after(2000,lambda:label.destroy())

    if (arg==4):
      DB.EditMedicinePrice(entry6.get(),entry10.get()) # EditMedicinePrice(name,price)

      label= Label(GUI,text="Price Modified Successfuly",bg="GREY",fg="RED",font=("Times", 15))
      label.place(x=800,y=400)
      GUI.after(2000,lambda:label.destroy())


####################################
############_Receipt_###############
#################################### 
def MakeReceiptUI():
    DestroyAll()
    global label7,entry11,ButtonAddToReceipt, label8,entry12,ButtonMakeReceipt,receiptContents,labelPaymentType,buttoncash,buttonvisa,labelOrderType,buttonstore,buttondelivery
    label7= Label(GUI,text="Enter Medicine Name: ",bg="LightBlue",fg="white",font=("Times", 18),width=20,relief="ridge")
    label7.place(x=360,y=120)
    
    entry11=Entry(GUI , font=("Times", 20),width=20)
    entry11.place(x=350,y=160)
    #######################################
    
    label8= Label(GUI,text="Enter Quantity: ",bg="LightBlue",fg="white",font=("Times", 15),width=15,relief="ridge")
    label8.place(x=670,y=120)
  
    entry12=Entry(GUI , font=("Times", 20),width=15)
    entry12.place(x=650,y=160)
    #######################################
    
    ButtonAddToReceipt = Button(GUI, text ="AddToReceipt",font=("Arial", 14),command = lambda : AddToReceiptUI(entry11.get(),entry12.get()))
    ButtonAddToReceipt.configure(height=1,width=15)
    ButtonAddToReceipt.place(x=550,y=200)
    #######################################
    
    labelPaymentType = Label(GUI,text="Choose Payment Type: ",bg="LightBlue",font=("Arial", 14),relief="ridge")
    labelPaymentType.place(x=400,y=250)
    
    buttoncash=Radiobutton(GUI, text="Cash",variable=PaymentType, value=1,bg="grey",font=("Arial", 14))
    buttoncash.place(x=420,y=280)
    buttonvisa=Radiobutton(GUI,text="Visa",variable=PaymentType, value=2,bg="grey",font=("Arial", 14))
    buttonvisa.place(x=520,y=280)

    
    labelOrderType = Label(GUI,text="Choose Oder Type: ",bg="LightBlue",font=("Arial", 14),relief="ridge")
    labelOrderType.place(x=620,y=250)
    buttonstore=Radiobutton(GUI, text="In-Store",variable=OrderType, value=1,bg="grey",font=("Arial", 14))
    buttonstore.place(x=620,y=280)
    buttondelivery=Radiobutton(GUI,text="Delivery",variable=OrderType, value=2,bg="grey",font=("Arial", 14))
    buttondelivery.place(x=720,y=280)
   
    ######################################
    ButtonMakeReceipt = Button(GUI, text ="Generate Receipt",font=("Arial", 20),command = lambda : MakeReceipt())
    ButtonMakeReceipt.configure(height=1,width=20)
    ButtonMakeReceipt.place(x=550,y=400)
    #####################################
    receiptContents = Text(GUI, height=40, width=30)
    receiptContents.insert(END,"Item           "+"Q   "+"Price\n" )


def AddToReceiptUI(MedName,Quantity): # make initial look of receipt contents
  MedDB = MedicineDatabase()
  PriceFromDB = MedDB.SearchMedicineByName(MedName)["price"]
  QuantityInDB= int(MedDB.SearchMedicineByName(MedName)["quantity"])
  
  receiptContents.place(x=900,y=120)
  
  if (int(Quantity)>QuantityInDB):
    ShowError("Insufficient Quantity\n only "+ str(QuantityInDB) +" in stock")
  if (PriceFromDB!="Not Found" and int(Quantity)<=QuantityInDB ):
    receiptContents.insert(END, MedName+space(MedName,15)+Quantity+space(Quantity,5)+PriceFromDB+"\n")


def MakeReceipt(): #construct receipt object
  OrderList=receiptContents.get("2.0",END).split("\n")[:-2] #Make list of lines starting from line2 > item:quantiy:price
  receipt = Receipt()
  receipt.items.clear()      #######
  receipt.quantities.clear() #######
  receipt.prices.clear()    #######
  
  if (PaymentType.get()==1):
    receipt.SetPaymentType("Cash")
  else:
     receipt.SetPaymentType("Visa")

  for i in range(0,len(OrderList)): # add items to receipt object
    item=OrderList[i].split()[0]
    quantity=OrderList[i].split()[1]
    price=OrderList[i].split()[2]
    receipt.AddItem(item,quantity,price)

  GenerateReceipt(receipt,len(OrderList))
  receiptContents.destroy()

   
def GenerateReceipt(receipt,receiptlength): # make file for receipt and preview it
  
 with open("receipt.txt", "w") as receiptfile:
    receiptfile.write("    Group25 Pharmacy\n")
    receiptfile.write("========================\n")
    receiptfile.write("       receipt#"+str(receipt.receiptnum)+"\n")
    receiptfile.write("Payment: "+receipt.PaymentType+"\n")
    
    receiptfile.write("========================\n")

    receiptfile.write("Item           Q   Price\n")
    
    receiptfile.write("------------------------\n")
    for i in range(0,receiptlength): ## write all items in receipt
      item=receipt.items[i]
      quantity=receipt.quantities[i]
      price=receipt.prices[i]
      receiptfile.write(item+space(item,15)+quantity+space(quantity,5)+price+"\n")
      
    receiptfile.write("========================\n")
      
    totalprice=str(receipt.CalcSum())    
    receiptfile.write("Total:"+space(totalprice,12)+totalprice+" L.E\n")

    receiptfile.write("========================\n")
    
    receiptfile.write("Thank You For Your Visit!\n")
    receiptfile.write("   "+str(datetime.datetime.now())[:16]+"\n")

 with open("receipt.txt", "r") as receiptfile:
    ReceiptWindow = Tk()
    ReceiptWindow.minsize(300,600)
    Label(ReceiptWindow, text=receiptfile.read()).pack()

    ButtonPrint=Button(ReceiptWindow, text ="Print",font=("Arial", 13),command = lambda : os.startfile("receipt.txt", "print"))
    ButtonPrint.configure(height=1,width=10)
    ButtonPrint.place(x=30,y=500)
    
    ButtonClose=Button(ReceiptWindow, text ="Close",font=("Arial", 13),command = lambda : ReceiptWindow.destroy())
    ButtonClose.configure(height=1,width=10)
    ButtonClose.place(x=160,y=500)     

 receipt.AddToDataBase()

####################################
####################################
####################################


####################################
############_Profit_################
####################################
def DailyProfitUI():
    ooDB = OrderDatabase()
    profit = ooDB.DailyProfit()

    text1.place(x=600,y=200)
    text1.insert(END,str(profit)+"LE")
def MonthlyProfitUI():
    ooDB = OrderDatabase()
    profit = ooDB.MonthlyProfit()

    text2.place(x=800,y=200)
    text2.insert(END, str(profit)+"LE")
def ProfitButtons():
    global Button1, Button2,text2,text1
    DestroyAll()
    Button1 = Button(GUI, text ="Daily profit",font=("Arial", 12),command=lambda: DailyProfitUI())
    Button1.configure(height=2, width=16)
    Button1.place(x=570, y=150)
    Button2 = Button(GUI, text="Monthly profit", font=("Arial", 12), command=lambda: MonthlyProfitUI())
    Button2.configure(height=2, width=16)
    Button2.place(x=770,y=150)
    text1 = Text(master=GUI, height=1, width=10,font=("Arial",12))
    text2 = Text(master=GUI, height=1, width=10,font=("Arial",12))

####################################
####################################
####################################
  
def main():
 global GUI
 GUI = Tk()
 GUI.title("Pharmacy Managment System")
 GUI.configure(bg='Grey')
 GUI.minsize(1400,650)
 GUI.resizable(0,0)
 global PaymentType
 PaymentType = IntVar() ###############
 global OrderType
 OrderType = IntVar()

 labelbanner= Label(GUI,text="Pharmacy Managment System",bg="LightBlue",fg="White",font=("Times", 30),relief="ridge")
 labelbanner.grid(columnspan=7,padx=500)
# LoginScreen.destroy()


 B0 = Button(GUI, text ="Add New Medicine", font=("Arial", 15),command = lambda : AddMedicineUI())
 B0.configure(height=2,width=16)
 B0.grid(row=1,column=0)

 B1 = Button(GUI, text ="Edit Existing Medicine",font=("Arial", 15), command =lambda :  EditExistingMedicineUI())
 B1.configure(height=2,width=17)
 B1.grid(row=1,column=1)

 B2 = Button(GUI, text ="Make A Receipt",font=("Arial", 15), command =lambda :  MakeReceiptUI())
 B2.configure(height=2,width=16)
 B2.grid(row=1,column=2)

 B3 = Button(GUI, text ="Income",font=("Arial", 15), command=lambda: ProfitButtons())
 B3.configure(height=2,width=16)
 B3.grid(row=1,column=3)

 B4 = Button(GUI, text ="Add Client",font=("Arial", 15), command =lambda :  DailyProfitUI())
 B4.configure(height=2,width=16)
 B4.grid(row=1,column=4)

 B5 = Button(GUI, text ="Return Medicine",font=("Arial", 15), command =lambda :  AddMedicineUI())
 B5.configure(height=2,width=16)
 B5.grid(row=1,column=5)

 B6 = Button(GUI, text ="Administration",font=("Arial", 15), command =lambda :  AddMedicineUI())
 B6.configure(height=2,width=16)
 B6.grid(row=1,column=6)

 labelfooter= Label(GUI,text="Version 1.00",bg="grey",font=("Times", 14))
 labelfooter.place(x=700,y=600)

 
 GUI.mainloop()
 
 

def login():
  global LoginScreen
  LoginScreen = Tk()
  LoginScreen.title("Pharmacy Managment System")
  LoginScreen.configure(bg='GREY')
  LoginScreen.minsize(1400,650)
  LoginScreen.resizable(0,0)
  
  labelbanner= Label(LoginScreen,text="Login To Continue",bg="RED",fg="BLACK",font=("Times", 30))
  labelbanner.grid(columnspan=7,padx=500)
  
  usernameLabel=Label(LoginScreen, text=" Username: ", width=7, bg="grey",font=("Times",20))
  usernameLabel.place(x=350,y=150)
  usernameEntry = Entry(LoginScreen,font=("Times", 20))
  usernameEntry.place(x=550,y=150)
  
  
  PasswordLabel=Label(LoginScreen, text="Password:" , width=7, bg="grey",font=("Times",20))
  PasswordLabel.place(x=350,y=250)
  passwordEntry = Entry(LoginScreen, font=("Times", 20), show= '*')
  passwordEntry.place(x=550,y=250)

  
  loginbutton= Button(LoginScreen, text ="Login",font=("Arial", 20), command =lambda :  main())
  loginbutton.place(x=600,y=400)
  LoginScreen.mainloop()


def DestroyAll(): # make sure that area we use is clear before placing objects
  try:
        label1.destroy()#add medicine
        label2.destroy()
        label3.destroy()
        label4.destroy()
        label5.destroy()
        entry1.destroy()
        entry2.destroy()
        entry3.destroy()
        entry4.destroy()
        entry5.destroy()
        ButtonAdd.destroy()
  except:
           pass
  try:
        label6.destroy() #edit Medicine
        entry6.destroy()
        ButtonSearch.destroy()
        entry7.destroy()
        entry8.destroy()
        entry9.destroy()
        entry10.destroy()
        ButtonBarcode.destroy()
        ButtonQuantity.destroy()
        ButtonExpire.destroy()
        ButtonPrice.destroy()
  except:
            pass
  try:  
        label7.destroy() #receipt
        entry11.destroy()
        ButtonAddToReceipt.destroy()
        label8.destroy()
        entry12.destroy()
        ButtonMakeReceipt.destroy()
        buttoncash.destroy()
        buttonvisa.destroy()
        labelPaymentType.destroy()
        receiptContents.destroy()

  except:
         pass
  try:
      Button1.destroy()
      Button2.destroy()
      text1.destroy()
      text2.destroy()
  except:

        pass

main()


'''receipt=Receipt()
receipt.AddItem("mon",12,14)
receipt.AddItem("ahmed",10,20)
receipt.AddItem("_",3,2)
receipt.printrec()
receipt.CalcSum()

for key,value in Receipt.items.items():
    print (key[0])'''
        

