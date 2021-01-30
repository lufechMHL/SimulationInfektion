import uuid
#import dataclasses
import random
import time
import math
import datetime

#region classes
#region HumanStat - Daten zum Darstellen in der GUI
class HumanStat():

    #nested class Position
    class Position():
        X: float
        Y: float

        def __init__(self, X, Y):
            self.X = X
            self.Y = Y

    Origin: Position  #Herkunft
    CurPos: Position  #Current Position
    Destination: Position  #Ziel
    DeltaPos: Position #Delta-Weg 
    Speed: float
    Angle: float   #Winkel zu Destination
    StopRadius: float
    StopAngle: float

    def __init__(self):
        self.Origin = self.Position(0.0, 0.0)
        self.CurPos = self.Position(0.0, 0.0)
        self.Destination = self.Position(0.0, 0.0)
        self.DeltaPos = self.Position(0.0, 0.0)
        self.Angle = 0.0
     

#endregion



#region HumanConfig - Configuration eines Objekts
class HumanConfig():
    
    MaxSpeed: float
    MinSpeed: float
    
    RadiusFar: float
    RadiusNear: float
    
    Acceleration: float
    MaxDistance: float
    
    #InfectRadius: float
    #IncarnationTime: float

    def __init__(self, MaxSpeed, MinSpeed, RadiusFar, RadiusNear, Acceleration, MaxDistance):
        self.MaxSpeed = MaxSpeed
        self.MinSpeed = MinSpeed
        self.RadiusFar = RadiusFar
        self.RadiusNear = RadiusNear
        self.Acceleration = Acceleration
        self.MaxDistance = MaxDistance

#endregion

#region Human - Klasse um die Bewegung und die Gesundheit der Objekte zu simulieren
class Human():

    guid: str  #zufälliger Name für Objekte
    Status: HumanStat  #Satus Daten
    Config: HumanConfig  #Daten zur Konfiguration 

    HumanID: int
    maxX: float #maximum range (area) in meters X-coordinate (direction west --> east) 
    maxY: float #maximum range (area) in meters Y-coordinate (direction north --> south)
    TimeDelay: float
    TimeStamp: datetime.date
    LastMovTime: datetime.date
    SpeedHuman: float   

 
    #region constructor
    def __init__(self, srcx, srcy, dstx, dsty, maxx, maxy):
        self.Status = HumanStat()
        self.guid = uuid.uuid4()
        if srcx == 0 and srcy == 0:
            self.Status.CurPos.X = random.uniform(0.0, maxx)
            self.Status.CurPos.Y = random.uniform(0.0, maxy)
        else:
            self.Status.CurPos.X = srcx
            self.Status.CurPos.Y = srcy

        if dstx == 0 and dsty == 0:
            self.Status.Destination.X = random.uniform(0.0, maxx)
            self.Status.Destination.Y = random.uniform(0.0, maxy)
        else:
            self.Status.Destination.X = dstx
            self.Status.Destination.Y = dsty
        self.Status.Origin.X = self.Status.CurPos.X
        self.Status.Origin.Y = self.Status.CurPos.Y

        self.Config = HumanConfig(1.5, 0.5, 1.0, 0.3, 0.5, 50)
        self.Status.Speed = random.uniform(self.Config.MinSpeed, self.Config.MaxSpeed)
        self.Status.StopRadius = self.Config.RadiusFar
        self.Status.StopAngle = 0.0

        self.TimeDelay = 0.0
        self.TimeStamp = datetime.datetime.now()
        self.SpeedHuman = 0
        self.LastMovTime = datetime.datetime.now()
        self.maxX = maxx
        self.maxY = maxy
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
        
        #Berechnung des neuen Ziels unter Beachtung der maximalen Bewegungsfreiheit MaxDestinationRadius
        diffX = random.uniform(self.Config.MaxDistance * -1, self.Config.MaxDistance)
        diffY = random.uniform(self.Config.MaxDistance * -1, self.Config.MaxDistance)
        radius = math.sqrt(math.pow(diffX, 2) + math.pow(diffY, 2))

        #Check maximum Distance / Radius
        if radius > self.Config.MaxDistance:
            diffX = diffX * self.Config.MaxDistance / radius
            diffY = diffY * self.Config.MaxDistance / radius

        #Set new Destination to Status
        self.Status.Destination.X = self.Status.Origin.X + diffX
        self.Status.Destination.Y = self.Status.Origin.Y + diffY

        #Check borders of area
        if self.Status.Destination.X > self.maxX:
            self.Status.Destination.X = self.maxX - self.Config.RadiusNear

        if self.Status.Destination.X < 0:
            self.Status.Destination.X = self.Config.RadiusNear

        if self.Status.Destination.Y > self.maxY:
            self.Status.Destination.Y = self.maxY - self.Config.RadiusNear

        if self.Status.Destination.Y < 0:
            self.Status.Destination.Y = self.Config.RadiusNear

        #MinDist = math.pow(self.Status.Speed, 2) / (2 * self.Config.Acceleration) + 0.03

    #endregion
    #endregion

    #region Simulation Go
    def Go(self):
        #region Zeitstempel Zeitdifferenz berechnen
        timedelta = datetime.datetime.now() - self.TimeStamp
        self.TimeDelay = timedelta.total_seconds()
        self.TimeStamp = datetime.datetime.now()
        #endregion

        #region UpdateSpeed
        self.UpdateSpeed()
        #endregion

        #region Berechnung des Winkels Laufrichtung
        self.Status.DeltaPos.X = self.Status.Destination.X - self.Status.CurPos.X
        self.Status.DeltaPos.Y = self.Status.Destination.Y - self.Status.CurPos.Y
        RadiusDest = math.sqrt(self.Status.DeltaPos.X**2 +self.Status.DeltaPos.Y**2)
        
        #Winkel der Bewegung berechnen, wenn kein Hindernis
        if RadiusDest > 0:
            self.Status.Angle = (math.acos(self.Status.DeltaPos.X / RadiusDest)) * 180 / math.pi
            if self.Status.DeltaPos.Y < 0:
                self.Status.Angle = self.Status.Angle * (-1)
        #endregion

        #region Berechnung der Schrittweite
        if self.SpeedHuman == 0:
            StopTime = datetime.datetime.now() - self.LastMovTime
            DistX = abs(self.Status.Destination.X - self.Status.CurPos.X)
            DistY = abs(self.Status.Destination.Y - self.Status.CurPos.Y)

            if (DistX < 0.02 and DistY < 0.02) or (StopTime.total_seconds() > 20):
                self.UpdateDestination()
                self.LastMovTime = datetime.datetime.now()

        else:

            DeltaRadius = self.TimeDelay * self.SpeedHuman 
            self.Status.DeltaPos.X = DeltaRadius * math.cos(self.Status.Angle / 360 * 2 * math.pi)
            self.Status.DeltaPos.Y = DeltaRadius * math.sin(self.Status.Angle / 360 * 2 * math.pi)

            DistX = self.Status.Destination.X - self.Status.CurPos.X
            DistY = self.Status.Destination.Y - self.Status.CurPos.Y

            if RadiusDest > DeltaRadius:
                self.Status.CurPos.X = self.Status.CurPos.X + self.Status.DeltaPos.X
                self.Status.CurPos.Y = self.Status.CurPos.Y + self.Status.DeltaPos.Y
            else:
                self.Status.CurPos.X = self.Status.CurPos.X + DistX
                self.Status.CurPos.Y = self.Status.CurPos.Y + DistY

            self.LastMovTime = datetime.datetime.now()
        #endregion

        return (self.Status.CurPos.X, self.Status.CurPos.Y)
    #endregion


    #region Return
    def GetCurrentPosition(self):
        return (self.Status.CurPos.X, self.Status.CurPos.Y)

    def GetGuid(self):
        return self.guid

    #endregion

#endregion
#endregion

#region -- Main module -------------------------------------------------------------------------------------------

#region constants
simulation_scale_time_multiplicator = 1.0

#endregion

#region globale variables
HumanList = [] #List

#endregion

#region module fuctions / interface 
def Initialize(maxx, maxy, humancount):

    for x in range(humancount):
        newi = Human(0, 0, 0, 0, maxx, maxy)
        HumanList.append(newi)

def PrintHumanStats():
    for humi in HumanList:
        x, y = humi.GetCurrentPosition()
        print(humi.guid)
        #print(x)
        #print(y)    
        print(humi.Status.DeltaPos.X)
        print(humi.Status.DeltaPos.Y)
        
def Simulate():
    for humi in HumanList:
        x, y = humi.Go()
        print(humi.guid)
        print(x)
        print(y)    
        
      
#endregion 



