import smtplib

smtpObj=smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.starttls()
smtpObj.login('grulan042@gmail.com','isvwngvilrmhtbeh')
smtpObj.sendmail("grulan042@gmail.com","akul6999@gmail.com","go to bed!")