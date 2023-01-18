#Cashier/inventory management system

import unittest
import sys
from IPython.utils.io import Tee
from contextlib import closing
import ast
import os


class Inventory:
    '''Create inventory class'''
    def __init__(self, inv):
        self.inv = inv

    def getInv(self):
        return self.inv

    def getValues(self, code):
        return [self.inv[code][0], self.inv[code][1]]


    def addItem(self, code, item_name, item_price, file):
        self.inv[int(code)] = [item_name, item_price]
        if file.closed:
            file = open("cashierfile.txt", "a+")
        print()
        with closing(Tee(file, "w", channel="stdout")) as outputstream:
            print("\nItem [",item_name,"] has been added to the inventory!",sep="")
            self.displayItemDetails(int(code))
        file.close()
        return self.inv


    def delItem(self, code, file):
        if file.closed:
            file = open("cashierfile.txt", "a+")
        with closing(Tee(file, "w", channel="stdout")) as outputstream:
            print("Item [",self.inv[code][0],"] has been deleted from the inventory!",sep="")
        del self.inv[code]
        return self.inv
            

    def editItem(self, code, item_name, item_price, file):
        self.inv[code][0] = item_name
        self.inv[code][1] = item_price
        if file.closed:
            file = open("cashierfile.txt", "a+")
        with closing(Tee(file, "w", channel="stdout")) as outputstream:
            print("Item [",self.inv[code][0],"] has been successfully edited!", sep="")
            self.displayItemDetails(int(code))
        return self.inv
    

    def retrieveItemPrice(self, code):
        for key in self.inv:
                if key == code:
                    return int(self.inv[key][1])


    def checkInInv(self, code):
        if code in self.inv:
            return True
        else:
            return False


    def checkNewCode(code, inv):
        while True:
            try:
                value = int(input(code))
            except ValueError:
                print("Sorry, barcodes are only numbers.")
                continue
            if value < 0:
                print("Sorry, there are no negative barcodes.")
                continue
            if Inventory.checkInInv(inv, value):
                print("Sorry, that barcode already exists!")
                continue
            else:
                break
        return value
    

    def checkEditCode(code, inv):
        while True:
            try:
                value = int(input(code))
            except ValueError:
                print("Sorry, barcodes are only numbers.")
                continue
            if not Inventory.checkInInv(inv, value):
                print("Sorry, that barcode doesn't exist!")
                continue
            else:
                break
        return value


    def checkPrice(price, inv):
        while True:
            try:
                value = float(input(price))
            except ValueError:
                print("The price must be a number.")
                continue
            if value < 0:
                print("The price must be positive.")
                continue
            else:
                break
        return value
    

    def displayInv(self):
        print()
        print("{: >45}".format("---Inventory---"))
        print()
        print("{: >20} {: >20} {: >20}".format("Item Name", "Barcode", "Price"))
        print()
        for key in self.inv:
            print("{: >20} {: >20} {: >20}".format(self.inv[key][0], key, ("$"+str(self.inv[key][1]))))
        print()
        

    def displayItemDetails(self, key):
        print()
        print("Item name:", self.inv[key][0])
        print("Barcode:",key)
        print("Price: $", self.inv[key][1],sep="")
        print()

    def writeInv(self, file):
        if file.closed:
            file = open("cashfile.txt", "a+")
        file.write(self.inv)

    def getNewInv(self, file):
        with open('cashierfile.txt', 'r') as f:
            if os.stat("cashierfile.txt").st_size == 0:
                return self.inv
            if os.stat("cashierfile.txt").st_size != 0:
                for line in f:
                    pass
                last_line = line
                self.inv = ast.literal_eval(last_line)

class Cart(Inventory):
    '''Customer shopping cart class'''
    def __init__(self, cart, inv):
        self.cart = cart
        super().__init__(inv)

    
    def scanning(self, code):
        while code != "pay":
            code = int(code)
            self.cart.append(Inventory.getValues(self.inv, code))
            total_price, total_items = self.updateTotals(self.inv, code)
            self.displayCart(total_items, total_price)
            return self.cart
        print("\nThank you for shopping!")
        self.cart = []


    def updateTotals(self, inv, code):
        total_price = 0
        total_items = 0
        for i in range(len(self.cart)):
            price = self.cart[i][1]
            total_price += float(price)
            total_items += 1
        return total_price, total_items

    
    def displayCart(self, total_items, total_price):
        print()
        print("{: >36}".format("---Your Cart---"))
        print()
        print("{: >20} {: >20} ".format("Item", "Price"))
        print()
        for i in range(len(self.cart)):
            print("{: >20} {: >20}".format(self.cart[i][0], ("$"+str(self.cart[i][1]))))
        print("------------------------------------------")
        print("Total price: {: >28}".format("$"+str(round(total_price, 2))))
        print()
        


def stillWorking():
    while True:
        try:
            working = input("Are you still managing the inventory (y/n)? ").lower()
            if working == "y":
                return True
            if working == "n":
                return False
            print("Invalid response")
        except Exception as e:
            pass


def customer(cart, inv):
    scanning = True
    print("\nOur list of items:\n")
    Inventory.displayInv(inv)
    while scanning == True:
        code = input("\nPlease scan an item, or type 'pay' to pay: ")
        checking = True
        isdigit = code.isdigit()
        if isdigit == True:
            code = int(code)
            checker = Cart.checkInInv(inv, code)
        while checking == True:
            if isdigit and checker == True:
                cart.scanning(code)
                checking = False
            elif isdigit and checker == False:
                print("Sorry, that barcode doesn't exist, try again!")
                break
            elif not isdigit and code.lower() == "pay":
                cart.scanning(code)
                checking = False
                scanning = False
            elif not isdigit and code.lower() != "pay":
                print("Barcodes are only numbers, try again!")
                break


def employee(inv, file):
    working = True
    while working == True:
        print("\nPlease input an action to perform:")
        action = input("Add item - 'a'\nRemove item - 'r'\nEdit item - 'e'\nDisplay inventory - 'd'\nDisplay item details - 'i'\nQuit employee menu - 'q'\n")
        if action.lower() == "a":
            code = Inventory.checkNewCode("Please enter a barcode for the new item: ", inv)
            item_name = input("Please input a name for the new item: ").capitalize()
            item_price = Inventory.checkPrice("Please input a price for the new item: ", inv)
            Inventory.addItem(inv, code, item_name, item_price, file)
            working = stillWorking()
        
        if action.lower() == "r":
            code = int(input("\nPlease input the barcode for the item you wish to delete: "))
            Inventory.delItem(inv, code, file)
            working = stillWorking()

        if action.lower() == "e":
            code = Inventory.checkEditCode("\nPlease input the barcode for the item you wish to edit: ", inv)
            item_name = input("Please input a name for the item: ").capitalize()
            item_price = Inventory.checkPrice("Please input a price for the item: ", inv)
            Inventory.editItem(inv, code, item_name, item_price, file)
            working = stillWorking()

        if action.lower() == "d":
            Inventory.displayInv(inv)
            working = stillWorking()

        if action.lower() == "i":
            code = int(input("\nPlease input the barcode for the item you wish to display: "))
            Inventory.displayItemDetails(inv, code)
            working = stillWorking()
        
        if action.lower() == "q":
            print("Leaving employee menu...")
            working = False



def main():

    cashfile = open("cashierfile.txt", "a+")

    inv = Inventory({0:["Boots",34.74],
                1:["T-shirt",12.63],
                2:["Jeans", 25.67],
                3:["Socks", 4.36],
                4:["Flip-flops", 13.99],
                5:["Sweatpants", 22.50],
                6:["Hoodie", 30.15]
                })
    
    inv.getNewInv(cashfile)
    
    cart = Cart([], inv)

    cashfile.write("\n\n------------------------------------------------------------------------------\n")
    cashfile.write("\n--------------------NEW SESSION------------------\n\n")
    running = True
    print("\n\nWelcome to Sam's Attire!\n")
    while running == True:
        person = input("\nAre you a Customer (c) or Employee (e)...\nor enter 'quit' to quit the program: ").lower()
        if person.lower() == "c":
            customer(cart, inv)

        if person.lower() == "e":
            employee(inv, cashfile)
        
        if person.lower() == "quit":
            cashfile = open("cashierfile.txt", "a+")
            lastInv = str(inv.getInv())
            cashfile.write("\n")
            cashfile.write(lastInv)
            cashfile.close()
            running = False
        
        if person.lower() != "quit" and person.lower() != "e" and person.lower() != "c":
            print("\nSorry, that's not an option!")
            

main()

