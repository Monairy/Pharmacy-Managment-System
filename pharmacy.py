from openpyxl import Workbook,load_workbook

# Give the location of the file 
Path = ("db.xlsx")

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
 def SetBarcode(self,NewBarcode):
    self.barcode=Barcode
 def SetQuantity(self,NewQuantity):
    self.quantity=Quantity    
 def SetExpire(self,NewExpire):
    self.expire=NewExpire    
 def SetPrice(self,NewPrice):
    self.price=NewPrice
    
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


                 
Medicines = []
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
