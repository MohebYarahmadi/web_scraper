import requests
import selectorlib
import smtplib, ssl
import os

# This script scrapes a webpage for tour information and sends an email if new tours are found.
# It uses the SelectorLib library to extract data from the HTML source.


URL = 'http://programmer100.pythonanywhere.com/tours/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def scrape(url):
    """Scrape the page source"""
    # Make a GET request to the URL 
    response = requests.get(url, headers=HEADERS)
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return None
    source = response.text
    return source


def extract_data(source):
    """Extract data from the page source"""
    # Create a SelectorLib extractor
    # The YAML file should contain the selector for the data you want to extract
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    # Extract the data using the extractor
    # The "tours" key should match the key in your YAML file
    value = extractor.extract(source)["tours"]
    return value


def send_email(msg):
    host = 'smtp.gmail.com'
    port = 465
    sender = 'momobitcoin1986@gmail.com'
    password = '**************'
    reciever = 'momobitcoin1986@gmail.com'
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, reciever, msg)
    print("Email sent!")


def store(data):
    """Store data in a file"""
    with open("data.txt", "a") as file: # Open the file in append mode
        file.write(data + "\n")


def read_file():
    """Read the file and return its contents"""
    with open("data.txt", "r") as file:
        return file.read()

if __name__ == "__main__":
    scraped = scrape(URL)
    ex_data = extract_data(scraped)
    print(ex_data)
    content = read_file()
    # Check if the data is not already in the file
    if ex_data != "No upcoming tours":
        if ex_data not in content:
            store(ex_data)
            send_email(msg=f"Hey new event founded.\n{ex_data}")
