import smtplib
from email.mime.text import MIMEText
import sqlite3


ausleihe_id = 71
query = f"""SELECT kontaktdaten.vorzuname, kontaktdaten.email
            FROM ausleihe
            JOIN kontaktdaten ON ausleihe.kontaktdaten_id = kontaktdaten.kontaktdaten_id
            WHERE ausleihe.ausleihe_id = {ausleihe_id}
                """

conn = sqlite3.connect("db\\verleihverwaltung.db")
cursor = conn.cursor()
data = cursor.execute(query).fetchall()

conn.commit()
cursor.close()


vorname = data[0][0].split()[0]
email = data[0][1]

print(vorname)
print(email)



def sendmail(vorname, email):
    text = f"""Hallo {vorname},\n
hiermit bestätigen wir die Rückgabe deiner Ausleihe.

Solltest du in Zukunft wieder etwas benötigen, schreib uns gerne.
Wir würden uns freuen, wenn wir dich in unserem Newsletter begrüßen dürfen.

Darin erhältst du Updates zu unseren Ausleihartikeln und zusätzlich 10% bei deiner nächsten Ausleihe.

Eintragen kannst du dich über folgenden Link: linklink

Vielen dank für dein Vetrauen in uns und bis zum nächsten Mal.

Dein Outleih Team """

    mail = MIMEText(text)
    mail["subject"] = "Rückgabe GoPRo"
    sender = "Outleih <mail@outleih.de>"
    receiver = "o.thomaschewski@gmail.com"

    s = smtplib.SMTP_SSL("smtp.strato.de", 465)

    s.login("mail@outleih.de", "ohiwc1Bt1Md")
    s.sendmail(sender, receiver, mail.as_string())
    s.quit()

sendmail(vorname, email)