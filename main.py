__author__ = 'will'





#python code based on work by electronut: https://gist.github.com/electronut/5641933




from collections import deque
from matplotlib import pyplot as plt
from serial.tools import list_ports
import serial
import os


def list_serial_ports():
    # Windows
    if os.name == 'nt':
        # Scan for available ports.
        available = []
        for i in range(256):
            try:
                s = serial.Serial(i)
                available.append('COM' + str(i + 1))
                s.close()
            except serial.SerialException:
                pass
        return available
    else:
        # Mac / Linux
        return [port[0] for port in list_ports.comports()]


print list_serial_ports()



# class that holds analog data for N samples
class AnalogData:
    # constr

    def __init__(self, maxLen):
        self.ax = deque([0.0] * maxLen)
        self.ay = deque([0.0] * maxLen)
        self.maxLen = maxLen
        self.datas = 0

    # ring buffer
    def addToBuf(self, buf, val):
        if len(buf) < self.maxLen:
            buf.append(val)
        else:
            buf.pop()
            buf.appendleft(val)

    # add data
    def add(self, data):
        self.addToBuf(self.ax, data)
        self.datas+=1

# plot class
class AnalogPlot:
    # constr
    def __init__(self, analogData):
        # set plot to animated
        plt.ion()
        self.axline, = plt.plot(analogData.ax)
        self.ayline, = plt.plot(analogData.ay)
        plt.ylim([0, 500])

    # update plot
    def update(self, analogData):
        self.axline.set_ydata(analogData.ax)
        self.ayline.set_ydata(analogData.ay)
        plt.draw()


# main() function
def main():
    # expects 1 arg - serial port string

    analogData = AnalogData(50)
    analogPlot = AnalogPlot(analogData)
    # open serial port
    ser = serial.Serial(list_serial_ports()[-1], 1000000)
    while True:
        try:
            while ser.inWaiting()>2:
                while ord(ser.read(1)) != 255:
                    pass
                high = ord(ser.read(1))
                low = ord(ser.read(1))
                data =(high << 8) + low
                #print high,low, data
                analogData.add(data)
            analogPlot.update(analogData)

        except KeyboardInterrupt:
            print 'exiting'
            break
    # close serial
    ser.flush()
    ser.close()

# call main
if __name__ == '__main__':
    main()