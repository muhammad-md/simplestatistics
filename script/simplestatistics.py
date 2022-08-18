import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from sklearn.linear_model import LinearRegression
import tkinter
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter.messagebox import showinfo


#setting the window
window = Tk()
window.title("SIMPLE STATISTICS")
window.configure(width=1000, height=900)
fontStyle = tkFont.Font(family="Lucida Grande", size=13)


#list o send the excel file for pd to read
excelfile = list()

#first window            
class mainwindow:
    def __init__(self, master):
        self.master = master
        fontStyle = tkFont.Font(family="Lucida Grande", size=25)
        self.btn1 = tk.Button(self.master, text ="ONE-WAY ANOVA", font = fontStyle, command = self.clearpage1)
        self.btn1.place(relx = 0.5, rely = 0.40, anchor = CENTER)
        self.btn2 = tk.Button(self.master, text ="TWO-WAY ANOVA", font = fontStyle, command = self.clearpage2)
        self.btn2.place(relx = 0.5, rely = 0.55, anchor = CENTER)
        self.btn3 = tk.Button(self.master, text ="BAR CHART", font = fontStyle, command = self.clearpage3)
        self.btn3.place(relx = 0.5, rely = 0.10, anchor = CENTER)
        self.btn4 = tk.Button(self.master, text ="PIE CHART", font = fontStyle, command = self.clearpage4)
        self.btn4.place(relx = 0.5, rely = 0.25, anchor = CENTER)
        self.btn5 = tk.Button(self.master, text ="SIMPLE LINEAR REGRESSION", font = fontStyle, command = self.clearpage5)
        self.btn5.place(relx = 0.5, rely = 0.70, anchor = CENTER)
        self.btn6 = tk.Button(self.master, text ="MULTIPLE LINEAR REGRESSION", font = fontStyle, command = self.clearpage6)
        self.btn6.place(relx = 0.5, rely = 0.85, anchor = CENTER)

    #functionro clear the page to view the next page elements
    def clearpage1(self):
        self.btn1.destroy()
        self.btn2.destroy()
        self.btn3.destroy()
        self.btn4.destroy()
        self.btn5.destroy()
        self.btn6.destroy()
        self.another = Oneway(self.master)
    def clearpage2(self):
        self.btn1.destroy()
        self.btn2.destroy()
        self.btn3.destroy()
        self.btn4.destroy()
        self.btn5.destroy()
        self.btn6.destroy()
        self.another = Twoway(self.master)
    def clearpage3(self):
        self.btn1.destroy()
        self.btn2.destroy()
        self.btn3.destroy()
        self.btn4.destroy()
        self.btn5.destroy()
        self.btn6.destroy()
        self.another = Barchart(self.master)
    def clearpage4(self):
        self.btn1.destroy()
        self.btn2.destroy()
        self.btn3.destroy()
        self.btn4.destroy()
        self.btn5.destroy()
        self.btn6.destroy()
        self.another = Piechart(self.master)
    def clearpage5(self):
        self.btn1.destroy()
        self.btn2.destroy()
        self.btn3.destroy()
        self.btn4.destroy()
        self.btn5.destroy()
        self.btn6.destroy()
        self.another = simplelinearreg(self.master)
    def clearpage6(self):
        self.btn1.destroy()
        self.btn2.destroy()
        self.btn3.destroy()
        self.btn4.destroy()
        self.btn5.destroy()
        self.btn6.destroy()
        self.another = multiplelinearreg(self.master)

#One way anova component
class Oneway:
    def __init__(self, master):
        # keep `root` in `self.master`
        self.master = master
        fontStyle1 = tkFont.Font(family="Lucida Grande", size=13)

        #back button to view previous page, that is the main page
        self.btn4 = tk.Button(self.master, text ="BACK", font = fontStyle1, command = self.load_back)
        self.btn4.place(relx = 0.90, rely = 0.84, anchor = CENTER)
        
        self.label1 = Label(self.master, text="File Selected:", font = fontStyle)
        self.label1.place(relx = 0.3, rely = 0.15, anchor = CENTER)
        
        self.label2 = Label(self.master, text="Dependent Variable: ", font = fontStyle)
        self.label2.place(relx = 0.3, rely = 0.20, anchor = CENTER)
        
        self.label3= Label(self.master, text="Independent Variable: ", font = fontStyle)
        self.label3.place(relx = 0.3, rely = 0.25, anchor = CENTER)

        #entry box for dependent and independent variavles
        self.entry_1 = Entry(self.master)
        self.entry_2 = Entry(self.master)
        self.entry_1.place(relx = 0.5, rely = 0.20, anchor = CENTER)
        self.entry_2.place(relx = 0.5, rely = 0.25, anchor = CENTER)

        #function for all the one way anova analysis   
        def analyse():
            #Check if a file selected whenever the user clicks "Analyse" button and showinformation if there is no file selected
            if len(excelfile) == 0:
                messagebox.showinfo("showinfo", "Please, select a file")
            #Continue with the analysis if a file is selected
            else:
                dependent_var = (self.entry_1.get())
                independent_var = (self.entry_2.get())
                for file in excelfile:
                    data = pd.read_excel(file)
                    model = ols('%s ~ %s ' %(dependent_var, independent_var), data = data).fit()
                    aov = sm.stats.anova_lm(model, type=2)
                    
                    #setting up newwindow to embed the result on
                    newwindow = Toplevel()      #TOPLEVEL() USED
                    newwindow.title("RESULT WINDOW - ONE WAY ANOVA")
                    newwindow.geometry("700x500")

                    #setting space to view result on inside of the new window
                    aovspace = tk.StringVar()
                    aovspace.set(aov)
                    self.label4= Label(newwindow, text="", textvariable=aovspace, font = fontStyle)
                    self.label4.place(relx = 0.5, rely = 0.10, anchor = CENTER)

                    #Run new window
                    newwindow.mainloop()
        def boxplot():
            dependent_var = (self.entry_1.get())
            independent_var = (self.entry_2.get())
            for file in excelfile:
                data = pd.read_excel(file)
                data.boxplot('%s' %(dependent_var), by='%s' %(independent_var) )
                plt.show()
                
        #settinf up space to view the name of selected file
        selectedfilespace = tk.StringVar()
        
        #function for selecting excel file to be used in the analysis
        def select_file():
            filetypes = (('text files', '*.xlsx'),('All files', '*.*'))
            filename = fd.askopenfilename(title='Open a file',initialdir='/',filetypes=filetypes)

            #send the selected excel file to the excelfile list
            excelfile.append(filename)

            #split and remove the path of the selected file and be left with that main filename
            head, tail = os.path.split(filename)
            mainfilename = tail
            selectedfilespace.set(mainfilename)

        #Buttons
        self.label5= Label(self.master, text="File Selected: ", textvariable=selectedfilespace, font = fontStyle)
        self.label5.place(relx = 0.5, rely = 0.15, anchor = CENTER)
        #creating a checkbox to allow view boxplot
        self.btn5 = tk.Checkbutton(self.master, text="show boxplot", command=boxplot, font=fontStyle)
        self.btn5.place(relx = 0.5, rely = 0.33  , anchor = CENTER)
        self.btn6 = tk.Button(self.master,text='Open a File',font= fontStyle1, command=select_file)
        self.btn6.place(relx = 0.5, rely = 0.07, anchor = CENTER)
        self.btn7 = tk.Button(self.master,text='Analyse',font= fontStyle1, command=analyse)
        self.btn7.place(relx = 0.5, rely = 0.40, anchor = CENTER)
                        
        #function to clear the current page to view the previous page elements
    def load_back(self):
        self.entry_1.destroy()
        self.entry_2.destroy()
        self.label1.destroy()
        self.label2.destroy()
        self.label3.destroy()
        self.label5.destroy()
        self.btn4.destroy()
        self.btn5.destroy()
        self.btn6.destroy()
        self.btn7.destroy()
        excelfile.clear()
        self.another = mainwindow(self.master)

#Two way anova component
class Twoway:
    def __init__(self, master):
        # keep `root` in `self.master`
        self.master = master
        fontStyle1 = tkFont.Font(family="Lucida Grande", size=13)
        #back button to view previous page, that is the main page
        self.btn4 = tk.Button(self.master, text ="BACK", font = fontStyle1, command = self.load_back)
        self.btn4.place(relx = 0.90, rely = 0.84, anchor = CENTER)
        self.label1 = Label(self.master, text="File Selected:", font = fontStyle)
        self.label1.place(relx = 0.3, rely = 0.15, anchor = CENTER)
        self.label2 = Label(self.master, text="Dependent Variable: ", font = fontStyle)
        self.label2.place(relx = 0.3, rely = 0.20, anchor = CENTER)
        self.label3= Label(self.master, text="Independent Variable one : ", font = fontStyle)
        self.label3.place(relx = 0.3, rely = 0.25, anchor = CENTER)
        self.label4= Label(self.master, text="Independent Variable two : ", font = fontStyle)
        self.label4.place(relx = 0.3, rely = 0.30, anchor = CENTER)

        #entry box for dependent and independent variavles
        self.entry_1 = Entry(self.master)
        self.entry_2 = Entry(self.master)
        self.entry_3 = Entry(self.master)
        self.entry_1.place(relx = 0.5, rely = 0.20, anchor = CENTER)
        self.entry_2.place(relx = 0.5, rely = 0.25, anchor = CENTER)
        self.entry_3.place(relx = 0.5, rely = 0.30, anchor = CENTER)

        #function for all the two way anova analysis
        def analyse():
            #Check if a file selected whenever the user clicks "Analyse" button and showinformation if there is no file selected
            if len(excelfile) == 0:
                messagebox.showinfo("showinfo", "Please, select a file")
            #Continue with the analysis if a file is selected
            else:
                dependent_var = (self.entry_1.get())
                independent_var1 = (self.entry_2.get())
                independent_var2 = (self.entry_3.get())
                for file in excelfile:
                    data = pd.read_excel(file)
                    model = ols('%s ~ %s+%s ' %(dependent_var, independent_var1, independent_var2), data = data).fit()
                    aov = sm.stats.anova_lm(model, type=2)
                        
                    #setting up newwindow to embed the result on
                    newwindow = Toplevel()      #TOPLEVEL() USED
                    newwindow.title("RESULT WINDOW - ONE WAY ANOVA")
                    newwindow.geometry("700x500")
                    
                    #setting space to view result on inside of the new window
                    aovspace = tk.StringVar()
                    aovspace.set(aov)
                    self.label5= Label(newwindow, text="", textvariable=aovspace, font = fontStyle)
                    self.label5.place(relx = 0.5, rely = 0.10, anchor = CENTER)
                    #Run new window
                    newwindow.mainloop()

        def boxplot():
            dependent_var = (self.entry_1.get())
            independent_var1 = (self.entry_2.get())
            independent_var2 = (self.entry_3.get())
            for file in excelfile:
                data = pd.read_excel(file)
                data.boxplot('%s' %(dependent_var), by='%s' %(independent_var1) )
                data.boxplot('%s' %(dependent_var), by='%s' %(independent_var2) )
                plt.show()

        #settinf up space to view the name of selected file
        selectedfilespace = tk.StringVar()
        
        #function for selecting excel file to be used in the analysis
        def select_file():
            filetypes = (('text files', '*.xlsx'),('All files', '*.*'))
            filename = fd.askopenfilename(title='Open a file',initialdir='/',filetypes=filetypes)
            
            #send the selected excel file to the excelfile list
            excelfile.append(filename)

            #split and remove the path of the selected file and be left with that main filename
            head, tail = os.path.split(filename)
            mainfilename = tail
            selectedfilespace.set(mainfilename)

        #Buttons
        self.label6= Label(self.master, text="File Selected: ", textvariable=selectedfilespace, font = fontStyle)
        self.label6.place(relx = 0.5, rely = 0.15, anchor = CENTER)
        #creating a checkbox to allow view boxplot
        self.btn5 = tk.Checkbutton(self.master, text="show boxplot", command=boxplot, font=fontStyle)
        self.btn5.place(relx = 0.5, rely = 0.36  , anchor = CENTER)
        self.btn6 = tk.Button(self.master,text='Open a File',font= fontStyle1, command=select_file)
        self.btn6.place(relx = 0.5, rely = 0.07, anchor = CENTER)
        self.btn7 = tk.Button(self.master,text='Analyse',font= fontStyle1, command=analyse)
        self.btn7.place(relx = 0.5, rely = 0.43, anchor = CENTER)
              
        #function to clear the current page to view the previous page elements
    def load_back(self):
        self.entry_1.destroy()
        self.entry_2.destroy()
        self.entry_3.destroy()
        self.label1.destroy()
        self.label2.destroy()
        self.label3.destroy()
        self.label4.destroy()
        self.btn4.destroy()
        self.btn5.destroy()
        self.btn6.destroy()
        self.btn7.destroy()
        excelfile.clear()
        self.another = mainwindow(self.master)

class Barchart:
    def __init__(self, master):
        # keep `root` in `self.master`
        self.master = master
        fontStyle1 = tkFont.Font(family="Lucida Grande", size=13)
        #back button to view previous page, that is the main page
        self.btn4 = tk.Button(self.master, text ="BACK", font = fontStyle1, command = self.load_back)
        self.btn4.place(relx = 0.90, rely = 0.84, anchor = CENTER)
        self.label1 = Label(self.master, text="File Selected:", font = fontStyle)
        self.label1.place(relx = 0.3, rely = 0.15, anchor = CENTER)
        self.label2 = Label(self.master, text="Variable one(Labels): ", font = fontStyle)
        self.label2.place(relx = 0.3, rely = 0.20, anchor = CENTER)
        self.label3= Label(self.master, text="Variable Two: ", font = fontStyle)
        self.label3.place(relx = 0.3, rely = 0.25, anchor = CENTER)

        #entry box for dependent and independent variavles
        self.entry_1 = Entry(self.master)
        self.entry_2 = Entry(self.master)
        self.entry_1.place(relx = 0.5, rely = 0.20, anchor = CENTER)
        self.entry_2.place(relx = 0.5, rely = 0.25, anchor = CENTER)

        #function for plotting bar chart   
        def analyse():
            if len(excelfile) == 0:
                messagebox.showinfo("showinfo", "Please, select a file")
            else:
                var11 = (self.entry_1.get())
                var22 = (self.entry_2.get())
                for file in excelfile:
                    data = pd.read_excel(file)
                    var1 = data['%s' %(var11)].tolist()
                    var2 = data['%s' %(var22)].tolist()
                    yy = np.array(var2)
                    plt.bar(var1, yy)
                    plt.ylabel("networth")
                    plt.xlabel("companies")
                    # Show plot
                    plt.show()
                
        #settinf up space to view the name of selected file
        selectedfilespace = tk.StringVar()
        
        #function for selecting excel file to be used in the analysis
        def select_file():
            filetypes = (('text files', '*.xlsx'),('All files', '*.*'))
            filename = fd.askopenfilename(title='Open a file',initialdir='/',filetypes=filetypes)

            #send the selected excel file to the excelfile list
            excelfile.append(filename)

            #split and remove the path of the selected file and be left with that main filename
            head, tail = os.path.split(filename)
            mainfilename = tail
            selectedfilespace.set(mainfilename)
            
        self.label5= Label(self.master, text="File Selected: ", textvariable=selectedfilespace, font = fontStyle)
        self.label5.place(relx = 0.5, rely = 0.15, anchor = CENTER)
        self.btn6 = tk.Button(self.master,text='Open a File',font= fontStyle1, command=select_file)
        self.btn6.place(relx = 0.5, rely = 0.07, anchor = CENTER)
        self.btn7 = tk.Button(self.master,text='Analyse',font= fontStyle1, command=analyse)
        self.btn7.place(relx = 0.5, rely = 0.40, anchor = CENTER)
                         
    #function to clear the current page to view the previous page elements
    def load_back(self):
        self.entry_1.destroy()
        self.entry_2.destroy()
        self.label1.destroy()
        self.label2.destroy()
        self.label3.destroy()
        self.label5.destroy()
        self.btn4.destroy()
        self.btn6.destroy()
        self.btn7.destroy()
        excelfile.clear()  
        self.another = mainwindow(self.master)

#Two way anova component
class Piechart:
    def __init__(self, master):
        # keep `root` in `self.master`
        self.master = master
        fontStyle1 = tkFont.Font(family="Lucida Grande", size=13)
        #back button to view previous page, that is the main page
        self.btn4 = tk.Button(self.master, text ="BACK", font = fontStyle1, command = self.load_back)
        self.btn4.place(relx = 0.90, rely = 0.84, anchor = CENTER)
        self.label1 = Label(self.master, text="File Selected:", font = fontStyle)
        self.label1.place(relx = 0.3, rely = 0.15, anchor = CENTER)
        self.label2 = Label(self.master, text="Variable one(labels): ", font = fontStyle)
        self.label2.place(relx = 0.3, rely = 0.20, anchor = CENTER)
        self.label3= Label(self.master, text="Variable Two : ", font = fontStyle)
        self.label3.place(relx = 0.3, rely = 0.25, anchor = CENTER)

        #entry box for dependent and independent variavles
        self.entry_1 = Entry(self.master)
        self.entry_2 = Entry(self.master)
        self.entry_1.place(relx = 0.5, rely = 0.20, anchor = CENTER)
        self.entry_2.place(relx = 0.5, rely = 0.25, anchor = CENTER)

        #function for all the two way anova analysis
        def analyse():
            if len(excelfile) == 0:
                messagebox.showinfo("showinfo", "Please, select a file")
            else:
                var11 = (self.entry_1.get())
                var22 = (self.entry_2.get())
                for file in excelfile:
                    data = pd.read_excel(file)
                    var1 = data['%s' %(var11)].tolist()
                    var2 = data['%s' %(var22)].tolist()
                    y = np.array(var2)
                    plt.pie(y, labels = var1)
                    plt.legend()
                    plt.show()

        #settinf up space to view the name of selected file
        selectedfilespace = tk.StringVar()
        
        #function for selecting excel file to be used in the analysis
        def select_file():
            filetypes = (('text files', '*.xlsx'),('All files', '*.*'))
            filename = fd.askopenfilename(title='Open a file',initialdir='/',filetypes=filetypes)

            #send the selected excel file to the excelfile list
            excelfile.append(filename)

            #split and remove the path of the selected file and be left with that main filename
            head, tail = os.path.split(filename)
            mainfilename = tail
            selectedfilespace.set(mainfilename)

        self.label6= Label(self.master, text="File Selected: ", textvariable=selectedfilespace, font = fontStyle)
        self.label6.place(relx = 0.5, rely = 0.15, anchor = CENTER)
        self.btn6 = tk.Button(self.master,text='Open a File',font= fontStyle1, command=select_file)
        self.btn6.place(relx = 0.5, rely = 0.07, anchor = CENTER)
        self.btn7 = tk.Button(self.master,text='Analyse',font= fontStyle1, command=analyse)
        self.btn7.place(relx = 0.5, rely = 0.43, anchor = CENTER)
                        
    #function to clear the current page to view the previous page elements
    def load_back(self):
        self.entry_1.destroy()
        self.entry_2.destroy()
        self.label1.destroy()
        self.label2.destroy()
        self.label3.destroy()
        self.btn4.destroy()
        self.btn6.destroy()
        self.btn7.destroy()
        excelfile.clear()
        self.another = mainwindow(self.master)

class simplelinearreg:
    def __init__(self, master):
        # keep `root` in `self.master`
        self.master = master
        fontStyle1 = tkFont.Font(family="Lucida Grande", size=13)

        #back button to view previous page, that is the main page
        self.btn4 = tk.Button(self.master, text ="BACK", font = fontStyle1, command = self.load_back)
        self.btn4.place(relx = 0.90, rely = 0.84, anchor = CENTER)
        
        self.label1 = Label(self.master, text="File Selected:", font = fontStyle)
        self.label1.place(relx = 0.3, rely = 0.15, anchor = CENTER)
        
        self.label2 = Label(self.master, text="Dependent Variable: ", font = fontStyle)
        self.label2.place(relx = 0.3, rely = 0.20, anchor = CENTER)
        
        self.label3= Label(self.master, text="Independent Variable: ", font = fontStyle)
        self.label3.place(relx = 0.3, rely = 0.25, anchor = CENTER)

        #entry box for dependent and independent variavles
        self.entry_1 = Entry(self.master)
        self.entry_2 = Entry(self.master)
        self.entry_1.place(relx = 0.5, rely = 0.20, anchor = CENTER)
        self.entry_2.place(relx = 0.5, rely = 0.25, anchor = CENTER)

        #function for all the one way anova analysis   
        def analyse():
            #Check if a file selected whenever the user clicks "Analyse" button and showinformation if there is no file selected
            if len(excelfile) == 0:
                messagebox.showinfo("showinfo", "Please, select a file")
            #Continue with the analysis if a file is selected
            else:
                dependent_var = (self.entry_1.get())
                independent_var = (self.entry_2.get())
                for file in excelfile:
                    data = pd.read_excel(file)
                    
                    #getting the values in the selected columns
                    columnindependent_var = data['%s' %(independent_var)]
                    columndependent_var = data['%s' %(dependent_var)]

                    x = list(columnindependent_var)
                    y = list(columndependent_var)

                    x = np.array(x).reshape((-1, 1))
                    y = np.array(y)

                    x = sm.add_constant(x)
                    model = sm.OLS(y, x)
                    result = model.fit()
                    summary = result.summary()
                    print(result.summary())

                    model2 = LinearRegression().fit(x, y)
                    interc = model2.intercept_
                    print("Intercept: ", interc)

                    slop = model2.coef_
                    print("Slope: ", slop)

                    y_pred = model2.predict(x)
                    print("predicted response: ", y_pred)

                    #setting up newwindow to embed the result on
                    newwindow = Toplevel()      #TOPLEVEL() USED
                    newwindow.title("RESULT WINDOW - SIMPLE LINEAR REGRESSION")
                    newwindow.geometry("700x500")

                    #setting space to view result on inside of the new window
                    aovspace = tk.StringVar()
                    aovspace2 = tk.StringVar()
                    aovspace.set(summary)
                    aovspace2.set(y_pred)

                    self.label4= Label(newwindow, text="", textvariable=aovspace, font = fontStyle)
                    self.label4.place(relx = 0.5, rely = 0.25, anchor = CENTER)

                    self.label99= Label(newwindow, text="", textvariable=aovspace2, font = fontStyle)
                    self.label99.place(relx = 0.5, rely = 0.60, anchor = CENTER)

                    #Run new window
                    newwindow.mainloop()
        #def boxplot():
         #   dependent_var = (self.entry_1.get())
          #  independent_var = (self.entry_2.get())
           # for file in excelfile:
            #    data = pd.read_excel(file)
             #   data.boxplot('%s' %(dependent_var), by='%s' %(independent_var) )
              #  plt.show()
                
        #settinf up space to view the name of selected file
        selectedfilespace = tk.StringVar()
        
        #function for selecting excel file to be used in the analysis
        def select_file():
            filetypes = (('text files', '*.xlsx'),('All files', '*.*'))
            filename = fd.askopenfilename(title='Open a file',initialdir='/',filetypes=filetypes)

            #send the selected excel file to the excelfile list
            excelfile.append(filename)

            #split and remove the path of the selected file and be left with that main filename
            head, tail = os.path.split(filename)
            mainfilename = tail
            selectedfilespace.set(mainfilename)

        #Buttons
        self.label5= Label(self.master, text="File Selected: ", textvariable=selectedfilespace, font = fontStyle)
        self.label5.place(relx = 0.5, rely = 0.15, anchor = CENTER)
        #creating a checkbox to allow view boxplot
        #self.btn5 = tk.Checkbutton(self.master, text="show boxplot", command=boxplot, font=fontStyle)
        #self.btn5.place(relx = 0.5, rely = 0.33  , anchor = CENTER)
        self.btn6 = tk.Button(self.master,text='Open a File',font= fontStyle1, command=select_file)
        self.btn6.place(relx = 0.5, rely = 0.07, anchor = CENTER)
        self.btn7 = tk.Button(self.master,text='Analyse',font= fontStyle1, command=analyse)
        self.btn7.place(relx = 0.5, rely = 0.40, anchor = CENTER)
                        
        #function to clear the current page to view the previous page elements
    def load_back(self):
        self.entry_1.destroy()
      #  self.entry_2.destroy()
       # self.label1.destroy()
        #self.label2.destroy()
        #self.label3.destroy()
        #self.label5.destroy()
        #self.btn4.destroy()
        #self.btn5.destroy()
        #self.btn6.destroy()
        #self.btn7.destroy()
        #excelfile.clear()
        #self.another = mainwindow(self.master)

class multiplelinearreg:
    def __init__(self, master):
        # keep `root` in `self.master`
        self.master = master
        fontStyle1 = tkFont.Font(family="Lucida Grande", size=13)

        #back button to view previous page, that is the main page
        self.btn4 = tk.Button(self.master, text ="BACK", font = fontStyle1, command = self.load_back)
        self.btn4.place(relx = 0.90, rely = 0.84, anchor = CENTER)
        
        self.label1 = Label(self.master, text="File Selected:", font = fontStyle)
        self.label1.place(relx = 0.3, rely = 0.15, anchor = CENTER)
        
        self.label2 = Label(self.master, text="Dependent Variable: ", font = fontStyle)
        self.label2.place(relx = 0.3, rely = 0.20, anchor = CENTER)
        self.label3= Label(self.master, text="Independent Variable one : ", font = fontStyle)
        self.label3.place(relx = 0.3, rely = 0.25, anchor = CENTER)
        self.label4= Label(self.master, text="Independent Variable two : ", font = fontStyle)
        self.label4.place(relx = 0.3, rely = 0.30, anchor = CENTER)

        #entry box for dependent and independent variavles
        self.entry_1 = Entry(self.master)
        self.entry_2 = Entry(self.master)
        self.entry_3 = Entry(self.master)
        self.entry_1.place(relx = 0.5, rely = 0.20, anchor = CENTER)
        self.entry_2.place(relx = 0.5, rely = 0.25, anchor = CENTER)
        self.entry_3.place(relx = 0.5, rely = 0.30, anchor = CENTER)

        #function for all the one way anova analysis   
        def analyse():
            #Check if a file selected whenever the user clicks "Analyse" button and showinformation if there is no file selected
            if len(excelfile) == 0:
                messagebox.showinfo("showinfo", "Please, select a file")
            #Continue with the analysis if a file is selected
            else:
                dependent_var = (self.entry_1.get())
                independent_var1 = (self.entry_2.get())
                independent_var2 = (self.entry_3.get())
                for file in excelfile:
                    data = pd.read_excel(file)
                    
                    #getting the values in the selected columns
                    columnindependent_var1 = data['%s' %(independent_var1)]
                    columnindependent_var2 = data['%s' %(independent_var2)]
                    columndependent_var = data['%s' %(dependent_var)]

                    x = []
                    x1 = list(columnindependent_var1)
                    x2 = list(columnindependent_var2)
                    lengthx1 = len(x1)
                    for i in range(0, lengthx1):
                        x.append([x1[i], x2[i]])
                    print(x)
                    y = list(columndependent_var)

                    x = np.array(x)
                    y = np.array(y)

                    x = sm.add_constant(x)
                    model = sm.OLS(y, x)
                    result = model.fit()
                    summary = result.summary()
                    print(result.summary())

                    model2 = LinearRegression().fit(x, y)
                    interc = model2.intercept_
                    print("Intercept: ", interc)

                    slop = model2.coef_
                    print("Slope: ", slop)

                    y_pred = model2.predict(x)
                    print("predicted response: ", y_pred)

                    #setting up newwindow to embed the result on
                    newwindow = Toplevel()      #TOPLEVEL() USED
                    newwindow.title("RESULT WINDOW - MULTIPLE LINEAR REGRESSION")
                    newwindow.geometry("700x500")

                    #setting space to view result on inside of the new window
                    aovspace = tk.StringVar()
                    aovspace2 = tk.StringVar()
                    aovspace.set(summary)
                    aovspace2.set(y_pred)

                    self.label4= Label(newwindow, text="", textvariable=aovspace, font = fontStyle)
                    self.label4.place(relx = 0.5, rely = 0.25, anchor = CENTER)

                    self.label99= Label(newwindow, text="", textvariable=aovspace2, font = fontStyle)
                    self.label99.place(relx = 0.5, rely = 0.60, anchor = CENTER)

                    #Run new window
                    newwindow.mainloop()
        #def boxplot():
         #   dependent_var = (self.entry_1.get())
          #  independent_var = (self.entry_2.get())
           # for file in excelfile:
            #    data = pd.read_excel(file)
             #   data.boxplot('%s' %(dependent_var), by='%s' %(independent_var) )
              #  plt.show()
                
        #settinf up space to view the name of selected file
        selectedfilespace = tk.StringVar()
        
        #function for selecting excel file to be used in the analysis
        def select_file():
            filetypes = (('text files', '*.xlsx'),('All files', '*.*'))
            filename = fd.askopenfilename(title='Open a file',initialdir='/',filetypes=filetypes)

            #send the selected excel file to the excelfile list
            excelfile.append(filename)

            #split and remove the path of the selected file and be left with that main filename
            head, tail = os.path.split(filename)
            mainfilename = tail
            selectedfilespace.set(mainfilename)

        #Buttons
        self.label5= Label(self.master, text="File Selected: ", textvariable=selectedfilespace, font = fontStyle)
        self.label5.place(relx = 0.5, rely = 0.15, anchor = CENTER)
        #creating a checkbox to allow view boxplot
        #self.btn5 = tk.Checkbutton(self.master, text="show boxplot", command=boxplot, font=fontStyle)
        #self.btn5.place(relx = 0.5, rely = 0.33  , anchor = CENTER)
        self.btn6 = tk.Button(self.master,text='Open a File',font= fontStyle1, command=select_file)
        self.btn6.place(relx = 0.5, rely = 0.07, anchor = CENTER)
        self.btn7 = tk.Button(self.master,text='Analyse',font= fontStyle1, command=analyse)
        self.btn7.place(relx = 0.5, rely = 0.40, anchor = CENTER)
                        
        #function to clear the current page to view the previous page elements
    def load_back(self):
        self.entry_1.destroy()
      #  self.entry_2.destroy()
       # self.label1.destroy()
        #self.label2.destroy()
        #self.label3.destroy()
        #self.label5.destroy()
        #self.btn4.destroy()
        #self.btn5.destroy()
        #self.btn6.destroy()
        #self.btn7.destroy()
        #excelfile.clear()
        #self.another = mainwindow(self.master)



#set default window as mainwindow and run
mainwindow(window)
window.mainloop()

