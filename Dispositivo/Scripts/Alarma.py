import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
from datetime import datetime
from datetime import date
# DEFINICIONES PARA ASIGNACION DE PINES
LCD_RS    = 27
LCD_E     = 22
LCD_D4    = 24
LCD_D5    = 25
LCD_D6    = 4
LCD_D7    = 17
####salidas
Alar=5
Puerta=20
Indicador=19
###entradas
Btnac=6
Btnds=12
BtnOpen=13
BtnClose=16
BtnAun=26
BtnDis=21
BtnCon=18
GPIO.setmode(GPIO.BCM)
activar=0
valA="00:00"
valD="00:00"
Datos=["","","","","",""]
Seabrir="0"
Secerrar="0"
Sebactivar="0"
Sebdesac="0"
mqttc=mqtt.Client()
# DEFINIR CONSTANTES DEL DISPOSITIVO
LCD_WIDTH = 16 # CARACTERES MAXIMOS POR FILA
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80 # DIRECCION RAM PARA PRIMERA LINEA
LCD_LINE_2 = 0xC0 # DIRECCION RAM PARA SEGUNDA LINEA
E_PULSE = 0.00005 # CONSTANTES PARA RETARDOS
E_DELAY = 0.00005

def on_message(client,obj,msg):
    
    Mensaje=msg.payload.decode('utf-8')
    Dividir(Mensaje)
    

def Open():
    pwm=GPIO.PWM(Puerta,100)
    pwm.start(AngleToDuty(180))
    time.sleep(0.2)
    pwm.stop()

def Close():
    pwm=GPIO.PWM(Puerta,100)
    pwm.start(AngleToDuty(0))
    time.sleep(0.2)
    pwm.stop()

def AngleToDuty(ang):
  return float(ang)/10.+5.

def main():
    global mqttc
    #DEFINIR PARAMETROS DE CONEXION
    mqttc=mqtt.Client()
    mqttc.on_message=on_message
    mqttc.username_pw_set("jomsk@hotmail.com","Jomsk4all1996")
    mqttc.connect("maqiatto.com",1883)
    mqttc.subscribe("jomsk@hotmail.com/IoT1",0)
    
    # DEFINIR GPIO COMO SALIDA PARA USAR LA LCD
    GPIO.setup(LCD_E, GPIO.OUT) # E
    GPIO.setup(LCD_RS, GPIO.OUT) # RS
    GPIO.setup(LCD_D4, GPIO.OUT) # DB4
    GPIO.setup(LCD_D5, GPIO.OUT) # DB5
    GPIO.setup(LCD_D6, GPIO.OUT) # DB6
    GPIO.setup(LCD_D7, GPIO.OUT) # DB7
    
    ##establecer en modo de los pines 
    GPIO.setup(Alar,GPIO.OUT)
    GPIO.setup(Puerta,GPIO.OUT)
    GPIO.setup(Indicador,GPIO.OUT)
    GPIO.setup(Btnac,GPIO.IN)
    GPIO.setup(Btnds,GPIO.IN)
    GPIO.setup(BtnClose,GPIO.IN)
    GPIO.setup(BtnOpen,GPIO.IN)
    GPIO.setup(BtnAun,GPIO.IN)
    GPIO.setup(BtnDis,GPIO.IN)
    GPIO.setup(BtnCon,GPIO.IN)

    # INICIALIZAR DISPLAY
    lcd_init()
    time.sleep(1)
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string("ALARMA TEMPORI..")

    global activar
    global valA
    global valD
    global Datos
    global Seabrir
    global Secerrar
    global Sebactivar
    global Sebdesac
    abrir=0
    cerrar=0
    bactivar=0
    bdesac=0
    abrir=0
    cerrar=0
    bactivar=0
    bdesac=0
    pwm=0
    cont=0
    Hora=0
    Min=0
    Open()
    
    while(1):

        mqttc.loop()
        abrir=GPIO.input(BtnOpen)
        cerrar=GPIO.input(BtnClose)
        bactivar=GPIO.input(Btnac)
        bdesac=GPIO.input(Btnds)
        if(bactivar==1 or Sebactivar=="1"):##aplastar Activar
            activar=1
            GPIO.output(Indicador,1)
            Close()
        if(bdesac==1 or Sebdesac=="1"):##aplastar Desactivar
            activar=0
            GPIO.output(Indicador,0)
            GPIO.output(Alar,0)
            Open()
        if((abrir==1 or Seabrir=="1") and activar==1):##cuando abre la puerta y la alarma esta activada
            GPIO.output(Alar,1)
        if(cerrar==1 or Secerrar=="1"):##cuando se cierra la cerradura desactiva la alarma
            GPIO.output(Alar,0)
            Close()
        if(abrir==1 or Seabrir=="1"):##presiona el btn abrir
            Open()       
        if(activar==0 and (bdesac==1 or Sebdesac=="1")):##desactiva la alarma y apaga la silencia
            GPIO.output(Alar,0)

        if(GPIO.input(BtnCon)==1):
            valA=CTime(0)
            valD=CTime(1)
            mqttc.publish("jomsk@hotmail.com/IoT","0/"+valA+"/"+valD)
           
        
            
##        today = datetime.now().time()
        lcd_byte(LCD_LINE_2, LCD_CMD)
        lcd_string("S "+valA+" F "+valD)
        
        ComTimes(valA+":00",valD+":00")
        
        mqttc.publish("jomsk@hotmail.com/IoT","1/"+valA+"/"+valD)
        
        if(Datos!=""):
            valA=(Datos[0])
            valD=(Datos[1])
            Seabrir=(Datos[4])
            Secerrar=(Datos[5])
            Sebactivar=(Datos[2])
            Sebdesac=(Datos[3])
            

    
#################FUNCIONES PARA EL LCD#################
def lcd_init():													#
    # PROCESO DE INICIALIZACION								#
    lcd_byte(0x33,LCD_CMD)										#
    lcd_byte(0x32,LCD_CMD)										#
    lcd_byte(0x28,LCD_CMD)										#
    lcd_byte(0x0C,LCD_CMD)										#	
    lcd_byte(0x06,LCD_CMD)										#
    lcd_byte(0x01,LCD_CMD)										#
########################################################
def lcd_string(message):											#	
    # ENVIAR UN STRING A LA LCD								#
    message = message.ljust(LCD_WIDTH," ")						#
    for i in range(LCD_WIDTH):										#
        lcd_byte(ord(message[i]),LCD_CHR)							#
########################################################
def lcd_byte(bits, mode):											#			
    GPIO.output(LCD_RS, mode) # RS								#			
    GPIO.output(LCD_D4, False)									#
    GPIO.output(LCD_D5, False)									#
    GPIO.output(LCD_D6, False)									#
    GPIO.output(LCD_D7, False)									#
    if bits&0x10==0x10:											#	
        GPIO.output(LCD_D4, True)									#
    if bits&0x20==0x20:											#
        GPIO.output(LCD_D5, True)									#
    if bits&0x40==0x40:											#
        GPIO.output(LCD_D6, True)									#
    if bits&0x80==0x80:											#
        GPIO.output(LCD_D7, True)									#
    time.sleep(E_DELAY)											#			
    GPIO.output(LCD_E, True)										#
    time.sleep(E_PULSE)											#
    GPIO.output(LCD_E, False)										#
    time.sleep(E_DELAY)											#				
    GPIO.output(LCD_D4, False)									#
    GPIO.output(LCD_D5, False)									#
    GPIO.output(LCD_D6, False)									#
    GPIO.output(LCD_D7, False)									#
    if bits&0x01==0x01:											#
        GPIO.output(LCD_D4, True)									#
    if bits&0x02==0x02:											#
        GPIO.output(LCD_D5, True)									#	
    if bits&0x04==0x04:											#
        GPIO.output(LCD_D6, True)									#
    if bits&0x08==0x08:											#
        GPIO.output(LCD_D7, True)									#
    time.sleep(E_DELAY)											#
    GPIO.output(LCD_E, True)										#
    time.sleep(E_PULSE)											#
    GPIO.output(LCD_E, False)										#
    time.sleep(E_DELAY)											#
########################################################

def CTime(Title):
    global mqttc
    time.sleep(0.5)
    if(Title==0):
        lcd_byte(LCD_LINE_1, LCD_CMD)
        lcd_string(" Hora Encendido ")
    else:
        lcd_byte(LCD_LINE_1, LCD_CMD)
        lcd_string("  Hora Apagado  ")
    horaS="00"
    minS="00"
    Value=""
    i=0
    CnTime=0
    while(1):
        if(GPIO.input(BtnAun)==1):
            time.sleep(0.5)
            i=1+i;
            if(CnTime==0):
                if(i>23):
                    i=0
            if(CnTime==1):
                if(i>59):
                    i=0
        if(GPIO.input(BtnDis)==1):
            time.sleep(0.5)
            i=i-1;
            if(CnTime==0):
                if(i<0):
                    i=23
            if(CnTime==1):
                if(i<0):
                    i=59
        if(GPIO.input(BtnCon)==1):
            time.sleep(0.5)
            CnTime=CnTime+1
            i=0
            if(CnTime==2):
                lcd_byte(LCD_LINE_1, LCD_CMD)
                lcd_string("ALARMA TEMPORI..")
                break
            
        if(CnTime==0):
            Value="Horas:     "
            if(i<10):
                horaS="0"+str(i)
            else:
                horaS=str(i)
        if(CnTime==1):
            Value="Minutos:   "
            if(i<10):
                minS="0"+str(i)
            else:
                minS=str(i)
        
            
        lcd_byte(LCD_LINE_2, LCD_CMD)
        lcd_string(Value+horaS+":"+minS)
        
    if(Title==0):
        mqttc.publish("jomsk@hotmail.com/IoT","0/"+str(horaS)+":"+str(minS)+"/"+valD)
        print("valor 1")
    else:
        mqttc.publish("jomsk@hotmail.com/IoT","0/"+valA+"/"+str(horaS)+":"+str(minS))
        print("valor 2")
        
    time.sleep(0.5)        
    return str(horaS)+":"+str(minS)

def ComTimes(valA,valD):
    timeS =time.strftime("%H:%M:%S")
    global activar
    
    if(timeS==valA):
        activar=1
        GPIO.output(Indicador,1)
        Close()
        print(timeS)
    if(timeS==valD):
        activar=0
        GPIO.output(Indicador,0)
        GPIO.output(Alar,0)
        Open()
        print(timeS)
        
def Dividir(Mensaje):
    global Datos
    Datos[0]=Mensaje.split("/")[0]
    Datos[1]=Mensaje.split("/")[1]
    Datos[2]=Mensaje.split("/")[2]
    Datos[3]=Mensaje.split("/")[3]
    Datos[4]=Mensaje.split("/")[4]
    Datos[5]=Mensaje.split("/")[5]
    

