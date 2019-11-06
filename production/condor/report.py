import os, sys, smtplib, subprocess, time
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import sys 

user=str(os.environ['USER'])
cmsswBase=str(os.environ['CMSSW_BASE'])
voms=bool(os.environ.get('VOMSINITVAR'))

cnts={}

def sendMailTo(main, error=False): #, sample, status):
        
    curTime=(time.strftime("%H:%M:%S"))
    curDate=(time.strftime("%d/%m/%Y"))

    fromaddr = "DTDPG-report"
    toaddr = user+"@cern.ch"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "DT DPG ntuple producer report ("+curDate+" ; "+curTime+") "
    if error:
        msg['Subject']+=" ABORTED"
    msg.attach(MIMEText(main, 'plain'))
    
    text = msg.as_string()

    #server = smtplib.SMTP('smtp.cern.ch', 587)
    #server.starttls()
    #server.login(toaddr, passw)
    server = smtplib.SMTP("localhost")
    server.sendmail(toaddr, toaddr, text)
    server.quit()

msg = ''
for x in range(1,4):
    try:
        msg_file = open('log%d_%s'%(x,sys.argv[1]),'r')
        msg +=  'Log of step %d \n'%x
        msg += msg_file.read() + '\n'
    except IOError: 
        msg += "Step %d was not run"%x

sendMailTo( msg ) 
