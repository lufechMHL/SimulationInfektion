#=====================================================================================================
#   Projekt Seminararbeit SimulationInfektion
#   Modul GUI - grafische Darstellung der Simulation
#   
#   Changelog
#   2021-01-29  -   Erstellung
#   2021-02-28  -   Umstellung Animation auf pygame
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
# width of the simulation window
simulation_window_width=1300
# height of the simulation window
simulation_window_height=800
# background color 
simulation_backgroundcolor = colour.dark_green
# radius of the ball
simulation_ball_radius = 5
# delay between successive frames in seconds
simulation_refresh_seconds = 0.01
#endregion
 
#region create and animate humans in an infinite loop
#def simulate_humans(window, canvas):
def simulate_humans():
    #region initialize Simulatorbase
    maxx, maxy = HumanDataBase.GetAreaSize()

    simulation_scale_meter2pixel = maxx / simulation_window_width
    simulation_window_height = math.floor( maxy / simulation_scale_meter2pixel)
    simulation_ball_radius = math.ceil(0.5 / simulation_scale_meter2pixel)

    HumanDataBase.Initialize()
    if simulation_ball_radius < 2:
        simulation_ball_radius = 2
    #endregion

    #region Init pygame
    pygame.init()
    pygame.display.set_caption('SimulationInfection St-El-Lu')
    pygame.key.set_repeat(250, 125)
    screen = pygame.display.set_mode((simulation_window_width, simulation_window_height))
    font = pygame.font.Font('consola.ttf', 20)

    table = pygame.Surface((simulation_window_width, simulation_window_height))
    table.fill(simulation_backgroundcolor)
    screen.blit(table, (0,0))
    pygame.display.flip()
    #endregion

    #region init tkinter
    root= tk.Tk()
    canvas1 = tk.Canvas(root, width = 400, height = 300)
    canvas1.pack()
    entry1 = tk.Entry (root) 
    canvas1.create_window(200, 140, window=entry1)

    def getSquareRoot ():  
        simulation_ball_radius = int(entry1.get())
        #label1 = tk.Label(root, text= float(x1)**0.5)
        canvas1.create_window(200, 230, window=label1)
        
    button1 = tk.Button(text='Get the Square Root', command=getSquareRoot)
    canvas1.create_window(200, 180, window=button1)
    #endregion

    #region main-loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE):
                sys.exit()

        start = time.time()

        for x in range(len(HumanDataBase.HumanList)):  
            #aktuelle grafik ausblenden - mit Background-color übermalen
            xval = HumanDataBase.HumanList[x].Status.CurPos.X / simulation_scale_meter2pixel
            yval = HumanDataBase.HumanList[x].Status.CurPos.Y / simulation_scale_meter2pixel
            pygame.draw.circle(table, simulation_backgroundcolor,(xval,yval),simulation_ball_radius, 0)    

            #neue Position berechnen
            HumanDataBase.HumanList[x].Go()

            #neue Position zeichnen
            xval = HumanDataBase.HumanList[x].Status.CurPos.X / simulation_scale_meter2pixel
            yval = HumanDataBase.HumanList[x].Status.CurPos.Y / simulation_scale_meter2pixel
            pygame.draw.circle(table, colour.light_yellow,(xval,yval),simulation_ball_radius, 0)    

        #frame auf Display blenden
        screen.blit(table, (0,0))
        pygame.display.flip()
        time.sleep(simulation_refresh_seconds)

        ticks = time.time() - start
        print(ticks)

        root.update()
    #endregion
#endregion 

#region main-program ------------------------------------------------------------------------------------------
simulate_humans()
#endregion ----------------------------------------------------------------------------------------------------

