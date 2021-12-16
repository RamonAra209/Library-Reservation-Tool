import smtplib
from email.mime.text import MIMEText

BURNER_EMAIL_LOGIN_PATH = "/home/pi/Desktop/LibraryReservationToolBookingInfo/burnerEmailLogin.txt"

def sendEmailNotification(message):
    with open(BURNER_EMAIL_LOGIN_PATH, 'r') as file:
        # inside lines: senderEmail, recieverEmail, senderPassword
        # message = "Something went wrong with the code!"
        lines = file.readlines()
        senderEmail = lines[0]
        recieverEmail = lines[1]
        password = lines[2]
        
        msg = MIMEText(message)
        msg['Subject'] = "Library Reservation Tool Error"
        msg['From'] = senderEmail
        msg['To'] = recieverEmail
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(senderEmail, password)
        server.sendmail(senderEmail, recieverEmail, msg.as_string())
        server.quit()