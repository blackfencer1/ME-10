#-*- coding: utf-8 -*-
# MADE BY: Seunghan
import RPi.GPIO as GPIO
import pygame as py
import pygame.gfxdraw
import math
import serial
import time
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import threading, requests


if not firebase_admin._apps:
    
    cred = credentials.Certificate('/home/pi/practice/me-10server-firebase-adminsdk-ljxt1-e3c959b426.json')
    firebase_admin.initialize_app(cred,{
        'databaseURL':'https://me-10server-default-rtdb.firebaseio.com/'})
dir = db.reference()




# setup GPIO
start_switch = 5  # pin 26, switch to gnd
stop_switch = 6  # pin 40, switch to gnd
start = 0
stop = 0


        

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(start_switch,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stop_switch,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    

def displayupdate():
    
    global voltage
    #global V
    global left_degree
    #global ldegree
    global right_degree
    #global rdegree
    global time1

    
    try:
            
        rangauge = ser.readline().decode().strip()
        print(rangauge)
        sowow = rangauge.split("w")
        
        voltage = str(sowow[0])
        left_degree = str(sowow[1])
        right_degree = str(sowow[2])
        wow = sowow[3]

        woww= float(wow)
        V = float(voltage)
        ldegree = float(left_degree)
        rdegree = float(right_degree)
        percentage = int(woww)
        
    except ValueError:
            
        percentage = 0
        voltage = "0"
        V = 0
        left_degree = "0"
        ldegree = 0
        right_degree = "0"
        rdegree = 0
        
    if ldegree >= 70:
        
        lcolor =  [255,0,0]
    else:
        
        lcolor = [29,219,22]
    
    if rdegree >= 70:
        
        rcolor =  [255,0,0]
    else:
        
        rcolor = [29,219,22]
        
    if V <= 40:
        
        vcolor =  [255,0,0]
    else:
        
        vcolor = [29,219,22]
        
    
    screen.blit(background,(0,0)) ## Blit the background onto the screen first
    my_gauge.draw(percent=percentage)
    my_gauge.textdraw(msg,[50,55])
    my_gauge.textdraw(str(lapnum),[680,60])
    
    my_gauge.twrite("Left:   " + left_degree + " °C",lcolor,[560,195])
    my_gauge.twrite("Right: " + right_degree + " °C",rcolor,[560,245])
    my_gauge.twrite("Voltage:",vcolor,[565,325])
    my_gauge.twrite(voltage + " V",vcolor,[625,390])
    my_gauge.textdraw(time1,[15,170])
    my_gauge.textdraw(time2,[15,210])
    my_gauge.textdraw(time3,[15,250])
    my_gauge.textdraw(time4,[15,290])
    my_gauge.textdraw(time5,[15,330])
    my_gauge.textdraw(time6,[15,370])
    my_gauge.textdraw(time7,[15,410])
    
    my_gauge.textdraw("LAP:",[560,60])
    my_gauge.textdraw("km/h",[365,300])
    pygame.draw.line(screen,[255,255,255], [250,0],[250,480],3)
    pygame.draw.line(screen,[255,255,255], [550,0],[550,480],3)
    pygame.draw.line(screen,[255,255,255], [0,150],[250,150],3)
    pygame.draw.line(screen,[255,255,255], [550,160],[800,160],3)
    pygame.draw.line(screen,[255,255,255], [550,320],[800,320],3)
        
        
    pygame.display.update()
    clock.tick(fps)
    
def server():
    global mark
    
    
    while True:
        
        
        dir.update({'Laptime': msg})
        dir.update({'voltage': voltage})
        dir.update({'left_degree': left_degree})
        dir.update({'right_degree': right_degree})
        if mark == 1:
            dir.child("Past_Lap").push(time1)
            mark = 0
        else:
            pass
         
        dir.update({'lap': lapnum})


class Gauge:

    def __init__(self, screen, FONT, x_cord, y_cord, thickness, radius, circle_colour, glow=True):
        self.screen = screen
        self.Font = FONT
        self.tFont = textFONT
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.thickness = thickness
        self.radius = radius
        self.circle_colour = circle_colour
        self.glow = glow
        pygame.mouse.set_visible(0)
        
        
    def textdraw(self, text,loc):
        
        anotext = self.tFont.render(text, True, [29,219,22])
        self.screen.blit(anotext, loc)
        
    def twrite(self, text,color,loc):
        
        anotext = self.tFont.render(text, True, color)
        self.screen.blit(anotext, loc)
        

    def draw(self, percent):
        fill_angle = int(percent*270/100)
        per=percent
        
        if per <= 40:
            per=0
            ac = [29,219,22]
        else: 
            per = 100
            ac = [255,0,0]
            
            
        for indexi in range(len(ac)):
            if ac[indexi] < 0:
                ac[indexi] = 0
            if ac[indexi] > 255:
                ac[indexi] = 255
        
    
        #print(ac)
        pertext = self.Font.render(str(percent), True, ac) #+ "%"
        pertext_rect = pertext.get_rect(center=(int(self.x_cord), int(self.y_cord)))
        self.screen.blit(pertext, pertext_rect)
        
        for i in range(0, self.thickness):
            pygame.gfxdraw.arc(screen, int(self.x_cord), int(self.y_cord), self.radius - i, -225, 270 - 225, self.circle_colour)
            if percent >4:
                pygame.gfxdraw.arc(screen, int(self.x_cord), int(self.y_cord), self.radius - i, -225, fill_angle - 225-8, ac)
        if percent < 4:
            return
        if self.glow:
            for i in range(0,15):
                ac [3] = int(150 - i*10)
                pygame.gfxdraw.arc(screen, int(self.x_cord), int(self.y_cord), self.radius + i, -225, fill_angle - 225-8, ac)
            for i in range(0,15):
                ac [3] = int(150 - i*10)
                pygame.gfxdraw.arc(screen, int(self.x_cord), int(self.y_cord), self.radius -self.thickness - i, -225, fill_angle - 225-8, ac)
            angle_r = math.radians(fill_angle-225-8)
            lx,ly = int((self.radius-self.thickness/2)*math.cos(angle_r)), int( (self.radius-self.thickness/2)*math.sin(angle_r))
            ac[3] = 255
            lx = int(lx+self.x_cord)
            ly = int(ly + self.y_cord)
            pygame.draw.circle(self.screen,ac,(lx,ly),int(self.thickness/2),0)
            for i in range(0,10):
                ac [3] = int(150 - i*15)
                pygame.gfxdraw.arc(screen, int(lx), int(ly), (self.thickness//2)+i , fill_angle -225-10, fill_angle - 225-180-10, ac)

def start(channel):
    
    global start
    if start == 1:
        start = 2
    else:
        start = 1

def stop(channel):
        
    global stop   
    stop = 1
    
    
try:
    ser = serial.Serial('/dev/ttyACM0',115200)
    
except serial.serialutil.SerialException:
    os.system("/home/pi/practice/perfect.py")
    
if __name__ == '__main__':

    time.sleep(1)
    circle_c = (116,116,116)   # circle color RGB

    pygame.init()
    width = 800
    height = 480
    
    background = py.image.load("/home/pi/practice/me10.png") ## Load the image file
    background = py.transform.scale(background,(width,height)) ## Make it the same size as the screen
    
    
    
    
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height),pygame.FULLSCREEN)
    pygame.display.set_caption('Gauge')
    fps = 100
    
    
    FONT = pygame.font.SysFont('ARIAL', 70)   #center number('gul-ggol', font size)
    textFONT = pygame.font.SysFont('ARIAL', 35)   #km/h ('gul-ggol', font size)
    
    
    my_gauge = Gauge(
        screen=screen,
        FONT=FONT,
        x_cord=width / 2,
        y_cord=height / 2,
        thickness=25, #gauge thickness
        radius=130,   #gauge radius
        circle_colour=circle_c,
        glow=False)
    percentage = 0
    ifdelay = 0
    msg = "00:00:000"
    run = 0
    lapnum = 1
    mark = 0

    
    time1=""
    time2=""
    time3=""
    time4=""
    time5=""
    time6=""
    time7=""
    
    GPIO.add_event_detect(start_switch,GPIO.RISING,callback = start,bouncetime = 200)
    GPIO.add_event_detect(stop_switch,GPIO.RISING,callback = stop,bouncetime = 200)
    
    
    t1 = threading.Thread(target = server)
    t1.daemon = True
    t1.start()
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    GPIO.cleanup()
                    dir.delete()
                    sys.exit()
                    
                    
        # check for start
        
    
        
        if start == 1 or run == 1:
            if run == 0:
                start_time = time.time()

            now = time.time() - start_time
            # calculate h,m,s
            m,s = divmod(now,60)
            #h,m = divmod(m,60)
            # Display
            msg= "%02d:%02d" % (m,s)
            psec = str(now-int(now))
            pstr = psec[1:5]    #decimal
            msg = msg + str(pstr)
            # set to run continuously
            run = 1
            
            
        if start == 2:
            start = 1
            time7=time6
            time6=time5
            time5=time4
            time4=time3
            time3=time2
            time2=time1
            time1= str(lapnum) + " :  " + str(msg)
            mark = 1
            start_time = time.time()
            lapnum += 1
            
      # check for stop
        if stop == 1:
            stop = 0
            start = 0
            msg = "00:00:000"
            run = 0
            first = 1
            
            lapnum = 1
            time1=""
            time2=""
            time3=""
            time4=""
            time5=""
            time6=""
            time7=""
            dir.child("Past_Lap").delete()
            
            
        displayupdate()
        
    

        

        
    # FOR SHOWING CHANGE IN GAUGE

# KeyboardInterrupt:
GPIO.cleanup()
