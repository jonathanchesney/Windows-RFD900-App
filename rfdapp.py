from time import sleep
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import font
import serial.tools.list_ports
import serial


data = True
# ser data input format: "b/11.11/22.22/33.33/\n"
ser = serial.Serial()
ser.baudrate = 9600                                # Match baud rate setting on RFD900, or serial transmitter.
ser.timeout = 0


# Allows for automatic GUI updating, while waiting for keyboard interrupts
class SensorThread(threading.Thread):
    def run(self):
        try:
            while True:
                sleep(1)
        except KeyboardInterrupt:
            exit()


class Gui(object):

    # Instantiates all tkinter objects within Gui constructor
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Armada Aeronautics: Remote Vehicle Interface")
        self.customFont = font.Font(family="Helvetica", size=10, weight=font.BOLD, slant=font.ITALIC)
        self.root.configure(bg="snow")
        self.label = tk.Label(self.root, text="Live Data Feed:", bg="snow", font =self.customFont)
        self.label2 = tk.Label(self.root, text="Controls:", bg="snow", font =self.customFont)
        self.Sensor1 = tk.Label(self.root, text="Sensor1:", bg="snow", font =self.customFont)
        self.Sensor2 = tk.Label(self.root, text="Sensor2:", bg="snow", font =self.customFont)
        self.Sensor3 = tk.Label(self.root, text="Sensor3:", bg="snow", font =self.customFont)
        self.Sensor4 = tk.Label(self.root, text="Sensor4:", bg="snow", font =self.customFont)
        self.Sensor5 = tk.Label(self.root, text="Sensor5:", bg="snow", font =self.customFont)
        self.Throttle = tk.Label(self.root, text="Throttle:", bg="snow", font =self.customFont)
        self.Pitch = tk.Label(self.root, text="Pitch:", bg="snow", font =self.customFont)
        self.Yaw = tk.Label(self.root, text="Yaw:", bg="snow", font =self.customFont)
        self.Roll = tk.Label(self.root, text="Roll:", bg="snow", font =self.customFont)
        self.portLbl = tk.Label(self.root, text="Choose Serial Port:", bg="snow")
        self.serPorts = ttk.Combobox(self.root, values=self.serial_ports())
        self.Data1 = tk.Label(self.root, text="NULL", bg="snow")
        self.Data2 = tk.Label(self.root, text="NULL", bg="snow")
        self.Data3 = tk.Label(self.root, text="NULL", bg="snow")
        self.Data4 = tk.Label(self.root, text="NULL", bg="snow")
        self.Data5 = tk.Label(self.root, text="NULL", bg="snow")
        self.DataT = tk.Label(self.root, text="NULL", bg="snow")
        self.DataP = tk.Label(self.root, text="NULL", bg="snow")
        self.DataY = tk.Label(self.root, text="NULL", bg="snow")
        self.DataR = tk.Label(self.root, text="NULL", bg="snow")
        self.serPorts.bind('<<ComboboxSelected>>', self.on_select)
        self.Scale = tk.Scale(self.root, from_=100, to=0, troughcolor="gray0", highlightcolor="red", command= self.throttle_select, bg="snow")
        self.ThrottleLbl = tk.Label(self.root, text="Throttle:", bg="snow", font =self.customFont)
        self.Refresh = tk.Button(self.root, text="Reconnect", command = self.refresh_ser, bg="snow")
        self.HeadlightLbl = tk.Label(self.root, text="Headlights:", bg="snow", font =self.customFont)
        self.Lights = tk.Button(self.root, text="OFF", command = self.toggle_lights, bg = "gray0", fg="white smoke")
        self.light = False
        self.EstopLbl = tk.Label(self.root, text="Emergency:", bg="snow", font =self.customFont)
        self.Estop = tk.Button(self.root, text="STOP", command = self.EmergencyStop, bg="red")
        
        self.DataArray = ["","NULL", "NULL", "NULL", "NULL"]
        self.updateGUI()
        self.readSensor()

    # Function that is run as initialization step, determining coordinates of tkinter
    # objects in grid formatting
    def run(self):
        self.label.grid(column=0, row=0)
        self.Sensor1.grid(column=5, row=2)
        self.Sensor2.grid(column=5, row=3)
        self.Sensor3.grid(column=5, row=4)
        self.Sensor4.grid(column=5, row=5)
        self.Sensor5.grid(column=5, row=6)
        self.Data1.grid(column=6, row=2)
        self.Data2.grid(column=6, row=3)
        self.Data3.grid(column=6, row=4)
        self.Data4.grid(column=6, row=5)
        self.Data5.grid(column=6, row=6)
        self.Throttle.grid(column=3, row=2)
        self.Pitch.grid(column=3, row=3)
        self.Yaw.grid(column=3, row=4)
        self.Roll.grid(column=3, row=5)
        self.DataT.grid(column=4, row=2)
        self.DataP.grid(column=4, row=3)
        self.DataY.grid(column=4, row=4)
        self.DataR.grid(column=4, row=5)
        self.portLbl.grid(column=9, row=0)
        self.serPorts.grid(column=9, row=1)
        self.Refresh.grid(column=9, row=2)
        self.label2.grid(column=0, row=7)
        self.ThrottleLbl.grid(column=3,row=8)
        self.Scale.grid(column=4, row=8)
        self.Lights.grid(column=6, row=8)
        self.HeadlightLbl.grid(column=5, row=8)
        self.EstopLbl.grid(column=7, row=8)
        self.Estop.grid(column=8, row=8)
        self.root.after(1000, self.updateGUI)
        self.root.mainloop()
        

    def updateGUI(self):
        self.root.update()
        self.root.after(1000, self.updateGUI) 

    # Reads sensor data
    def readSensor(self):
        if ser.is_open:
            try:
                data = ser.readline().decode('ascii')
                if data.count('/') == 4:                       # 4 slashes indicates 3 "data objects" being read, increase to n + 1,
                    self.DataArray = data.split('/')           # where n is number of "data objects" in string
            except:
                self.root.after(527, self.readSensor)

            print(self.DataArray)                              # Directly updates data values in GUI
            self.DataP["text"] = self.DataArray[1]
            self.DataY["text"] = self.DataArray[2]
            self.DataR["text"] = self.DataArray[3]
            self.DataT["text"] = self.Scale.get()
            self.root.update()
        self.root.after(527, self.readSensor)


    # Function for writing data back to prototype
    # Improve in future by modularizing formatting
    def writeData(self, msg):
        ser.write(msg)
        print("Message Written:")
        print(msg)

    # Returns list of serial ports accessible by computer (COM)
    # Necessary for selecting serial port
    def serial_ports(self):    
        return serial.tools.list_ports.comports()

    # Opens a serial port upon its selection in tkinter combobox
    def on_select(self, event=None):
        # get selection directly from combobox
        print("comboboxes: ", self.serPorts.get())
        s = self.serPorts.get()
        ser.port = s.split(' ')[0]	
        ser.open()			# maybe want to raise exception here, notify user if bad port
        sleep(1)
        self.root.after(100, self.updateGUI)

    # Writes selected throttle value to prototype
    def throttle_select(self, event=None):
        if ser.is_open:
            self.writeData(self.Scale.get())            # format to match receiving end syntax
    
    # Opens and closes serial ports, in case of transmission failure within this application
    def refresh_ser(self):
        if ser.is_open:
            ser.close()
            sleep(1)
            ser.open()
        else:
            ser.open()
            sleep(1)

    # Writes data to prototype to turn lights either on or off
    # Lights are represented as a tkinter button, which changes color as toggled
    def toggle_lights(self):    
        if ser.is_open: 
            if self.light == False: 
                self.writeData(1001)                # format to match receiving end syntax  
                self.light = True   
                self.Lights["text"] = "ON"  
                self.Lights.configure(bg = "yellow", fg="gray0")    

            else:   
                self.writeData(1000)                # format to match receiving end syntax
                self.light = False  
                self.Lights["text"] = "OFF" 
                self.Lights.configure(bg = "gray0", fg="white smoke")   
   
    # Writes emergency stop transmission to prototype         
    def EmergencyStop(self):
        if ser.is_open:
            self.writeData(1101)                   # format to match receiving end syntax
            self.Scale.set(0)

    # GUI deconstructor
    # Necessary to automatically close COM port upon closing App
    def __del__(self):
        ser.close()

if __name__ == "__main__":
    SensorThread().start()
    Gui().run()                                    # Initialize grid coordinates in GUI
