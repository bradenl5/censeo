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


def server():
    # open a log file to log communications
    logging.basicConfig(filename="server.log", filemode="a", level=logging.INFO)

    # open a tcp socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the port
    ip = "172.20.10.2"
    if len(sys.argv) > 1:
        ip = sys.argv[1]
    port = 5555
    server_address = (ip, port)
    s.bind(server_address)
    # listen for incoming connections
    # s.listen()
    logging.info("####### Server is bound #######")
    # block and wait for a new incoming connection
    # conn = s.accept()
    # print("####### Server accepted connection #######")

    while True:
        # block and wait for a new incoming connection
        logging.info("####### Server is listening #######")
        msg, address = s.recvfrom(4096)
        # conn = s.accept()
        # print("####### Server accepted connection #######")
        # We expect a new connection to send us two strings:
        # the supply ID
        # and the event that happened (like "dispensed")
        # msg = conn[0].recv(4096)
        logging.info("Received %s" % msg)
        message = msg.decode("utf-8").rstrip().lstrip()
        parts = message.split("|", 3)
        supplyID = parts[0]
        event = parts[1]
        value = parts[2]
        logging.info(
            "\nServer received: %s Event: %s Value: %s\n" % (supplyID, event, value)
        )

        fd = open("data.json", "r")
        data = json.loads(fd.read())
        fd.close()

        if event == "dispensed":
            # Subtract one from the current quantity
            currQuantity = data[supplyID]["quantity"]
            newQuantity = currQuantity - 1
            data[supplyID]["quantity"] = newQuantity
            logging.info("New quantity = %s" % newQuantity)
            s.sendto(("%s" % newQuantity).encode("utf-8"), address)
            # conn[0].send(("%s" % newQuantity).encode("utf-8"))
            logging.info("\n\n 1. Server sent : %s\n\n" % newQuantity)
        elif event == "refilled":
            # Add standard refill amount to quantity
            refillSize = data[supplyID]["refillSize"]
            currQuantity = data[supplyID]["quantity"]
            newQuantity = currQuantity + refillSize
            data[supplyID]["quantity"] = newQuantity
            logging.info("New quantity = %s" % newQuantity)
            # conn[0].send(("%s" % newQuantity).encode("utf-8"))
            s.sendto(("%s" % newQuantity).encode("utf-8"), address)
            logging.info("\n\n 1. Server sent : %s\n\n" % newQuantity)
        elif event == "calculated":
            # Replace current quantity with the newly calculated quantity
            currQuantity = data[supplyID]["quantity"]
            newQuantity = value
            data[supplyID]["quantity"] = newQuantity
            logging.info("New quantity = %s" % newQuantity)
            # conn[0].send(("%s" % newQuantity).encode("utf-8"))
            s.sendto(("%s" % newQuantity).encode("utf-8"), address)
            logging.info("\n\n 1. Server sent : %s\n\n" % newQuantity)
        # else:
        #    s.close()
        js = json.dumps(data)
        fd = open("data.json", "w")
        fd.write(js)
        fd.close()


# Creating Dictionary to store data
available_supplies = {
    1001: {
        "name": "Pill 1",
        "category": "pill",
        "quantity": 10,
        "refillSize": 10,
        "date": "01/01/2023",
    },
    1002: {
        "name": "Cream 1",
        "category": "cream",
        "quantity": 100,
        "refillSize": 50,
        "date": "01/01/2023",
    },
    1003: {
        "name": "Bandage",
        "category": "other",
        "quantity": 50,
        "refillSize": 25,
        "date": "01/01/2023",
    },
    1004: {
        "name": "Cream 2",
        "category": "cream",
        "quantity": 50,
        "refillSize": 25,
        "date": "01/01/2023",
    },
    1005: {
        "name": "Pill 2",
        "category": "pill",
        "quantity": 100,
        "refillSize": 50,
        "date": "01/01/2023",
    },
    1006: {
        "name": "Cream 3",
        "category": "cream",
        "quantity": 75,
        "refillSize": 25,
        "date": "01/01/2023",
    },
    1007: {
        "name": "Pill 3",
        "category": "pill",
        "quantity": 70,
        "refillSize": 50,
        "date": "01/01/2023",
    },
    1008: {
        "name": "Cream 4",
        "category": "cream",
        "quantity": 90,
        "refillSize": 50,
        "date": "01/01/2023",
    },
    1009: {
        "name": "Pill 4",
        "category": "pill",
        "quantity": 50,
        "refillSize": 10,
        "date": "01/01/2023",
    },
    1010: {
        "name": "Cream 5",
        "category": "cream",
        "quantity": 60,
        "refillSize": 40,
        "date": "01/01/2023",
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
# does not exists then it will create file too'''
fd.write(js)  # writing string into file
fd.close()  # Close File After Inserting Data


def overall():
    print(
        "========\
	NASA Hunch Inventory Management System \
	=============="
    )
    while 1:
        print("1)Display DataBase/All Supplies with their details")
        print("2)Display Certain Supply with its details")
        print("3)Add New Supply to DataBase")
        print("4)Update Supply in Database")
        print("5)Delete Supply in DataBase")
        print("6)Display User Reports")
        print("7)Exit")
        print("Enter Your Choice :- ")
        n = int(input())
        if n == 1:
            display_data()
        elif n == 2:
            display_specific_data()
        elif n == 3:
            add_new()
        elif n == 4:
            update_prod_data()
        elif n == 5:
            delete_prod()
        elif n == 6:
            display_reports_overall()
        elif n == 7:
            break
        else:
            print("Invalid Choice...!!!")


def display_data():
    fd = open("data.json", "r")
    txt = fd.read()  # reading data from file
    data = json.loads(txt)

    # This will parse the JSON data, populates a
    # Python dictionary with the data
    fd.close()
    print(
        "Enter '0' to order data by category or '1' to order data by the time it was added to the system :- "
    )
    n = int(input())

    # Display All Records
    if n == 1:
        table = pd.DataFrame(columns=["ID", "name", "category", "quantity", "date"])

        # Creating Pandas dataframe to show data in table format later
        for i in data.keys():
            # Fetch all keys in dictionary
            temp = pd.DataFrame(columns=["ID"])
            temp["ID"] = [i]
            for j in data[i].keys():
                temp[j] = [data[i][j]]
            table = table.append(temp)
        table = table.reset_index(drop=True)
        """This will reset index of dataframe"""
        from IPython.display import display

        display(table)

    elif n == 0:
        # Display Records by Category
        table = pd.DataFrame(columns=["ID", "name", "category", "quantity", "date"])
        cat = []

        for i in data.keys():
            temp = pd.DataFrame(columns=["ID"])
            temp["ID"] = [i]
            for j in data[i].keys():
                temp[j] = [data[i][j]]
                if j == "category":
                    cat.append(data[i][j])
            table = table.append(temp)
            table = table.reset_index(drop=True)
            cat = set(cat)
            cat = list(cat)

        for k in cat:
            temp = pd.DataFrame()
            temp = table[table["category"] == k]
            print("Data Of Supplies Of Category " + k + " is:- ")
            from IPython.display import display

            display(temp)
    else:
        print("Enter Valid Choice...!!!")


# display_data() # Uncomment This Line To Run This Function


def display_specific_data():
    fd = open("data.json", "r")
    txt = fd.read()
    data = json.loads(txt)
    fd.close()
    print("Enter Supply ID Whose Details You Want to Have a Look on :- ")
    i = input()

    # Following Code will Filter out Supply ID from Records
    if i in data.keys():
        temp = pd.DataFrame(columns=["ID"])
        temp["ID"] = [i]
        for j in data[i].keys():
            temp[j] = [data[i][j]]
        from IPython.display import display

        display(temp)
    else:
        print(
            "That Supply ID is not Present in DataBase...!!!"
        )


# display_specific_data() # Uncomment This Line To Run This Function
def add_new():
    fd = open("data.json", "r")
    txt = fd.read()
    data = json.loads(txt)
    fd.close()
    print("Enter New Supply ID :- ")
    id = input()

    if id not in data.keys():
        print("Enter Supply Name :- ")
        name = input()
        print("Enter Category of Supply :- ")
        category = input()
        print("Enter Quantity of Supply :- ")
        quantity = input()
        print("Enter The Date on Which Supply is Added in Inventory :- ")
        date = input()
        data[id] = {
            "name": name,
            "category": category,
            "quantity": quantity,
            "date": date,
        }
        print(
            "Please Press '0' to Add New Attributes/Properties of Supply or Press '1' to Continue :- "
        )
        z = int(input())
        if z == 0:
            print("Enter Number of New Attributes/Properties of Supply :- ")
            n = int(input())
            for i in range(n):
                print("Enter Attribute Name That you Want To Add :- ")
                nam = input()
                print("Enter The " + str(nam) + " of Supply :- ")
                pro = input()
                data[id][nam] = pro
        print("Supply ID " + str(id) + " Added Successfully...!!!")
    else:
        print(
            "The Supply ID you Have Entered Is Already Present in DataBase...!!!"
        )
    js = json.dumps(data)
    fd = open("data.json", "w")
    fd.write(js)
    fd.close()


# add_new() # Uncomment This Line To Run This Function


def delete_prod():
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


# delete_prod() # Uncomment This Line To Run This Function


def update_prod_data():
    fd = open("data.json", "r")
    txt = fd.read()
    data = json.loads(txt)
    fd.close()
    print(
        "Enter The Supply ID of The Supply Which You Want To Update :- "
    )
    temp = input()

    if temp in data.keys():
        print(
            "To update each supply attribute, enter '0'; For one specific attribute, enter '1' :- "
        )
        q = int(input())

        if q == 0:
            print("Enter Supply Name :- ")
            name = input()
            print("Enter Category of Supply :- ")
            category = input()
            print("Enter Quantity of Supply :- ")
            quantity = input()
            print(
                "Enter the date that the supply was added to the inventory :- "
            )
            date = input()
            data[temp] = {
                "name": name,
                "category": category,
                "quantity": quantity,
                "date": date,
            }
            print(
                "Please Press '0' to Add more Attributes/Properties of Supply or Press '1' to Continue :- "
            )
            z = int(input())

            if z == 0:
                print("Enter Number of New Attributes/Properties of Supply :- ")
                n = int(input())
                for i in range(n):
                    print("Enter Attribute Name That you Want To Add :- ")
                    nam = input()
                    print("Enter The " + str(nam) + " of Supply :- ")
                    pro = input()
                    data[temp][nam] = pro
            print("Supply ID " + str(temp) + " Updated Successfully...!!!")

        elif q == 1:
            print("Enter Which Attribute of Supply You want to Update :- ")
            p = input()

            if p in data[temp].keys():
                print("Enter " + str(p) + " of Supply :- ")
                u = input()
                data[temp][p] = u
                print(
                    "Supply ID "
                    + str(temp)
                    + "'s attribute "
                    + str(p)
                    + " is Updated Successfully...!!!"
                )
            else:
                print("Invalid Supply Attribute...!!!")
        else:
            print("Invalid Choice...!!!")
    else:
        print("Invalid Supply ID...!!!")
    js = json.dumps(data)
    fd = open("data.json", "w")
    fd.write(js)
    fd.close()


# update_prod_data() # Uncomment This Line To Run This Function


def display_reports_overall():
    if os.path.isfile("user_data.json") is False:
        # Check for if file is present or not
        # File will be generated only if any user records usage
        print("No User Reports are Present")
        return
    fd = open("user_data.json", "r")
    txt = fd.read()
    user_data = json.loads(txt)
    fd.close()
    print(
        "Enter '0' to Check All User Reports or '1' To Check the Reports of One Specific User :- "
    )
    n = int(input())
    if n == 1:
        print("Enter User ID Whose Details You Want to Have a Look on")
        i = input()
        temp = pd.DataFrame()
        if i in user_data.keys():
            for j in user_data[i].keys():
                d = dict()
                d["User ID"] = i
                d["Usage Number"] = j
                for k in user_data[i][j].keys():
                    d[k] = user_data[i][j][k]
                temp = temp.append(d, ignore_index=True)
                d = dict()
            temp = temp.reset_index(drop=True)
            from IPython.display import display

            display(temp)
        else:
            print(
                "You Have Entered Wrong User ID that is not Present in DataBase...!!!"
            )
    elif n == 0:
        table = pd.DataFrame()
        for i in user_data.keys():
            temp = pd.DataFrame()
            for j in user_data[i].keys():
                d = dict()
                d["User ID"] = i
                d["Usage Number"] = j
                for k in user_data[i][j].keys():
                    d[k] = user_data[i][j][k]
                temp = temp.append(d, ignore_index=True)
                d = dict()
            table = table.append(temp)
        table = table.reset_index(drop=True)
        from IPython.display import display

        display(table)
    else:
        print("Please Enter Valid Choice...!!!")


# display_reports_overall() # Uncomment This Line To Run This Function


def delete_all():
    fd = open("data.json", "r")
    txt = fd.read()
    data = json.loads(txt)
    fd.close()
    data = {}  # Replacing Data with NULL Dictionary
    js = json.dumps(data)
    fd = open("data.json", "w")
    fd.write(js)
    fd.close()


def user():
    print("======= NASA Hunch Inventory Management System ====")
    while 1:
        print("1)Display all supplies with details")
        print("2)Display certain supply with details")
        print("3)Display all of your previous records")
        print("4)Record usage")
        print("5)Exit")
        print("Enter Your Choice :- ")
        n = int(input())
        if n == 1:
            display_data()
        elif n == 2:
            display_specific_data()
        elif n == 3:
            display_user_data()
        elif n == 4:
            remove_supply()
        elif n == 5:
            break
        else:
            print("Invalid Choice...!!!")


def display_user_data():
    if os.path.isfile("user_data.json") is False:
        print("No User Reports are Present")
        return
    fd = open("user_data.json", "r")
    txt = fd.read()
    user_data = json.loads(txt)
    fd.close()
    print("Enter your User ID to Display All your User Reports :- ")
    i = input()
    temp = pd.DataFrame()

    if i in user_data.keys():
        for j in user_data[i].keys():
            d = dict()
            d["User ID"] = i
            d["Usage Number"] = j
            for k in user_data[i][j].keys():
                d[k] = user_data[i][j][k]
            temp = temp.append(d, ignore_index=True)
            d = dict()
        temp = temp.reset_index(drop=True)
        from IPython.display import display

        display(temp)
    else:
        print("You Have Entered Wrong User ID that is not Present in DataBase...!!!")


def generate_bill(
    user_id, prod_id, time_date, usage_no, name, category, quantity_all, transaction_id
):
    print("========= User Report ========")
    print("#######################")
    print(" User ID :-", user_id)
    print("#################")
    amount = 0
    n = len(usage_no)

    for i in range(n):
        print("-----------------------------------------")
        print(
            "Usage number",
            usage_no[i],
            "\nUsage Time :-",
            time_date[i],
            "\nSupply ID :-",
            prod_id[i],
            "\nName Of Supply :-",
            name[i],
            "\nCategory Of Supply :-",
            category[i],
            "\nUsage Quantity :-",
            quantity_all[i],
        )
        print("-----------------------------------")
    print("*****************************************")
    print("Transaction ID :-", transaction_id)
    print("***************************************")


def remove_supply():
    if os.path.isfile("user_data.json") is False:
        user_data = {}
    else:
        fd = open("user_data.json", "r")
        txt = fd.read()
        user_data = json.loads(txt)
        fd.close()
    fd = open("data.json", "r")
    txt = fd.read()
    data = json.loads(txt)
    fd.close()
    print("Returning users, please enter ID. New users, press 0 :- ")
    p = int(input())
    if p == 0:
        if len(user_data.keys()) == 0:
            user_id = 1000
        else:
            user_id = int(list(user_data.keys())[-1]) + 1
    else:
        if str(p) in user_data.keys():
            user_id = p
        else:
            user_id = -1
    if user_id != -1:
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
        print("Enter Number of Supplies You Want To Update :- ")
        n = int(input())
        print("Enter Data As Follows :- ")
        if user_id not in user_data.keys():
            user_data[user_id] = {}
            g = 0
        else:
            g = int(list(user_data[user_id].keys())[-1]) + 1
        for i in range(n):
            print(
                "Enter Supply ID of Supply " + str(i + 1) + " that you want to update"
            )
            id = input()
            if id in data.keys():
                user_data[user_id][str(i + 1 + g)] = {}
                user_data[user_id][str(i + 1 + g)]["time_date"] = str(time.ctime())
                time_date.append(str(time.ctime()))
                if float(data[id]["quantity"]) == 0.0:
                    print("Supply You Want is Currently Out Of Stock...!!!")
                    continue
                usage_no.append(i + 1 + g)
                name.append(data[id]["name"])
                user_data[user_id][str(i + 1 + g)]["name"] = data[id]["name"]
                prod_id.append(id)
                user_data[user_id][str(i + 1 + g)]["supply_id"] = id
                category.append(data[id]["category"])
                user_data[user_id][str(i + 1 + g)]["category"] = data[id]["category"]
                print(
                    "For Supply "
                    + str(data[id]["name"])
                    + " Available Quantity is :- "
                    + str(data[id]["quantity"])
                )
                print("Enter Quantity of Supply " + str(i + 1) + " that you used")
                quantity = input()
                if float(quantity) <= float(data[id]["quantity"]):
                    data[id]["quantity"] = str(
                        float(data[id]["quantity"]) - float(quantity)
                    )
                    quantity_all.append(quantity)
                    user_data[user_id][str(i + 1 + g)]["quantity"] = str(quantity)
                    user_data[user_id][str(i + 1 + g)]["Transaction ID"] = str(
                        transaction_id
                    )
                else:
                    print(
                        "The quantity entered exceeds the available quantity of the supply"
                    )
                    print(
                        "Enter '0' to use the maximum amount of supply. Enter '1' to skip this supply and move on."
                    )
                    key = int(input())
                    if key == 0:
                        print(
                            "Enter Quantity of Supply "
                            + str(i + 1)
                            + " that you used"
                        )
                        quantity = input()
                        if float(quantity) <= float(data[id]["quantity"]):
                            data[id]["quantity"] = str(
                                float(data[id]["quantity"]) - float(quantity)
                            )
                            quantity_all.append(quantity)
                            user_data[user_id][str(i + 1)]["quantity"] = str(quantity)
                            user_data[user_id][str(i + 1 + g)]["Transaction ID"] = str(
                                transaction_id
                            )
                        else:
                            print("Invalid Operation Got Repeated...!!!")
                    elif key == 1:
                        continue
                    else:
                        print("Invalid Choice...!!!")
            else:
                print("Invalid Supply ID...!!!")
        if len(usage_no) != 0:
            generate_bill(
                user_id,
                prod_id,
                time_date,
                usage_no,
                name,
                category,
                quantity_all,
                transaction_id,
            )
    else:
        print("User ID Doesn't Exists...!!!")
    js = json.dumps(data)
    fd = open("data.json", "w")
    fd.write(js)
    fd.close()
    js = json.dumps(user_data)
    fd = open("user_data.json", "w")
    fd.write(js)
    fd.close()


def main():
    _thread.start_new_thread(server, ())

    while 1:
        print("Choose Any One of The Following :- ")
        print("1)Manage Overall Inventory (Mission Control)")
        print("2)Record Specific Use (Astronauts)")
        print("3)Exit")
        print("Enter Your Choice Here :- ")
        n = int(input())
        if n == 1:
            overall()
        elif n == 2:
            user()
        elif n == 3:
            break
        else:
            print("Invalid Choice...!!!")
