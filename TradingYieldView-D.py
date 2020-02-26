# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 12:03:44 2020

@author: johany.carmona@udea.edu.co
"""

# -*- coding: utf-8 -*-
import time
import math
import os
import matplotlib.pyplot as plt

#Glosario
#Registro: Un registro contiene los datos de un conjunto de sesiones de trading.
#Sesión: Una sesión contiene los datos de un conjunto de operaciones de trading.
#Operación: Una operación contiene los datos de la operación ejecutada por marco de tiempo.

choice=-1 # 'Choice' Opción elegida en el menú.
nr=0 # 'NumberRecords' Número de registros almacenados.

while choice!=3: #Mientras la opción elegida por el usuario no sea 'Salir', el programa seguirá ejecutándose.
    
    CG=100#Capital inicial configuración general de los registros. Al momento de crearse un nuevo registro, éste tomará el valor del parámetro configurado en el menú principal.
    C=CG #Capital inicial configuración privada del registro
    lp=1 # 'LaborPrice' Precio mínimo hora de trabajo en Colombia (USD$0.92 Hora SMMLV(COL))
    lps=-0.03 # 'LossPerSesion' Proporción de pérdida máxima por operación.
    pps=0.06 #'ProfitPerSesion' Proporción de ganancia máxima por operación.
    CIotmi=20#'CompoundInterestTimeMinuteInitial' Momento en el tiempo expresado en minutos a partir del cual se realiza el cálculo del Interés Compuesto, a valores más cercanos a (0), mayor será la fluctuación y la amplitud del nivel de interés compuesto en la gráfica. 
    pts=3#'ProcessingTimeSecond' Parámetro que proporciona el tiempo máximo que está dispuesto el usuario a esperar para realizar correctamente la iteración para el cálculo de 'm' o el número de operaciones esperadas hasta quemar la cuenta.
    ipo=1#'InvestimentPerOperation' Parámetro de cantidad mínima invertida en dólares en cada operación UNITARIA por marco temporal.
    request="none" #Petición que realiza el usuario dentro de un registro de datos.
    
    dss="000000" #'DateStartSession' Variable que almacena la fecha en que se ha realizado la última sesión en el registro.
    Pss=[]#'ProbabilityStartSession' Vector que expresa la probabilidad que se tiene en cada inicio de sesión en un registro.
    CIss=[]#'CompoundInterestStartSession' Vector que expresa la tasa de interés compuesto que se tiene en cada inicio de sesión en un registro.
    Rss=[]#'RentabilityStartSession' Vector que expresa la tasa de rentabilidad que se tiene en cada inicio de sesión en un registro.
    Iss=[]#'IncomeStartSession' Vector que expresa el nivel de ingreso que se tiene en cada inicio de sesión en un registro.
    INVss=[]#'RentabilityStartSession' Vector que expresa el nivel de inversión que se ha realizado en cada inicio de sesión en un registro.
    avINVss=[]#'AverageInvestimentStartSession' Vector que expresa el nivel de inversión promedio en el momento en el que se inicia operación en el registro.
    Coss=[]#'CapitalOperationStartSession' Vector que expresa el nivel de capital que se ha tenido en cada inicio de sesión en un registro.
    Rrss=[]#'RentabilityRelativeStartSession' Vector que expresa la tasa de rentabilidad relativa que se tiene en cada inicio de sesión en un registro.
    Oss=[] #'OperationStartSession' Vector que expresa el ID de la primera operación realizada para cada una de las sesiones de un registro.
    tmss=[] #TimeMinuteStartOperation, Vector que expresa el tiempo transcurrido para la primera operación realizada en cada una de las sesiones de un registro.
    po=[] #'ProbabilityOperation'Vector de probabilidades del juego.
    CIo=[] #'CompoundInterestOperation' Vector que expresa la tasa de interés compuesto real obtenido para cada una de las operaciones realizadas.
    Ro=[] #'RentabilityOperation' vector que expresa la rentabilidad real obtenida para cada una de las operaciones realizadas.
    Io=[] #'IncomeOperation' Vector que expresa el nivel de ingreso obtenido para cada una de las operaciones realizadas.
    Iof=0.0 #Variable que almacena el nivel de ingresos que tiene al momento de realizar la última operación de trading.
    INVo=[] #'InvestimentOperation' Variable que registra el nivel de inversión total que se tiene por cada operación
    INVof=0.0 #'InvestimentOperationFinal' Valor de la última inversión realidad.
    avINVo=[] #'AverageInvestimentOperationVector' Es el vector que almacenará el promedio de dinero invertido por operación por marco temporal
    avINVoMax=[]#'AverageInvestimentMaximum' Promedio de inversión máxima por operación
    avINVoc=0.0 #'InvestimentOperationAverage' Es el promedio de dinero invertido por operación de marco de tiempo.
    Co=[] #'CapitalOperation' Vector que contiene para cada operación realizada su nivel de capital resultante.
    Cof=0 #'CapitalOperationFinal' Es el último valor del capital que se tiene al operar.
    Rro=[] #'RentabilityRelativeOperation' Vector que expresa la rentabilidad relativa en base al capital inicial.
    tmo=[] #'TimeMinuteOperation' Vector que expresa el tiempo transcurrido para cada operación ejecutada en el registro.
    
    CIos=[] #'CompoundInterestOperationSample' Vector muestral de tasa de interés compuesta en el tiempo
    Ros=[] #'RentabilityOperationSample' vector de rentabilidad muestral en el tiempo
    tms=[] #'TimeMinuteSample' Vector muestral temporal que servirá para extraer las últimas diez operaciones para analizarlas de forma independiente.
    for i in range(10):
           CIos.append(0)
           Ros.append(0)
           tms.append(0)
    
    alpha=float(0) #Variable que almacena la tasa de rentabilidad ofrecida por el broker al momento de la operación.
    beta=[] #Vector general que almacena la tasa de rentabilidad 'alpha' relativa para más de una operación en un mismo tramo temporal (Más de una operación por trama de tiempo). Al hallar el promedio de este vector 'Avbeta' nos servirá para hacer cálculos posteriores sobre la probabilidad de obtener tasas de rentabilidad por encima del 50% o por debajo del -25%
    avbeta=0 #Promedio del vector de rentabilidad alpha relativa a más de una operación.
    
    A=0 #Número de éxitos acumulados
    As=0#Exitos acumulados en la sesión
    B=0#Número de fracasos acumulados
    Bs=0#Fracasos acumulados en la sesión
    n=0 #Número total de operaciones realizadas en el registro.
    nbs=0#'NúmberBeforeSessión' Número total de operaciones realizadas antes de esta sesión.
    m=int(0) #Cantidad de operaciones restantes esperadas.
    
    
    Iup=0#Ingresos positivos de la sesión actual, tal que Is=Iup+Idown
    Idown=0#Ingresos negativos de la sesión actual, tal que Is=Iup+Idown
    paint="none"#Color de cierre de sesión actual, si es verde se superó ganancia máxima por sesión, si es rojo, se superó pérdida máxima por sesión.
    Is=0 #'IncomeSession' Ingreso de la sesión actual
    Ibs=0 #'IncomeBeforeSession' Ingreso antes de empezar la sesión
    
    i=0 #Contador
    j=0 #Contador para iteraciones bidimensionales
    
    main=1 #Variable lógica que activa el menú principal siempre que sea '1' y se desactiva para entrar al submenú o registros con '0'
    
    clockts=time.time() #'ClockTimeReloj' encargado de contabilizar el tiempo en segundos entre operación
    clockpts=0 #'ClockPauseTimeSecond' Reloj encargado de contabilizar el tiempo en segundos transcurrido cuando se inició la pausa de la sesión.
    
    counterptm=0 #'CounterPauseTimeMinute' Contador encargado de contabilizar el tiempo en minutos total transcurrido en pausas durante la sesión.
    counterlth=0 #'CounterLifeTimeHour' Contador encargado de contabilizar el tiempo en horas total transcurrido para el registro que se está ejecutando.
    counterbltm=0 #'CounterBeforeLifeTimeMinute' Contador encargado de contabilizar el tiempo en minutos total transcurrido para la última sesión del registro que se está ejecutando, esto facilita el cálculo de tiempo de sesión actual
    
    average=0#Promedio de la probabilidad en todo el registro.
    deviation=0#Desviación estándar de la probabilidad en todo el registro.
    
    #Sección Menú Principal
    while main==1:
        choice=-1
        #Variables que ayudan en la comprobación de la apertura correcta de ficheros de texto.
        error0=0 
        error=0
        profile="none" #Variable que almacena el tipo de registro que se está ejecutando por el usuario.
        profiles=[] #Vector que almacena todos los nombres de los registros almacenados por el usuario.
        
        try:
            fichero=open('dataparameters.txt',mode='r',newline='\n')
        except IOError:
            error0=1
            fichero = open('dataparameters.txt', mode='w',newline='\n')
            fichero.write(str(lp)+'\n')
            fichero.write(str(lps)+'\n')
            fichero.write(str(pps)+'\n')
            fichero.write(str(CG)+'\n')
            fichero.close()
        if error0==0:
            nl=len(fichero.readlines()) #'NumberLines' Número de líneas del fichero, nos servirá para comprobar que haya información almacenada en el fichero de análisis.
            fichero.seek(0)
            if nl>0:
                lp=eval(fichero.readline())
                lps=eval(fichero.readline())
                pps=eval(fichero.readline())
                CG=eval(fichero.readline())
                pts=eval(fichero.readline())
                ipo=eval(fichero.readline())
                fichero.close()
        
        try:
            fichero=open('dataprofile.txt',mode='r',newline='\n')
        except IOError:
            error=1 #Error que sirve para cuando hay problemas con la lectura del dato o de la información en el fichero.
            while(error==1):
                try:
                    profile=input("Profile Name: ")
                    fichero = open('dataprofile.txt', mode='w',newline='\n')
                    fichero.write(profile+'\n')
                    fichero.close()
                    archivo = open(profile+'.txt', mode='w',newline='\n')
                    archivo.close()
                    main=0
                except:
                    error=1
        if error==0:
            nr=len(fichero.readlines())
            fichero.seek(0)
            print("------------------------------------------------------------------\n")
            print("0) Create a new profile\n")
            print("1) Delete a profile\n")
            print("2) General Settings\n")
            print("3) Exit\n")
            for i in range(nr):
                profile_temp=str(fichero.readline())
                profiles.append(profile_temp[0:len(profile_temp)-1])
                print(str(i+4)+") "+str(profiles[i]),"\n")
            fichero.close()
            print("------------------------------------------------------------------\n")
        
        while choice<0 or choice>nr+3:
            while(choice<0 or choice>nr+3):
                try:
                    choice=int(input("Choice: "))
                except:
                    choice=-1
            
            if choice==0:
                error=1 #Error que sirve para cuando hay problemas con la lectura del dato o de la información en el fichero.
                error0=0#Error que se activa cuando el registro a crear ya existe.
                while((error==1 or error0==1) and profile!="e"):
                    try:
                        error0=0
                        profile=input("Profile Name: ")
                        if(len(profiles)>0 and profile!="e"):
                            for i in range(len(profiles)):
                                if(profile==profiles[i]):
                                    error0=1
                        if(error0==0 and profile!="e"):
                            fichero = open('dataprofile.txt', mode='a',newline='\n')
                            fichero.write(profile+'\n')
                            fichero.close()
                            archivo = open(profile+'.txt', mode='w',newline='\n')
                            archivo.close()
                            C=CG #Se configura el nuevo registro con el capital ajustado en la configuración general del usuario.
                            error=0
                            main=0
                        
                    except:
                        error=1
                 
            if choice==1 and nr>0:
                 delid=-1
                 requests="none"
                 while (delid<4 or delid>nr+3) and requests!="e":
                     try:
                         requests=input("Delete Profile: ")
                         delid=int(requests)
                     except:
                         delid=-1
                 if(requests!="e"):
                     fichero = open('dataprofile.txt', mode='w',newline='\n')
                     for i in range(nr):
                         if i!=delid-4:
                             fichero.write(profiles[i]+'\n')
                     fichero.close()
                     os.remove(profiles[delid-4]+'.txt')
                     main=1
                         
            if choice==2:
                 choicet=-1#Variable temporal para el submenú de configuración general.
                 
                 while choicet<0 or choicet>6 or choicet!=6:
                     print("\nGeneral Settings\n\n")
                     print("0) Labor Price (lp: $%.2f/h)\n"%lp)
                     print("1) Loss Per Session (lps: %.2f)\n"%lps)
                     print("2) Profit Per Session (pps: %.2f)\n"%pps)
                     print("3) Capital Per Register (CG: %.2f)\n"%CG)
                     print("4) Processing Time (pts: %.2fs)\n"%pts)
                     print("5) Investiment Per Operation (ipo: $%.2f)\n"%ipo)
                     print("6) Return to main menu\n")
                     try:
                         choicet=int(input("Choice: "))  
                     except:
                         choicet=-1
                     requests="none"
                     if choicet==0:
                         error=1
                         while(error==1 and requests!="e" or lp<0):
                             try:
                                 requests=input("Labor Price (lp): ")
                                 lp=float(requests) 
                                 error=0
                             except:
                                 error=1
                     if choicet==1:
                         error=1
                         while(error==1 and requests!="e" or lps<-1 or lps>0):
                             try:
                                 requests=input("Loss Per Session (lps): ")
                                 lps=float(requests) 
                                 error=0
                             except:
                                 error=1
                     if choicet==2:
                         error=1
                         while(error==1 and requests!="e" or pps<0):
                             try:
                                 requests=input("Profit Per Session (pps): ")
                                 pps=float(requests)                  
                                 error=0
                             except:
                                 error=1           
                     if choicet==3:
                         error=1
                         while(error==1 and requests!="e" or CG<0):
                             try:
                                 requests=input("Capital Per Register (CG): ")
                                 CG=float(requests)              
                                 error=0
                             except:
                                 error=1           
                     if choicet==4:
                         error=1
                         while(error==1 and requests!="e" or pts<0):
                             try:
                                 requests=input("Processing Time (pts): ")
                                 pts=float(requests)              
                                 error=0
                             except:
                                 error=1           
                     if choicet==5:
                         error=1
                         while(error==1 and requests!="e" or ipo<1):
                             try:
                                 requests=input("Investiment Per Operation (ipo): ")
                                 ipo=float(requests)              
                                 error=0
                             except:
                                 error=1
                 
                 fichero = open('dataparameters.txt', mode='w',newline='\n')
                 fichero.write(str(lp)+'\n')
                 fichero.write(str(lps)+'\n')
                 fichero.write(str(pps)+'\n')
                 fichero.write(str(CG)+'\n')
                 fichero.write(str(pts)+'\n')
                 fichero.write(str(ipo)+'\n')
                 fichero.close()
                 main=1
                 
            if choice>3 and choice<nr+4:
                 profile=profiles[choice-4]
                 archivo=open(profile+'.txt',mode='r',newline='\n')
                 nl=len(archivo.readlines())
                 archivo.seek(0)
                 
                 if nl>0:
                     dss=str(archivo.readline())
                     C=eval(archivo.readline())
                     Oss=eval(archivo.readline())
                     tmo=eval(archivo.readline())
                     INVo=eval(archivo.readline())
                     Io=eval(archivo.readline())
                     
                     n=len(tmo)
                     if(n>0): #Con esta línea de código se evita el procesamiento de datos con información incompleta.
                         #Inicio de la lectura de datos para los valores iniciales de A, B y el vector po[i]
                         if(Io[0]>0):
                             A=A+1
                             po.append(float(1))
                         else:
                             B=B+1
                             po.append(float(0))
                         #Inicio de lectura de datos para el valor beta o tasa alpha relativa.
                         beta.append(Io[0]/INVo[0]) 
                         for i in range(1,n,1):
                             #Apartado para obtener las variables A,B y el vector po[i]
                             if (Io[i]-Io[i-1]>0):
                                 A=A+1
                             else:
                                 B=B+1
                             po.append(float(A/(A+B)))
                             #Apartado para obtener el valor beta o de tasa alpha relativa.
                             beta.append((Io[i]-Io[i-1])/(INVo[i]-INVo[i-1]))
                         
                         counterbltm=tmo[n-1] #Acumulador de minutos de las sesiones previas.
                         nbs=n
                         Iof=Io[n-1]
                         Ibs=Io[n-1]
                         #Apartado para procesar y extraer la información para la tasa de rentabilidad (Ro), rentabilidad relativa (Rro) y capital operativo (Co)                     
                         for i in range(0,n,1):
                             Ro.append(Io[i]/INVo[i])
                             Co.append(C+Io[i])
                             Rro.append((C+Io[i])/C-1)
                             avINVo.append(INVo[i]/(i+1))
                             avINVoMax.append(-lps*(C+Io[i]))
                             if(tmo[i]<CIotmi):
                                 #Cuando no haya pasado aún el 'AntiNoiseTime' el tiempo para limpiar el ruido de la variable CIo en los primeros segundo de operación en todo el registro, no se realizarán cálculos para el interés compuesto debido altos niveles de fluctuación de la variable en este rango de tiempo seleccionado por el usuario.
                                 CIo.append(0.0)
                             if(tmo[n-1]>=CIotmi):
                                 try:
                                     CIo.append((1+Ro[i])**(60/tmo[i-1])-1)
                                 except:
                                     CIo.append(max(CIo))
                         Cof=Co[n-1]
                         for i in range(0,len(Oss),1):
                             tmss.append(tmo[Oss[i]])
                             Pss.append(po[Oss[i]])
                             CIss.append(CIo[Oss[i]])
                             Rss.append(Ro[Oss[i]])
                             Coss.append(Co[Oss[i]])
                             Rrss.append(Rro[Oss[i]])
                             Iss.append(Io[Oss[i]])
                             INVss.append(INVo[Oss[i]])
                             avINVss.append(avINVo[Oss[i]])
                             
                 archivo.close()
                 main=0

            if choice==3:
                 #Línea de código para cierre del menú principal.
                 main=0
    
    if choice!=3:
        #Sección donde se realiza la comprobación del día actual con el fin de que el usuario sepa el conjunto de operaciones del mismo día.
        if(str(dss)!=str("000000")): #Se comprueba que el archivo de fecha esté creado.
            if(str(dss)!=str(time.strftime("%d%m%y"))+'\n'): #Se comprueba que esa fecha almacenada por el archivo sea diferente a la del día de hoy. De lo contrario se actualiza a la fecha actual. Note como tiene el caracter adicional '\n', es probable que al usar el comando str() en una variable dentro de una conjunción lógica if(), genera que el vector se le autoañada un carácter repetido '\n'. El bug ya está corregido.
                 Oss.append(n-1) #Vector que guarda el ID o posición donde se empieza la sesión.
                 tmss.append(tmo[n-1])
                 Pss.append(po[n-1])
                 CIss.append(CIo[n-1])
                 Rss.append(Ro[n-1])
                 Coss.append(Co[n-1])
                 Rrss.append(Rro[n-1])
                 Iss.append(Io[n-1])
                 INVss.append(INVo[n-1])
                 avINVss.append(avINVo[n-1])
                 dss=str(time.strftime("%d%m%y"))
            else:
                dss=str(time.strftime("%d%m%y"))
        if(str(dss)==str("000000")): #Si la fecha no existe, se crea a la del día actual.
            dss=str(time.strftime("%d%m%y"))
        clockts=time.time() #Reloj para cálculos de tiempo entre operación
        alpha=float(0)
        
    #Sección del registro de datos donde el usuario realiza las operaciones.
    while request!="e" and request!="E" and choice!=3:
        request="none"
        request_f=float(0)#'Resquest Float' Variable request en formato float para las entradas numéricas.
        error_r=0#'Error Request' Error temporal para detectar si la entrada de la variable request es tipo texto (1) o dígitos (0).
        #Este bucle nos sirve para poder entrar al algoritmo sí y sólo si se ha ingresado una entrada correcta.
        #Notar que el apartado "(request=="g" and n==0)) and (request!="G" or (request=="G" and n==0))" nos sirve para corregir el error al intentar visualizar un registro sin ningún dato, y que no se quede en el bucle de forma perpetua.
        if (request=="none" or (error_r!=0 and (request!="e" and request!="E" and request!="A" and request!="a" and request!="C" and request!="c" and request!="d" and request!="D" and request!="r" and request!="R" and (request!="g" or (request=="g" and n==0)) and (request!="G" or (request=="G" and n==0)) and request!="p" and request!="P"))):
            error=1
            while(error==1):
                try:
                    request=input("Request: ")
                    error=0
                except:
                    error=1
            try: #Se efectúa comprobación para ver si el ingreso por el usuario fue una entrada tipo texto o numérica.
                request_f=float(request)
                error_r=0
            except:
                error_r=1
        if request!="A" and request!="a" and request!="C" and request!="c" and request!="d" and request!="D" and request!="r" and request!="R" and request!="g" and request!="G" and request!="p" and request!="P" and request!="e"and request!="E": #Es necesario ingresar esta línea para poder excluir las letras que son para uso y configuración
            requests="none" #'RequestSample' Variable de petición o request temporal
            if(n>0 and Cof<1):
                request="none"
            if ((error_r==0 and n==0) or (error_r==0 and n>0 and Cof>=1)):#Este NÚMERO UNO servirá para parámetro posterior cuando se pueda configurar la cantidad de dinero por operación unitaria, para que no sea un dólar.
                if ((request_f==0 or request_f==1) and alpha==0): #Línea que permite detectar si se ha ganado o perdido una ÚNICA operación por marco temporal, para poder preguntar cuál es la tasa de rentabilidad que ofrece el broker.
                    error=1
                    while(error==1 and requests!="e" or alpha<0):
                        try:
                            requests=input("Alpha (α): ")
                            alpha=float(requests)
                            error=0
                        except:
                            error=1
            if(requests!="e"):
                try:
                    requests=float(request)
                    requests="y"#Variable que verifica si una petición tiene formato numérico para evitar errores en la sentencia lógica float(request)>0
                except:
                    requests="n"
            if(request!="e" and requests!="e" and requests=="y"):
                requests="none"
                clocktts=time.time() #'ClockTemporalTimeSeconds' Reloj temporal que registra el tiempo actual en segundos desde el siglo pasado.
                counterots=clocktts-clockts #'CounterOperationTimeSeconds' Contador que almacena el tiempo en segundos transcurrido por operación.
                clockts=clocktts
                counterbltm=counterbltm+counterots/60-counterptm
                counterptm=0 #Es necesario reiniciar el acumulador en cada conteo de tiempo realizado por operación
                #Apartado para operaciones únicas perdidas
                if request=="0":
                    n=n+1
                    tmo.append(counterbltm)
                    beta.append(float(-1))
                    B=B+1
                    Bs=Bs+1
                    if n>1:
                        INVo.append(INVo[n-2]+ipo)
                        INVof=ipo
                        Iof=Iof-ipo
                        R0=(Iof)/(INVo[n-1])
                        Is=Is-ipo
                    if n==1:
                        INVo.append(ipo)
                        INVof=ipo
                        Iof=-ipo
                        R0=-1
                        Is=-ipo
                        nbs=1

                #Apartado para operaciones únicas ganadas.
                if request=="1":
                    n=n+1
                    tmo.append(counterbltm)
                    beta.append(float(alpha))
                    A=A+1
                    As=As+1
                    if n>1:
                        INVo.append(INVo[n-2]+ipo)
                        INVof=ipo
                        Iof=Iof+alpha*ipo
                        R0=(Iof)/(INVo[n-1])
                        Is=Is+alpha*ipo
                    if n==1:
                        INVo.append(ipo)
                        INVof=ipo
                        Iof=alpha*ipo
                        R0=alpha
                        Is=alpha*ipo
                        nbs=1
                        
                #Apartado para la toma de datos del usuario para operaciones conjuntas, de esta forma se evita combinaciones de datos que no existen en la realidad para Ro<-1
                if(request!="0" and request!="1"):
                    error=1
                    request_f=0#Variable peticion tipo float.
                    while(error==1 and requests!="e"):
                        try:
                            requests=input("Investiment (INVo): ")
                            INVof=float(requests)
                            error=0
                        except:
                            error=1
                            if(len(INVo)>0): #Línea de código que ayuda a volver a recuperar el valor real de INVo.
                                INVof=INVo[len(INVo)-1]-INVo[len(INVo)-2]
                    try:
                        while(error==1 and request!="e" and requests!="e" or INVof<=0 or float(request)/INVof<-1 or INVof>Co[n-2]):
                            try: 
                                request=input("Request: ")
                                request_f=float(request)
                                if(request!="1" and request!="0"):
                                    requests=input("Investiment (INVo): ")
                                    INVof=float(requests)
                                    error=0
                                #Apartado para operaciones únicas ganadas.
                                if(request=="1"):
                                    n=n+1
                                    tmo.append(counterbltm)
                                    beta.append(float(alpha))
                                    A=A+1
                                    As=As+1
                                    if n>1:
                                        INVo.append(INVo[n-2]+ipo)
                                        INVof=ipo
                                        Iof=Iof+alpha*ipo
                                        R0=(Iof)/(INVo[n-1])
                                        Is=Is+alpha*ipo
                                    if n==1:
                                        INVo.append(ipo)
                                        INVof=ipo
                                        Iof=alpha*ipo
                                        R0=alpha
                                        Is=alpha*ipo
                                #Apartado para operaciones únicas perdidas
                                if request=="0":
                                    n=n+1
                                    tmo.append(counterbltm)
                                    beta.append(float(-1))
                                    B=B+1
                                    Bs=Bs+1
                                    if n>1:
                                        INVo.append(INVo[n-2]+ipo)
                                        INVof=ipo
                                        Iof=Iof-ipo
                                        R0=(Iof)/(INVo[n-1])
                                        Is=Is-ipo
                                    if n==1:
                                        INVo.append(ipo)
                                        INVof=ipo
                                        Iof=-ipo
                                        R0=-1
                                        Is=-ipo
                            except: 
                                error=1
                                if(len(INVo)>0):
                                    INVof=INVo[len(INVo)-1]-INVo[len(INVo)-2]
                    except:
                        error=1
                        
                if(request!="e" and requests!="e" and request!="none" and requests!="none"):
                    if(request!="0" and request!="1"):
                        beta.append(float(request)/INVof)
                        Iof=Iof+float(request)
                    
                    #Apartado para operaciones neutras. Donde no se gana ni se pierde.
                    if float(request)==0 and request=="0.0":
                        n=n+1
                        tmo.append(counterbltm)
                        B=B+1
                        Bs=Bs+1
                        if n>1:
                            INVo.append(INVo[n-2]+INVof)
                            R0=(Iof)/(INVo[n-1])
                            Is=Is#No se suma nada, porque no hubo ni pérdida ni ganancia
                            
                        if n==1:
                            INVo.append(INVof)
                            R0=float(request)/INVo[n-1]
                            Is=0
                            nbs=1
                    
                    if float(request)<0 and request!="0":
                        n=n+1
                        tmo.append(counterbltm)
                        B=B+1
                        Bs=Bs+1
                        if n>1:
                            INVo.append(INVo[n-2]+INVof)
                            R0=(Iof)/(INVo[n-1])
                            Is=Is-INVof
                        if n==1:
                            INVo.append(INVof)
                            R0=float(request)/INVo[n-1]
                            Is=-INVof
                            nbs=1
                            
                    if float(request)>0 and request!="1":
                        n=n+1
                        tmo.append(counterbltm)
                        A=A+1
                        As=As+1
                        if n>1:
                            INVo.append(INVo[n-2]+INVof)
                            R0=(Iof)/(INVo[n-1])
                            Is=Is+float(request)
                        if n==1:
                            INVo.append(INVof)
                            R0=float(request)/INVo[n-1]
                            Is=float(request)
                            nbs=1
                try:
                    requests=float(request)
                    requests="y"#Variable que verifica si una petición tiene formato numérico para evitar errores en la sentencia lógica float(request)>0
                except:
                    requests="n"
                if(request!="e" and requests=="y"):    
                    po.append(A/(A+B))
                    Ro.append(R0)
                    Cof=C+Iof
                    Rro.append((Cof)/C-1)
                    Co.append(Cof)
                    avINVo.append(INVo[n-1]/(n))
                    avINVoMax.append(-lps*(Cof))
                    if(tmo[n-1]<CIotmi):
                        #Cuando no haya pasado aún el tiempo de procesamiento máximo en todo el registro, no se realizarán cálculos para el interés compuesto debido altos niveles de fluctuación de la variable en este rango de tiempo.
                        CIo.append(0.0)
                    if(tmo[n-1]>=CIotmi):
                        try:
                            CIo.append((1+R0)**(60/tmo[n-1])-1)
                        except:
                            if(n==1):
                                CIo.append(0.0)
                            if(n>1):
                                #CIo[n-1]=max(CIo) #<<<<>>>>Si en alguna ejecución la línea de abajo aparece como error, entonces dejar esta línea <<
                                CIo.append(max(CIo))
                    #Apartado para el cálculo independiente del ingreso positivo y negativo, para cálculos a futuro límite de ganancia o pérdida máximo por sesión.
                    Io.append(Iof)
                    if(n==1):
                        if(Io[0]>=0):
                            Iup=Io[0]
                        if(Io[0]<0):
                            Idown=Io[0]
                    if (n>1):
                        if Io[n-1]-Io[n-2]>=0:
                            Iup=Iup+(Io[n-1]-Io[n-2])
                        if Io[n-1]-Io[n-2]<0:
                            Idown=Idown+(Io[n-1]-Io[n-2])
        
                    numerator=0 #Contador para facilitar el cálculo del promedio y desviación de la probabilidad del registro de datos.
                    for i in range(n):
                        numerator=numerator+po[i]
                    average=numerator/n
                    numerator=0
                    for i in range(n):
                        numerator=(po[i]-average)**2
                    deviation=(numerator/n)**(1/2)
                    if(n>As+Bs):
                        print("\nn: %i\t\ttmo: %.2fm\t(ns: %i)"%(n,counterbltm,As+Bs))
                    if(n==As+Bs):
                        print("\nn: %i\t\ttmo: %.2fm\t(ns: %i)"%(n,counterbltm,As+Bs))
                    print ("Io: $%.2f\tINVo: $%.2f\t(%iW|%iL)" % (Iof,INVo[n-1],As,Bs))
                    if(CIo[n-1]<100): #Línea de código que controla el tamaño máximo de la salida de la variable en pantalla, para cuando es un número muy grande no se salga de la columna del registro de datos.
                        print ("CIo: %.2f\tRo: %.2f\tRro: %.2f" % (CIo[n-1],Ro[n-1],Rro[n-1]))
                    else:
                        print ("CIo: %.2E\tRo: %.2f\tRro: %.2f" % (CIo[n-1],Ro[n-1],Rro[n-1]))
                    print ("po: %.2f\tE(po): %.2f\tδ(po): %.2f" % (A/(A+B),average,deviation ))
                    
                    #Gráfica de los últimos 10 datos de la tasa de rentabilidad.
                    if n>1 and n<=10:
                        numerator_s=0
                        for i in range(n):
                            CIos[i]=CIo[i]
                            tms[i]=tmo[i]
                            numerator_s=numerator_s+CIos[i]
                        average_s=numerator_s/n
                        for i in range(n):
                            try: #Línea de código que corrige el bug para número de interés compuesto demasiado elevados en los primeros tramos de tiempo del registro.
                                numerator_s=(CIos[i]-average_s)**2
                            except:
                                numerator_s=0
                        try:
                            deviation_s=(numerator_s/(n-1))**(1/2) #Se pone nueve en vez de diez, porque la desv. estándar muestral se divide sobre N-1
                        except: deviation_s=0
                    
                    if n>10:
                        numerator_s=0
                        for i in range(10):
                            CIos[i]=CIo[n-10+i]
                            tms[i]=tmo[n-10+i]
                            numerator_s=numerator_s+CIos[i]
                        average_s=numerator_s/10
                        for i in range(10):
                            try: #Línea de código que corrige el bug para número de interés compuesto demasiado elevados en los primeros tramos de tiempo del registro.
                                numerator_s=(CIos[i]-average_s)**2
                            except:
                                numerator_s=0
                        try:
                            deviation_s=(numerator_s/9)**(1/2) #Se pone nueve en vez de diez, porque la desv. estándar muestral se divide sobre N-1
                        except: deviation_s=0
                    if n>1:
                       #Apartado para comprobar si es una sesión de pérdida o ganancia.
                       if(Idown/C<=lps and Iup/C<pps): #Pérdida máxima superada con ganancia máxima no superada
                           paint="r"
                       if(Iup/C>=pps and Idown/C>lps): #Ganancia máxima superada con pérdida máxima no superada.
                           paint="g"
                       if(Idown/C<=lps and Iup/C>=pps): #Si se ha superado la pérdida máxima y también la ganancia máxima por sesió
                           if(paint=="r"):
                               Iup=0
                               Idown=Is
                               paint="g"
                           if(paint=="g"):
                               Iup=Is
                               Idown=0
                               paint="r" 
                       #Apartado para graficar el punto de cierre máximo de sesión. Verde para límite ganancia superado, rojo para límite pérdida superado.
                       if(n<10):
                           plt.plot(tms[n-1],CIos[n-1],'.', color=paint)
                       if (n>=10):
                           plt.plot(tms[9],CIos[9],'.', color=paint)  
                       #Apartado para graficar las líneas de rentabilidades inferiores y superiores.
                       plt.axhline(y=average_s+deviation_s*(2)**(1/2), color='g', linestyle='--')
                       plt.axhline(y=average_s, color='k', linestyle=':')
                       plt.axhline(y=average_s-deviation_s*(2/((3)**(1/2))), color='r', linestyle='--')
                       counterlth=tmo[n-1]/60
                       if min(CIos)<=(1+(counterlth*lp/INVo[n-1]))**(1/counterlth)-1:
                           plt.axhline(y=(1+(counterlth*lp/INVo[n-1]))**(1/counterlth)-1, color='m', linestyle='--')
                           plt.axhline(y=0, color='r', linestyle='-')
                       if n<10:
                            plt.plot(tms[0:n],CIos[0:n])
                       if n>=10:
                            plt.plot(tms,CIos)
                            plt.xlabel('Minutes (m)')
                            plt.ylabel('Compound Interest')                         
                       if n<=10:
                           if (CIo[n-1]<100):
                               plt.title('Compound Interest for %i latest steps (CIo: %.2f)' %(n,CIo[n-1]))
                           if(CIo[n-1]>=100):
                               plt.title('Compound Interest for %i latest steps (CIo: %.2E)' %(n,CIo[n-1]))
                       if n>10:
                           if(CIo[n-1]<100):
                               plt.title('Compound Interest for 10 latest steps (CIo: %.2f)' %CIo[n-1])
                           if(CIo[n-1]>=100):
                               plt.title('Compound Interest for 10 latest steps (CIo: %.2E)' %CIo[n-1])
                       plt.grid()
                       plt.show()
                    #Gráfica de los últimos 10 datos de la tasa de interés compuesto.
                    if n>1 and n<=10:
                         numerator_s=0
                         for i in range(n):
                             Ros[i]=Ro[i]
                             tms[i]=tmo[i]
                             numerator_s=numerator_s+Ros[i]
                         average_s=numerator_s/n
                         for i in range(n):
                             numerator_s=(Ros[i]-average_s)**2
                         deviation_s=(numerator_s/(n-1))**(1/2) #Se pone nueve en vez de diez, porque la desv. estándar muestral se divide sobre N-1
                         
                     
                    if n>10:
                         numerator_s=0
                         for i in range(10):
                             Ros[i]=Ro[n-10+i]
                             tms[i]=tmo[n-10+i]
                             numerator_s=numerator_s+Ros[i]
                         average_s=numerator_s/10
                         for i in range(10):
                             numerator_s=(Ros[i]-average_s)**2
                         deviation_s=(numerator_s/9)**(1/2) #Se pone nueve en vez de diez, porque la desv. estándar muestral se divide sobre N-1
                    
                    if n>1:
                        #Apartado para graficar el punto de cierre máximo de sesión. Verde para límite ganancia superado, rojo para límite pérdida superado.
                        if(n<10):
                            plt.plot(tms[n-1],Ros[n-1],'.', color=paint)
                        if (n>=10):
                            plt.plot(tms[9],Ros[9],'.', color=paint)
                        #Apartado para graficar las líneas de rentabilidades inferiores y superiores.
                        plt.axhline(y=average_s+deviation_s*(2)**(1/2), color='g', linestyle='--')
                        plt.axhline(y=average_s, color='k', linestyle=':')
                        plt.axhline(y=average_s-deviation_s*(2/((3)**(1/2))), color='r', linestyle='--')
                        counterlth=tmo[n-1]/60
                        if min(Ros)<=(counterlth*lp)/INVo[n-1]:
                            plt.axhline(y=(counterlth*lp)/INVo[n-1], color='m', linestyle='--')
                            plt.axhline(y=0, color='r', linestyle='-')
                        if n<10:
                            plt.plot(tms[0:n],Ros[0:n])
                        if n>=10:
                            plt.plot(tms,Ros)
                        plt.xlabel('Minutes (m)')
                        plt.ylabel('Rentability')
                        if n<=10:
                            plt.title('Rentability for %i latest steps (Ro: %.2f)' %(n,Ro[n-1]))
                        if n>10:
                            plt.title('Rentability for 10 latest steps (Ro: %.2f)' %Ro[n-1])
                        plt.grid()
                        plt.show()
                    
                        print("------------------------------------------------------------------\n")
                        
                    archivo = open(profile+'.txt', mode='w',newline='\n')
                    archivo.write(str(dss)+'\n')
                    archivo.write(str(C)+'\n')
                    archivo.write(str(Oss)+'\n')
                    archivo.write(str(tmo)+'\n')
                    archivo.write(str(INVo)+'\n')
                    archivo.write(str(Io)+'\n')
                    archivo.close()
                    
            if(request=="e" or requests=="e"):
                request="none"
                requests="none"
                
                    
        if request!='e' and ((request=="g" and n>0) or (request=="G" and n>0)) or (n>0 and Cof<1):
             #Fórmula general delta=(r+n)/(1+α), con r la ganancia bruta deseada en n operaciones.
             avbeta=sum(beta)/len(beta)
             if(avbeta==-1): #Línea que permite corregir el error de división por cero generado al intentar encontrar los valores delta respectivos.
                 avbeta=-0.99
             #Apartado para el cálculo del número de operaciones faltantes esperadas.
             avINVoc=INVo[n-1]/n
             ms=Cof/avINVoc #'mStart' Variable que representa el número mínimo posible de operaciones para quemar la cuenta.
             if ms%1!=0:
                 ms=ms//1+1 #Aquí sí se suma +1, para garantizar que sí sea el número mínimo posible para quemar la cuenta.
             m=ms-1 #Aquí se resta -1, porque dentro del ciclo While se empieza nuevamente a sumar +1. Nota: No bajar el conteo de m=m+1 a la parte de abajo del ciclo while porque crea bug de almacenamiento del valor m, por el valor m+1.
             px=[] #Vector de probabilidad de que la cuenta se queme en 'm' operaciones posteriores.
             pxm=0 #Valor de la probabilidad que se tiene de que la cuenta se queme para 'm' operaciones siguientes.
             try:
                 error=1
                 py=0
                 clockpts=time.time()#Reloj para contar el tiempo de procesamiento que se lleva en segundo
                 counterpts=0#Contador para contar el tiempo acumulado en segundos realizando los análisis estadísticos.
                 print("\nProcessing")
                 while (error==1 and py<=0.99 and (pts==0 or (pts>0 and (counterpts<=pts)))): #Bucle infinito
                     m=m+1
                     py=0 #Vector de probabilidad de que la cuenta se queme en 'm' operaciones posteriores.
                     a=(m-Cof/avINVoc)/(1+avbeta)
                     if a%1!=0:
                         a=a//1 #Aquí no se suma +1, para garantizar que sí sea la cantidad máxima de éxitos para quemar la cuenta al realizar 'm' operaciones realizadas.
                     #Bucle para encontrar la probabilidad de que la cuenta se queme en 'm' operaciones.
                     
                     for i in range(0,int(a+1),1):
                         py=py+(math.factorial(m)/(math.factorial(i)*math.factorial(m-i)))*(po[n-1]**i)*((1-po[n-1])**(m-i))
                     px.append(py)
                     counterpts=time.time()-clockpts
                 error=0
                 m=px.index(max(px))
                 if m%1!=0:
                     m=m//1+1 #Aquí sí se suma +1, para garantizar que sí sea el número mínimo posible para quemar la cuenta.
                 pxm=px[m]
             except: 
                 error=0
                 if(len(px)>0):
                     m=px.index(max(px))
                     if m%1!=0:
                         m=m//1+1 #Aquí sí se suma +1, para garantizar que sí sea el número mínimo posible para quemar la cuenta.
                     pxm=px[m]
                 if(len(px)==0):
                    m=ms
                    pxm=0
             if(m<ms): #Línea que permite agregar el número máximo de operaciones posible para quemar la cuenta para el caso en que la memoria del computador no pueda soportar esta iteración estadística.
                 m=ms
             #Cálculo para el tiempo promedio de cada operación
             dtmo=[]#'DiferentialTimeMinuteOperation' Vector de cambio de tiempo o diferencia de tiempo entre operaciones.
             dtmo.append(0)
             for i in range(1,n,1):
                 dtmo.append(tmo[i]-tmo[i-1])
             dtmoav=sum(dtmo)/n#Cálculo del promedio del tiempo entre operaciones.
             thl=(m*dtmoav)/60 #'TimeHourLife' Cálculo del tiempo de vida esperado que le queda a la cuenta con una confiabilidad de 'pxm'.
             
             #Apartado para encontrar el valor relativo ppsi, lpsi, opsi necesario para que se cumpla las exigencias lps, y pps para la rentabilidad Rro relativa, y no la Ro, absoluta, con el fin de evaluar y comparar en base al capital inicial
             Rroi=lps#Valor de rentabilidad relativa i
             lpsi=0#Valor de pérdida máxima i por sesión para rentabilidad relativa
             opsi=0#Valor neutro i por sesión de rentabilidad relativa.
             ppsi=0#Valor de ganancia máxima i por sesión para rentabilidad relativa
             lpsi=(Rroi*C-Io[n-1]+m*avINVoc)/(m*avINVoc)-1
             Rroi=0
             opsi=(Rroi*C-Io[n-1]+m*avINVoc)/(m*avINVoc)-1
             Rroi=pps
             ppsi=(Rroi*C-Io[n-1]+m*avINVoc)/(m*avINVoc)-1
             #Valores delta que nos permite encontrar la cantidad de éxitos necesarios para obtener una rentabilidad particular deseada.
             #delta_u_lps=m*(1+lps)/(1.0+avbeta) 
             #delta_o_0=m/(1.0+avbeta) 
             #delta_o_pps=m*(1+pps)/(1.0+avbeta)
             delta_u_lps=m*(1+lpsi)/(1.0+avbeta)
             delta_o_0=m*(1+opsi)/(1.0+avbeta) 
             delta_o_pps=m*(1+ppsi)/(1.0+avbeta)
             if delta_o_0%1!=0:
                 delta_o_0=delta_o_0//1+1
             if delta_o_pps%1!=0:
                 delta_o_pps=delta_o_pps//1+1 #Aquí sí se suma +1, porque se pide buscar la probabilidad de que halla una ganancia mayor al pps%
             if delta_u_lps%1!=0:
                 delta_u_lps=delta_u_lps//1 #Aquí no se suma +1, porque se pide buscar la probabilidad de que halla una pérdida menor al lps%
             #R0=Ro[n-1]
             R0=Rro[n-1]
             #Valor de rentabilidad futura
             R1_u_lps=(Io[n-1]+delta_u_lps*avINVoc*(1+avbeta)-m*avINVoc)/C
             R1_o_0=(Io[n-1]+delta_o_0*avINVoc*(1+avbeta)-m*avINVoc)/C
             R1_o_pps=(Io[n-1]+delta_o_pps*avINVoc*(1+avbeta)-m*avINVoc)/C
             #R1_u_lps=(Io[n-1]+delta_u_lps*avINVoc*(1+avbeta)-m*avINVoc)/(INVo[n-1]+m*avINVoc)
             #R1_o_0=(Io[n-1]+delta_o_0*avINVoc*(1+avbeta)-m*avINVoc)/(INVo[n-1]+m*avINVoc)
             #R1_o_pps=(Io[n-1]+delta_o_pps*avINVoc*(1+avbeta)-m*avINVoc)/(INVo[n-1]+m*avINVoc)
             #Diferencia del valor de rentabilidad futura con el valor actual de rentabilidad.
             dR1_u_lps=R1_u_lps-R0
             dR1_o_0=R1_o_0-R0 
             dR1_o_pps=R1_o_pps-R0
             prob_o_0=0 
             if(delta_o_0<=m):
                 for i in range(int(delta_o_0),int(m)+1,1):
                     prob_o_0=prob_o_0+ (math.factorial(m)/(math.factorial(i)*math.factorial(m-i)))*(po[n-1]**i)*((1-po[n-1])**(m-i))
             prob_o_pps=0 
             if(delta_o_pps<=m):
                 for i in range(int(delta_o_pps),int(m)+1,1):
                     prob_o_pps=prob_o_pps+ (math.factorial(m)/(math.factorial(i)*math.factorial(m-i)))*(po[n-1]**i)*((1-po[n-1])**(m-i))
             prob_u_lps=0
             if(delta_u_lps<=m):
                for i in range(0,int(delta_u_lps)+1,1):
                     prob_u_lps=prob_u_lps+ (math.factorial(m)/(math.factorial(i)*math.factorial(m-i)))*(po[n-1]**i)*((1-po[n-1])**(m-i))
             if (delta_u_lps>m):
                 prob_u_lps=1
             average_x=m*po[n-1]
             deviation_x=(m*po[n-1]*(1-po[n-1]))**(1/2)
             average_r=(po[n-1]*(1+avbeta)-1)
             if(m!=0):
                 deviation_r=(deviation_x*(1+avbeta))/m
             else:
                 deviation_r=0
             
             #Salida de datos grafica general "g"
             
             if(alpha==0):print("\nα: %.2f\t\tβ: %.2f"%(avbeta,avbeta))
             if(alpha!=0):print("\nα: %.2f\t\tβ: %.2f"%(alpha,avbeta))
             print("lp: $%.2f/h\tipo: $%.2f"%(lp,ipo))
             print("lps: %.2f\tops: 0.00\tpps: %.2f"%(lps,pps))
             print("lpsi: %.2f\topsi: %.2f\tppsi: %.2f"%(lpsi,opsi,ppsi))
             print("------------------------------------------------------------------")
             if(n>As+Bs):
                 print("n: %i\t\ttmo: %.2fm\t(ns:%i)"%(n,counterbltm,As+Bs))
             if(n==As+Bs):
                 print("n: %i\t\ttmo: %.2fm"%(n,counterbltm))
             print("Co: %.2f\tC: %.2f\t(%iW|%iL)"%(C+Iof,C,As,Bs))
             print ("Io: $%.2f\tINVo: $%.2f\tavINVo: $%.2f" % (Iof,INVo[n-1],avINVoc))
             if(CIo[n-1]<100): #Línea de código que controla el tamaño máximo de la salida de la variable en pantalla, para cuando es un número muy grande no se salga de la columna del registro de datos.
                 print ("CIo: %.2f\tRo: %.2f\tRro: %.2f" % (CIo[n-1],Ro[n-1],Rro[n-1]))
             else:
                 print ("CIo: %.2E\tRo: %.2f\tRro: %.2f" % (CIo[n-1],Ro[n-1],Rro[n-1]))
             print ("po: %.2f\tE(po): %.2f\tδ(po): %.2f" % (A/(A+B),average,deviation))
             print("------------------------------------------------------------------")
             
             counterlth=tmo[n-1]/60 #Variable necesario para la ubicacion de los límites de las siguientes gráficas.
             CIoMin=[]#Vector de interés compuesto mínimo para poder solventar el gasto de trabajo generado al operar.
             RoMin=[]#Vector de rentabilidad mínima para solventar el gasto de trabajo humano generado al operar.
             RroMin=[]#Vector de rentabilidad relativa mínima para solventar el gasto de trabajo humano generado al operar.
             CoMin=[]#Vector de Capital operativo mínimo para solventar gastos de trabajo.
             poMin=[]#Vector de probabilidad mínimo necesaria para general la rentabilidad necesaria para solventar los gastos laborales de operación. 
             IoMin=[]#Vector de ingreso mínimo necesario para solventar gastos laborales.
             counterlthi=0#Contador para facilitar la expresión de los valores mínimos necesarios para tener rentabilidades por encima del costo laboral.
             #Apartado para inicializar los límites mínimos o máximos (según el caso) necesarios para tener rentabilidades por encima del costo de trabajo invertido en el proceso.
             for i in range(n):
                 counterlthi=tmo[i]/60
                 CIoMin.append((1+counterlthi*lp/INVo[i])**(1/counterlthi)-1)
                 RoMin.append(counterlthi*lp/INVo[i])
                 RroMin.append(counterlthi*lp/C)
                 CoMin.append(counterlthi*lp+C)
                 poMin.append(((counterlthi*lp)/INVo[i]+1)/(1+avbeta))
                 IoMin.append(counterlthi*lp)
                 
             plt.plot([0]+tmo,[0]+CIoMin, color='m', linestyle='--')
             plt.axhline(y=0, color='r', linestyle='-')
             plt.plot([0]+tmo,[0]+CIo,color='b')
             plt.plot([0]+tmss,[0]+CIss,'.', color='r')
             plt.xlabel('Minutes (m)')
             plt.ylabel('Compound Interest')
             if(CIo[n-1]<100):
                 plt.title('Compound Interest for %i steps (CIo: %.2f)' %(n,CIo[n-1]))
             if(CIo[n-1]>=100):
                 plt.title('Compound Interest for %i steps (CIo: %.2E)' %(n,CIo[n-1]))
             plt.grid()
             plt.show()
                 
             plt.plot([0]+tmo,[0]+RoMin, color='m', linestyle='--')
             plt.axhline(y=0, color='r', linestyle='-')
             plt.plot([0]+tmo,[0]+Ro,color='b')
             plt.plot([0]+tmss,[0]+Rss,'.', color='r')
             plt.xlabel('Minutes (m)')
             plt.ylabel('Rentability')
             plt.title('Rentability for %i steps (Ro: %.2f)' %(n,Ro[n-1]))
             plt.grid()
             plt.show()
             
             plt.plot([0]+tmo,[0]+RroMin, color='m', linestyle='--')
             plt.axhline(y=0, color='r', linestyle='-')
             plt.plot([0]+tmo,[0]+Rro,color='b')
             plt.plot([0]+tmss,[0]+Rrss,'.', color='r')
             plt.xlabel('Minutes (m)')
             plt.ylabel('Relative Rentability')
             plt.title('Relative Rentability for %i steps (Rro: %.2f)' %(n,Rro[n-1]))
             plt.grid()
             plt.show()
             
             plt.plot([0]+tmo,[C]+CoMin, color='m', linestyle='--')
             plt.axhline(y=C, color='r', linestyle='-')   
             plt.plot([0]+tmo,[C]+Co,color='b')
             plt.plot([0]+tmss,[C]+Coss,'.', color='r')
             plt.xlabel('Minutes (m)')
             plt.ylabel('Capital ($)')
             plt.title('Capital for %i steps (Co: $%.2f)' %(n,Co[n-1]))
             plt.grid()
             plt.show()
             
             plt.plot([0]+tmo,[1/(1+avbeta)]+poMin, color='m', linestyle='--')
             plt.axhline(y=1/(1+avbeta), color='r', linestyle='-')
             plt.plot([0]+tmo,[0]+po,color='b')
             plt.plot([0]+tmss,[0]+Pss,'.', color='r')
             plt.xlabel('Minutes (m)')
             plt.ylabel('Probability')
             plt.title('Win probability for %i steps (po: %.2f)' %(n,po[n-1]))
             plt.grid()
             plt.show()
             
             #Apartado para crear la gráfica de avINVoMax inversión promedio máxima para cada operación realizada en el registro.
             if(avINVoMax[n-1]>=avINVo[n-1]): #Se mostrará una línea punteada roja que no se debe sobrepasar.
                 plt.plot([0]+tmo,[0]+avINVoMax, color='r', linestyle='-.')
             else: #En caso de que el último valor sobrepase la línea, entonces ésta se ocultará y aparecerá una línea negra horizontal avisando momento de retirarse.
                 plt.axhline(y=avINVoMax[n-1], color='r', linestyle='-.')
             plt.axhline(y=0, color='r', linestyle='-')   
             plt.plot([0]+tmo,[0]+avINVo,color='b')
             plt.plot([0]+tmss,[0]+avINVss,'.', color='r')
             plt.xlabel('Minutes (m)')
             plt.ylabel('Average Investiment ($/step)')
             plt.title('Average Investiment for %i steps (avINVo: $%.2f/step)' %(n,avINVo[n-1]))
             plt.grid()
             plt.show()
             
             if Io[n-1]>-C:
                 if C+Io[n-1]<(C+Ibs)*(1+lps)+1:
                     #Gráfica de color rojo punteado que avisa cuando se ha cumplido el porcentaje de pérdida máximo por sesión
                     plt.axhline(y=(C+Ibs)*(1+lps)-C, color='r', linestyle='-.')
                 if C+Io[n-1]>(C+Ibs)*(1+pps)-1:
                     #Gráfica de color verde punteado que avisa cuando se ha cumplido el porcentaje de ganancia máxima por sesión.
                     plt.axhline(y=(C+Ibs)*(1+pps)-C, color='g', linestyle='-.')
             if min(Io)<-C+1: 
                 #Línea negra punteada que aparece cuando falta como máximo un (1) dólar para quemar su cuenta. 
                 plt.axhline(y=-C, color='k', linestyle='-.') 
             plt.plot([0]+tmo,[0]+IoMin, color='m', linestyle='--')
             plt.axhline(y=0, color='r', linestyle='-')   
             plt.plot([0]+tmo,[0]+Io, color='b')
             plt.plot([0]+tmss,[0]+Iss,'.', color='r')
             plt.xlabel('Minutes (m)')
             plt.ylabel('Income ($)')
             plt.title('Income for %i steps (Io: $%.2f)' % (n,Iof))
             plt.grid()
             plt.show()
             
             if(pxm>=0.5):
                 print("for Δn: %i\t\tp(Rro≥0): %.2f\t\tp(thl≤%.2fh): %.2f" % (m,prob_o_0,thl,pxm))
             else: #Línea en caso de que la confiabilidad del número 'm' de operaciones para quemar la cuenta resulta ser muy baja.
                 print("for Δn: %i\t\tp(Rro≥0): %.2f\t\tp(thl>%.2fh): %.2f" % (m,prob_o_0,thl,1-pxm))
             print("po: %.2f\t\tE[Ro]: %.2f\t\tδ(Ro): %.2f" %(po[n-1],average_r,deviation_r))
             print("p(Rro≤%.2f):%.2f\tp(%.2f<Rro<%.2f):%.2f\tp(Rro≥%.2f):%.2f" % (lps,prob_u_lps,lps,pps,abs(1-prob_o_pps-prob_u_lps),pps,prob_o_pps))
             print("p(Ro≤%.2f)\t\tp(%.2f<Ro<%.2f)\tp(Ro≥%.2f)" % (lpsi,lpsi,ppsi,ppsi))
             print("------------------------------------------------------------------")
             print("for n': %i" %(n+m))
             print("Rro≤ %.2f\t\t%.2f<Rro<%.2f\t\tRro≥ %.2f" % (R1_u_lps,R1_u_lps,R1_o_pps,R1_o_pps))
             print("ΔRro≤ %.2f\t\t%.2f<ΔRro<%.2f\t\tΔRro≥ %.2f" % (dR1_u_lps,dR1_u_lps,dR1_o_pps,dR1_o_pps))
             print("------------------------------------------------------------------")
             
             
        if request=="a" or request=="A":
            error=1
            while(error==1 or alpha<0):
                try:
                    alpha=float(input("Alpha (α): "))
                    error=0
                except:
                    error=1
                    
        if request=="c" or request=="C":
            error=1
            requests="none"
            Cb=C#'CapitalBefore' Capital anterior a la configuración del usuario.
            while(error==1 and requests!="e"):
                try:
                    requests=input("Capital (C): ")
                    if(float(requests)>=Cb):
                        C=float(requests)
                        error=0
                except:
                    error=1
            for i in range(0,len(tmo),1):
                Co[i]=C+Io[i]
                Cof=C+Io[i]
                Rro[i]=(C+Io[i])/C-1
            for i in range(0,len(Oss),1):
                Coss[i]=Co[Oss[i]]
            for i in range(0,len(Oss),1):
                Rrss[i]=Rro[Oss[i]]
            archivo = open(profile+'.txt', mode='w',newline='\n')
            archivo.write(str(dss)+'\n')
            archivo.write(str(C)+'\n')
            archivo.write(str(Oss)+'\n')
            archivo.write(str(tmo)+'\n')
            archivo.write(str(INVo)+'\n')
            archivo.write(str(Io)+'\n')
            archivo.close()

        if request=="p" or request=="P":
             pause="none"
             clockpts=time.time()
             while pause!="p":
                 print("\n---------------------------------------------------------------------------------\n")
                 pause=input("Pausa Activada\n---------------------------------------------------------------------------------\n")
             clockpts=time.time()-clockpts
             counterptm=counterptm+clockpts/60
             print("\n---------------------------------------------------------------------------------\n")
             print("Pausa Desactivada\n---------------------------------------------------------------------------------\n")
             request="none"
             pause="none"
             
        if n>0 and (request=="d" or request=="D"):
            if(Io[n-1]-Io[n-2]>=0): #Se comprueba si el elemento a eliminar fue una operación exitosa o fracasada.
                A=A-1
            else:
                B=B-1
            n=n-1
            if(len(Oss)>0):
                if(Oss[len(Oss)-1]==len(tmo)-1): #Se comprueba que el elemento a eliminar sea o no un inicio de sesión 'StartSession'
                    Oss.pop()
            tmo.pop()
            INVo.pop()
            Io.pop()
            archivo = open(profile+'.txt', mode='w',newline='\n')
            archivo.write(str(dss)+'\n')
            archivo.write(str(C)+'\n')
            archivo.write(str(Oss)+'\n')
            archivo.write(str(tmo)+'\n')
            archivo.write(str(INVo)+'\n')
            archivo.write(str(Io)+'\n')
            archivo.close()
            po.pop()
            beta.pop()
            if(n>0):
                counterbltm=tmo[n-1]
                Iof=Io[n-1]
                #Línea para asignar el número de operaciones y el ingreso antes de la sesión de forma correcta.
                if(n<=nbs):
                    nbs=nbs-1
                    Ibs=Io[nbs-1]
                Ro.pop()
                Co.pop()
                Rro.pop()
                avINVo.pop()
                avINVoMax.pop()
                CIo.pop()
                Cof=Co[n-1]
            if(n==0):
                counterbltm=0
                Iof=0
                Ibs=0
                Ro.pop()
                Co.pop()
                Rro.pop()
                avINVo.pop()
                avINVoMax.pop()
                CIo.pop()
                Cof=C
            if (len(Oss)<len(tmss)):
                tmss.pop()
                Pss.pop()
                CIss.pop()
                Rss.pop()
                Coss.pop()
                Rrss.pop()
                Iss.pop()
                INVss.pop()
                avINVss.pop()
            print("Step No. %i deleted"%(n+1))
             
        if request=="R" or request=="r":
            error=1
            idel=0#el n-ésimo elemento almacenado en el registro de datos, empezando por 1, y terminando por n.
            iOss=0#El ID de la operación inicial en caso de encontrarse y encajar con el valor que se piensa eliminar, esto servirá para asignar a ese Oss particular el siguiente valor.
            while(request!="e" and (error==1 or (error==0 and (idel<0 or idel>n-1)))):
                try:
                    request=input("Remove Step No. ")
                    idel=int(request)-1
                    error=0
                except:
                    error=1
            if(request!="e"):
                n=n-1
                if(n==0):
                    A=0
                    B=0
                    p=[]
                #Se realiza el conteo nuevamente de éxitos y fracasos efectuados para los datos anteriores (a la izquierda) al dato a eliminar
                if(n>0):
                    A=0
                    B=0
                    if(Io[0]>=0):
                        A=1
                    if(Io[0]<0):
                        B=1
                    for i in range(1,idel,1):
                        if(Io[i]-Io[i-1]>=0): #Se comprueba si el elemento a eliminar fue una operación exitosa o fracasada.
                            A=A+1
                        else:
                            B=B+1
                #Apartado para hallar la diferencia o cambio que se debe efectuar a cada uno de los datos posteriores (A la derecha) al dato a eliminar.
                if(idel>0):
                    dtmo=tmo[idel]-tmo[idel-1] #Diferencia de tiempo, o desplazamiento horizontal hacia la izquierda que deben sufrir los datos al momento de eliminar un dato intermedio.
                    dINVo=INVo[idel]-INVo[idel-1]
                    dIo=Io[idel]-Io[idel-1]
                if(idel==0):
                    dtmo=tmo[idel] #Diferencia de tiempo, o desplazamiento horizontal hacia la izquierda que deben sufrir los datos al momento de eliminar un dato intermedio.
                    dINVo=INVo[idel]
                    dIo=Io[idel]

                tmo.pop(idel)
                INVo.pop(idel)
                Io.pop(idel)
                for i in range(idel,n,1):
                    tmo[i]=tmo[i]-dtmo
                    INVo[i]=INVo[i]-dINVo
                    Io[i]=Io[i]-dIo
                archivo = open(profile+'.txt', mode='w',newline='\n')
                archivo.write(str(dss)+'\n')
                archivo.write(str(C)+'\n')
                archivo.write(str(Oss)+'\n')
                archivo.write(str(tmo)+'\n')
                archivo.write(str(INVo)+'\n')
                archivo.write(str(Io)+'\n')
                archivo.close()
                beta.pop(idel)
                po.pop(idel)
                if(n>0):
                    #Apartado para ajustar el valor de la probabilidad po.
                    for i in range(idel,n,1):
                         #Apartado para obtener las variables A,B y el vector po[i]
                         if (Io[i]-Io[i-1]>=0):
                             A=A+1
                         else:
                             B=B+1
                         po[i]=float(A/(A+B))
                    
                    counterbltm=tmo[n-1]
                    Iof=Io[n-1]
                    #Línea para asignar el número de operaciones y el ingreso antes de la sesión de forma correcta.
                    if(idel<=nbs):
                        nbs=nbs-1
                        Ibs=Io[nbs-1]

                    Ro.pop(idel)
                    Co.pop(idel)
                    Rro.pop(idel)
                    avINVo.pop(idel)
                    avINVoMax.pop(idel)
                    CIo.pop(idel)
                    for i in range(idel,n,1):
                        Ro[i]=Io[i]/INVo[i]
                        Co[i]=C+Io[i]
                        Rro[i]=(C+Io[i])/C-1
                        avINVo[i]=INVo[i]/(i+1)
                        avINVoMax[i]=-lps*(C+Io[i])
                        if(tmo[i]<CIotmi):
                            #Cuando no haya pasado aún el 'AntiNoiseTime' el tiempo para limpiar el ruido de la variable CIo en los primeros segundo de operación en todo el registro, no se realizarán cálculos para el interés compuesto debido altos niveles de fluctuación de la variable en este rango de tiempo seleccionado por el usuario.
                            CIo[i]=0.0
                        if(tmo[i]>=CIotmi):
                            try:
                                CIo[i]=(1+Ro[i])**(60/tmo[i])-1
                            except:
                                CIo[i]=max(CIo)
                    Cof=Co[n-1]
                if(n==0):
                    counterbltm=0
                    Iof=0
                    Ibs=0
                    Ro.pop()
                    Co.pop()
                    Rro.pop()
                    avINVo.pop()
                    avINVoMax.pop()
                    CIo.pop()
                    Cof=C
                if(len(Oss)>0):#Línea de código para corroborrar que el elemento del registro a eliminar no concuerde con un elemento de inicio de operación, si ese es el caso se trasladará el inicio de operación para el elemento inmediatamente anterior.
                    #try:
                    iOss=Oss.index(idel)
                    Oss[iOss]=Oss[iOss]-1
                    tmss[iOss]=tmo[Oss[iOss]]
                    Pss[iOss]=po[Oss[iOss]]
                    CIss[iOss]=(CIo[Oss[iOss]])
                    Rss[iOss]=(Ro[Oss[iOss]])
                    Coss[iOss]=(Co[Oss[iOss]])
                    Rrss[iOss]=(Rro[Oss[iOss]])
                    Iss[iOss]=(Io[Oss[iOss]])
                    INVss[iOss]=(INVo[Oss[iOss]])
                    avINVss[iOss]=(avINVo[Oss[iOss]])
                print("Step No. %i deleted"%(idel+1))
            if(request=="e"):
                request="g"
