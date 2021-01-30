import HumanDataBase
import time

HumanDataBase.Initialize(500, 100, 5)

HumanDataBase.PrintHumanStats()

while(True):
    HumanDataBase.Simulate()
    HumanDataBase.PrintHumanStats()
    time.sleep(1)

