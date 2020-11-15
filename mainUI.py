import paintAPI as paint
import time
import threading
import tkinter as tk
#----------- display function -----------#


coorlocation = ""
jointlocation = ""
status = ""
connect = False

# auto parameter
width = 0; height = 0
rail_direction = 1
isspraying = False

def connection():
    global connect,robot
    #print(connect)
    if connect:
        #click to disconnect
        connectbtn['text'] = 'connect'
        connectbtn['bg']    ='green'
        status['text'] = "disconnect"
        connect = False
        robot.close()
        
    else:
        #click to connect
        connectbtn['text'] = 'disconnect'
        connectbtn['bg']    ='red'
        status['text'] = "connect"
        robot.connection()
        connect = True
        
def startfx(mode):
    global status,width,height,robot,location,jointlocation
    if not connect:
        print("Warning: not connect")
        status['text'] = "Warning: not connect"
    else:
        display1 = threading.Thread(target=showlocation)
        

        display1.start()
        robot.start()
        if mode == "Auto" :
            robotrun = threading.Thread(target=run)
            robotrun.start()        

        #print(width.get(),height.get())
        status['text'] = "start"       
        


def showlocation():
    global robot,coorlocation,jointlocation
    while True:
        global connect
        if not connect: 
            print("..")
            break

        displaylocation = [str(int(e)) for e in robot.getLocation()[0:4]]
        showText = ",".join(displaylocation)
        
        if type(coorlocation)!= str :  coorlocation['text'] = "Coordinate (x,y,z,rHead) : " +showText
      
        displaylocation = [str(int(e)) for e in robot.getLocation()[-1]]
        showText = ",".join(displaylocation)

        if type(jointlocation)!= str :   jointlocation['text'] = "joint (j1,j2,j3,j4) : " +showText
      
        time.sleep(0.5)

def setIsspraying():
    global isspraying
    isspraying = tkisspraying.get()
    #print(isspraying)


def setRailDirection():
    global rail_direction
    rail_direction = tkrail_direction.get()
    #print(rail_direction)


#----------------------- swap UI ------------------------#

def swap(frameI):
    global frame2,app
    #print("frame:",frameI)
    frame2.destroy()
    frame2 = tk.Frame(app,width=400, height=330)
    frame2.pack(fill=tk.BOTH,)
    if frameI == "Auto":
        AutoUI()
        status['text'] = "Automatic Mode"
 
    else:
        ManualUI()
        status['text'] = "Manual Mode"


def AutoUI():
    mode = "Auto"
    global width,height,tkisspraying,tkrail_direction,frame2

    tk.Label(frame2, text="Automatic Control", font=('Helvetica', 16, "bold")).grid(row = 0,column = 1,padx = 1,pady = 2)

    tk.Label(frame2,text = "width [mm] :").grid(row = 1,column = 0)
    tk.Label(frame2,text = "height [mm] :").grid(row = 2,column = 0)

    width = tk.Entry(frame2)
    width.grid(row = 1,column = 1)
    height = tk.Entry(frame2)
    height.grid(row = 2,column = 1)



    tk.Label(frame2,text = "Spraying :").grid(row = 3,column = 0)
    sp1 = tk.Radiobutton(frame2, text='Spray', variable=tkisspraying, value=True,command = setIsspraying).grid(row = 3,column = 1)
    sp2 = tk.Radiobutton(frame2, text='not Spray', variable=tkisspraying, value=False,command = setIsspraying).grid(row = 3,column = 2)

    tk.Label(frame2,text = "Rail Direction :").grid(row = 4,column = 0)
    sp3 = tk.Radiobutton(frame2, text='L-', variable=tkrail_direction, value=-1,command = setRailDirection).grid(row = 4,column = 1)
    sp4 = tk.Radiobutton(frame2, text='L+', variable=tkrail_direction, value=1,command = setRailDirection).grid(row = 4,column = 2)

    startbtn = tk.Button(frame2,text = "start",command = lambda : startfx(mode)).grid(row = 5,column = 1)

def ManualUI():
    mode = "Manual"
    global frame2
    tk.Label(frame2, text="Manual Control", font=('Helvetica', 16, "bold")).grid(row = 0,column = 1,padx = 1,pady = 2)
    
    startbtn = tk.Button(frame2,text = "start",command = lambda : startfx(mode)).grid(row = 5,column = 1)

    joy = tk.Frame(frame2,width=150, height=150,bg = "Red") 
    joy.grid(row = 2,column = 0)
    tk.Label(frame2,text = "Cartesian control [mm]").grid(row = 1,column = 0)
    tk.Button(joy,text = "y-",command = lambda : xyzcontrol("y-")).grid(row = 0,column = 1,padx = 4,pady = 4)
    tk.Button(joy,text = "y+",command = lambda : xyzcontrol("y+")).grid(row = 2,column = 1,padx = 4,pady = 4)
    tk.Button(joy,text = "x-",command = lambda : xyzcontrol("x-")).grid(row = 1,column = 0,padx = 4,pady = 4)
    tk.Button(joy,text = "x+",command = lambda : xyzcontrol("x+")).grid(row = 1,column = 2,padx = 4,pady = 4)
    tk.Button(joy,text = "home",command = toHome).grid(row = 1,column = 1,padx = 4,pady = 4)

    tk.Button(joy,text = "z-",command = lambda : xyzcontrol("z-")).grid(row = 0,column = 3,padx = 4,pady = 4)
    tk.Button(joy,text = "z+",command = lambda : xyzcontrol("z+")).grid(row = 2,column = 3,padx = 4,pady = 4)

    #tk.Label(frame2,text = "control Y [mm] :").grid(row = 2,column = 0)
    #tk.Label(frame2,text = "control Z [mm] :").grid(row = 3,column = 0)

    tk.Label(frame2,text = "control rail direction :").grid(row = 4,column = 0)
    railjoy = tk.Frame(frame2,width=100, height=30,bg = "Red") 
    tk.Button(railjoy,text = "L-",command = lambda : railControl(-1)).grid(row = 0,column = 0,padx = 4,pady = 4)
    tk.Button(railjoy,text = "L+",command = lambda : railControl(1)).grid(row = 0,column = 1,padx = 4,pady = 4)
    railjoy.grid(row = 5,column = 0)

#----------- dobot run : maunal command -----------#
def xyzcontrol(cmd):
    if not connect:
        print("Warning: not connect")
        status['text'] = "Warning: not connect"
    else:
        robot.setJog("xyz",cmd)

def railControl(rail_direction):
    if not connect:
        print("Warning: not connect")
        status['text'] = "Warning: not connect"
    else:
        status['text'] = "rail is moving"
        defaultSpeed = 2

        robot.stepperDriveDis(1,defaultSpeed,1,rail_direction)
        robot.update()   
        None

def toHome():
    if not connect:
        print("Warning: not connect")
        status['text'] = "Warning: not connect"
    else:

        global robot
        robot.setPosition(x = 150,y = 0,z = 0)
        status['text'] = "to home 150,0,0"
        time.sleep(1)
        robot.update()

#------------- dobot run : automatic --------------#
def run():
    #Max height 240
    global width,height,status,isspraying,rail_direction
    if width.get().isnumeric() : w = int(width.get())
    else: w = 160
    if height.get().isnumeric() : h = int(height.get())
    else: h = 360

    if w> 160: w = 160
    if h> 360: h = 360 
    elif h < 120:
        status['text'] = "Height is lower than limit"

        return
    hUpper = h-5-240
    wUpper = w-5
    hLower = -120
    wLower = 0 

    robot.setPosition(x = 200,y = 0,z = 0)
    time.sleep(1)
    robot.update()
    step = 20



    for dis in range(wLower,wUpper+step,step):

        #move rail    
        if dis !=0 :
            if dis+step > w:
                move  = ( wUpper-dis+step)%step
                #print("move special",w-dis) 
            else:
                move = step
                #print("move normal",stp)


            defaultSpeed = 2
            robot.stepperDriveDis(1,defaultSpeed,move,rail_direction)
            robot.update()  

        status['text'] = "painting at "+str(dis//step+1)

        for i in range(2):
            robot.setPosition(x = 150,y = 0,z = 0)
            time.sleep(1)
            robot.update()


            robot.setPosition(x = 230,y = 0,z = hLower)
            time.sleep(1)
            robot.update()
            
            if isspraying:
                status['text'] = "Spraying"
                robot.switch12V(16,"on")
                robot.update()
                timespray = 7
                for ti in range(timespray):
                    status['text'] = "Spraying left:"+str(timespray-ti)+" [s]"
                    time.sleep(1)
                robot.switch12V(16,"off")
                status['text'] = "finish Spraying"
                robot.update()
            else : status['text'] = "not Spraying"


            robot.setPosition(x = 230,y = 0,z = hUpper)
            time.sleep(1)
            robot.update()

            robot.setPosition(x = 200,y = 0,z = hUpper)
            status['text'] = "finish loop :"+str(i+1)+"/2"
            time.sleep(1)
            robot.update()

        robot.setPosition(x = 200,y = 0,z = 0)
        time.sleep(1)
        robot.update()

    status['text'] = "Complete" 


        
          
 

#----------- dobot connect -----------#

robot = paint.paintingAPI()



#------------ user interface ---------#


app =tk.Tk()
app.geometry("400x400")

frame1 = tk.Frame(app,width=400, height=50, bg="black")     #connection bar
frame2 = tk.Frame(app,width=400, height=330,)               #main body
frame3 = tk.Frame(app,width=400, height=20)                 #status bar  
frame1.pack(fill=tk.BOTH)
frame2.pack(fill=tk.BOTH,)
frame3.pack(fill=tk.BOTH,side = tk.BOTTOM)

tkrail_direction = tk.IntVar()
tkisspraying = tk.BooleanVar()

connectbtn =tk.Button(frame1,text = "connect",bg = "green",command = connection)
connectbtn.grid(padx = 2)

#--------------------- main body ---------------------#
AutoUI()

#--------------------- status Label -------------------#
statusLabel = tk.Label(frame3, text="status :", bd=1, relief=tk.SUNKEN).grid(row = 0,column = 0,columnspan = 2)
status = tk.Label(frame3,text = "None", relief=tk.SUNKEN)
status.grid(row = 0,column = 2,padx = 1,columnspan = 2)

coorlocation = tk.Label(frame3,text = "Coordinate (x,y,z,rHead) : ",relief=tk.SUNKEN)
coorlocation.grid(row = 0,column = 4,sticky = tk.SE)
jointlocation = tk.Label(frame3,text = "joint (j1,j2,j3,j4) : ")
jointlocation.grid(row = 1,column = 4)



app.title("painting dobot")
menubar = tk.Menu(app)
menubar.add_command(label="Automatic",command=lambda: swap("Auto"))    
menubar.add_command(label="Manual",command=lambda : swap("Manual"))  



app.config(menu=menubar)  
app.mainloop()
exit()






