from tkinter import *
from tkinter import ttk

import time
import HumanDataBase

def simulate_humans():
    
    global simulation_area_xmeters
    global simulation_area_ymeters
    global simulation_timelapse_val
    simulation_timelapse_val = 1.0
    global start_Infected
    global totalPopulation
    global max_distance

    global Simulator
    Simulator = HumanDataBase.Simulation()
    Simulator.InitModule()

    def setStartSim():
        if entryXmeters.get() != "":
            try:
                simulation_area_xmeters = int(entryXmeters.get())
            except:
                entryXmeters.setvar("")
                simulation_area_xmeters = 0
        else:
            simulation_area_xmeters = 300
        
        if entryYmeters.get() != "":
            try:
                simulation_area_ymeters = int(entryYmeters.get())
            except:
                entryYmeters.setvar("")
                simulation_area_ymeters = 0
        else:
            simulation_area_ymeters = 200
        
        if entryInfected.get() != "":
            try:
                start_Infected = int(entryInfected.get())
            except:
                entryInfected.setvar("")
                start_Infected = 0
        else:
            start_Infected = 2
        
        if entryPopulation.get() != "":
            try:
                totalPopulation= int(entryPopulation.get())
            except:
                entryPopulation.setvar("")
                totalPopulation = 0
        else:
            totalPopulation = 50

        if entryDistance.get() != "":
            try:
                max_distance= int(entryDistance.get())
            except:
                entryDistance.setvar("")
                max_distance = 0
        else:
            max_distance = 50

        if simulation_area_xmeters > 0 and simulation_area_ymeters > 0 and start_Infected > 0 and totalPopulation > 0:
            Simulator.Initialize(simulation_area_xmeters, simulation_area_ymeters, totalPopulation, start_Infected, max_distance)
    
    def setStopSim ():
        Simulator.Terminate()
    
    def setIncTime ():
        global simulation_timelapse_val
        simulation_timelapse_val =simulation_timelapse_val * 2
        print(simulation_timelapse_val)
    
    def setDecTime ():
        global simulation_timelapse_val
        simulation_timelapse_val = simulation_timelapse_val/2
        if simulation_timelapse_val < 1.0:
            simulation_timelapse_val = 1.0
        print(simulation_timelapse_val)
    
    root=Tk()

    root.title("Eingabefenster")

    mainFrame=ttk.Frame(root, borderwidth=2, relief='solid', width=460, height=380, padding='20')
    mainFrame.grid_propagate(0)
    mainFrame.grid(column=0, row=0)
    mainFrame.columnconfigure(0, weight=1)
    mainFrame.columnconfigure(1, weight=1)
    mainFrame.columnconfigure(2, weight=1)
    mainFrame.columnconfigure(3, weight=1)
    mainFrame.rowconfigure(0, weight=2)
    mainFrame.rowconfigure(1, weight=1)
    mainFrame.rowconfigure(2, weight=1)
    mainFrame.rowconfigure(3, weight=1)
    mainFrame.rowconfigure(4, weight=1)
    mainFrame.rowconfigure(5, weight=1)
    mainFrame.rowconfigure(6, weight=1)
    mainFrame.rowconfigure(7, weight=2)
    mainFrame.rowconfigure(8, weight=2)

    Überschrift=Label(mainFrame, text="Kontrollfeld", font=('arial', 20))
    Überschrift.grid(column=0, row=0, columnspan=4)

    LabelN=Label(mainFrame, text="Anzahl der Personen insgesamt:", font=('arial', 12))
    LabelN.grid(column=0, row=1, columnspan=3)
    LabelI=Label(mainFrame, text="Anzahl der zu Beginn Infizierten", font=('arial', 12))
    LabelI.grid(column=0, row=2, columnspan=3)
    Labelxmeters=Label(mainFrame, text="Breite (X Meter)", font=('arial', 12))
    Labelxmeters.grid(column=0, row=3, columnspan=3)
    Labelymeters=Label(mainFrame, text="Höhe (Y Meters)", font=('arial', 12))
    Labelymeters.grid(column=0, row=4, columnspan=3)
    Labeldistance=Label(mainFrame, text="Distanz (Meters)", font=('arial', 12))
    Labeldistance.grid(column=0, row=5, columnspan=3)
    Labelvelocity=Label(mainFrame, text="Geschwindigkeit der Simulation", font=('arial', 12))
    Labelvelocity.grid(column=0, row=6, columnspan=3)
    timetext = StringVar()
    timetext.set("Test")
    Labelvelodisp = Label(mainFrame, textvariable=timetext, font=('arial', 11))
    Labelvelodisp.grid(column=3, row=6, columnspan=3)

    entryPopulation=Entry(mainFrame, width=10)
    entryPopulation.grid(column=3, row=1)
    entryInfected=Entry(mainFrame, width=10)
    entryInfected.grid(column=3, row=2)
    entryXmeters=Entry(mainFrame, width=10)
    entryXmeters.grid(column=3, row=3)
    entryYmeters=Entry(mainFrame, width=10)
    entryYmeters.grid(column=3, row=4)
    entryDistance=Entry(mainFrame, width=10)
    entryDistance.grid(column=3, row=5)

    Button(mainFrame, text="langsamer", command=setDecTime, width=16, font=('arial', 15)).grid(column=0, row=7, columnspan=2)    
    Button(mainFrame, text="schneller", command=setIncTime, width=16, font=('arial', 15)).grid(column=2, row=7, columnspan=2)
    Button(mainFrame, text="Start Simulation", command=setStartSim, width=16, font=('arial', 15)).grid(column=0, row=8, columnspan=2)
    Button(mainFrame, text="Stop Simulation", command=setStopSim, width=16, font=('arial', 15)).grid(column=2, row=8, columnspan=2)

    print("Simulation started")
    while True:
        start = time.time()

        Simulator.Simulate(simulation_timelapse_val)

        timestr = Simulator.GetSimulationTime()

        ticks = time.time() - start
        timetext.set(timestr)

        root.update()


simulate_humans()