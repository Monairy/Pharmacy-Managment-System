from openpyxl import Workbook,load_workbook
from Tkinter import *
import tkMessageBox
 
Path = ("MedicineDatabase.xlsx") #Path Of DataBase

"""
Notes:
   for writing in cell; column=letter, row=number(starting with 1)
   save is a must after writing
"""
  
class Database:
  DataBaseFile=Path
  workbook = load_workbook(filename=DataBaseFile) #Write
  sheet= workbook.active #Write
  
  def GetRowIndex(self): #index of row to write in
       return self.sheet.max_row+1
  def SaveDatabase(self):
      self.workbook.save(filename=self.DataBaseFile)


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
    DB=Database()
    RowIndex=str(DB.GetRowIndex())
    DB.sheet["A"+RowIndex]= self.name
    DB.sheet["B"+RowIndex]= self.barcode
    DB.sheet["C"+RowIndex]= self.quantity
    DB.sheet["D"+RowIndex]= self.expire
    DB.sheet["E"+RowIndex]= self.price
    DB.SaveDatabase()
    

def EditPrice(MedicineName,NewPrice):
   db=Database()
   for row in range(1,db.sheet.max_row): # loop over rows
      if(db.sheet["A"+str(row)].value.lower()==MedicineName.lower()):
            db.sheet["E"+str(row)]= NewPrice #update price
            db.SaveDatabase()

def AddMedicineUI():
    global label1,label2,label3,label4,label5,entry1,entry2,entry3,entry4,entry5
    label1= Label(GUI,text="Name",bg="LightBlue",fg="white",font=("Times", 20),width=7,relief="ridge")
    label1.place(x=0,y=120)
    label2= Label(GUI,text="Barcode",bg="LightBlue",fg="white",font=("Times", 20),width=7,relief="ridge")
    label2.place(x=0,y=160)
    label3= Label(GUI,text="Quantity",bg="LightBlue",fg="white",font=("Times", 20),width=7,relief="ridge")
    label3.place(x=0,y=200)
    label4= Label(GUI,text="Expire",bg="LightBlue",fg="white",font=("Times", 20),width=7,relief="ridge")
    label4.place(x=0,y=240)
    label5= Label(GUI,text="Price",bg="LightBlue",fg="white",font=("Times", 20),width=7,relief="ridge")
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

    B4 = Button(GUI, text ="Add",font=("Arial", 14),command = lambda : NewMedicine())
    B4.configure(height=1,width=10)
    B4.place(x=100,y=320)

def NewMedicine():
  Med=Medicine()
  Med.SetName(entry1.get())
  Med.SetBarcode(entry2.get())
  Med.SetQuantity(entry3.get())   
  Med.SetExpire(entry4.get())   
  Med.SetPrice(entry5.get())
  Med.AddToDataBase()
  HideMedicineUI()

def HideMedicineUI():
  label1.destroy()
  label2.destroy()
  label3.destroy()
  label4.destroy()
  label5.destroy()
  entry1.destroy()
  entry2.destroy()
  entry3.destroy()
  entry4.destroy()
  entry5.destroy()

   
GUI = Tk()
GUI.title("Pharmacy Managment System")
GUI.configure(bg='GREY')
GUI.minsize(1400,650)
GUI.resizable(0,0)

labelbanner= Label(GUI,text="Pharmacy Managment System",bg="LightBlue",fg="white",font=("Times", 30))
labelbanner.grid(columnspan=8,padx=500)

labelfooter= Label(GUI,text="Version 1.00",bg="grey",font=("Times", 14))
labelfooter.place(x=700,y=600)


B1 = Button(GUI, text ="Add New Medicine", command = lambda : AddMedicineUI())
B1.configure(height=3)
B1.grid(row=1,column=0)


B2 = Button(GUI, text ="Add Medicine2", command =lambda :  AddMedicineUI())
B2.configure(height=3)
B2.grid(row=1,column=1)


B3 = Button(GUI, text ="Add Medicine", command =lambda :  AddMedicineUI())
B3.configure(height=3)
B3.grid(row=1,column=2)


GUI.mainloop()
                 
"""Medicines = []
i=0
while True:
    print "Enter Medicine Name:  "
    MedName = raw_input()

    if (MedName == 'done'):
        break
    
    Medicines.append(MedName)
    Medicines[i] = Medicine()
    Medicines[i].SetName(MedName)
    Medicines[i].AddToDataBase()
    i=i+1


    print "Medicine %s is added to Database" % MedName
    




EditPrice("ketofan","76")
print "Price Updated"
"""
