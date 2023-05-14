import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import math
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def convert_to_float(x, i):
    try: return float(x)
    except: return [298, 10**5, 300, -20000, 50, 0][i]

LabelList = [ 
    "reference temperature for equilibrium constant? ",
    "equilibrium constant at the above reference temperature? ",
    "feed temperature(T0)? ",
    "Heat of Reaction at 298K? ",
    "molar heat capacity of A? ",
    "delta Cp of reaction? "
]

Tref2, kc0, T0, DeltaHR, CPA, delCp = [1 for _ in range(6)]
R = 1.987 # TODO should I also give a box for inputing R



root = tk.Tk()


#Heading
heading_label = tk.Label(root, text="Calculator for Xe in adiabetic reactor", font=("Helvetica", 24, "bold"))
heading_label.grid(row = 0, column = 0, padx = 5, pady = 5)


#InputBoxes
inputBoxes = []
for i in range(6):
    tk.Label(root, text=LabelList[i]).grid(row=i + 1, column=0, padx=20, pady=5)
    inputBoxes.append(tk.Entry(root))
    inputBoxes[i].grid(row = i + 1, column = 1, padx = 5, pady = 5)


def delHr(T):
    return DeltaHR + delCp * (T - Tref2)

def Kc(T):
    return kc0 * math.exp(-1 * DeltaHR/R * (1/T - 1/Tref2))

def xe(kc):
    return kc / (1 + kc)

def x(T):
    return CPA * (T - T0) / (-1 * delHr(T))


def loadGraphOnCanvas():
    global Tref2, kc0, T0, DeltaHR, CPA, delCp
    Tref2, kc0, T0, DeltaHR, CPA, delCp = [convert_to_float(x.get(), i) for i, x in enumerate(inputBoxes)]


    t_eval = []
    y_xe = []
    y_x = []

    for i in range(300, 601):
        t_eval.append(i)

    for i in range(len(t_eval)):
        y_xe.append(xe(Kc(t_eval[i])))    
        y_x.append(x(t_eval[i]))

     
    # Create a simple plot
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.plot(t_eval, y_x, label="X")
    ax.plot(t_eval, y_xe, label="Xe")
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row = 11, column = 0,  padx=5, pady=5)
    ax.legend()
    ax.set_xlabel('Temperature(K)')
    ax.set_ylabel('X')
    
    # fig2, ax2 = plt.subplots(figsize=(4, 4))
    # ax2.plot(t_eval, y_xe, label="xe")
    # canvas2 = FigureCanvasTkAgg(fig2, master=root)
    # canvas2.draw()
    # canvas2.get_tk_widget().grid(row = 10, column = 1, padx=5, pady=5)



# print(t_eval)
# print(y_xe)  
# print(y_x)  

# # Plot the solution
# #plt.plot(sol.t, sol.y[0], label="T")
# plt.plot(t_eval, y_x, label="x")
# plt.plot(t_eval, y_xe, label="xe")
# plt.xlabel('V')
# plt.ylabel('State variables')
# plt.title("Solution of the differential equations")
# plt.legend()
# plt.grid()
# plt.show()

submit_button = tk.Button(root, text="Show The results", command=loadGraphOnCanvas)
submit_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)


root.mainloop()