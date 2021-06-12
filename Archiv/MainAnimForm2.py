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
            Simulator.Initialize(simulation_area_xmeters, simulation_area_ymeters, start_Infected, totalPopulation)
    
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
        #print(simulation_timelapse_val)
    
    root=Tk()

    root.title("Eingabefenster")

    mainFrame=ttk.Frame(root, borderwidth=2, relief='solid', width=460, height=460, padding='20')
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
    mainFrame.rowconfigure(7, weight=1)
    mainFrame.rowconfigure(8, weight=1)
    mainFrame.rowconfigure(9, weight=1)
    mainFrame.rowconfigure(10, weight=1)
    mainFrame.rowconfigure(11, weight=1)
    mainFrame.rowconfigure(12, weight=2)

    Ueberschrift=Label(mainFrame, text="Eingabe", font=('arial', 20))
    Ueberschrift.grid(column=0, row=0, columnspan=4)

    LabelN=Label(mainFrame, text="Anzahl der Personen insgesamt:", font=('arial', 12))
    LabelN.grid(column=0, row=1, columnspan=3)
    LabelI=Label(mainFrame, text="Anzahl der zu Beginn Infizierten", font=('arial', 12))
    LabelI.grid(column=0, row=2, columnspan=3)
    Labelxmeters=Label(mainFrame, text="Breite (X Meters)", font=('arial', 12))
    Labelxmeters.grid(column=0, row=3, columnspan=3)
    Labelymeters=Label(mainFrame, text="Höhe (Y Meters)", font=('arial', 12))
    Labelymeters.grid(column=0, row=4, columnspan=3)
    Labeldistance=Label(mainFrame, text="Distance (Meters)", font=('arial', 12))
    Labeldistance.grid(column=0, row=5, columnspan=3)
    Labelvelocity=Label(mainFrame, text="Geschwindigkeit der Simulation", font=('arial', 12))
    Labelvelocity.grid(column=0, row=6, columnspan=3)
    timetext = StringVar()
    timetext.set("Test")
    Labelvelodisp = Label(mainFrame, textvariable=timetext, font=('arial', 11))
    Labelvelodisp.grid(column=3, row=6)

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

    Labelgreen=Label(mainFrame, text="für die Krankheit empfängliche Personen (S): grün dargestellt", font=('arial', 12))
    Labelgreen.grid(column=0, row=7, columnspan=4)
    Labellightred=Label(mainFrame, text="infizierte Personen (I): hellrot dargestellt", font=('arial', 12))
    Labellightred.grid(column=0, row=8, columnspan=4)
    Labeldarkred=Label(mainFrame, text="erkrankte Personen (I): dunkelrot dargestellt", font=('arial', 12))
    Labeldarkred.grid(column=0, row=9, columnspan=4)
    Labelblue=Label(mainFrame, text="immune und gestorbene Personen (R): blau dargestellt", font=('arial', 12))
    Labelblue.grid(column=0, row=10, columnspan=4)

    Button(mainFrame, text="langsamer", command=setDecTime, width=16, font=('arial', 15)).grid(column=0, row=11, columnspan=2)    
    Button(mainFrame, text="schneller", command=setIncTime, width=16, font=('arial', 15)).grid(column=2, row=11, columnspan=2)
    Button(mainFrame, text="Start Simulation", command=setStartSim, width=16, font=('arial', 15)).grid(column=0, row=12, columnspan=2)
    Button(mainFrame, text="Stop Simulation", command=setStopSim, width=16, font=('arial', 15)).grid(column=2, row=12, columnspan=2)

    print("Simulation started")
    
    while True:
        start = time.time()

        Simulator.Simulate(simulation_timelapse_val)

        timestr = Simulator.GetSimulationTime()

        ticks = time.time() - start
        timetext.set(timestr)

        root.update()


simulate_humans()
