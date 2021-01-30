#=====================================================================================================
#   Projekt Seminararbeit SimulationInfektion
#   Modul GUI - grafische Darstellung der Simulation
#   
#   Changelog
#   2021-01-29  -   Erstellung
#=====================================================================================================

import tkinter
import time
import HumanDataBase


#region constant definitions 
# width of the simulation window
simulation_window_width=1500
# height of the simulation window
simulation_window_height=800
# radius of the ball
simulation_ball_radius = 5
# delay between successive frames in seconds
simulation_refresh_seconds = 0.01
# Scale pixel / meters
simulation_scale_meter2pixel = 0.05
# Scale time multiplicator 
simulation_human_count = 50

#endregion

#region create the main window of the simulation
def create_simulation_window():
    window = tkinter.Tk()
    window.title("Tkinter simulation Demo")
    # Uses python 3.6+ string interpolation
    window.geometry(f'{simulation_window_width}x{simulation_window_height}')
    return window
#endregion
 
#region Create a canvas for simulation and add it to main window
def create_simulation_canvas(window):
    canvas = tkinter.Canvas(window)
    canvas.configure(bg="black")
    canvas.pack(fill="both", expand=True)
    return canvas
#endregion
 
#region create and animate humans in an infinite loop
def simulate_humans(window, canvas):
    #initialize Simulatorbase
    maxx = simulation_window_width * simulation_scale_meter2pixel
    maxy = simulation_window_height * simulation_scale_meter2pixel
    HumanDataBase.Initialize(maxx, maxy, simulation_human_count)
    hradius = simulation_ball_radius * simulation_scale_meter2pixel
    if hradius < 2:
        hradius = 2

    #create here all human-instances at first loop imported from HumanDataBase
    humanCanvasList = []    #Liste der Grafikobjekte Humans

    #initialize with absolute position
    for x in range(len(HumanDataBase.HumanList)):  
        tagstr = "human, " + str(HumanDataBase.HumanList[x].GetGuid())
        humanCanvas = canvas.create_oval(
                (HumanDataBase.HumanList[x].Status.CurPos.X / simulation_scale_meter2pixel) - simulation_ball_radius,
                (HumanDataBase.HumanList[x].Status.CurPos.Y / simulation_scale_meter2pixel) - simulation_ball_radius,
                (HumanDataBase.HumanList[x].Status.CurPos.X / simulation_scale_meter2pixel) + simulation_ball_radius,
                (HumanDataBase.HumanList[x].Status.CurPos.Y / simulation_scale_meter2pixel) + simulation_ball_radius,
                fill="blue", outline="white", width=1, tags=tagstr)
        humanCanvasList.append(humanCanvas) 

    window.update()

    #region main-loop
    while True:

        HumanDataBase.Simulate()
#try with moving instead of delete and new paint.. 
#        for x in range(len(HumanDataBase.HumanList)):  
#            item = str(HumanDataBase.HumanList[x].GetGuid())
#            Stepx = int(HumanDataBase.HumanList[x].Status.DeltaPos.X)
#            Stepy = int(HumanDataBase.HumanList[x].Status.DeltaPos.Y)
#            hitem = canvas.find_withtag(item)
#            canvas.move( hitem, Stepx, Stepy)

        canvas.delete("all")
        for x in range(len(HumanDataBase.HumanList)):  
            canvas.create_oval(
                (HumanDataBase.HumanList[x].Status.CurPos.X / simulation_scale_meter2pixel) - simulation_ball_radius,
                (HumanDataBase.HumanList[x].Status.CurPos.Y / simulation_scale_meter2pixel) - simulation_ball_radius,
                (HumanDataBase.HumanList[x].Status.CurPos.X / simulation_scale_meter2pixel) + simulation_ball_radius,
                (HumanDataBase.HumanList[x].Status.CurPos.Y / simulation_scale_meter2pixel) + simulation_ball_radius,
                fill="blue", outline="white", width=1)

        window.update()

        time.sleep(simulation_refresh_seconds)

        #region simulation movement here 
        #human_pos = canvas.coords(human)
        # unpack array to variables
        #xl,yl,xr,yr = human_pos
        #if xl < abs(xinc) or xr > simulation_window_width-abs(xinc):
        #    xinc = -xinc
        #if yl < abs(yinc) or yr > simulation_window_height-abs(yinc):
        #    yinc = -yinc
        #endregion
    #endregion
#endregion 


#region main-program ------------------------------------------------------------------------------------------
simulation_window = create_simulation_window()
simulation_canvas = create_simulation_canvas(simulation_window)
simulate_humans(simulation_window,simulation_canvas)
#endregion ----------------------------------------------------------------------------------------------------