import json
import random
import httpx

DOMAINS = ["gmailb.tk", "gmailb.ml", "gmailb.ga"]


class TempMail:
    global BASE_URL
    BASE_URL = "https://api.tempmail.lol"

    def makeHTTPRequest(endpoint):
        headers = {"User-Agent": "TempMailPythonAPI/1.0", "Accept": "application/json"}
        try:
            connection = httpx.get(BASE_URL + endpoint, headers=headers)
            if connection.status_code >= 400:
                raise Exception("HTTP Error: " + str(connection.status_code))
        except Exception as e:
            print(e)
            return None
        response = connection.text
        return response

    def generateInbox(rush=False):
        try:
            random_domain = random.choice(DOMAINS)
            s = TempMail.makeHTTPRequest(f"/generate/{random_domain}")
        except:
            print("Website responded with: " + s)
        data = json.loads(s)
        return Inbox(data["address"], data["token"])

    def getEmails(inbox):
        s = TempMail.makeHTTPRequest("/auth/" + inbox.token)
        data = json.loads(s)
        if "token" in s:
            if data["token"] == "invalid":
                raise Exception("Invalid Token")
        if data["email"] == None:
            return ["None"]
        else:
            emails = []
            for email in data["email"]:
                emails.append(
                    Email(
                        email["from"],
                        email["to"],
                        email["subject"],
                        email["body"],
                        email["html"],
                        email["date"],
                    )
                )
            return emails


class Email:
    def __init__(self, sender, recipient, subject, body, html, date):
        self._sender = sender
        self._recipient = recipient
        self._subject = subject
        self._body = body
        self._html = html
        self._date = date

    @property
    def sender(self):
        return self._sender

    @property
    def recipient(self):
        return self._recipient

    @property
    def subject(self):
        return self._subject

    @property
    def body(self):
        return self._body

    @property
    def html(self):
        return self._html

    @property
    def date(self):
        return self._date

    def __repr__(self):
        return "Email (sender={}, recipient={}, subject={}, body={}, html={}, date={} )".format(
            self.sender, self.recipient, self.subject, self.body, self.html, self.date
        )


class Inbox:
    def __init__(self, address, token):
        self._address = address
        self._token = token

    @property
    def address(self):
        return self._address

    @property
    def token(self):
        return self._token

    def __repr__(self):
        return "Inbox (address={}, token={} )".format(self.address, self.token)
