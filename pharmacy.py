import xlrd
from openpyxl import Workbook,load_workbook


# Give the location of the file 
DataBaseFile = ("db.xlsx") 
  
class Database:
  WorkBook = xlrd.open_workbook(DataBaseFile) #read
  SheetForRead = WorkBook.sheet_by_index(0) #read
  workbookwr = load_workbook(filename=DataBaseFile) #Write
  SheetForWrite = workbookwr.active #Write
  
  def UpdateRowIndex(self): #update row index for next addition
       self.SheetForRead.nrows = self.SheetForRead.nrows+1
  
  def GetRowIndex(self): #index of row to write in
       return self.SheetForRead.nrows+1


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
    DB=Database()
    RowIndex=str(DB.GetRowIndex())
    DB.SheetForWrite["A"+RowIndex]= self.name
    DB.SheetForWrite["B"+RowIndex]= self.barcode
    DB.SheetForWrite["C"+RowIndex]= self.quantity
    DB.SheetForWrite["D"+RowIndex]= self.expire
    DB.SheetForWrite["E"+RowIndex]= self.price
    DB.workbookwr.save(filename=DataBaseFile)
    DB.UpdateRowIndex() #update row index for next addition



A=Medicine()
A.SetName("Panadol")
A.AddToDataBase()
print A.name

DB=Database()
print DB.GetRowIndex()


