import uuid
import sys
import os
import random
from collections import namedtuple


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def format_ID(ID):
    try:
        return str(int(ID)).zfill(4)
    except TypeError:
        raise ValueError


class BikeObject:
    breakdownChance = 0.4  # we use only the cheapest bikes
    totalTimesRented = 0
    isBroken = False
    isRented = False
    customerID = None
    id = ""
    rentalPrice = 2.13

    def __init__(self):
        self.id = uuid.uuid1()


class CustomerObject:
    name = ""
    customerID = None
    bikesRented = None

    def __init__(self, name):
        if type(name) is not str:
            raise TypeError
        self.name = name
        self.bikesRented = []


class CustomerManagementObject:
    customerDatabase = None
    lastID = 0

    def get_free_ID(self):
        self.lastID += 1
        return format_ID(self.lastID)

    def get_customer_by_ID(self, ID):
        ID = format_ID(ID=ID)
        if ID not in self.customerDatabase.keys():
            raise ValueError
        return self.customerDatabase[ID]

    def register_new_customer(self, name):
        if type(name) is not str:
            raise TypeError
        newCustomer = CustomerObject(name=name)
        newCustomer.customerID = self.get_free_ID()
        self.customerDatabase[newCustomer.customerID] = newCustomer
        return newCustomer.customerID

    def get_all_customer_IDs(self):
        return self.customerDatabase.keys()

    def __init__(self):
        self.customerDatabase = {}


class InventoryManagementObject:
    bikeInventory = None

    def get_all_bikes(self):
        return list(self.bikeInventory.values())

    def get_bike_by_ID(self, bikeID):
        if bikeID not in self.bikeInventory.keys():
            raise ValueError
        return self.bikeInventory[bikeID]

    def get_new_bikes(self, numBikes):
        for i in range(numBikes):
            bike = BikeObject()
            self.bikeInventory[bike.id] = bike

    def get_bike_count(self):
        return len(self.get_all_bikes())

    def get_broken_bike_count(self):
        ret = 0
        for bike in self.get_all_bikes():
            if bike.isBroken and not bike.isRented:
                ret += 1
        return ret

    def get_available_bike_count(self):
        ret = 0
        for bike in self.get_all_bikes():
            if not bike.isBroken and not bike.isRented:
                ret += 1
        return ret

    def fix_broken_bikes(self):
        for bike in self.get_all_bikes():
            if bike.isBroken and not bike.isRented:
                bike.isBroken = False

    def return_bike(self, bikeID):
        bike = self.get_bike_by_ID(bikeID)
        bike.isRented = False
        bike.customerID = None
        bike.totalTimesRented += 1
        if bike.breakdownChance > random.random():
            bike.isBroken = True
            return True
        return False

    def get_bikes_for_customer(self, numBikes, customerID):
        if numBikes > self.get_available_bike_count():
            raise ValueError
        ret = []
        for bike in self.get_all_bikes():
            if not bike.isBroken and not bike.isRented:
                bike.isRented = True
                bike.customerID = customerID
                ret.append(bike.id)
            if len(ret) == numBikes:
                return ret

    def __init__(self, numBikes=0):
        self.bikeInventory = {}
        self.get_new_bikes(numBikes=numBikes)


class GameObject:
    currentDay = 0
    currentFunds = 0
    customers = CustomerManagementObject()
    inventory = InventoryManagementObject()
    repairCost = 2
    rentalCostPerDay = 10
    volumeDiscount = 0.2

    def __init__(self, numBikes=10, startingFunds=10):
        self.inventory.get_new_bikes(numBikes=numBikes)
        self.currentFunds = startingFunds

    def run_customer_registration(self):
        name = input("Enter customer name: ")
        ID = self.customers.register_new_customer(name=name)
        print("Done! Their assigned ID is: {ID}".format(ID=ID))
        input("Press Enter to return to menu.")

    def run_bike_repair(self):
        brokenBikes = self.inventory.get_broken_bike_count()
        if brokenBikes == 0:
            print("No bikes need repairs right now!")
            input("Press Enter to return to menu.")
            return
        totalCost = brokenBikes * self.repairCost
        if totalCost > self.currentFunds:
            print("Not enough funds, you need {need:.2f}, you have {have:.2f}.".format(need=totalCost,
                                                                                       have=self.currentFunds))
        else:
            self.inventory.fix_broken_bikes()
            print("Fixed {num} bikes, paid {paid:.2f}$.".format(num=brokenBikes, paid=totalCost))
        input("Press Enter to return to menu.")

    def run_bike_return(self):
        ID = input("Enter customer ID for the return: ")
        customer = None
        try:
            ID = format_ID(ID=ID)
        except ValueError:
            print("{ID} is not a valid customer ID!".format(ID=ID))
            input("Press Enter to return to menu.")
            return
        try:
            customer = self.customers.get_customer_by_ID(ID=ID)
        except ValueError:
            print("No customer with ID {ID}!".format(ID=ID))
            input("Press Enter to return to menu.")
            return
        if len(customer.bikesRented) == 0:
            print("Customer with ID {ID} has no bikes to return!".format(ID=ID))
            input("Press Enter to return to menu.")
            return
        broken = 0
        returned = 0
        for bikeID in customer.bikesRented:
            if self.inventory.return_bike(bikeID=bikeID):
                broken += 1
            returned += 1
        customer.bikesRented = []
        print("Processed return of {returned} bikes from customer {ID}. {broken} of them are now broken."
              .format(ID=ID, returned=returned, broken=broken))
        input("Press Enter to return to menu.")

    def run_bike_rental(self):
        ID = input("Enter customer ID for the rental: ")
        customer = None
        try:
            ID = format_ID(ID=ID)
        except ValueError:
            print("{ID} is not a valid customer ID!".format(ID=ID))
            input("Press Enter to return to menu.")
            return
        try:
            customer = self.customers.get_customer_by_ID(ID=ID)
        except ValueError:
            print("No customer with ID {ID}!".format(ID=ID))
            input("Press Enter to return to menu.")
            return
        numBikes = input("Enter number of bikes to rent: ")
        try:
            numBikes = int(numBikes)
        except ValueError:
            print("{numBikes} is not a valid number!".format(numBikes=numBikes))
            input("Press Enter to return to menu.")
            return
        if numBikes > self.inventory.get_available_bike_count():
            print("You don't have {numBikes} bikes available!".format(numBikes=numBikes))
            input("Press Enter to return to menu.")
            return
        bikeIDList = self.inventory.get_bikes_for_customer(numBikes=numBikes, customerID=ID)
        customer.bikesRented += bikeIDList
        print("Customer {ID} successfully rented following bikes: ".format(ID=ID))
        price = 0
        for bikeID in bikeIDList:
            print(bikeID)
            price += self.inventory.get_bike_by_ID(bikeID=bikeID).rentalPrice
        self.currentFunds += price
        print("They paid: {price:.2f}$, you now have {currentFunds:.2f}$.".format(price=price,
                                                                                  currentFunds=self.currentFunds))
        input("Press Enter to return to menu.")
        return

    def run_customer_list(self):
        for customerID in self.customers.get_all_customer_IDs():
            print("ID: {customerID}, name: {name}".format(customerID=customerID,
                                                          name=self.customers.get_customer_by_ID(customerID).name))
            for bikeID in self.customers.get_customer_by_ID(customerID).bikesRented:
                print("    {bikeID}".format(bikeID=bikeID))
        input("Press Enter to return to menu.")
        return

    def run_bike_list(self):
        for bike in self.inventory.get_all_bikes():
            status = "available"
            if bike.isBroken:
                status = "broken"
            elif bike.isRented:
                status = "rented to customer with ID {customerID}".format(customerID=bike.customerID)
            print("ID: {bikeID}, status: {status}".format(bikeID=bike.id, status=status))
        input("Press Enter to return to menu.")
        return

    def nextIteration(self):
        self.currentDay += 1
        cls()
        print("Day: {currentDay: >3}, funds: {currentFunds:.2f}$.".format(currentDay=self.currentDay,
                                                                          currentFunds=self.currentFunds))
        print("You currently have {total} bikes in inventory.".format(total=self.inventory.get_bike_count()))
        print("{broken} of them are broken, {available} are available."
              .format(broken=self.inventory.get_broken_bike_count(),
                      available=self.inventory.get_available_bike_count()))
        print("Choose an option:")

        Option = namedtuple("Option", ["text", "handler"])
        menuOptions = [
            Option(text="Exit app", handler=sys.exit),
            Option(text="Register a new customer", handler=self.run_customer_registration),
            Option(text="Fix broken bikes", handler=self.run_bike_repair),
            Option(text="Process a return", handler=self.run_bike_return),
            Option(text="Process a rental", handler=self.run_bike_rental),
            Option(text="List customers", handler=self.run_customer_list),
            Option(text="List owned bikes", handler=self.run_bike_list)
        ]
        for i in range(len(menuOptions)):
            print("{i}: {text}".format(i=i, text=menuOptions[i].text))

        option = input("Enter option number: ")
        try:
            menuOptions[int(option)].handler()
        except ValueError:
            print("Invalid option: {option}".format(option=option))
            input("Press Enter to try again.")
            return


def run_GUI():
    print("Welcome to the ultra-modern bike rental app, please pretend it's 1980 and this is written in COBOL.")
    input("Press Enter to start!")
    game = GameObject()
    while True:
        game.nextIteration()


if __name__ == '__main__':
    run_GUI()