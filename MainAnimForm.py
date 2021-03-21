#=====================================================================================================
#   Projekt Seminararbeit SimulationInfektion
#   Modul GUI - grafische Darstellung der Simulation
#   
#   Changelog
#   2021-01-29  -   Erstellung
#   2021-02-28  -   Umstellung Animation auf pygame
#   2021-03-21  -   Verlagerung Pygame in ext. Modul HumanDatabase und Steuerung der Simulation über Dialog begonnen
#=====================================================================================================

#import tkinter
#python -python -m pip install -U pygame --user

import tkinter as tk
import pygame
from pygame.locals import *

import colour
import time
import sys
import math
import HumanDataBase


#region constant definitions 
#x-range area in meters
simulation_area_xmeters = 200
#y-range area in meters
simulation_area_ymeters = 120
#count of humans in the area
simulation_human_count = 50
# delay between successive frames in seconds
simulation_refresh_seconds = 0.01
#endregion

#region MainForm

#def simulate_humans(window, canvas):
def simulate_humans():
    #region initialize Simulatorbase
    #maxx, maxy = HumanDataBase.GetAreaSize()
    global Simulator
    Simulator = HumanDataBase.Simulation()
    Simulator.InitModule()
    #endregion

    #region Event-Handler 
    #region Event-handler für Button StartSim
    def setStartSim ():  

        if entryXmeters.get() != "":
            #Input einlesen und prüfen
            try:
                simulation_area_xmeters = int(entryXmeters.get())
            except:
                entryXmeters.setvar("")
                simulation_area_xmeters = 0
        else:
            simulation_area_xmeters = 200

        if entryYmeters.get() != "":
            #Input einlesen und prüfen
            try:
                simulation_area_ymeters = int(entryYmeters.get())
            except:
                entryYmeters.setvar("")
                simulation_area_ymeters = 0
        else:
            simulation_area_ymeters = 100

        if entryHumans.get() != "":
            #Input einlesen und prüfen
            try:
                simulation_human_count = int(entryHumans.get())
            except:
                entryHumans.setvar("")
                simulation_human_count = 0
        else:
            simulation_human_count = 30

        #Wenn Input gültig ist, Initialisierung ausführen
        if simulation_area_xmeters > 0 and simulation_area_ymeters > 0 and simulation_human_count > 0:
            Simulator.Initialize(simulation_area_xmeters, simulation_area_ymeters, simulation_human_count)
    #endregion

    #region Event-Handler für Button StopSim
    def setStopSim ():  
        Simulator.Terminate()
    #endregion


    #endregion

    #region init tkinter
    root= tk.Tk()
    canvas1 = tk.Canvas(root, width = 400, height = 300)
    canvas1.pack()
    #Definition der Eingabefelder
    entryXmeters = tk.Entry (root) 
    entryYmeters = tk.Entry (root) 
    entryHumans = tk.Entry (root) 

    #Definition der Labels/Bezeichner
    label1 = tk.Label(root, text= "Breite X Meter")
    label2 = tk.Label(root, text= "Höhe Y Meter")
    label3 = tk.Label(root, text= "Anz Personen")

    #Erzeugung der Windows zu den obigen Objekten im Windows
    canvas1.create_window(50, 100, window=label1)    
    canvas1.create_window(200, 100, window=entryXmeters)
    canvas1.create_window(50, 130, window=label2)    
    canvas1.create_window(200, 130, window=entryYmeters)
    canvas1.create_window(50, 160, window=label3)    
    canvas1.create_window(200, 160, window=entryHumans)

    #Definition der Funktionsknöpfe Button 
    buttonStart = tk.Button(text='Start Simulation', command=setStartSim) #Verknüpfung mit dem Event-Handler!!!!
    buttonStop = tk.Button(text='Stop Simulation', command=setStopSim)  #Verknüpfung mit dem Event-Handler!!!!
    canvas1.create_window(50, 200, window=buttonStart)
    canvas1.create_window(200, 200, window=buttonStop)
    #endregion

    #region main-loop
    while True:
        start = time.time()

        #Simulation ausführen im Modul HumanDataBase
        Simulator.Simulate()

        ticks = time.time() - start
        print(ticks)

        root.update()
    #endregion
#endregion 

#region main-program ------------------------------------------------------------------------------------------
simulate_humans()
#endregion ----------------------------------------------------------------------------------------------------

