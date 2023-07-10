from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import urllib
import csv

# Read the CSV file initially
contatos_df = pd.read_csv("teste.csv")

# Function to send messages
def send_messages():
    # Create a webdriver instance
    navegador = webdriver.Chrome()
    
    navegador.get("https://web.whatsapp.com/")
    time.sleep(10)  # Adjust the sleep time as needed
    
    # Wait for the WhatsApp login
    while True:
        input("Press Enter after scanning the QR code")
        if len(navegador.find_elements("id", "side")) >= 1:
            break
        else:
            print("WhatsApp login failed. Please try again.")
    
    # Iterate through the contacts in the CSV file
    for i, row in contatos_df.iterrows():
        pessoa = row['Pessoa']
        numero = row['Número']
        mensagem = row['Mensagem']
        
        texto = urllib.parse.quote(f"Oi {pessoa}! {mensagem}")
        link = f"https://web.whatsapp.com/send?phone={numero}&text={texto}"
        navegador.get(link)
        time.sleep(5)  # Adjust the sleep time as needed
        
        # Check if the chat window is loaded
        while len(navegador.find_elements("xpath", '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p/span')) < 1:
            time.sleep(1)
        
        # Send the message
        navegador.find_element("xpath", '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p/span').send_keys(Keys.ENTER)
        
        print(f"Message sent to {pessoa} - {numero}")
        time.sleep(10)  # Adjust the sleep time as needed
    
    print("All messages sent!")
    navegador.quit()  # Close the webdriver after sending messages

# Function to add a contact to the CSV file
def add_contact(name, phone_number):
    # Append the new contact to the CSV file
    with open('teste.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, phone_number, "hello!"])
    
    print("Contact added successfully.")

# Option 1: Send messages to existing contacts
def option1():
    send_messages()

# Option 2: Add a new contact to the CSV file
def option2(name, phone_number):
    add_contact(name, phone_number)

# Main program
while True:
    choice = input("Enter your choice (1: Send Messages, 2: Add Contact): ")
    
    if choice == "1":
        option1()
    elif choice == "2":
        name = input("Enter the contact name: ")
        phone_number = input("Enter the contact phone number: ")
        option2(name, phone_number)
    else:
        print("Invalid choice. Please try again.")
