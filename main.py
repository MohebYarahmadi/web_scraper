import requests
import selectorlib
import smtplib, ssl
import os
import time
import sqlite3

# This script scrapes a webpage for tour information and sends an email if new tours are found.
# It uses the SelectorLib library to extract data from the HTML source.


URL = 'http://programmer100.pythonanywhere.com/tours/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}



class Events:
    def scrape(self, url):
        """Scrape the page source"""
        # Make a GET request to the URL 
        response = requests.get(url, headers=HEADERS)
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to retrieve data: {response.status_code}")
            return None
        source = response.text
        return source
    
    
    def extract_data(self, source):
        """Extract data from the page source"""
        # Create a SelectorLib extractor
        # The YAML file should contain the selector for the data you want to extract
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        # Extract the data using the extractor
        # The "tours" key should match the key in your YAML file
        value = extractor.extract(source)["tours"]
        return value


class Mailing:
    def __init__(self):
        self.host = 'smtp.gmail.com'
        self.port = 465
        self.sender = 'momobitcoin1986@gmail.com'
        self.password = '**********'
        self.reciever = 'momobitcoin1986@gmail.com'
        print("Mailing init function")
        
    def send(self, msg):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.host, self.port, context=context) as server:
            server.login(self.sender, self.password)
            server.sendmail(self.sender, self.reciever, msg)
        print("Email sent!")


class TextDB:
    def __init__(self, filepath):
        self.filepath = filepath
        
    def store(self, data):
        """Store data in a file"""
        with open(self.filepath, "a") as file: # Open the file in append mode
            file.write(data + "\n")
    
    
    def read_file(self):
        """Read the file and return its contents"""
        with open(self.filepath, "r") as file:
            return file.read()


class Database:
    def __init__(self, database_path):
        self.con = sqlite3.connect(database_path)
        
    def read(self, extracted):
        row = extracted.split(",")
        row = [item.strip() for item in row]
        print(row)
        band, city, date = row
        cursor = self.con.cursor()
        cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?",
                        (band, city, date)
                        )
        rows = cursor.fetchall()
        return rows

    def store(self, extracted):
        row = extracted.split(",")
        row = [item.strip() for item in row]
        cursor = self.con.cursor()
        cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
        self.con.commit()


if __name__ == "__main__":
    event = Events()
    mail = Mailing()
    db = Database('data.db')
    while True:
        scraped = event.scrape(URL)
        ex_data = event.extract_data(scraped)
        print(ex_data)
        # Check if the data is not already in the file
        if ex_data != "No upcoming tours":
            row = db.read(ex_data)
            if not row:
                db.store(ex_data)
                mail.send(msg=f"Hey new event founded.\n{ex_data}")
        time.sleep(10)
        # You can use pythonanywhere too
