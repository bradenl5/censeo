import customtkinter as ctk
import pandas as pd
import json
import os.path
import time
import random
import socket
import sys
import _thread
import time
import logging
import numpy as np
from scipy import integrate
import asyncio
from threading import Thread
from bleak import BleakClient
import struct

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

#TO RESET DATA.JSON: comment out the ''' in the line below, save, and run once
'''
available_supplies = {
    1: {
        "name": "Cream 1",
        "category": "cream",
        "quantity": 1,
        "refillSize": 50,
        "date": "01/01/2023",
    },
    2: {
        "name": "Pill 1",
        "category": "pill",
        "quantity": 10,
        "refillSize": 100,
        "date": "01/01/2023",
    },
    3: {
        "name": "Bandage",
        "category": "other",
        "quantity": 50,
        "refillSize": 25,
        "date": "01/01/2023",
    },
    4: {
        "name": "Cream 2",
        "category": "cream",
        "quantity": 50,
        "refillSize": 25,
        "date": "01/01/2023",
    },
    5: {
        "name": "Pill 2",
        "category": "pill",
        "quantity": 100,
        "refillSize": 50,
        "date": "01/01/2023",
    },
    6: {
        "name": "Cream 3",
        "category": "cream",
        "quantity": 75,
        "refillSize": 25,
        "date": "01/01/2023",
    },
    7: {
        "name": "Pill 3",
        "category": "pill",
        "quantity": 70,
        "refillSize": 50,
        "date": "01/01/2023",
    },
    8: {
        "name": "Cream 4",
        "category": "cream",
        "quantity": 90,
        "refillSize": 50,
        "date": "01/01/2023",
    },
    9: {
        "name": "Pill 4",
        "category": "pill",
        "quantity": 50,
        "refillSize": 10,
        "date": "01/01/2023",
    },
    10: {
        "name": "Pill 5",
        "category": "pill",
        "quantity": 60,
        "refillSize": 40,
        "date": "12/06/2023",
    },
}

# Formatting Dictionary into JSON format
js = json.dumps(available_supplies)

# json.dumps() function converts a
# Python object into a json string
js  # so we got all data in json string format here

# Create Jason File for DataBase and Write data Into File
fd = open("data.json", "w")
# it will open file into write mode if file
# does not exists then it will create file too
fd.write(js)  # writing string into file
fd.close()  # Close File After Inserting Data'''

user_id = 0
isLoggedIn = False

tableRows = 0
tableCols = 0
bandage_connected = False

async def connectDevices():
    async with BleakClient("58:BF:25:9C:4E:C6") as client:
        await client.start_notify("19b10001-e8f2-537e-4f6c-d104768a1214", handle_rotation_change)
        print("connected")
        bandage_connected = True
        # Continuously run the loop
        while True:
            await asyncio.sleep(0.001)

#class Supply:
#    def __init__(self, id, name, category, quantity, refillSize, date):
#        self.id = id
#        self.name = name
#        self.category = category
#        self.quantity = quantity
#        self.refillSize = refillSize
#        self.data = date
#
#    def __str__(self):
#        return (str(self.id) + self.name + self.category + str(self.quantity) + str(self.refillSize) + self.date)

class Login(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Login System")
        self.minsize(500, 350)

        loginFrame = ctk.CTkFrame(master=self)
        loginFrame.pack(pady=20, padx=60, fill="both", expand=True)

        label = ctk.CTkLabel(master=loginFrame, text="Login System", font=("Roboto-Black", 32))
        label.pack(pady=12, padx=10)

        entry = ctk.CTkEntry(master=loginFrame, placeholder_text="User ID")
        entry.pack(pady=12, padx=10)
        self.entry = entry

        loginButton = ctk.CTkButton(master=loginFrame, text="Log In", command=self.checkUser)
        loginButton.pack(pady=12, padx=10)
    
        newUserButton = ctk.CTkButton(master=loginFrame, text="New User", command=self.newUser)
        newUserButton.pack(pady=12, padx=10)

    def newUser(self):
        if os.path.isfile("user_data.json") is False:
            user_data = {}
        else:
            fd = open("user_data.json", "r")
            txt = fd.read()
            user_data = json.loads(txt)
            fd.close()

        global user_id

        if len(user_data.keys()) == 0:
            user_id = 1000
        else:
            user_id = int(list(user_data.keys())[-1]) + 1
        
        user_id = str(user_id)
        time_date = []
        usage_no = []
        name = []
        category = []
        quantity_all = []
        prod_id = []
        transaction_id = "".join(
            random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(10)
        )

        print("Welcome New User!")
        print("Your user ID is " + user_id)

        if user_id not in user_data.keys():
            user_data[user_id] = {}

        global isLoggedIn
        isLoggedIn = True

        self.withdraw()
        global home
        home.updateUserLabel()
        home.deiconify()

        loginButton = home.getLoginButton()
        loginButton.configure(text="Sign Out")
        loginButton.configure(command=home.signOut)

        js = json.dumps(user_data)
        fd = open("user_data.json", "w")
        fd.write(js)
        fd.close()

    def checkUser(self):
        if os.path.isfile("user_data.json") is False:
            user_data = {}
        else:
            fd = open("user_data.json", "r")
            txt = fd.read()
            user_data = json.loads(txt)
            fd.close()

        global user_id
        userInput = self.entry.get()
        global isLoggedIn

        if (userInput in user_data.keys()):
            user_id = userInput
            isLoggedIn = True
            print("Welcome User " + user_id + "!")
            self.withdraw()
            global home
            home.updateUserLabel()
            home.deiconify()

            loginButton = home.getLoginButton()
            loginButton.configure(text="Sign Out")
            loginButton.configure(command=home.signOut)

        else:
            print("Please enter a valid user ID or press \"New User\"")

        js = json.dumps(user_data)
        fd = open("user_data.json", "w")
        fd.write(js)
        fd.close()


class RecordUse(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Record Use")
        self.minsize(550, 375)

        #self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        #self.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight=1)

        recordUseFrame = ctk.CTkFrame(master=self)
        recordUseFrame.pack(pady=20, padx=60, fill="both", expand=True)

        label = ctk.CTkLabel(master=recordUseFrame, text="Record Use", font=("Roboto-Black", 26))
        label.pack(pady=(32,20), padx=15)

        nameidEntry = ctk.CTkEntry(master=recordUseFrame, placeholder_text="Supply Name or ID")
        nameidEntry.pack(pady=12, padx=10)
        self.nameidEntry = nameidEntry

        quantAddEntry = ctk.CTkEntry(master=recordUseFrame, placeholder_text="Quantity Added")
        quantAddEntry.pack(pady=12, padx=10)
        self.quantAddEntry = quantAddEntry

        quantRemEntry = ctk.CTkEntry(master=recordUseFrame, placeholder_text="Quantity Removed")
        quantRemEntry.pack(pady=12, padx=10)
        self.quantRemEntry = quantRemEntry

        dateEntry = ctk.CTkEntry(master=recordUseFrame, placeholder_text="Date of Usage")
        dateEntry.pack(pady=12, padx=10)
        self.dateEntry = dateEntry

        confirmButton = ctk.CTkButton(master=recordUseFrame, text="Confirm", command=self.confirm)
        confirmButton.pack(pady=12, padx=10)


    def confirm(self):
        tempNameid = self.nameidEntry.get() #tempNameid will be a string, even for IDs
        tempQuantAdd = self.quantAddEntry.get() #tempQuantAdd will be a string
        tempQuantRem = self.quantRemEntry.get() #tempQuantRem will be a string
        date = self.dateEntry.get()
        self.date = date

        # Checking if entries exist and are the correct variable types  
        if tempNameid!=(""): # Checking nameid
            fd = open("data.json", "r")
            txt = fd.read()
            data = json.loads(txt)
            fd.close()

            if isinstance(tempNameid, int):
                print("except")
                name = tempNameid
                self.name = name

                if tempQuantAdd!=(""): # Checking quantAdd
                    try:
                        quantAdd = int(tempQuantAdd)
                    except:
                        print("Error: Quantity Added should be an int")
                    else:
                        quantAdd = int(tempQuantAdd)
                        self.quantAdd = quantAdd
                else:
                    quantAdd = 0
                    self.quantAdd = quantAdd

                if tempQuantRem!=(""): # Checking quantRem
                    try:
                        quantRem = int(tempQuantRem)
                    except:
                        print("Error: Quantity Removed should be an int")
                    else:
                        quantRem = int(tempQuantRem)
                        self.quantRem = quantRem
                else:
                    quantRem = 0
                    self.quantRem = quantRem

                self.recordUse()

            else:
                print("else")
                name = tempNameid
                self.name = name

                for i in data.keys():
                    if data[str(i)]["name"] == name:
                        id = i
                        self.id = id

                if tempQuantAdd!=(""): # Checking quantAdd
                    try:
                        quantAdd = int(tempQuantAdd)
                    except:
                        print("Error: Quantity Added should be an int")
                    else:
                        quantAdd = int(tempQuantAdd)
                        self.quantAdd = quantAdd
                else:
                    quantAdd = 0
                    self.quantAdd = quantAdd

                if tempQuantRem!=(""): # Checking quantRem
                    try:
                        quantRem = int(tempQuantRem)
                    except:
                        print("Error: Quantity Removed should be an int")
                    else:
                        quantRem = int(tempQuantRem)
                        self.quantRem = quantRem
                else:
                    quantRem = 0
                    self.quantRem = quantRem

                self.recordUse()

        else:
            print("Error: please enter a supply name or id")

    def recordUse(self):
        print("recordUse")

        fd = open("data.json", "r")
        txt = fd.read()
        data = json.loads(txt)
        fd.close()

        deltaQuant = self.quantAdd - self.quantRem
        self.deltaQuant = deltaQuant

        # ADJUST JSON
        id = self.id
        currQuant = data[str(id)]["quantity"]
        newQuant = currQuant + deltaQuant
        data[str(id)]["quantity"] = newQuant

        self.withdraw()
        global home
        home.deiconify()

        js = json.dumps(data)
        fd = open("data.json", "w")
        fd.write(js)
        fd.close()

        home.refresh()


class AddItem(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Add Item")
        self.minsize(550, 375)

        #self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        #self.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight=1)

        addItemFrame = ctk.CTkFrame(master=self)
        addItemFrame.pack(pady=20, padx=60, fill="both", expand=True)

        label = ctk.CTkLabel(master=addItemFrame, text="Add New Item to Database", font=("Roboto-Black", 26))
        label.pack(pady=(32,20), padx=15)

        nameEntry = ctk.CTkEntry(master=addItemFrame, placeholder_text="Name")
        nameEntry.pack(pady=12, padx=10)
        self.nameEntry = nameEntry

        quantityEntry = ctk.CTkEntry(master=addItemFrame, placeholder_text="Quantity")
        quantityEntry.pack(pady=12, padx=10)
        self.quantityEntry = quantityEntry

        # Change category from entry to dropdown for final product.
        categoryEntry = ctk.CTkEntry(master=addItemFrame, placeholder_text="Category")
        categoryEntry.pack(pady=12, padx=10)
        self.categoryEntry = categoryEntry

        dateEntry = ctk.CTkEntry(master=addItemFrame, placeholder_text="Date Added")
        dateEntry.pack(pady=12, padx=10)
        self.dateEntry = dateEntry

        confirmButton = ctk.CTkButton(master=addItemFrame, text="Confirm", command=self.confirm)
        confirmButton.pack(pady=12, padx=10)


    def confirm(self):
        name = self.nameEntry.get()
        self.name = name
        tempQuantity = self.quantityEntry.get() #tempQuantity will be a string
        category = self.categoryEntry.get()
        self.category = category
        date = self.dateEntry.get()
        self.date = date

        # Checking if entries exist and are the correct variable types    
        if isinstance(name, str) and name!=(""):
            if tempQuantity!=(""):
                try:
                    quantity = int(tempQuantity)
                except:
                    print("Error: Quantity must be an int.")
                else:
                    quantity = int(tempQuantity)
                    self.quantity = quantity
                    print("Confirmed")
                    self.addItem()
            else:
                print("Error: Please enter a value for quantity.")
        elif not isinstance(name, str):
            print("Error: Name must be a string.")
        elif name==(""):
            print("Error: Please enter a value for name.")

    
    def addItem(self):
        print("addItem")

        fd = open("data.json", "r")
        txt = fd.read()
        data = json.loads(txt)
        fd.close()

        id = 1
        for i in data.keys():
            id+=1

        data[id] = {
            "name": self.name,
            "category": self.category,
            "quantity": self.quantity,
            "date": self.date,
        }

        print(data[id]["name"])

        self.withdraw()
        global home
        home.deiconify()

        js = json.dumps(data)
        fd = open("data.json", "w")
        fd.write(js)
        fd.close()

        home.refresh()


class RemoveItem(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Remove Item")
        self.minsize(550, 375)

        removeItemFrame = ctk.CTkFrame(master=self)
        removeItemFrame.pack(pady=20, padx=60, fill="both", expand=True)

        label = ctk.CTkLabel(master=removeItemFrame, text="Remove item from inventory?", font=("Roboto-Black", 26))
        label.pack(pady=(32,20), padx=15)

        confirmButton = ctk.CTkButton(master=removeItemFrame, text="Confirm", command=self.confirm)
        confirmButton.pack(pady=12, padx=10)

        cancelButton = ctk.CTkButton(master=removeItemFrame, text="Cancel", command=self.cancel)
        cancelButton.pack(pady=12, padx=10)

    def confirm(self):
        fd = open("data.json", "r")
        txt = fd.read()
        data = json.loads(txt)
        fd.close()

        print("Enter The Supply ID of The Supply Which You Want To Delete :- ")
        temp = input()
        if temp in data.keys():
            data.pop(temp)  # here we are removing that particular data
            print("Supply ID " + str(temp) + " Deleted Successfully...!!!")
        else:
            print("Invalid Supply ID...!!!")
        js = json.dumps(data)
        fd = open("data.json", "w")
        fd.write(js)
        fd.close()

        self.withdraw()
        global home
        home.deiconify()

        home.refresh()

    def cancel(self):
        self.withdraw()
        global home
        home.deiconify()    


class Home(ctk.CTk):
    def __init__(self):
        super().__init__()

        fd = open("data.json", "r")
        txt = fd.read()
        data = json.loads(txt)
        fd.close()

        main_font = ctk.CTkFont(family="Microsoft Sans Serif Regular", size=15)
        self.main_font = main_font

        self.geometry("900x550")
        self.title("Censeo Inventory")

        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)

        frame1 = ctk.CTkFrame(master=self)
        frame1.pack(pady=(20,0), padx=60, fill="both", expand=True)

        scrollFrame = ctk.CTkScrollableFrame(master=self)
        scrollFrame.pack(pady=10, padx=60, fill="both", expand=True)
        #scrollFrame.configure( *SOMETHING TO ELIMINATE CORNERS* )
        scrollFrame.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.scrollFrame = scrollFrame

        frame2 = ctk.CTkFrame(master=self)
        frame2.pack(pady=(0,20), padx=60, fill="both", expand=True)

        # CREATING FRAME1 WIDGETS

        userLabel = ctk.CTkLabel(master=frame1, font=(main_font, 18))
        #printButton.pack(pady=12, padx=10)
        userLabel.grid(row=0, column=0, columnspan=2, padx=(40,0), pady=(50,30), sticky="nsew")
        self.userLabel = userLabel
        self.updateUserLabel()

        homeLabel = ctk.CTkLabel(master=frame1, text="Censeo Inventory", font=(main_font,30))
        #homeLabel.pack(pady=12, padx=10)
        homeLabel.grid(row=0, column=2, columnspan=3, padx=(0,15), pady=(50,30), sticky="nsew")
        self.homeLabel = homeLabel

        loginButton = ctk.CTkButton(master=frame1, text="Log In", command=self.enterLogin, font=(main_font, 14), fg_color="#0b5394")
        #loginButton.pack(pady=12, padx=10)
        loginButton.grid(row=0, column=5, columnspan=2, padx=(25,50), pady=(50,30), sticky="nsew")
        self.loginButton = loginButton

        #Title Text Boxes

        idTitle = ctk.CTkTextbox(master=frame1, width=100, height=20, font=(main_font, 14), border_color="#0b5394", border_width=3)
        idTitle.grid(row=2, column=0, columnspan=2, padx=(115,5), pady=(5,0), sticky="nsew")
        self.idTitle = idTitle
        self.idTitle.insert("0.0", "Supply ID")
        idTitle.configure(state="disabled")

        nameTitle = ctk.CTkTextbox(master=frame1, width=100, height=20, font=(main_font, 14), border_color="#0b5394", border_width=3)
        nameTitle.grid(row=2, column=2, columnspan=1, padx=5, pady=(5,0), sticky="nsew")
        self.nameTitle = nameTitle
        self.nameTitle.insert("0.0", "Name")
        nameTitle.configure(state="disabled")

        quantityTitle = ctk.CTkTextbox(master=frame1, width=100, height=25, font=(main_font, 14), border_color="#0b5394", border_width=3)
        quantityTitle.grid(row=2, column=3, columnspan=1, padx=5, pady=(5,0), sticky="nsew")
        self.quantityTitle = quantityTitle
        self.quantityTitle.insert("0.0", "Quantity")
        quantityTitle.configure(state="disabled")

        categoryTitle = ctk.CTkTextbox(master=frame1, width=100, height=25, font=(main_font, 14), border_color="#0b5394", border_width=3)
        categoryTitle.grid(row=2, column=4, columnspan=1, padx=5, pady=(5,0), sticky="nsew")
        self.categoryTitle = categoryTitle
        self.categoryTitle.insert("0.0", "Category")
        categoryTitle.configure(state="disabled")

        lastEditedTitle = ctk.CTkTextbox(master=frame1, width=100, height=25, font=(main_font, 14), border_color="#0b5394", border_width=3)
        lastEditedTitle.grid(row=2, column=5, columnspan=1, padx=(5,105), pady=(5,0), sticky="nsew")
        self.lastEditedTitle = lastEditedTitle
        self.lastEditedTitle.insert("0.0", "Last Edited")
        lastEditedTitle.configure(state="disabled")

        #CREATING SCROLLFRAME WIDGETS

        #Data Table

        #Remove Buttons
        for i in data.keys():
            self.button = ctk.CTkButton(master=scrollFrame, text="-", command=lambda:self.enterRemoveItem(int(i)), font=(main_font, 20), fg_color="#0b5394", width=30)
            self.button.grid(row=i, column=1, padx=(70,5))

        #Supply IDs
        for i in data.keys():
            self.table = ctk.CTkEntry(scrollFrame, width=100, font=(main_font, 14))
            self.table.grid(row=i, column=2, padx=5)
            self.table.insert(ctk.END, str(i))
            self.table.configure(state="disabled")

        #Names
        for i in data.keys():
            self.table = ctk.CTkEntry(scrollFrame, width=100, font=(main_font, 14))
            self.table.grid(row=i, column=3, padx=5)
            supplyID = i
            name = data[supplyID]["name"]
            self.table.insert(ctk.END, str(name))
            self.table.configure(state="disabled")

        #Quantities
        for i in data.keys():
            self.table = ctk.CTkEntry(scrollFrame, width=100, font=(main_font, 14))
            self.table.grid(row=i, column=4, padx=5)
            supplyID = i
            quantity = data[supplyID]["quantity"]
            self.table.insert(ctk.END, str(quantity))
            self.table.configure(state="disabled")

        #Categories
        for i in data.keys():
            self.table = ctk.CTkEntry(scrollFrame, width=100, font=(main_font, 14))
            self.table.grid(row=i, column=5, padx=(5))
            supplyID = i
            category = data[supplyID]["category"]
            self.table.insert(ctk.END, str(category))
            self.table.configure(state="disabled")

        #Last Edited Dates
        for i in data.keys():
            self.table = ctk.CTkEntry(scrollFrame, width=100, font=(main_font, 14))
            self.table.grid(row=i, column=6, padx=5)
            supplyID = i
            lastEdited = data[supplyID]["date"]
            self.table.insert(ctk.END, str(lastEdited))
            self.table.configure(state="disabled")
        

        # CREATING WIDGETS FOR FRAME2

        recordUseButton = ctk.CTkButton(master=frame2, text="Record Use", command=self.enterRecordUse, font=(main_font, 14), fg_color="#0b5394")
        recordUseButton.grid(row=0, column=0, columnspan=3, padx=(155,25), pady=(30,15), sticky="nsew")
        self.recordUseButton = recordUseButton

        addItemButton = ctk.CTkButton(master=frame2, text="Add Item", command=self.enterAddItem, font=(main_font, 14), fg_color="#0b5394")
        addItemButton.grid(row=0, column=3, columnspan=3, padx=(0,25), pady=(30,15) , sticky="nsew")
        self.addItemButton = addItemButton

        updateButton = ctk.CTkButton(master=frame2, text="Update", command=self.update, font=(main_font, 14), fg_color="#0b5394")
        updateButton.grid(row=0, column=6, columnspan=3, padx=(0,25), pady=(30,15) , sticky="nsew")
        self.updateButton = updateButton

        #checkButton = ctk.CTkButton(master=frame2, text="Check", command=self.checkBluetooth, font=(main_font, 14), fg_color="#0b5394")
        #checkButton.grid(row=0, column=9, columnspan=3, padx=(0,25), pady=(30,15) , sticky="nsew")
        #self.checkButton = checkButton

        self.login_window = None

        self.addItem_window = None

        self.recordUse_window = None

        js = json.dumps(data)
        fd = open("data.json", "w")
        fd.write(js)
        fd.close()

    def enterLogin(self):
        self.iconify()  # maybe switch to self.withdraw() for presentation
        if self.login_window is None or not self.login_window.winfo_exists():
            self.login_window = Login(self)  # create window if its None or destroyed
        else:
            self.login_window.deiconify()
            self.login_window.focus()  # if window exists focus it

    def signOut(self):
        global user_id
        user_id = 0
        global isLoggedIn
        isLoggedIn = False
        print("You have signed out.")
        self.updateUserLabel()

        self.loginButton.configure(text="Log In")
        self.loginButton.configure(command=self.enterLogin)

    def print(self):
        global isLoggedIn
        print(isLoggedIn)

    def getLoginButton(self):
        return self.loginButton
    
    def updateUserLabel(self):
        global user_id
        if(user_id == 0):
            self.userLabel.configure(text="Signed Out")
        else:
            self.userLabel.configure(text="User " + str(user_id))

    def enterRecordUse(self):
        print("Record Use")
        global isLoggedIn
        if isLoggedIn:
            self.iconify()  # maybe switch to self.withdraw() for presentation
            if self.recordUse_window is None or not self.recordUse_window.winfo_exists():
                self.recordUse_window = RecordUse(self)  # create window if its None or destroyed
            else:
                self.recordUse_window.deiconify()
                self.recordUse_window.focus()  # if window exists focus it
        else:
            print("Please log in before recording use")

    def enterAddItem(self):
        global isLoggedIn
        if isLoggedIn:
            self.iconify()  # maybe switch to self.withdraw() for presentation
            if self.addItem_window is None or not self.addItem_window.winfo_exists():
                self.addItem_window = AddItem(self)  # create window if its None or destroyed
            else:
                self.addItem_window.deiconify()
                self.addItem_window.focus()  # if window exists focus it
        else:
            print("Please log in before adding item")

    def enterRemoveItem(self, row):
        print(row)

    def refresh(self):
        print("Refresh")

        fd = open("data.json", "r")
        txt = fd.read()
        data = json.loads(txt)
        fd.close()

        scrollFrame = self.scrollFrame
        main_font = self.main_font

        #Data Table

        #Supply IDs
        for i in data.keys():
            self.table = ctk.CTkEntry(scrollFrame, width=100, font=(main_font, 14))
            self.table.grid(row=i, column=1, padx=(110,5))
            self.table.insert(ctk.END, str(i))
            self.table.configure(state="disabled")

        #Names
        for i in data.keys():
            self.table = ctk.CTkEntry(scrollFrame, width=100, font=(main_font, 14))
            self.table.grid(row=i, column=2, padx=5)
            supplyID = i
            name = data[supplyID]["name"]
            self.table.insert(ctk.END, str(name))
            self.table.configure(state="disabled")

        #Quantities
        for i in data.keys():
            self.table = ctk.CTkEntry(scrollFrame, width=100, font=(main_font, 14))
            self.table.grid(row=i, column=3, padx=5)
            supplyID = i
            quantity = data[supplyID]["quantity"]
            self.table.insert(ctk.END, str(quantity))
            self.table.configure(state="disabled")

        #Categories
        for i in data.keys():
            self.table = ctk.CTkEntry(scrollFrame, width=100, font=(main_font, 14))
            self.table.grid(row=i, column=4, padx=(5))
            supplyID = i
            category = data[supplyID]["category"]
            self.table.insert(ctk.END, str(category))
            self.table.configure(state="disabled")

        #Last Edited Dates
        for i in data.keys():
            self.table = ctk.CTkEntry(scrollFrame, width=100, font=(main_font, 14))
            self.table.grid(row=i, column=5, padx=5)
            supplyID = i
            lastEdited = data[supplyID]["date"]
            self.table.insert(ctk.END, str(lastEdited))
            self.table.configure(state="disabled")

        

        js = json.dumps(data)
        fd = open("data.json", "w")
        fd.write(js)
        fd.close()

    def update(self):
        fd = open("data.json", "r")
        txt = fd.read()
        data = json.loads(txt)
        fd.close()

        js = json.dumps(data)
        fd = open("data.json", "w")
        fd.write(js)
        fd.close()

        self.refresh()

    def calculate(self):
        r = 18
        w = 54
        l1 = 175
        l2 = 165
        #total length = 175

        upperz1 = l1
        uppery1 = lambda z: (-r)*z/l1+r
        upperx1 = lambda z, y: (w/2-r)*z/l1+r

        upperz2 = l2
        uppery2 = lambda z: (-r)*z/l2+r
        upperx2 = lambda z, y: (w/2-r)*z/l2+r

        f = lambda z, y, x: 1

        solve1 = integrate.tplquad(f, 0, upperz1, 0, uppery1, 0, upperx1)
        solve2 = integrate.tplquad(f, 0, upperz2, 0, uppery2, 0, upperx2)
        solution = 4*(solve1[0]-solve2[0])/1000
        error = solve1[1]+solve2[1]
        print(solution)


def handle_rotation_change(sender, data):
    rotation = struct.unpack('<L', data)

    print(rotation[0])
    fd = open("data.json", "r")
    txt = fd.read()
    data = json.loads(txt)
    fd.close()

    data["3"]["quantity"] = rotation[0]

    js = json.dumps(data)
    fd = open("data.json", "w")
    fd.write(js)
    fd.close()

    home.refresh()


def asyncioThread():
    asyncio.run(connectDevices())

if __name__ == "__main__":
    t = Thread(target=asyncioThread)
    t.start()

    home = Home()
    home.mainloop()