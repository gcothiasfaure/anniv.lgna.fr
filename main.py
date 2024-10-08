import resend
from datetime import datetime
import os
import requests
import logging
import schedule
import time
from pytz import timezone

def timetz(*args):
    return datetime.now(timezone('Europe/Paris')).timetuple()
logging.Formatter.converter = timetz

logging.basicConfig(filename='./output/output.log',
                    level=logging.INFO,
                    format='%(asctime)s : %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
NOTION_API_TOKEN = os.getenv("NOTION_API_TOKEN")
NOTION_DATABASE_ID = "31c4b817bea9492e96c1cc12dcf18843"
NOTION_API_URL = "https://api.notion.com/v1"
NOTION_HEADERS = {
    "accept": "application/json",
    "Notion-Version": "2022-06-28",
    "content-type": "application/json",
    "Authorization": "Bearer "+NOTION_API_TOKEN
}

def getBirthdatesFromNotion():
    uri = NOTION_API_URL+"/databases/"+NOTION_DATABASE_ID+"/query"
    response = requests.post(uri,headers=NOTION_HEADERS)
    birthdates = []
    for result in response.json()["results"]:
        birthdates.append({
            "name": result['properties']['Nom']['title'][0]['plain_text'],
            "birthdate": result['properties']['Date']['rich_text'][0]['plain_text'],
            "contact-type": result['properties']['Type de contact']['rich_text'][0]['plain_text'],
            "contact":result['properties']['Contact']['rich_text'][0]['plain_text']
        })
    return birthdates

def checkTodayBirthdays(birthdates):
    birthdays_today = []
    for contact in birthdates:
        if contact['birthdate'] == datetime.today().strftime("%d/%m"):
            birthdays_today.append(contact)
    return birthdays_today

def generatePTags(today_birthdays):
    string = ""
    for person in today_birthdays:
        if person["contact-type"] == "messenger":
            string = string + """<p style="font-size:16px;font-weight:bold;line-height:22px;margin:16px 0;font-family:-apple-system, BlinkMacSystemFont, &#x27;Segoe UI&#x27;, &#x27;Roboto&#x27;, &#x27;Oxygen&#x27;, &#x27;Ubuntu&#x27;, &#x27;Cantarell&#x27;, &#x27;Fira Sans&#x27;, &#x27;Droid Sans&#x27;, &#x27;Helvetica Neue&#x27;, sans-serif;margin-top:12px;margin-bottom:24px">"""+person["name"]+""" <a href='https://m.me/"""+person["contact"]+"""' style="color:#898989;text-decoration:underline;font-family:-apple-system, BlinkMacSystemFont, &#x27;Segoe UI&#x27;, &#x27;Roboto&#x27;, &#x27;Oxygen&#x27;, &#x27;Ubuntu&#x27;, &#x27;Cantarell&#x27;, &#x27;Fira Sans&#x27;, &#x27;Droid Sans&#x27;, &#x27;Helvetica Neue&#x27;, sans-serif;font-size:14px;font-weight:normal;" target="_blank">(dm)</a></p>"""
        elif person["contact-type"] == "whatsapp":
            string = string + """<p style="font-size:16px;font-weight:bold;line-height:22px;margin:16px 0;font-family:-apple-system, BlinkMacSystemFont, &#x27;Segoe UI&#x27;, &#x27;Roboto&#x27;, &#x27;Oxygen&#x27;, &#x27;Ubuntu&#x27;, &#x27;Cantarell&#x27;, &#x27;Fira Sans&#x27;, &#x27;Droid Sans&#x27;, &#x27;Helvetica Neue&#x27;, sans-serif;margin-top:12px;margin-bottom:24px">"""+person["name"]+""" <a href='https://wa.me/"""+person["contact"]+"""' style="color:#898989;text-decoration:underline;font-family:-apple-system, BlinkMacSystemFont, &#x27;Segoe UI&#x27;, &#x27;Roboto&#x27;, &#x27;Oxygen&#x27;, &#x27;Ubuntu&#x27;, &#x27;Cantarell&#x27;, &#x27;Fira Sans&#x27;, &#x27;Droid Sans&#x27;, &#x27;Helvetica Neue&#x27;, sans-serif;font-size:14px;font-weight:normal;" target="_blank">(whatsapp)</a></p>"""
        elif person["contact-type"] == "insta":
            string = string + """<p style="font-size:16px;font-weight:bold;line-height:22px;margin:16px 0;font-family:-apple-system, BlinkMacSystemFont, &#x27;Segoe UI&#x27;, &#x27;Roboto&#x27;, &#x27;Oxygen&#x27;, &#x27;Ubuntu&#x27;, &#x27;Cantarell&#x27;, &#x27;Fira Sans&#x27;, &#x27;Droid Sans&#x27;, &#x27;Helvetica Neue&#x27;, sans-serif;margin-top:12px;margin-bottom:24px">"""+person["name"]+""" <a href='https://www.instagram.com/"""+person["contact"]+"""' style="color:#898989;text-decoration:underline;font-family:-apple-system, BlinkMacSystemFont, &#x27;Segoe UI&#x27;, &#x27;Roboto&#x27;, &#x27;Oxygen&#x27;, &#x27;Ubuntu&#x27;, &#x27;Cantarell&#x27;, &#x27;Fira Sans&#x27;, &#x27;Droid Sans&#x27;, &#x27;Helvetica Neue&#x27;, sans-serif;font-size:14px;font-weight:normal;" target="_blank">(insta)</a></p>"""
        else: # person["contact-type"] == "tel"
            string = string + """<p style="font-size:16px;font-weight:bold;line-height:22px;margin:16px 0;font-family:-apple-system, BlinkMacSystemFont, &#x27;Segoe UI&#x27;, &#x27;Roboto&#x27;, &#x27;Oxygen&#x27;, &#x27;Ubuntu&#x27;, &#x27;Cantarell&#x27;, &#x27;Fira Sans&#x27;, &#x27;Droid Sans&#x27;, &#x27;Helvetica Neue&#x27;, sans-serif;margin-top:12px;margin-bottom:24px">"""+person["name"]+""" <a href='tel:"""+person["contact"]+"""' style="color:#898989;text-decoration:underline;font-family:-apple-system, BlinkMacSystemFont, &#x27;Segoe UI&#x27;, &#x27;Roboto&#x27;, &#x27;Oxygen&#x27;, &#x27;Ubuntu&#x27;, &#x27;Cantarell&#x27;, &#x27;Fira Sans&#x27;, &#x27;Droid Sans&#x27;, &#x27;Helvetica Neue&#x27;, sans-serif;font-size:14px;font-weight:normal;" target="_blank">(tel)</a></p>"""
    return string

def sendEmail(today_birthdates):
    params: resend.Emails.SendParams = {
        "from": "anniv.lgna.fr <ajd@anniv.lgna.fr>",
        "to": ["gas.cothias@gmail.com"],
        "subject": "Anniversaire(s) du jour ("+datetime.today().strftime("%d/%m")+")",
        "html":
        """
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html dir="ltr" lang="fr">
            <head>
                <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
                <meta name="x-apple-disable-message-reformatting" />
            </head>
            <body style="background-color:#ffffff">
                <table align="center" width="100%" border="0" cellPadding="0" cellSpacing="0" role="presentation" style="max-width:37.5em;padding-left:12px;padding-right:12px;margin:0 auto">
                    <tbody>
                    <tr style="width:100%">
                        <td>
                            """+generatePTags(today_birthdates)+"""
                        </td>
                    </tr>
                    </tbody>
                </table>
            </body>
        </html>
        """
    }
    email = resend.Emails.send(params)
    return email

def job():
    # Logique ici
    # print("début du programme")
    # print(NOTION_API_TOKEN)
    # print(RESEND_API_KEY)
    birthdates = getBirthdatesFromNotion()
    # print("birthdates :")
    # print(birthdates)
    today_birthdates = checkTodayBirthdays(birthdates)
    # print("today_birthdates :")
    # print(today_birthdates)
    if len(today_birthdates)>0:
        # print("len(today_birthdates)>0")
        sendEmail(today_birthdates)
        logging.info(str(len(today_birthdates))+" anniversaire(s) ce jour : "+' - '.join([contact['name'] for contact in today_birthdates]))
    else:
        # print("len(today_birthdates)=0")
        logging.info("Pas d'anniversaire ce jour")
    # print("Fin du programme")

# schedule.every(1).minutes.do(job)
schedule.every().day.at("08:37", "Europe/Paris").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
