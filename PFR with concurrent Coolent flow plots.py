import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import math
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# graph generator 1

Tref1,k0,Tref2,kc0,DeltaHR,T0,E,Ta0,Ua,FA0,CPA,CA0,m_cool,cp_cool,delCp = [1 for x in range(15)]
R = 8.314

def delHr(T):
    return DeltaHR + delCp * (T - 298)

def Kc(T):
    return kc0 * math.exp(-1 * (DeltaHR/R) * (1/T - 1/Tref2))

def k(T):
    return k0 * math.exp(-1 * (E / R) * (1/T - 1/Tref1)) 

def neg_r_a(T,x):
    return k(T) * CA0*((1-x)*T0/T - x * T0/T/Kc(T))

def dxdV(T, Ta, x, V):
    return neg_r_a(T, x)/FA0

def dTdV(T, Ta, x, V):
    return (Ua * (Ta - T) + neg_r_a(T, x) *(-1) * delHr(T))/FA0/(CPA + x*delCp)

def dTadV(T, Ta, x, V) : 
    return Ua * (T - Ta)/m_cool/cp_cool

# Define the differential equation function
def diff_eq(t, y):
    return [dTdV(y[0], y[1], y[2], t), dTadV(y[0], y[1], y[2], t), dxdV(y[0], y[1], y[2], t)]

def loadGraphOnCanvas(sol):
    # Create a simple plot
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.plot(sol.t, sol.y[2], label="X")
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row = 17, column = 0, padx=10, pady=10)
    
    fig2, ax2 = plt.subplots(figsize=(4, 4))
    ax2.plot(sol.t, sol.y[1], label="Ta(K)")
    ax2.plot(sol.t, sol.y[0], label="T(K)")
    canvas2 = FigureCanvasTkAgg(fig2, master=root)
    canvas2.draw()
    canvas2.get_tk_widget().grid(row = 17, column = 1, padx=10, pady=10, columnspan=2)

    ax.set_xlabel('V(10^4 m3)')
    ax.set_ylabel('X')
    ax2.set_xlabel('V(10^4 m3)')
    ax2.set_ylabel('Temperature (K)')
    ax.legend()
    ax2.legend()


#     button = tk.Button(popup, text="OK", command=on_button_click)
#     button.pack(padx=10, pady=10)

#     popup.mainloop()
def convert_to_float(x, i):
    try:
        return float(x)
    except:
        # a default value is returned in case the x is not a number
        return [1035, 3.58, 298, 100, 80770, 1035, 284521.708, 1250, 16500, 0.0376, 163, 18.8, 0.111, 34.5, -9][i]

def generate_graph():
    global Tref1,k0,Tref2,kc0,DeltaHR,T0,E,Ta0,Ua,FA0,CPA,CA0,m_cool,cp_cool,delCp
    
    # print([x.get() for x in inputBoxes])
    Tref1,k0,Tref2,kc0,DeltaHR,T0,E,Ta0,Ua,FA0,CPA,CA0,m_cool,cp_cool,delCp = [convert_to_float(x.get(), i) for i,x in enumerate(inputBoxes)]
    # Tref1,k0,Tref2,kc0,DeltaHR,T0,E,Ta0,Ua,FA0,CPA,CA0,m_cool,cp_cool,delCp = [1035, 3.58, 298, 100, 80770, 1035, 284521.708, 1250, 16500, 0.0376, 163, 18.8, 0.111, 34.5, -9]
    # TODO remove the above line



    t_eval = np.linspace(0, 0.001, 1000)
    y0 = [T0, Ta0, 0]  # Initial reactor temperature, coolant temperature, and conversion

    # sol = solve_ivp(diff_eq, (0, 100), y0, t_eval=t_eval, method='BDF', rtol=1e-4, atol=1e-6, max_step=1)
    sol = solve_ivp(diff_eq, (0, 0.001), y0, t_eval=t_eval, method='BDF',rtol=1e-6, atol=1e-8, max_step=0.1)
    loadGraphOnCanvas(sol)


    # Plot the solution
    #plt.plot(sol.t, sol.y[0], label="T")
    #plt.plot(sol.t, sol.y[1], label="Ta")
#     plt.plot(sol.t, sol.y[2], label="x")
#     plt.xlabel('V')
#     plt.ylabel('State variables')
# #     plt.title("Solution of the differential equations")
#     plt.legend()
#     plt.grid()
#     plt.show()
    

# Create the main window
root = tk.Tk()

# Heading
heading_label = tk.Label(root, text="PFR with concurrent Coolent flow plots", font=("Helvetica", 15, "bold"))
heading_label.grid(row = 0, column = 1, padx = 5, pady = 5)



# Labels
LabelList = [
    "Reference Temperatre for specific rate constant:",
     "Specific rate at above reference temperature:",
     "Reference temperature for equilibrium constant:",
     "Equilibrium constant at the above reference temperature:",
     "Heat of Reaction at the above reference temperature(in J/mol):",
     "Feed temperature(T0)",
     "Activation energy(in J/mol)",
     "Coolant input temperature (parallel flow):",
     "UA (heat transfer coefficient * exchange area per unit volume):",
     "Molar Feed Rate:",
     "Molar heat capacity of A:",
     "Feed concentration of A:",
     "Mass flow rate of coolant:",
     "Specific heat capacity of coolant:",
     "Delta Cp of reaction:"
]

# labels and input boxes
inputBoxes = []
for i in range(15):
    tk.Label(root, text=LabelList[i]).grid(row=i//2 + 1, column=2*(i % 2), padx=10, pady=5)
    inputBoxes.append(tk.Entry(root))
    inputBoxes[i].grid(row = i//2 + 1, column = 2*(i % 2) + 1, padx = 5, pady = 5)

# Create a Button widget to submit the input
submit_button = tk.Button(root, text="Generate Graph", command=generate_graph)
submit_button.grid(row=16, column=0, columnspan=2, padx=10, pady=10)

# Run the main loop
root.mainloop()