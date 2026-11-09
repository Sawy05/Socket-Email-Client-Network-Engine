import smtplib
import imaplib
import email
import socket
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import *
from plyer import notification

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

NOTIFY_HOST = "127.0.0.1"
NOTIFY_PORT = 9999


def send_notification(msg):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((NOTIFY_HOST, NOTIFY_PORT))
        s.send(msg.encode())
        s.close()
    except:
        pass


def send_email():
    start_time = time.time()

    sender = sender_entry.get()
    password = password_entry.get()
    receiver = receiver_entry.get()
    subject = subject_entry.get()
    body = body_text.get("1.0", END)

    try:
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = receiver
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(sender, password)
        server.send_message(msg)
        server.quit()

        end_time = time.time()

        notification.notify(
            title="Email Client",
            message="Email Sent Successfully",
            timeout=5
        )

        send_notification("Email Sent Successfully")

        print("SMTP Send Time:", end_time - start_time)

    except Exception as e:
        send_notification("Email Sending Failed")
        print("Error:", e)


def receive_email():
    start_time = time.time()

    user = sender_entry.get()
    password = password_entry.get()

    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(user, password)
        mail.select("inbox")

        _, data = mail.search(None, "ALL")
        latest_email_id = data[0].split()[-1]

        _, msg_data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = msg_data[0][1]
        message = email.message_from_bytes(raw_email)

        subject = message["subject"]
        body = ""

        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
        else:
            body = message.get_payload(decode=True).decode()

        notification.notify(
            title="New Email Received",
            message=f"Subject: {subject}",
            timeout=6
        )

        send_notification("Email Received Successfully")

        mail.logout()

        end_time = time.time()
        print("IMAP Fetch Time:", end_time - start_time)

    except Exception as e:
        print("Error:", e)


# ================= GUI ===================
root = Tk()
root.title("Email Client")

Label(root, text="Sender Email").grid(row=0, column=0)
Label(root, text="Password").grid(row=1, column=0)
Label(root, text="Receiver Email").grid(row=2, column=0)
Label(root, text="Subject").grid(row=3, column=0)
Label(root, text="Body").grid(row=4, column=0)

sender_entry = Entry(root, width=40)
password_entry = Entry(root, show="*", width=40)
receiver_entry = Entry(root, width=40)
subject_entry = Entry(root, width=40)
body_text = Text(root, width=30, height=6)

sender_entry.grid(row=0, column=1)
password_entry.grid(row=1, column=1)
receiver_entry.grid(row=2, column=1)
subject_entry.grid(row=3, column=1)
body_text.grid(row=4, column=1)

Button(root, text="Send Email", command=send_email).grid(row=5, column=0)
Button(root, text="Receive Email", command=receive_email).grid(row=5, column=1)

root.mainloop()
