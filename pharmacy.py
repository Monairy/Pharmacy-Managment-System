import xlrd
from openpyxl import Workbook,load_workbook


# Give the location of the file 
DataBaseFile = ("db.xlsx") 
  
class Database:
  WorkBook = xlrd.open_workbook(DataBaseFile) #read
  SheetForRead = WorkBook.sheet_by_index(0) #read
  workbookwr = load_workbook(filename=DataBaseFile) #Write
  SheetForWrite = workbookwr.active #Write
  
  
  def func(self):
   print "77"

def GetRowIndex(): #index of row to write in
 return Database.SheetForRead.nrows+1

def UpdateRowIndex(): #update row index for next addition
 Database.SheetForRead.nrows = Database.SheetForRead.nrows+1

class Medicine:
 name="null"
 barcode="null"
 quantity="null"
 expire="null"
 price="null"
 def SetName(self,NewName):
    self.name=NewName
 def SetBarcode(self,NewBarcode):
    self.barcode=NewBarcode
 def SetQuantity(self,NewQuantity):
    self.quantity=NewQuantity    
 def SetExpire(self,NewExpire):
    self.expire=NewExpire    
 def SetPrice(self,NewPrice):
    self.price=NewPrice
    
 def AddToDataBase(self):
    RowIndex=str(GetRowIndex())
    Database.SheetForWrite["A"+RowIndex]= self.name
    Database.SheetForWrite["B"+RowIndex]= self.barcode
    Database.SheetForWrite["C"+RowIndex]= self.quantity
    Database.SheetForWrite["D"+RowIndex]= self.expire
    Database.SheetForWrite["E"+RowIndex]= self.price
    Database.workbookwr.save(filename=DataBaseFile)
    UpdateRowIndex() #update row index for next addition



A=Medicine()
A.SetName("Panadol")
A.AddToDataBase()
print A.name


print GetRowIndex()


