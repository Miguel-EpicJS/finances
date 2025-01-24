from tkinter import *
from tkinter import ttk

class InterestConversor: 

    def __init__(self, root):
        root.title = "Compound Interest Conversor"

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.monthly = StringVar()
        monthly_entry = ttk.Entry(mainframe, width=7, textvariable=self.monthly)
        monthly_entry.grid(column=2, row=1, sticky=(W, E))

        self.yearly= StringVar()
        yearly_entry = ttk.Entry(mainframe, width=7, textvariable=self.yearly)
        yearly_entry.grid(column=2, row=2, sticky=(W, E))

        ttk.Button(mainframe, text="Calculate Monthly to Yearly", command=self.calculate_monthly).grid(column=3, row=3, sticky=W)
        ttk.Button(mainframe, text="Calculate Yearly to Monthly", command=self.calculate_yearly).grid(column=2, row=3, sticky=W)

        ttk.Label(mainframe, text="per month").grid(column=3, row=1, sticky=W)
        ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
        ttk.Label(mainframe, text="per year").grid(column=3, row=2, sticky=W)

        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        monthly_entry.focus()

    def calculate_yearly(self, *args):
        yearly_interest  = float((self.yearly.get()).rstrip("%"))/100
        self.monthly.set(f"{round(((1+yearly_interest)**(1/12)-1)*100, 4)}%")

    def calculate_monthly(self, *args):
        monthly_interest  = float((self.monthly.get()).rstrip("%"))/100
        self.yearly.set(f"{round(((1+monthly_interest)**(12)-1)*100, 4)}%")



root = Tk()
InterestConversor(root)
root.mainloop()
