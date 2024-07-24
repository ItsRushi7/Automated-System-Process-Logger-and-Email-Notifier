######################################################################################################################
# Import statement
######################################################################################################################
import os
import sys
import csv
import time
import psutil
import smtplib
import schedule
import urllib.request
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

######################################################################################################################
#   Function Name   :   Is_Connected
#   Input           :   -
#   Output          :   -
#   Description     :   Fucnction is check connection
#   Author          :   Rushikesh Hemant Gholap
#   Date/Time       :   22/07/2024 01:33 pm
######################################################################################################################
     
def Is_Connected():

    url = 'https://www.google.com/'  # Replace with your URL

    try:
        response = urllib.request.urlopen(url)
        return True
        
    except Exception as Error:
        return False
    
######################################################################################################################
#   Function Name   :   Mail_Sender
#   Input           :   FileName Time
#   Output          :   -
#   Description     :   Fucnction is send mail
#   Author          :   Rushikesh Hemant Gholap
#   Date/Time       :   22/07/2024 01:33 pm
######################################################################################################################
def Mail_Sender(File_Name, Time,Uesr_Name,Pass_Word):
 
    try:
        From_Add = Uesr_Name
        To_Add = 'Add Mail to recived that mail'
        MSG = MIMEMultipart()
        
        MSG['From'] = From_Add
        
        MSG['To'] = To_Add 
        
        Body = """
        Hello From %s,
        Welcome to Rushikesh Infosystems.
        Please find attached ducument which 
        contains Log of Running process.
        Log file is created at: %s

        This is auto gennerated mail.
        Thanks & Regards,
        Rushikesh Hemant Gholap
        Rushikesh Infosystems
        """%(From_Add,Time)
        
        Subject = """
        Proccess Log Generated at : %s
        """%(Time)
        
        MSG['Subject'] = Subject
        
        MSG.attach(MIMEText(Body,'plain'))
        
        Attachment = open(File_Name, 'rb')
        
        Pay = MIMEBase('application','octet-stream')
        
        Pay.set_payload((Attachment).read())
        
        encoders.encode_base64(Pay)
        
        Pay.add_header('Content-Disposition',"Attachment File_Name=%s" %File_Name)
        
        MSG.attach(Pay)
        
        Send = smtplib.SMTP('smtp.gmail.com',587)
        
        Send.starttls()
        
        Send.login( Uesr_Name,Pass_Word)
        
        Text = MSG.as_string()
        
        Send.sendmail(From_Add,To_Add,Text)
        
        Send.quit()
        
        print("Log file send through mail")
        
    except Exception as Error:
        print("Exception For : ",Error)
        
######################################################################################################################
#   Function Name   :   Process_Log
#   Input           :   -
#   Output          :   -
#   Description     :   Create log File 
#   Author          :   Rushikesh Hemant Gholap
#   Date/Time       :   22/07/2024 01:33 pm
######################################################################################################################
def Process_Log( Log_Dir = 'Log_Folder'):
    
    List_Proccess = []
    
    Exits = os.path.exists(Log_Dir)
    
    if (Exits == False):
        
        try:
            os.mkdir(Log_Dir)
        except:
            pass
        
    DashLine = "*"*80
    
    timestamp = time.ctime()
    timestamp = timestamp.replace(" ", "")
    timestamp = timestamp.replace(":", "_")
    timestamp = timestamp.replace("/", "_")
    
    Log_Path = os.path.join(Log_Dir,"LogFile%s.Log" %(timestamp))
    
    File_Open = open(Log_Path,'w')
    File_Open.write(DashLine + '\n')
    File_Open.write("Process Logger :" + time.ctime() + '\n')
    File_Open.write(DashLine + '\n')
    File_Open.write('\n')
       
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        List_Proccess.append(proc.info)

    for Data in List_Proccess:
        File_Open.write("%s \n" %Data)
    
    File_Open.write(DashLine + "\n")
        
    File_Open.close()
        
    print("Log file is successfully genrated at location %s",(Log_Path))
      
    Connected = Is_Connected()
    
    if (Connected == True):
        
        OpenFile = open( 'Gmail.csv', mode='r')
        csv_reader = csv.DictReader(OpenFile)
        for row in csv_reader:
            username = row['username']
            password = row['password']
                 
        Mail_Sender(Log_Path,time.ctime(),username,password)

    else:
        print("There is no internet connection")
    
######################################################################################################################
#   Entery Point Function
######################################################################################################################
def main():


    print("------------------------------ MailSender Automation ------------------------------")
    
    if (len(sys.argv) != 3):

        if ((sys.argv[1] == "--h") or (sys.argv[1] == "--H")):
            print("This script is used log record of running processes")
            exit()

        if ((sys.argv[1] == "--u") or (sys.argv[1] == "--U")):
            print("Usage of the script : ")
            print("Name_Of_File Enter the time in minute")
            exit()

        try:
            Start_Time = time.time()
            schedule.every(int(sys.argv[1])).minute.do(Process_Log)
            End_Time = time.time()   
            print("Took %s second to send mail"%(End_Time-Start_Time))
            
            while True:
                schedule.run_pending()
                time.sleep(1)
                
        except ValueError:
            print("Datatype error")

        except Exception as Obj:
            print("Exception for : ", Obj)

    else:
        print("Invalid input")
        print("Use --h option to get the help and use --u option to get the usage of application")
        exit()

    print("------------------------------------ Thank You ------------------------------------")

######################################################################################################################
#   Starter
######################################################################################################################
if (__name__ == "__main__"):
    main()
