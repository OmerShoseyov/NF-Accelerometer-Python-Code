from tkinter import *
import time


def T():
    for i in range(len(names_T)):
        vars_T[i].set(1)
    root.update()

def B():
    for i in range(len(names_T)):
        vars_T[i].set(0)
    root.update()


root = Tk()
root.title("Testing Checkbox")
#root.geometry("200x200")

f0 = Frame(root, bd=5, relief=RAISED)
f1 = Frame(f0, bd=5)
f2 = Frame(f0, bd=5)
f3 = Frame(f0, bd=5)
f4 = Frame(f0, bd=5)

f0.grid(row=1, column=0, sticky=N)
f1.grid(row=0, columnspan=2, sticky=N)
f2.grid(row=1, column=1, sticky=NE)
f3.grid(row=1, column=0, sticky=NW)
f4.grid(row=2, columnspan=2, rowspan=2, sticky=S)

names_T = ["T_1", "T_2", "T_3", "T_4", "T_5", "T_6"]
names_B = ["B_1", "B_2", "B_3", "B_4", "B_5", "B_6"]
names_R = ["R_1", "R_2", "R_3", "R_4", "R_5", "R_6"]
names_L = ["L_1", "L_2", "L_3", "L_4", "L_5", "L_6"]


vars_T = []
vars_B = []
vars_R = []
vars_L = []

for i, checkboxname in enumerate(names_T):
    vars_T.append(IntVar())
    check = Checkbutton(f1, text=checkboxname, variable=vars_T[i], font=('Ariel 14'))
    check.grid(row=0, column=i)#pack(side=LEFT, padx=2, pady=2, expand=TRUE, anchor="n")

for i, checkboxname in enumerate(names_B):
    vars_B.append(IntVar())
    check = Checkbutton(f4, text=checkboxname, variable=vars_B[i], font=('Ariel 14'))
    check.grid(row=1, column=i)#pack(side=LEFT, padx=2, pady=2, expand=TRUE, anchor="s")

for i, checkboxname in enumerate(names_R):
    vars_R.append(IntVar())
    check = Checkbutton(f2, text=checkboxname, variable=vars_R[i], font=('Ariel 14'))
    check.grid(row=i, column=1)#pack(side=TOP, padx=2, pady=2, expand=TRUE, anchor="w")

for i, checkboxname in enumerate(names_L):
    vars_L.append(IntVar())
    check = Checkbutton(f3, text=checkboxname, variable=vars_L[i], font=('Ariel 14'))
    check.grid(row=i, column=0)#pack(side=TOP, padx=2, pady=2, expand=TRUE, anchor="e")

T_button = Button(f1, text="T", font=("Ariel 12 bold"), width=6, height=1, command=T, activebackground='green').grid(row=1, column=0, columnspan=6)
B_button = Button(f4, text="B", font=("Ariel 12 bold"), width=6, height=1, command=B, activebackground='green').grid(row=0, column=0, columnspan=6)
R_button = Button(f2, text="R", font=("Ariel 12 bold"), width=2, height=3, command=T, activebackground='green').grid(row=0, rowspan=6, column=0)
L_button = Button(f3, text="L", font=("Ariel 12 bold"), width=2, height=3, command=T, activebackground='green').grid(row=0, rowspan=6, column=1)

""" while TRUE:
    if vars_T[0].get() == 1:
        print(names_T[0] + ' = ' + '1')
    else:
        print(names_T[0] + ' = ' + '0')
    root.update()
    time.sleep(1) """


root.mainloop()


