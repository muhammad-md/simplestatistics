import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import statsmodels.api as sm
import tkinter as tk
import tkinter.font as tkFont
from statsmodels.formula.api import ols
from sklearn.linear_model import LinearRegression
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter.messagebox import showinfo

#setting up the window
window = Tk()
window.title("SIMPLE STATISTICS")
window.geometry("800x500")
fontStyle1 = tkFont.Font(family="Lucida Grande", size=25)
fontStyle2 = tkFont.Font(family="Lucida Grande", size=13)

#lists to be used in the process of the analysis
excelfile = []
predicted_vals = []
slops1 = []
slops2 = []

#first window            
class mainwindow:
    def __init__(self, master):
        self.master = master
        self.btn1 = tk.Button(self.master, text ="ONE-WAY ANOVA", font = fontStyle1, command = self.clearpage1).place(relx = 0.5, rely = 0.40, anchor = CENTER)
        self.btn2 = tk.Button(self.master, text ="TWO-WAY ANOVA", font = fontStyle1, command = self.clearpage2).place(relx = 0.5, rely = 0.55, anchor = CENTER)
        self.btn3 = tk.Button(self.master, text ="BAR CHART", font = fontStyle1, command = self.clearpage3).place(relx = 0.5, rely = 0.10, anchor = CENTER)
        self.btn4 = tk.Button(self.master, text ="PIE CHART", font = fontStyle1, command = self.clearpage4).place(relx = 0.5, rely = 0.25, anchor = CENTER)
        self.btn5 = tk.Button(self.master, text ="SIMPLE LINEAR REGRESSION", font = fontStyle1, command = self.clearpage5).place(relx = 0.5, rely = 0.70, anchor = CENTER)
        self.btn6 = tk.Button(self.master, text ="MULTIPLE LINEAR REGRESSION", font = fontStyle1, command = self.clearpage6).place(relx = 0.5, rely = 0.85, anchor = CENTER)

    #functions to clear the page to view the next page elements
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

        #back button to view previous page, that is the main page
        self.btn1 = tk.Button(self.master, text ="BACK", font = fontStyle2, command = self.load_back).place(relx = 0.90, rely = 0.84, anchor = CENTER)
        self.label1 = Label(self.master, text="File Selected:", font = fontStyle2).place(relx = 0.3, rely = 0.15, anchor = CENTER)
        self.label2 = Label(self.master, text="Dependent Variable: ", font = fontStyle2).place(relx = 0.3, rely = 0.20, anchor = CENTER)
        self.label3= Label(self.master, text="Independent Variable: ", font = fontStyle2).place(relx = 0.3, rely = 0.25, anchor = CENTER)

        #entry box for dependent and independent variavles
        self.entry_1 = Entry(self.master).place(relx = 0.5, rely = 0.20, anchor = CENTER)
        self.entry_2 = Entry(self.master).place(relx = 0.5, rely = 0.25, anchor = CENTER)

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
                    newwindow.geometry("800x500")

                    #setting space to view result on inside of the new window
                    space1 = tk.StringVar()
                    space1.set(aov)
                    self.label4= Label(newwindow, text="", textvariable=space1, font = fontStyle2).place(relx = 0.5, rely = 0.10, anchor = CENTER)

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
            #add the selected excel file to the excelfile list
            excelfile.append(filename)

            #split and remove the path of the selected file and be left with that main filename
            head, tail = os.path.split(filename)
            mainfilename = tail
            selectedfilespace.set(mainfilename)

        #Buttons
        self.label5= Label(self.master, text="File Selected: ", textvariable=selectedfilespace, font = fontStyle2).place(relx = 0.5, rely = 0.15, anchor = CENTER)
        #creating a checkbox to allow view boxplot
        self.btn2 = tk.Checkbutton(self.master, text="show boxplot", command=boxplot, font=fontStyle2).place(relx = 0.5, rely = 0.33  , anchor = CENTER)
        self.btn3 = tk.Button(self.master,text='Open a File',font= fontStyle2, command=select_file).place(relx = 0.5, rely = 0.07, anchor = CENTER)
        self.btn4 = tk.Button(self.master,text='Analyse',font= fontStyle2, command=analyse).place(relx = 0.5, rely = 0.40, anchor = CENTER)
                        
    #function to clear the current page to view the previous page elements
    def load_back(self):
        self.entry_1.destroy()
        self.entry_2.destroy()
        self.label1.destroy()
        self.label2.destroy()
        self.label3.destroy()
        self.label5.destroy()
        self.btn1.destroy()
        self.btn2.destroy()
        self.btn3.destroy()
        self.btn4.destroy()
        excelfile.clear()
        self.another = mainwindow(self.master)

#Two way anova component
class Twoway:
    def __init__(self, master):
        # keep `root` in `self.master`
        self.master = master
        #back button to view previous page, that is the main page
        self.btn1 = tk.Button(self.master, text ="BACK", font = fontStyle1, command = self.load_back).place(relx = 0.90, rely = 0.84, anchor = CENTER)
        self.label1 = Label(self.master, text="File Selected:", font = fontStyle2).place(relx = 0.3, rely = 0.15, anchor = CENTER)
        self.label2 = Label(self.master, text="Dependent Variable: ", font = fontStyle2).place(relx = 0.3, rely = 0.20, anchor = CENTER)
        self.label3= Label(self.master, text="Independent Variable one : ", font = fontStyle2).place(relx = 0.3, rely = 0.25, anchor = CENTER)
        self.label4= Label(self.master, text="Independent Variable two : ", font = fontStyle2).place(relx = 0.3, rely = 0.30, anchor = CENTER)

        #entry box for dependent and independent variavles
        self.entry_1 = Entry(self.master).place(relx = 0.5, rely = 0.20, anchor = CENTER)
        self.entry_2 = Entry(self.master).place(relx = 0.5, rely = 0.25, anchor = CENTER)
        self.entry_3 = Entry(self.master).place(relx = 0.5, rely = 0.30, anchor = CENTER)

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
                    newwindow.geometry("800x500")
                    
                    #setting space to view result on inside of the new window
                    space1 = tk.StringVar()
                    space1.set(aov)
                    self.label5= Label(newwindow, text="", textvariable=space1, font = fontStyle2).place(relx = 0.5, rely = 0.10, anchor = CENTER)
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
            #add the selected excel file to the excelfile list
            excelfile.append(filename)

            #split and remove the path of the selected file and be left with that main filename
            head, tail = os.path.split(filename)
            mainfilename = tail
            selectedfilespace.set(mainfilename)

        #Buttons
        self.label6= Label(self.master, text="File Selected: ", textvariable=selectedfilespace, font = fontStyle2).place(relx = 0.5, rely = 0.15, anchor = CENTER)
        #creating a checkbox to allow view boxplot
        self.btn2 = tk.Checkbutton(self.master, text="show boxplot", command=boxplot, font=fontStyle2).place(relx = 0.5, rely = 0.36  , anchor = CENTER)
        self.btn3 = tk.Button(self.master,text='Open a File',font= fontStyle2, command=select_file).place(relx = 0.5, rely = 0.07, anchor = CENTER)
        self.btn4 = tk.Button(self.master,text='Analyse',font= fontStyle2, command=analyse).place(relx = 0.5, rely = 0.43, anchor = CENTER)
              
    #function to clear the current page to view the previous page elements
    def load_back(self):
        self.entry_1.destroy()
        self.entry_2.destroy()
        self.entry_3.destroy()
        self.label1.destroy()
        self.label2.destroy()
        self.label3.destroy()
        self.label4.destroy()
        self.btn1.destroy()
        self.btn2.destroy()
        self.btn3.destroy()
        self.btn4.destroy()
        excelfile.clear()
        self.another = mainwindow(self.master)

class Barchart:
    def __init__(self, master):
        # keep `root` in `self.master`
        self.master = master

        #back button to view previous page, that is the main page
        self.btn1 = tk.Button(self.master, text ="BACK", font = fontStyle1, command = self.load_back).place(relx = 0.90, rely = 0.84, anchor = CENTER)
        self.label1 = Label(self.master, text="File Selected:", font = fontStyle2).place(relx = 0.3, rely = 0.15, anchor = CENTER)
        self.label2 = Label(self.master, text="Variable one(Labels): ", font = fontStyle2).place(relx = 0.3, rely = 0.20, anchor = CENTER)
        self.label3= Label(self.master, text="Variable Two: ", font = fontStyle2).place(relx = 0.3, rely = 0.25, anchor = CENTER)

        #entry box for dependent and independent variavles
        self.entry_1 = Entry(self.master).place(relx = 0.5, rely = 0.20, anchor = CENTER)
        self.entry_2 = Entry(self.master).place(relx = 0.5, rely = 0.25, anchor = CENTER)
    
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
                    var2 = np.array(var2)
                    plt.bar(var1, var2)
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
            #add the selected excel file to the excelfile list
            excelfile.append(filename)

            #split and remove the path of the selected file and be left with that main filename
            head, tail = os.path.split(filename)
            mainfilename = tail
            selectedfilespace.set(mainfilename)
            
        self.label5= Label(self.master, text="File Selected: ", textvariable=selectedfilespace, font = fontStyle2)
        self.label5.place(relx = 0.5, rely = 0.15, anchor = CENTER)
        self.btn2 = tk.Button(self.master,text='Open a File',font= fontStyle2, command=select_file).place(relx = 0.5, rely = 0.07, anchor = CENTER)
        self.btn3 = tk.Button(self.master,text='Analyse',font= fontStyle2, command=analyse).place(relx = 0.5, rely = 0.40, anchor = CENTER)
                         
    #function to clear the current page to view the previous page elements
    def load_back(self):
        self.entry_1.destroy()
        self.entry_2.destroy()
        self.label1.destroy()
        self.label2.destroy()
        self.label3.destroy()
        self.label5.destroy()
        self.btn1.destroy()
        self.btn2.destroy()
        self.btn3.destroy()
        excelfile.clear()  
        self.another = mainwindow(self.master)

#Two way anova component
class Piechart:
    def __init__(self, master):
        # keep `root` in `self.master`
        self.master = master
        fontStyle1 = tkFont.Font(family="Lucida Grande", size=13)
        #back button to view previous page, that is the main page
        self.btn1 = tk.Button(self.master, text ="BACK", font = fontStyle1, command = self.load_back).place(relx = 0.90, rely = 0.84, anchor = CENTER)
        self.label1 = Label(self.master, text="File Selected:", font = fontStyle2).place(relx = 0.3, rely = 0.15, anchor = CENTER)
        self.label2 = Label(self.master, text="Variable one(labels): ", font = fontStyle2).place(relx = 0.3, rely = 0.20, anchor = CENTER)
        self.label3= Label(self.master, text="Variable Two : ", font = fontStyle2).place(relx = 0.3, rely = 0.25, anchor = CENTER)

        #entry box for dependent and independent variavles
        self.entry_1 = Entry(self.master).place(relx = 0.5, rely = 0.20, anchor = CENTER)
        self.entry_2 = Entry(self.master).place(relx = 0.5, rely = 0.25, anchor = CENTER)

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
                    var2 = np.array(var2)
                    plt.pie(var2, labels = var1)
                    plt.legend()
                    plt.show()

        #settinf up space to view the name of selected file
        selectedfilespace = tk.StringVar()
        
        #function for selecting excel file to be used in the analysis
        def select_file():
            filetypes = (('text files', '*.xlsx'),('All files', '*.*'))
            filename = fd.askopenfilename(title='Open a file',initialdir='/',filetypes=filetypes)
            #add the selected excel file to the excelfile list
            excelfile.append(filename)

            #split and remove the path of the selected file and be left with that main filename
            head, tail = os.path.split(filename)
            mainfilename = tail
            selectedfilespace.set(mainfilename)

        self.label6= Label(self.master, text="File Selected: ", textvariable=selectedfilespace, font = fontStyle2).place(relx = 0.5, rely = 0.15, anchor = CENTER)
        self.btn2 = tk.Button(self.master,text='Open a File',font= fontStyle1, command=select_file).place(relx = 0.5, rely = 0.07, anchor = CENTER)
        self.btn3 = tk.Button(self.master,text='Analyse',font= fontStyle1, command=analyse).place(relx = 0.5, rely = 0.43, anchor = CENTER)
                        
    #function to clear the current page to view the previous page elements
    def load_back(self):
        self.entry_1.destroy()
        self.entry_2.destroy()
        self.label1.destroy()
        self.label2.destroy()
        self.label3.destroy()
        self.btn1.destroy()
        self.btn2.destroy()
        self.btn3.destroy()
        excelfile.clear()
        self.another = mainwindow(self.master)

class simplelinearreg:
    def __init__(self, master):
        # keep `root` in `self.master`
        self.master = master
        fontStyle1 = tkFont.Font(family="Lucida Grande", size=13)

        #back button to view previous page, that is the main page
        self.btn1 = tk.Button(self.master, text ="BACK", font = fontStyle1, command = self.load_back).place(relx = 0.90, rely = 0.84, anchor = CENTER)
        self.label1 = Label(self.master, text="File Selected:", font = fontStyle2).place(relx = 0.3, rely = 0.15, anchor = CENTER)
        self.label2 = Label(self.master, text="Dependent Variable: ", font = fontStyle2).place(relx = 0.3, rely = 0.20, anchor = CENTER)
        self.label3= Label(self.master, text="Independent Variable: ", font = fontStyle2).place(relx = 0.3, rely = 0.25, anchor = CENTER)

        #entry box for dependent and independent variavles
        self.entry_1 = Entry(self.master).place(relx = 0.5, rely = 0.20, anchor = CENTER)
        self.entry_2 = Entry(self.master).place(relx = 0.5, rely = 0.25, anchor = CENTER)

        #function for all the one way anova analysis   
        def analyse():
            #Check if a file selected whenever the user clicks "Analyse" button and showinformation if there is no file selected
            if len(excelfile) == 0:
                messagebox.showinfo("showinfo", "Please, select a file")
            #Continue with the analysis if a file is selected
            else:
                entry_1 = (self.entry_1.get())
                entry_2 = (self.entry_2.get())
                for file in excelfile:
                    data = pd.read_excel(file)
                    
                    #getting the values in the selected columns
                    independent_var_column = data['%s' %(entry_2)]
                    dependent_var_column = data['%s' %(entry_1)]

                    independent_var_list = list(independent_var_column)
                    dependent_var_list = list(dependent_var_column)

                    independent_var = np.array(independent_var_list).reshape((-1, 1))
                    dependent_var = np.array(dependent_var_list)

                    independent_var = sm.add_constant(independent_var)
                    model = sm.OLS(dependent_var, independent_var)
                    result = model.fit()
                    summary = result.summary()
                    print(result.summary())

                    model2 = LinearRegression().fit(independent_var, dependent_var)
                    interc = model2.intercept_
                    print("Intercept: ", interc)

                    slop = model2.coef_
                    print("Slope: ", slop)

                    y_pred = model2.predict(independent_var)
                    print("predicted response: ", y_pred)

                    equation = "EQUATION: "+ " "+ str(entry_1) + " " + "=" +" " + str(round(interc, 2)) + " " + "+" +" " + str(round(slop[1], 2))+str(entry_2)
                    
                    for num in independent_var_list:
                        predicted_val = "PREDICTED VALUE OF "+ str(entry_1) + " "+ "IF "+ str(entry_2)+ " " + "= "+ str(num) + " " + "is " + str(round(interc+ (slop[1]*num), 2))
                        predicted_vals.append("%s \n" %(predicted_val))

                    #setting up newwindow to embed the result on
                    newwindow = Toplevel()      #TOPLEVEL() USED
                    newwindow.title("RESULT WINDOW - SIMPLE LINEAR REGRESSION")
                    
                    #setting space to view result on inside of the new window
                    space1 = tk.StringVar()
                    space2 = tk.StringVar()
                    space1.set(summary)
                    space2.set(equation)
                    self.label4= Label(newwindow, text="", textvariable=space1, font = fontStyle2).pack(fill="y")
                    self.label5= Label(newwindow, text="", textvariable=space2, font = fontStyle2).pack(fill="y")
                    
                    for i in range(0, len(independent_var_list)):
                        independent_var_list[i] = tk.StringVar()
                        independent_var_list[i].set(predicted_vals[i])
                        self.label6= Label(newwindow, text="", textvariable=independent_var_list[i], font = fontStyle2).pack(fill="y")
                        print(predicted_vals[i])

                    #set the height and width and run newwindow
                    height = newwindow.winfo_screenheight() #get your Windows height size 
                    newwindow.geometry("%dx%d" % (800, height))
                    newwindow.resizable(False,False)
                    newwindow.mainloop()
    
        #settinf up space to view the name of selected file
        selectedfilespace = tk.StringVar()
        
        #function for selecting excel file to be used in the analysis
        def select_file():
            filetypes = (('text files', '*.xlsx'),('All files', '*.*'))
            filename = fd.askopenfilename(title='Open a file',initialdir='/',filetypes=filetypes)
            #add the selected excel file to the excelfile list
            excelfile.append(filename)

            #split and remove the path of the selected file and be left with that main filename
            head, tail = os.path.split(filename)
            mainfilename = tail
            selectedfilespace.set(mainfilename)

        #Buttons
        self.label7= Label(self.master, text="File Selected: ", textvariable=selectedfilespace, font = fontStyle2).place(relx = 0.5, rely = 0.15, anchor = CENTER)
        #creating a checkbox to allow view boxplot
        #self.btn5 = tk.Checkbutton(self.master, text="show boxplot", command=boxplot, font=fontStyle)
        #self.btn5.place(relx = 0.5, rely = 0.33  , anchor = CENTER)
        self.btn2 = tk.Button(self.master,text='Open a File',font= fontStyle1, command=select_file).place(relx = 0.5, rely = 0.07, anchor = CENTER)
        self.btn3 = tk.Button(self.master,text='Analyse',font= fontStyle1, command=analyse).place(relx = 0.5, rely = 0.40, anchor = CENTER)
                        
    #function to clear the current page to view the previous page elements
    def load_back(self):
        self.entry_1.destroy()
        self.entry_2.destroy()
        self.label1.destroy()
        self.label2.destroy()
        self.label3.destroy()
        self.label7.destroy()
        self.btn1.destroy()
        self.btn2.destroy()
        self.btn3.destroy()
        excelfile.clear()
        predicted_vals.clear()

        self.another = mainwindow(self.master)


class multiplelinearreg:
    def __init__(self, master):
        # keep `root` in `self.master`
        self.master = master

        #back button to view previous page, that is the main page
        self.btn1 = tk.Button(self.master, text ="BACK", font = fontStyle1, command = self.load_back).place(relx = 0.90, rely = 0.84, anchor = CENTER)
        self.label1 = Label(self.master, text="File Selected:", font = fontStyle2).place(relx = 0.3, rely = 0.15, anchor = CENTER)
        self.label2 = Label(self.master, text="Dependent Variable: ", font = fontStyle2).place(relx = 0.3, rely = 0.20, anchor = CENTER)
        self.label3= Label(self.master, text="Independent Variable one : ", font = fontStyle2).place(relx = 0.3, rely = 0.25, anchor = CENTER)
        self.label4= Label(self.master, text="Independent Variable two : ", font = fontStyle2).place(relx = 0.3, rely = 0.30, anchor = CENTER)

        #entry box for dependent and independent variavles
        self.entry_1 = Entry(self.master).place(relx = 0.5, rely = 0.20, anchor = CENTER)
        self.entry_2 = Entry(self.master).place(relx = 0.5, rely = 0.25, anchor = CENTER)
        self.entry_3 = Entry(self.master).place(relx = 0.5, rely = 0.30, anchor = CENTER)

        #function for all the one way anova analysis   
        def analyse():
            #Check if a file selected whenever the user clicks "Analyse" button and showinformation if there is no file selected
            if len(excelfile) == 0:
                messagebox.showinfo("showinfo", "Please, select a file")
            #Continue with the analysis if a file is selected
            else:
                entry_1 = (self.entry_1.get())
                entry_2 = (self.entry_2.get())
                entry_3 = (self.entry_3.get())
                for file in excelfile:
                    data = pd.read_excel(file)
                    
                    #getting the values in the selected columns
                    independent_var1_column = data['%s' %(entry_2)]
                    independent_var2_column = data['%s' %(entry_3)]
                    dependent_var_column = data['%s' %(entry_1)]

                    independent_vars = []
                    independent_var1 = list(independent_var1_column)
                    independent_var2 = list(independent_var2_column)
                    length = len(independent_var1)
                    for i in range(0, length):
                        independent_vars.append([independent_var1[i], independent_var2[i]])
                    print(independent_vars)
                    dependent_var = list(dependent_var_column)

                    independent_vars = np.array(independent_vars)
                    dependent_var = np.array(dependent_var)

                    independent_vars = sm.add_constant(independent_vars)
                    model = sm.OLS(dependent_var, independent_vars)
                    result = model.fit()
                    summary = result.summary()
                    print(result.summary())

                    model2 = LinearRegression().fit(independent_vars, dependent_var)
                    interc = model2.intercept_
                    print("Intercept: ", interc)

                    slop = model2.coef_
                    print("Slope: ", slop)

                    y_pred = model2.predict(independent_vars)
                    print("predicted response: ", y_pred)

                    equation = "EQUATION: "+ " "+ str(entry_1) + " " + "=" +" " + str(round(interc, 2)) + " " + "+" +" " + str(round(slop[1], 2))+str(entry_2) + " " + "+" + str(round(slop[2], 2))+str(entry_3)

                    for num in independent_var1:
                        slops1.append(slop[1]*num)
                    for num in independent_var2:
                        slops2.append(slop[2]*num)
                    
                    for num in range(0, len(independent_var1)):
                        predicted_val = "PREDICTED VALUE OF "+ str(entry_1) + " "+ "IF "+ str(entry_2)+ " = "+ str(independent_var1[num])+" and "+ str(entry_3)+ " = "+str(independent_var2[num]) + " is " + str(round(interc+ (slops1[num]) + (slops2[num]), 2))
                        predicted_vals.append("%s \n" %(predicted_val))

                    #setting up newwindow to embed the result on
                    newwindow = Toplevel()      #TOPLEVEL() USED
                    newwindow.title("RESULT WINDOW - MULTIPLE LINEAR REGRESSION")

                    #setting space to view result on inside of the new window
                    space1 = tk.StringVar()
                    space2 = tk.StringVar()
                    space1.set(summary)
                    space2.set(equation)
                    self.label5= Label(newwindow, text="", textvariable=space1, font = fontStyle2).pack(fill="y")
                    self.label6= Label(newwindow, text="", textvariable=space2, font = fontStyle2).pack(fill="y")

                    for i in range(0, len(independent_var1)):
                        independent_var1[i] = tk.StringVar()
                        independent_var1[i].set(predicted_vals[i])
                        self.label7= Label(newwindow, text="", textvariable=independent_var1[i], font = fontStyle2).pack(fill="y")
                        print(predicted_vals[i])

                    #set the height and width and run newwindow
                    height = newwindow.winfo_screenheight() #get your Windows height size 
                    newwindow.geometry("%dx%d" % (800, height))
                    newwindow.resizable(False,False)
                    newwindow.mainloop()

        #settinf up space to view the name of selected file
        selectedfilespace = tk.StringVar()
        
        #function for selecting excel file to be used in the analysis
        def select_file():
            filetypes = (('text files', '*.xlsx'),('All files', '*.*'))
            filename = fd.askopenfilename(title='Open a file',initialdir='/',filetypes=filetypes)
            #add the selected excel file to the excelfile list
            excelfile.append(filename)

            #split and remove the path of the selected file and be left with that main filename
            head, tail = os.path.split(filename)
            mainfilename = tail
            selectedfilespace.set(mainfilename)

        self.label8= Label(self.master, text="File Selected: ", textvariable=selectedfilespace, font = fontStyle2).place(relx = 0.5, rely = 0.15, anchor = CENTER)
        #creating a checkbox to allow view boxplot
        #self.btn5 = tk.Checkbutton(self.master, text="show boxplot", command=boxplot, font=fontStyle)
        #self.btn5.place(relx = 0.5, rely = 0.33  , anchor = CENTER)
        self.btn2 = tk.Button(self.master,text='Open a File',font= fontStyle1, command=select_file).place(relx = 0.5, rely = 0.07, anchor = CENTER)
        self.btn3 = tk.Button(self.master,text='Analyse',font= fontStyle1, command=analyse).place(relx = 0.5, rely = 0.40, anchor = CENTER)
                        
    #function to clear the current page to view the previous page elements
    def load_back(self):
        self.entry_1.destroy()
        self.entry_2.destroy()
        self.entry_3.destroy()
        self.label1.destroy()
        self.label2.destroy()
        self.label3.destroy()
        self.label4.destroy()
        self.label8.destroy()
        self.btn1.destroy()
        self.btn2.destroy()
        self.btn3.destroy()
        excelfile.clear()
        predicted_vals.clear()
        slops1.clear()
        slops2.clear()

        self.another = mainwindow(self.master)



#set default window as mainwindow and run
mainwindow(window)
window.mainloop()
