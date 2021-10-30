import pandas as pd, os, smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from  emailInfo import EMAIL, PASSWORD

# Define a folder to hold the tickers
Folder = "MACD/"

def get_propose_and_email():
    Path = os.getcwd() + Folder

    Analysis = pd.read_csv(Path+"MACD.csv")  # Read in the ranked stocks
    # top10 = Analysis.head(10)  # I want to see the 10 stocks in my analysis with the highest OBV values
    # bottom10 = Analysis.tail(10)  # I also want to see the 10 stocks in my analysis with the lowest OBV values

    try:
        # gmail_user = EMAIL
        # gmail_password = 'ihrkhofegyrbpuqq'
        
        sent_from = EMAIL
        to = [EMAIL]

        body = """\
        Good morning Mr. Frank
        Those are the required actions for today:
        """ + Analysis.to_string(index=False) + """
        Sincerely,
        Your Computer"""
        
        msg = MIMEMultipart()
        msg['To'] = ", ".join(to)
        msg['From'] = sent_from
        msg['subject'] = "Daily Stock Report"
        msg.attach(MIMEText(body,'plain'))
        
        message = msg.as_string()

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(EMAIL, PASSWORD)
        server.sendmail(sent_from, to, message)
        server.quit()

        print("Email sent!")
    except:
        print("Something went wrong...")
