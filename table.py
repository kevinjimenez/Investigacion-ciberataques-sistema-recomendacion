"""
#Create hiracchical treeview Application  
from tkinter import *  
from tkinter import ttk  
app=Tk()  
#App Title  
app.title("Python GUI Application ")  
#Lable  
#ttk.Label(app, text="Hierachical Treeview").pack()  



#Treeview  
treeview=ttk.Treeview(app)  
treeview.pack()  
#Treeview items  

treeview["columns"]=("#1","#2")
treeview.heading('#0', text='Anomalia')
treeview.heading('#1', text='rating')
treeview.heading('#2', text='numero raitings')
#treeview.heading('', text='Modification Date')

treeview.insert('','0','item1',text='Parent tree',values=("850 bytes", "18:30"))  
treeview.insert('','1','item2',text='1st Child',values=("850 bytes", "18:30"))  
treeview.insert('','end','item3',text='2nd Child',values=("850 bytes", "18:30"))  
treeview.insert('item2','end','A',text='A')  
treeview.insert('item2','end','B',text='B')  
treeview.insert('item2','end','C',text='C')  
treeview.insert('item3','end','D',text='D')  
treeview.insert('item3','end','E',text='E')  
treeview.insert('item3','end','F',text='F')  
treeview.move('item2','item1','end')  
treeview.move('item3','item1','end')  
#Calling Main()  
app.mainloop()  
"""
from tkinter import * 
 
root = Tk()
 
# Gets the requested values of the height and widht.
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
print("Width",windowWidth,"Height",windowHeight)
 
# Gets both half the screen width/height and window width/height
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
 
# Positions the window in the center of the page.
root.geometry("+{}+{}".format(positionRight, positionDown))
 
 
root.mainloop()
