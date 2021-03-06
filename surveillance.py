import numpy as np
import cv2, time, pandas
from datetime import datetime
import getpass
from sendemail import email
from multiprocessing import Process
from twilio.rest import Client
from graphplot import showgraph

def start_surveillance(sender,receivers,password):
    #mail_obj = email()
    #mail_obj.configure(sender,password)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    
    #Initializations for graph
    status_list=[None,None]
    times=[]
    df=pandas.DataFrame(columns=["Start","End"])

    #for sms
    account_sid = "Twilio Account ID"
    auth_token  = "Twilio Authorization Token"
    receiver=['Receiver Phone Number Here']

    # Initializations for saving the video!
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    detected_out = cv2.VideoWriter('/videos/detected.mp4',fourcc, 15.0, (640,480))
    full_out = cv2.VideoWriter('/videos/full_video.mp4',fourcc, 15.0, (640,480))
    cap = cv2.VideoCapture()
    cap.open(0) # pass 0 for inbuilt camera, pass 1 for external camera 
    count = 0
    lst = []
    while 1:
        status=0
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face = face_cascade.detectMultiScale(gray, 1.3, 5)
        full_out.write(img)
        for (x,y,w,h) in face:
            status=1
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),3)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,0,255),1)
            detected_out.write(img) 
            cv2.imwrite("/Detected_Faces/frame%d.jpg" % count, img)
            count+=1

        if status!=0:
            lst=[]
            for i in range(count):
                lst.append('/Detected_Faces/frame'+str(i)+'.jpg')
            print(lst)
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                    to=receiver,
                    from_="Phone Number",
                    body="Some intrusion has been detected at your home   ~Team automaticsurveillance")
            
            my_process = Process(target=mail_obj.send_email, args=(sender,password,lst,receivers,'Alert! Snapshots'))
            my_process.start()
            mail_obj.send_email(sender,password,lst,receivers,'Alert! Snapshots')

        status_list.append(status)
        status_list=status_list[-2:]

        if status_list[-1]==1 and status_list[-2]==0:
            times.append(datetime.now())
            
        if status_list[-1]==0 and status_list[-2]==1:
            times.append(datetime.now())

        cv2.imshow('Live View',img)

        k = cv2.waitKey(1)
        if k==ord('q'):
            my_process.terminate()
            if status==1:
                times.append(datetime.now())
            break    
    for i in range(0,len(times),2):
        df=df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)
    df.to_csv("Times.csv")
    cap.release()
    detected_out.release()
    full_out.release()
    lst = ['/videos/detected.mp4','/videos/full_video.mp4']
    cv2.destroyAllWindows()
    showgraph(df)
    if count!=0:
        mail_obj.send_email(sender,password,lst,receivers,'Video Alert')
    
if __name__ == '__main__':
    sender = 'Sender Email Address'
    receivers = ['Receiver Email Address']
    password = getpass.getpass("Password:")# Sender's Email Password
    start_surveillance(sender,receivers,password)
