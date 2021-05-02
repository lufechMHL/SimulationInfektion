#=====================================================================================================
#   Projekt Seminararbeit SimulationInfektion
#   Modul Simulation - Simulation der Bewegungen und der Infektion einer Anzahl von Personen  
#   
#   Changelog
#   2021-01-29  -   Erstellung
#   2021-02-06  -   Erweiterung Bewegungssimulation Ausweichen vor anderen Personen
#   2021-03-07  -   Erweiterung Speicherung der Position in einem Array/Cube zur schnelleren Suche benachbarter Personen
#   2021-03-21  -   Umbau Grafikausgabe in HumanDataBase und Steuerung der Simulation über Parameter begonnen
#   2021-04-06  -   Zeitraffer implementiert
#   2021-04-18  -   Infektionslogik implementiert
#=====================================================================================================

#-------------- Module in CMD-Kommandozeile mittels pip installieren!!!! Einmalig auf dem lokalen Rechner
#python -python -m pip install -U pygame --user
#python -python -m pip install -U numpy --user

import uuid
#import dataclasses
import random
import time
import math
import colour
import sys
import datetime
import numpy as np   #install via pip >>> python -m pip install -U numpy --user
import pygame
from enum import Enum
from pygame.locals import *

#region data classes ==================================================================================================================

class InfectionStat(Enum):
    HEALTHY = 1
    INFECTED = 2
    SICK = 3
    IMMUNE = 4
    DEATH = 5

#region HumanStat - Daten zum Darstellen in der GUI
class HumanStat():

    #nested class Position
    class Position():
        X: float
        Y: float

        def __init__(self, X, Y):
            self.X = X
            self.Y = Y


    Origin: Position  #Herkunft (Meter)
    CurPos: Position  #Current Position (Meter)
    Destination: Position  #Ziel (Meter)
    DeltaPos: Position #Delta-Weg (Meter)
    PicturePos: Position  #Current Position in Window (Pixel)
    Speed: float
    Angle: float   #Winkel zu Destination
    StopRadius: float
    StopAngle: float
    RecvInfections: int #Menge an empfangenen Viren / Ansteckung durch andere Personen
    InfectionLevel: int #Grad der Infektion / eigene Virenlast
    CurInfectionStat: int #Infektionsstatus/grad
    InfectionTimeStamp: datetime.datetime 
    InfUpdateTimeStamp: datetime.datetime 
    
    def __init__(self):
        self.Origin = self.Position(0.0, 0.0)
        self.CurPos = self.Position(0.0, 0.0)
        self.Destination = self.Position(0.0, 0.0)
        self.DeltaPos = self.Position(0.0, 0.0)
        self.PicturePos = self.Position(0.0, 0.0)
        self.Angle = 0.0
        self.RecvInfections = 0
        self.InfectionLevel = 0
        self.CurInfectionStat = InfectionStat.HEALTHY
        self.InfectionTimeStamp = datetime.datetime.now()
        self.InfUpdateTimeStamp = datetime.datetime.now()
     

#endregion

#region HumanConfig - Configuration eines Objekts
class HumanConfig():
    
    MaxSpeed: float
    MinSpeed: float
    
    RadiusFar: float    #Ab diesem Radius abbremsen
    RadiusNear: float   #Nicht näher, stopp
    InfectionRadius: float #Abstand Inektionsschutz
    
    Acceleration: float
    MaxDistance: float

    DeltaAngel: float
    
    #InfectRadius: float
    #IncarnationTime: float

    def __init__(self, MaxSpeed, MinSpeed, RadiusFar, RadiusNear, Acceleration, MaxDistance):
        self.MaxSpeed = MaxSpeed
        self.MinSpeed = MinSpeed
        self.RadiusFar = RadiusFar
        self.RadiusNear = RadiusNear
        self.Acceleration = Acceleration
        self.MaxDistance = MaxDistance
        self.DeltaAngel = 5.0
        self.InfectionRadius = RadiusFar #(RadiusFar - RadiusNear)/2 + RadiusNear #anpassbar im ersten Wurf genau zwischen RadiusFar und RadiusNear

#endregion
#endregion

#region class global param
class GlobalParam():
    # width of the simulation window
    simulation_window_width: int
    # height of the simulation window
    simulation_window_height: int
    # refresh cycle window in sec
    simulation_window_update_sec: float
    # background color 
    simulation_backgroundcolor: int
    # radius of the ball
    simulation_ball_radius: int
    #x-range area in meters
    simulation_area_xmeters: int
    #y-range area in meters
    simulation_area_ymeters: int 
    #count of humans in the area
    simulation_human_count: int
    #timelaps value
    simulation_time_lapse: float
    #initial number of infected humans
    simulation_start_inf: int
    #maximum movement distance
    simulation_move_radius: float

    def __init__(self):
        self.simulation_window_width=1300
        self.simulation_window_height=800
        self.simulation_backgroundcolor = colour.dark_green
        self.simulation_ball_radius = 5
        self.simulation_area_xmeters = 100
        self.simulation_area_ymeters = 80
        self.simulation_human_count = 30
        self.simulation_time_lapse = 1.0
        self.simulation_window_update_sec = 0.2
        self.simulation_move_radius = 50.0


#endregion


#region class Human - Klasse um die Bewegung und die Gesundheit der Objekte zu simulieren ============================================
class Human():

    guid: str  #zufälliger Name für Objekte
    Status: HumanStat  #Satus Daten
    Config: HumanConfig  #Daten zur Konfiguration 

    HumanID: int
    maxX: float #maximum range (area) in meters X-coordinate (direction west --> east) 
    maxY: float #maximum range (area) in meters Y-coordinate (direction north --> south)
    TimeBase: datetime.date
    TimeDelay: float
    TimeStamp: datetime.date
    LastMovTime: datetime.date
    SpeedHuman: float   
    MyIndexInHumanList: int
 
    #region constructor
    def __init__(self, srcx, srcy, dstx, dsty, maxx, maxy, maxdist):
        self.Status = HumanStat()
        self.guid = uuid.uuid4()
        if srcx == 0 and srcy == 0:
            self.Status.CurPos.X = self.Limit(random.uniform(0.0, maxx), maxx)
            self.Status.CurPos.Y = self.Limit(random.uniform(0.0, maxy), maxy)
        else:
            self.Status.CurPos.X = srcx
            self.Status.CurPos.Y = srcy

        self.Status.Origin.X = self.Status.CurPos.X
        self.Status.Origin.Y = self.Status.CurPos.Y

        if dstx == 0 and dsty == 0:
            self.Status.Destination.X = self.Status.CurPos.X
            self.Status.Destination.Y = self.Status.CurPos.Y
        else:
            self.Status.Destination.X = dstx
            self.Status.Destination.Y = dsty

        HcMaxSpeed: float = 1.3         #maximum speed in m/s
        HcMinSpeed: float = 0.5         #minimum speed in m/s
        HcRadiusFar: float = 2.0        #radius far as first distance for checking other people
        HcRadiusNear: float = 0.3       #radius near as safe-stop radius to other people
        HcAcceleration: float = 0.5     #acceleration of people 
        HcMaxDistance: float = maxdist  #maximum distance of movements
        self.Config = HumanConfig(HcMaxSpeed, HcMinSpeed, HcRadiusFar, HcRadiusNear, HcAcceleration, HcMaxDistance)
        self.Status.Speed = random.uniform(self.Config.MinSpeed, self.Config.MaxSpeed)
        self.Status.StopRadius = self.Config.RadiusFar
        self.Status.StopAngle = 0.0

        self.TimeBase = datetime.datetime.now()
        self.TimeDelay = 0.0
        self.TimeStamp = datetime.datetime.now()
        self.SpeedHuman = 0
        self.LastMovTime = datetime.datetime.now()
        self.maxX = maxx
        self.maxY = maxy
        self.MyIndexInHumanList = -1
    #endregion

    #region private functions
    #region UpdateSpeed
    def UpdateSpeed(self):
        if self.Status.StopRadius < self.Config.RadiusNear: #and math.abs(GetAngleDiffBetween(hStatus.Angle, hStatus.StopAngle)) < 90 )
            self.SpeedHuman = 0
        else:
            DeltaX = self.Status.Destination.X - self.Status.CurPos.X
            DeltaY = self.Status.Destination.Y - self.Status.CurPos.Y
            Radius = math.sqrt(math.pow(DeltaX, 2) + math.pow(DeltaY, 2))

            if (self.Status.StopRadius < self.Config.RadiusFar and self.SpeedHuman > 0) or (Radius < self.Config.RadiusFar and self.SpeedHuman > 0):
                self.SpeedHuman = self.SpeedHuman - (self.Config.Acceleration * self.TimeDelay)

            if (self.Status.StopRadius >= self.Config.RadiusFar and Radius > self.Config.RadiusFar and self.SpeedHuman < self.Status.Speed):
                self.SpeedHuman = self.SpeedHuman + (self.Config.Acceleration * self.TimeDelay)

            if self.SpeedHuman < 0:
                self.SpeedHuman = 0

            if self.SpeedHuman > self.Status.Speed:
                self.SpeedHuman = self.Status.Speed

        return self.SpeedHuman
    #endregion

    #region UpdateDestination
    def UpdateDestination(self):
        self.Speed = random.uniform(self.Config.MinSpeed, self.Config.MaxSpeed)
        self.SpeedHuman = 0
        DestFound = False

        while DestFound == False:
            #Berechnung des neuen Ziels unter Beachtung der maximalen Bewegungsfreiheit MaxDestinationRadius
            diffX = random.uniform(self.Config.MaxDistance * -1, self.Config.MaxDistance)
            diffY = random.uniform(self.Config.MaxDistance * -1, self.Config.MaxDistance)
            radius = math.sqrt(math.pow(diffX, 2) + math.pow(diffY, 2))

            #Check maximum Distance / Radius
            if radius > self.Config.MaxDistance:
                diffX = diffX * self.Config.MaxDistance / radius
                diffY = diffY * self.Config.MaxDistance / radius

            #Set new Destination to Status
            self.Status.Destination.X = self.Limit(self.Status.Origin.X + diffX, self.maxX)
            self.Status.Destination.Y = self.Limit(self.Status.Origin.Y + diffY, self.maxY)

            DestFound = True
            #Check borders of area
            if self.Status.Destination.X > self.maxX:
                DestFound = False
                
            if self.Status.Destination.X < 0:
                DestFound = False

            if self.Status.Destination.Y > self.maxY:
                DestFound = False

            if self.Status.Destination.Y < 0:
                DestFound = False

        #MinDist = math.pow(self.Status.Speed, 2) / (2 * self.Config.Acceleration) + 0.03

    #endregion

    #region UpdatePosition
    def UpdatePosition(self):
        if self.SpeedHuman == 0:
            StopTime = self.TimeBase - self.LastMovTime
            DistX = abs(self.Status.Destination.X - self.Status.CurPos.X)
            DistY = abs(self.Status.Destination.Y - self.Status.CurPos.Y)

            if (DistX < 0.02 and DistY < 0.02) or (StopTime.total_seconds() > 5):
                self.UpdateDestination()
                self.LastMovTime = self.TimeBase

        else:
            #self.SetCurrentPosInHumanArray(False)   #reset aktuelle Position im Array

            DeltaRadius = self.TimeDelay * self.SpeedHuman 
            self.Status.DeltaPos.X = DeltaRadius * math.cos(self.Status.Angle / 360 * 2 * math.pi)
            self.Status.DeltaPos.Y = DeltaRadius * math.sin(self.Status.Angle / 360 * 2 * math.pi)

            DistX = self.Status.Destination.X - self.Status.CurPos.X
            DistY = self.Status.Destination.Y - self.Status.CurPos.Y
            RadiusDest = math.sqrt(DistX**2 + DistY**2)

            if RadiusDest > DeltaRadius:
                self.Status.CurPos.X = self.Limit(self.Status.CurPos.X + self.Status.DeltaPos.X, self.maxX)
                self.Status.CurPos.Y = self.Limit(self.Status.CurPos.Y + self.Status.DeltaPos.Y, self.maxY)
            else:
                self.Status.CurPos.X = self.Limit(self.Status.CurPos.X + DistX, self.maxX)
                self.Status.CurPos.Y = self.Limit(self.Status.CurPos.Y + DistY, self.maxY)

            #self.SetCurrentPosInHumanArray(True)   #set aktuelle Position im Array >> neue Position
            self.LastMovTime = self.TimeBase
    #endregion

    #region UpdateAngle Berechnung des Winkels Laufrichtung
    def UpdateAngle(self, HumanList):

        # Suche nach Personen im Umkreis
        lastrad = self.Config.RadiusFar
        RadiusNext = lastrad

        #Über die Matrix HumanArray werden jetzt nur die Humans ermittelt, die sich im Umkreis von RadiusFar befinden
        #humansAround = self.CheckIfHumanAround()

        #region Schleife über die Liste aller Humans im Umkreis RadiusFar
        #for hidx in humansAround:  
        for hidx in range(len(HumanList)):
            tagstr = HumanList[hidx].GetGuid()
            if tagstr != self.guid:

                #region Berechnung Abstand und Winkel zu dieser anderen Person hidx
                DeltaX = HumanList[hidx].Status.CurPos.X - self.Status.CurPos.X
                DeltaY = HumanList[hidx].Status.CurPos.Y - self.Status.CurPos.Y
                Radius = math.sqrt(math.pow(DeltaX, 2) + math.pow(DeltaY, 2))
                if Radius == 0:
                    Radius = 0.001
                Angel = math.acos(DeltaX / Radius) * 180 / math.pi
                if DeltaY < 0:
                    Angel = Angel * -1
                #endregion

                #region Übertragung der eigenen Infektion auf die Person gegenüber ... passt hier gut rein, weil wir den Abstand berechnet haben
                if Radius < self.Config.InfectionRadius and self.Status.InfectionLevel > 0: 
                    HumanList[hidx].SetInfection(self.Status.InfectionLevel)
                    print(hidx, Radius, self.Status.InfectionLevel )
                #region

                #region Abstand kleiner als letzter Abstand - Übernahme in Berechnung
                if Radius < lastrad: #wenn die Person näher ist als die vorherige - neue Person merken
                    DiffAngle = self.GetAngleDiffBetween(self.Status.Angle, Angel)
                    RelRadius = 100 * (self.Config.RadiusFar - Radius) / (self.Config.RadiusFar - self.Config.RadiusNear)

                    if abs(DiffAngle) < 30: #Winkel zur Person ist weniger als 30° - stärker ausweichen
                        
                        if DiffAngle < 0: #Ziel befindet sich von aktueller Richtung links 
                            self.Status.Angle = DiffAngle + RelRadius
                            if self.Status.Angle > 180:
                                self.Status.Angle = self.Status.Angle - 360
                        
                        else: #Ziel ist rechts vorn vor mir  
                            self.Status.Angle = DiffAngle - RelRadius
                            if self.Status.Angle < -180:
                                self.Status.Angle = self.Status.Angle + 360

                        lastrad = Radius
                        self.Status.StopRadius = Radius
                        self.Status.StopAngle = Angel

                    elif abs(DiffAngle) < 90:  #Winkel zur Person ist zwischen 30° und 90° - schwächer ausweichen 
                        
                        if DiffAngle < 0: #Ziel befindet sich von aktueller Richtung links 
                            self.Status.Angle = DiffAngle + RelRadius
                            if self.Status.Angle > 180:
                                self.Status.Angle = self.Status.Angle - 360

                        else: #Ziel ist rechts vorn vor mir  
                            self.Status.Angle = DiffAngle - RelRadius
                            if self.Status.Angle < -180:
                                self.Status.Angle = self.Status.Angle + 360

                        lastrad = Radius
                        self.Status.StopRadius = Radius
                        self.Status.StopAngle = Angel
                #endregion
        #endregion

        #region wenn nichts im Weg ist den Winkel zum Ziel berechnen
        if lastrad >= self.Config.RadiusFar:

            #region Berechnung Radius und Winkel zum Ziel

            self.Status.DeltaPos.X = self.Status.Destination.X - self.Status.CurPos.X
            self.Status.DeltaPos.Y = self.Status.Destination.Y - self.Status.CurPos.Y
            RadiusDest = math.sqrt(self.Status.DeltaPos.X**2 +self.Status.DeltaPos.Y**2)

            #Abstand = aktueller Radius zum Ziel setzen
            if RadiusDest < self.Config.RadiusFar:
                self.Status.StopRadius = RadiusDest
            else:
                self.Status.StopRadius = self.Config.RadiusFar + 1
            
            #Winkel der Bewegung berechnen, wenn kein Hindernis
            if RadiusDest > 0:
                DestAngle = (math.acos(self.Status.DeltaPos.X / RadiusDest)) * 180 / math.pi
                if self.Status.DeltaPos.Y < 0:
                    DestAngle = DestAngle * (-1)
            else:
                DestAngle = 0.0
            #endregion

            #region schrittweise Anpassung der aktuellen Richtung auf das Ziel
            DiffAngle = self.GetAngleDiffBetween(self.Status.Angle, DestAngle)
            self.Status.StopAngle = DestAngle

            if DiffAngle < 0: #Ziel befindet sich von aktueller Richtung links 
                if abs(DiffAngle) > self.Config.DeltaAngel:
                    self.Status.Angle = self.Status.Angle - self.Config.DeltaAngel
                else:
                    self.Status.Angle = DestAngle

                if self.Status.Angle < -180:
                    self.Status.Angle = self.Status.Angle + 360
                    
            elif DiffAngle > 0: #Ziel ist rechts vorn vor mir  
                if abs(DiffAngle) > self.Config.DeltaAngel:
                    self.Status.Angle = self.Status.Angle + self.Config.DeltaAngel
                else:
                    self.Status.Angle = DestAngle

                if self.Status.Angle > 180:
                    self.Status.Angle = self.Status.Angle - 360
                    
            #endregion
            RadiusNext = RadiusDest
        else:
            RadiusNext = lastrad
        #endregion

        return RadiusNext
    #endregion
        #endregion


    #region UpdateInfection Berechnung der Infektion
    def UpdateInfection(self):
        #Status Healthy
        if self.Status.CurInfectionStat == InfectionStat.HEALTHY: 
            if self.Status.RecvInfections > 0:
                self.Status.InfectionLevel = self.Status.RecvInfections #empfangene Viren übernehmen
                self.Status.RecvInfections = 0    #und wieder zurück setzen

            timedelta = self.TimeBase - self.Status.InfUpdateTimeStamp
            if timedelta.total_seconds() > 10 and self.Status.InfectionLevel > 1: 
                #self.Status.InfectionLevel = self.Status.InfectionLevel - 1 
                self.Status.InfUpdateTimeStamp = self.TimeBase

            if self.Status.InfectionLevel > 5:                     
                self.Status.CurInfectionStat = InfectionStat.INFECTED   #Status auf Infected
                self.Status.InfectionTimeStamp = self.TimeBase
                self.Status.InfUpdateTimeStamp = self.TimeBase

        #Status Infected ... later
        if self.Status.CurInfectionStat == InfectionStat.INFECTED:
            #keine weitere Übernahme anderer Viren bei bereits infiziertem Zustand
            self.Status.RecvInfections = 0    #und wieder zurück setzen

            timedelta = self.TimeBase - self.Status.InfUpdateTimeStamp
            if timedelta.total_seconds() > 10: 
                self.Status.InfectionLevel = self.Status.InfectionLevel + 10 #
                self.Status.InfUpdateTimeStamp = self.TimeBase

            if self.Status.InfectionLevel > 100:                     
                self.Status.CurInfectionStat = InfectionStat.SICK       #Status auf Infected

        #Status Sick
        if self.Status.CurInfectionStat == InfectionStat.SICK:
            if self.Status.RecvInfections > 0:
                # Übernahme noch unklar
                self.Status.RecvInfections = 0    #und wieder zurück setzen

            timedelta = self.TimeBase - self.Status.InfUpdateTimeStamp
            if timedelta.total_seconds() > 10: 
                self.Status.InfectionLevel = self.Status.InfectionLevel - 1 #Selbstheilung 
                self.Status.InfUpdateTimeStamp = self.TimeBase

            if self.Status.InfectionLevel < 20:                     
                self.Status.CurInfectionStat = InfectionStat.IMMUNE       #Status auf Immun

            if self.Status.InfectionLevel > 200:                     
                self.Status.CurInfectionStat = InfectionStat.DEATH       #Status auf Death

        #Status Immune
        if self.Status.CurInfectionStat == InfectionStat.IMMUNE:
            self.Status.InfectionLevel = 0 #damit er keinen mehr infiziert

        #Status Death
        if self.Status.CurInfectionStat == InfectionStat.DEATH:
            self.Status.InfectionLevel = 0 #damit er keinen mehr infiziert
    #endregion

    #region SetInfection 
    def SetInfection(self, InfectionValue: int):
        if InfectionValue > 100:
            InfectionValue = 10 
        elif InfectionValue > 10:
            InfectionValue = InfectionValue / 10 
        else:
            InfectionValue = 1

        self.Status.RecvInfections = self.Status.RecvInfections + InfectionValue

    #endregion


    #region Positions-Array verwalten
    #Funktion ermittelt den eigenen Index in der globalen Liste HumanList
    def GetMyIndexInHumanList(self):
        if self.MyIndexInHumanList < 0:
            for x in range(len(HumanList)):  
                tagstr = HumanList[x].GetGuid()
                if tagstr == self.guid:
                    self.MyIndexInHumanList = x
        
        return self.MyIndexInHumanList

    def SetCurrentPosInHumanArray(self, SetPos: bool):
        tempx = math.floor( self.Status.CurPos.X) 
        tempy = math.floor( self.Status.CurPos.Y) 
        idx = self.GetMyIndexInHumanList()

        if SetPos == True:
            HumanArray[idx, tempx, tempy] = 1
        else:
            HumanArray[idx, tempx, tempy] = 0

    def CheckIfHumanAround(self):
        tempx = math.floor( self.Status.CurPos.X) 
        tempy = math.floor( self.Status.CurPos.Y) 
        idx = self.GetMyIndexInHumanList()
        humansAroundMe = []
        maxh = HumanArray.shape[0] - 1 #lese die länge der 0ten Dimension des Array >> Dimension Index HumanList >> 0-based 
        maxindex = math.ceil(self.Config.RadiusFar) #für die Prüfung relevanter Radius = Index
        for x in range(tempx - maxindex, tempx + maxindex):
            for y in range(tempy -maxindex, tempy + maxindex):
                for h in range(0,maxh): 
                    if x >= 0 and x < self.maxX and y >= 0 and y < self.maxY:
                        if HumanArray[h,x,y] > 0:
                            humansAroundMe.append(h)

        return humansAroundMe


    #endregion

    #region Simulation Go
    def Go(self, humanList, timelapseVal):
        #region Zeitstempel Zeitdifferenz berechnen

        self.TimeBase = datetime.datetime.now()
        timedelta = (datetime.datetime.now() - self.TimeStamp) 
        self.TimeDelay = timedelta.total_seconds()
        self.TimeStamp = datetime.datetime.now()
        #Timelapse 
        self.TimeDelay = self.TimeDelay * timelapseVal
        #endregion

        #region UpdateSpeed
        self.UpdateSpeed()
        #endregion

        #region Berechnung des Winkels Laufrichtung
        self.UpdateAngle(humanList)
        #endregion

        #region Berechnung der Schrittweite
        self.UpdatePosition()
        #endregion

        #region Berechnung des eigenen Infektionsstatus
        self.UpdateInfection()
        #endregion

        return (self.Status.CurPos.X, self.Status.CurPos.Y)
    #endregion

    #region helper
    #Funktion berechnet Winkel zwischen zwei Richtungen
    def GetAngleDiffBetween(self, CurrAngle: float, OtherAngle: float ):
        if CurrAngle >= 0:
            NormalizedCurrentAngle = CurrAngle
        else: 
            NormalizedCurrentAngle = CurrAngle + 360

        if OtherAngle >= 0:
            NormalizedOtherAngle = OtherAngle 
        else: 
            NormalizedOtherAngle = OtherAngle + 360

        DiffAngle = NormalizedOtherAngle - NormalizedCurrentAngle

        if DiffAngle > 180:
            DiffAngle = DiffAngle - 360

        if DiffAngle < -180:
            DiffAngle = DiffAngle + 360

        return DiffAngle
        
    #Function to limit the meter-value to the maximum array-size    
    def Limit(self, value, maxval):
        if value > (maxval - 1):
            value = maxval - 1
        return value

    #endregion



    #region Return
    def GetCurrentPosition(self):
        return (self.Status.CurPos.X, self.Status.CurPos.Y)

    def GetCurrentStep(self):
        return (self.Status.DeltaPos.X, self.Status.DeltaPos.Y)

    def GetGuid(self):
        return self.guid

    #endregion

#endregion
#endregion

#region -- Main module ===============================================================================================================

class Simulation():
    #region global Variables
    HumanList = [] #List
    HumanPara: GlobalParam
    IsInitialized: int
    LastRepaint: time
    LastDuration: float
    SimuDuration: float
    SimuTimeStamp: time

    #init numpy-array für die Fläche mit z-Koordinate für die Humans in einer Meterfläche
    #HumanArray = np.zeros((simulation_human_count,simulation_area_xmeters, simulation_area_ymeters ),dtype=int)
    #endregion

    #region Simulationmodule fuctions / interface 
    def __init__(self):
        self.IsInitialized = 0
        self.LastRepaint = time.time()
        self.SimuTimeStamp = time.time()
        self.LastDuration = 0.0
        self.SimuDuration = 0.0

        self.HumanPara = GlobalParam()
        self.HumanPara.simulation_window_width=1300
        self.HumanPara.simulation_window_height=800
        self.HumanPara.simulation_backgroundcolor = colour.dark_green
        self.HumanPara.simulation_time_lapse = 1.0
        self.HumanPara.simulation_area_xmeters = 100
        self.HumanPara.simulation_area_ymeters = 80
        self.HumanPara.simulation_human_count = 30
        self.HumanPara.simulation_start_inf = 2
        self.HumanPara.simulation_move_radius = 50.0

        self.HumanArray = np.zeros((self.HumanPara.simulation_human_count,self.HumanPara.simulation_area_xmeters, self.HumanPara.simulation_area_ymeters ),dtype=int)
        print("Init Module done")

    def InitModule(self):
        print("Init Module done")

    def GetAreaSize(self):
        return self.HumanPara.simulation_area_xmeters, self.HumanPara.simulation_area_ymeters

    def GetAreaHumanCount(self):
        return self.HumanPara.simulation_area_xmeters, self.HumanPara.simulation_area_ymeters

    def GetSimulationTime(self):
        timetup = time.gmtime(self.SimuDuration)
        return time.strftime('Tage %d %H:%M:%S', timetup)

    def Initialize(self,xmeters: int, ymeters: int, humancount: int, infectedcount: int, maxmovedist: float):

        #overwrite initialized values
        if xmeters > 0 and ymeters > 0 and humancount > 0 and maxmovedist > 0 and infectedcount > 0:
            self.HumanPara.simulation_human_count = humancount
            self.HumanPara.simulation_area_xmeters = xmeters
            self.HumanPara.simulation_area_ymeters = ymeters
            self.HumanPara.simulation_start_inf = infectedcount
            self.HumanPara.simulation_move_radius = maxmovedist

        #region Init HumanList
        self.HumanList.clear()

        for x in range(self.HumanPara.simulation_human_count):
            newi = Human(0, 0, 0, 0, self.HumanPara.simulation_area_xmeters, self.HumanPara.simulation_area_ymeters, self.HumanPara.simulation_move_radius)
            self.HumanList.append(newi)
        
        for x in range(self.HumanPara.simulation_start_inf):
            self.HumanList[x].Status.RecvInfections = 20 #die ersten Menschen infizieren 
        #endregion

        #region Init pygame
        self.HumanPara.simulation_scale_meter2pixel = self.HumanPara.simulation_area_xmeters / self.HumanPara.simulation_window_width
        self.HumanPara.simulation_window_height = math.floor( self.HumanPara.simulation_area_ymeters / self.HumanPara.simulation_scale_meter2pixel)
        self.HumanPara.simulation_ball_radius = math.ceil(0.5 / self.HumanPara.simulation_scale_meter2pixel)
        if self.HumanPara.simulation_ball_radius < 2:
            self.HumanPara.simulation_ball_radius = 2

        pygame.init()
        pygame.display.set_caption('SimulationInfection St-El-Lu')
        pygame.key.set_repeat(250, 125)

        global screen 
        screen = pygame.display.set_mode((self.HumanPara.simulation_window_width, self.HumanPara.simulation_window_height))
        global font 
        font = pygame.font.Font('consola.ttf', 20)
        global table 
        table = pygame.Surface((self.HumanPara.simulation_window_width, self.HumanPara.simulation_window_height))

        table.fill(self.HumanPara.simulation_backgroundcolor)
        screen.blit(table, (0,0))
        pygame.display.flip()
        self.SimuDuration = 0.0
        self.SimuTimeStamp = time.time()
        #endregion

        self.IsInitialized = 1
        print("Initialize Simulation done")


    def Terminate(self):
        self.HumanList.clear()
        pygame.display.quit()
        self.IsInitialized = 0
        print("Simulation terminated")

    #Funktion zeichnet einen Kreis/Bubbel für einen Human
    def PaintHuman(self, Idx: int):
        #aktuelle grafik ausblenden - mit Background-color übermalen
        xval = self.HumanList[Idx].Status.PicturePos.X
        yval = self.HumanList[Idx].Status.PicturePos.Y
        pygame.draw.circle(table, self.HumanPara.simulation_backgroundcolor,(xval,yval),self.HumanPara.simulation_ball_radius, 0)    

        #Farbe bestimmen
        setcolour = colour.light_green
        if self.HumanList[Idx].Status.CurInfectionStat == InfectionStat.INFECTED:
            setcolour = colour.light_red

        if self.HumanList[Idx].Status.CurInfectionStat == InfectionStat.SICK:
            setcolour = colour.red

        if self.HumanList[Idx].Status.CurInfectionStat == InfectionStat.IMMUNE:
            setcolour = colour.blue

        if self.HumanList[Idx].Status.CurInfectionStat == InfectionStat.DEATH:
            setcolour = colour.dark_grey

        #neue Position zeichnen
        xval = self.HumanList[Idx].Status.CurPos.X / self.HumanPara.simulation_scale_meter2pixel
        yval = self.HumanList[Idx].Status.CurPos.Y / self.HumanPara.simulation_scale_meter2pixel
        pygame.draw.circle(table, setcolour,(xval,yval),self.HumanPara.simulation_ball_radius, 0)    

        #zuletzt gezeichnete Position speichern
        self.HumanList[Idx].Status.PicturePos.X = xval
        self.HumanList[Idx].Status.PicturePos.Y = yval



    def Simulate(self, timelapseVal: float):

        self.HumanPara.simulation_time_lapse = timelapseVal
        self.SimuDuration = self.SimuDuration + (time.time() - self.SimuTimeStamp) * self.HumanPara.simulation_time_lapse
        self.SimuTimeStamp = time.time()

        start = time.time()
        if len(self.HumanList) > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE):
                    sys.exit()

            #Simulation Humans 
            for x in range(len(self.HumanList)):  
                #neue Position berechnen
                self.HumanList[x].Go(self.HumanList, self.HumanPara.simulation_time_lapse)

            #Refresh Window in a cycle of simulation_window_update_sec
            if (start - self.LastRepaint) > self.HumanPara.simulation_window_update_sec:
                self.LastRepaint = start
                for x in range(len(self.HumanList)):  
                    self.PaintHuman(x)

                #frame auf Display blenden


                screen.blit(table, (0,0))
                pygame.display.flip()

        self.LastDuration = time.time() - start



    def PrintHumanStats(self):
        for humi in self.HumanList:
            x, y = humi.GetCurrentPosition()
            print(humi.guid)
            #print(x)
            #print(y)    
            print(humi.Status.DeltaPos.X)
            print(humi.Status.DeltaPos.Y)
            
    #endregion 

#endregion


