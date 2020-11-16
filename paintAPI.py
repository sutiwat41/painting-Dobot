import DobotDllType as dType

class paintingAPI:
    def __init__(self):
        self.CON_STR = {
        dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
        dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
        dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

        self.x = 0
        self.y = 0
        self.z = 0 
        self.rHead = 0
        self.jointn = []
        #Load Dll and get the CDLL object
        self.api = dType.load() 
        self.state = None
        

    def connection(self):
        Tempstate = dType.ConnectDobot(self.api, "", 115200)[0]
        print("Connect status:",self.CON_STR[Tempstate])

        if dType.DobotConnect.DobotConnect_NoError == Tempstate:
            self.state = True
        else: 
            
            self.state = False
            self.close()

        return self.state



    def start(self):
        dType.SetQueuedCmdClear(self.api)
    
        #Async Motion Params Setting
        #dType.SetHOMEParams(self.api, 200, 0, 0, 0, isQueued = 1)
        #dType.SetPTPCoordinateParamsEx(self.api,30,50,30,50,1)
        dType.SetPTPJointParams(self.api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
        dType.SetPTPCommonParams(self.api, 100, 100, isQueued = 1)
        dType.SetJOGJointParams(self.api, 150, 150, 150, 150, 150, 150, 150, 150,  isQueued = 1)

        #dType.SetHOMECmd(self.api, temp = 0, isQueued = 1)

    def toHomeLocation(self):
        return dType.SetHOMECmd(self.api, isQueued = 1)

    def getHomeLocation(self):
        return dType.GetHOMEParams(self.api)

    def getLocation(self):
        pos = dType.GetPose(self.api)
        x,y,z,rHead = pos[0:4]
        jointn = pos[4:]
        self.x = x
        self.y = y 
        self.z = z
        self.rHead = rHead
        self.jointn = jointn
        return [x,y,z,rHead,jointn]

    def movePosition(self,moveX = 0,moveY = 0,moveZ = 0):
        self.lastIndex = dType.SetPTPCmd(self.api, 2, self.x+moveX, self.y+moveY, self.z+moveZ, self.rHead, 1)[0]
        return self.lastIndex

    def setPosition(self,x = None,y=None,z=None,rHead = None):
        if x == None : x = self.x
        if y == None : y = self.y
        if z == None : z = self.z
        if rHead == None : rHead = self.rHead
        #print(x,y,z,rHead)
        self.lastIndex = dType.SetPTPCmd(self.api, 2, x, y, z,rHead, 1)[0]
        
        return self.lastIndex

    def setJog(self,mode,cmd):
        
        if mode == "xyz":
            cmdDict = {"x+":1,"x-":2,"y+":3,"y-":4,"z+":5,"z-":6,"r+":7,"r-":8} 
            tempmode = 0        
        
        else:
            cmdDict = {"j1+":1,"j1-":2,"j2+":3,"j2-":4,"j3+":5,"j3-":6,"j4+":7,"j4-":8} 
            tempmode = 1

        tempcmd = cmdDict[cmd]

        self.lastIndex = dType.SetJOGCmd(self.api,tempmode,tempcmd,1)[0]
        self.update()

    
    def stopJog(self,mode):
        if mode == "xyz":
            tempmode = 0
        else:
            tempmode = 1  

        self.lastIndex = dType.SetJOGCmd(self.api,tempmode,0,1)[0]
        self.update()  
            

       


    def update(self):
        self.getLocation()
        dType.SetQueuedCmdStartExec(self.api)
        #Wait for Executing Last Command 
        while self.lastIndex > dType.GetQueuedCmdCurrentIndex(self.api)[0]:
            dType.dSleep(10)
            
            #print("cmd :",self.lastIndex,dType.GetQueuedCmdCurrentIndex(self.api)[0])
            #if self.lastIndex -1 == dType.GetQueuedCmdCurrentIndex(self.api)[0]: break
        dType.SetQueuedCmdStopExec(self.api)

       # dType.SetQueuedCmdClear(self.api)

    def stepperDriveDis(self,motor,speed,distance = 1,direction = 1):
        #speed -> mm/s distance -> mm
        #motor 1 -> stepper 1(0)  2 ->stepper2(1)
        #3200 pulse -> 2mm  
        #3200 pulse -> 1 rev/s
        #self.lastIndex = dType.SetEMotorSEx(self.api, (motor+1)%2, 1, -4000, 2000, 1)[0]
        ppm = 1600
        tempSpeed = int(ppm*speed*direction)
        tempDistance = int(distance*ppm)

        self.lastIndex = dType.SetEMotorS(self.api,(motor+1)%2,1,tempSpeed,tempDistance)[0]

    def switch12V(self,port,state):
        #port(16,17) -> int #state-> str
        if state == "on":
            self.lastIndex = dType.SetIODO(self.api,port, 1, 1)[0]
            #print(self.lastIndex)
        else:
            self.lastIndex = dType.SetIODO(self.api,port, 0, 1)[0]

    def EmergencyStop(self):
        dType.SetQueuedCmdForceStopExec(self.api)
        self.close()


    def getAlarm(self):
        return dType.GetAlarmsState(self.api)

    def close(self):
        dType.DisconnectDobot(self.api)
        print("Dobot disconnected")
        #exit()