#retail store management system

#importing all required modules
import mysql.connector
from prettytable import PrettyTable
from datetime import datetime
from datetime import date
import random

#establishing a connection with mysql
con=mysql.connector.connect(host='localhost',password='mysql',
                            user='root',database='retailstore')
cursor=con.cursor()

#creating table customer to store info about customers
create1="create table Customer(Name varchar(25) not null, DateOfPurchase date, TotalAmount decimal(10,2), PhoneNo char(10) unique, LuckyDraw char(3))"
cursor.execute(create1)
con.commit()

#creating table storestock to store info about products
create2="create table StoreStock(ProdCode int not null, ProdName varchar(25), Stock int, Price int, Discount int)"
cursor.execute(create2)
con.commit()

#creating table cart which is recurring for each customer
create3="create table Cart(ProdCode int, Prodname varchar(25), Quantity int, Price int, Discount int)"
cursor.execute(create3)
con.commit()
        

#defining a function checkout to produce bill
def checkout():
    #optional lucky draw for customer at checkout
    print("Before checking out would you like to participate in a lucky draw?")
    yn=input("Yes or No: ")

    if yn.lower()=='yes':
        a=random.randint(1,10)
        b=int(input("Enter any number between 1 and 10: "))
        if b==a:
            Flag=True
            print("Congratulations, you recieve 25 rupees off on your order")
        else:
            Flag=False
            print("Better Luck Next time")
    else:
        Flag=False
            
    print('******************************************')

    name=input("Hello, Please Enter your Name: ")
    phone=input("Enter Phone Number: ")

    print('Retail Store Purchase Order Bill')
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

    today = date.today()
    print("Today's date:", today)

    cursor.execute("select*from Cart")
    res=cursor.fetchall()

    #using prettytable for formatting
    table=PrettyTable()
    table.field_names=[desc[0] for desc in cursor.description]
    for j in res:
        table.add_row(j)
    print(table)

    m='select sum(Price) from Cart'
    cursor.execute(m)
    x=cursor.fetchone()[0]
    total=x

    h='select sum(Discount) from Cart'
    cursor.execute(h)
    p=cursor.fetchone()[0]
    discount=p

    #checking for lucky draw results
    if Flag==True:
        grandtot= total-discount-25
    else:
        grandtot= total-discount
 
    #checking the total amount to give extra discounts
    if grandtot<500:
        newtot=grandtot
    elif grandtot>500 and grandtot<1000:
        x=0.025
        newtot=float(grandtot)-(x*float(grandtot))
        print("You recieved an extra 2.5% off your bill")
    elif grandtot>1000 and grandtot<1500:
        x=0.05
        newtot=float(grandtot)-(x*float(grandtot))
        print("You recieved an extra 5% off your bill")
    elif grandtot>1500 and grandtot<2000:
        x=0.075
        newtot=float(grandtot)-(x*float(grandtot))
        print("You recieved an extra 7.5% off your bill")
    elif grandtot>2000:
        x=0.1
        newtot=float(grandtot)-(x*float(grandtot))
        print("You recieved an extra 10% off your bill")
            

    #inserting customer details into table    
    if Flag==True:
        ld="Yes"
        insertt="insert into Customer values(%s,%s,%s,%s,%s)"
        valu=(name, today, newtot, phone, ld)
        cursor.execute(insertt, valu)
        con.commit()
    else:
        ld="No"
        insertt="insert into Customer values(%s,%s,%s,%s,%s)"
        valu=(name, today, newtot, phone, ld)
        cursor.execute(insertt, valu)
        con.commit()
        

    #deleting cart for next customer after bill generation
    dele="delete from cart"
    cursor.execute(dele)
    con.commit()

    print("Total: ", total)
    print("Discount: ", discount)
    print("Grand Total: ", newtot)
    print("Thank you Visit Again...... ")
    print('**************************************')  


#defining a function cart add items
def cart():
    prodname=input("Enter Product Name you would like to add to Cart: ")
    sel="select*from StoreStock where ProdName=%s"

    cursor.execute(sel, (prodname,))
    one=cursor.fetchone()
            
    qtyy=int(input("Enter Quantity you would like to purchase: "))

    #checking for quantity availability
    if qtyy>one[2]:
        print("We Apologize for the Insufficient Stock")

    else:
        price=(one[3])
        dis=(one[4])

        pri=price*qtyy
        disc=dis*qtyy
                
        ins="insert into Cart values(%s,%s,%s,%s,%s)"
        vals=(one[0], one[1], qtyy, pri, disc)
        cursor.execute(ins, vals)
        con.commit()

        quan= one[2] - qtyy
        updss="update StoreStock set Stock=%s where ProdName=%s"
        v=(quan, prodname)
        cursor.execute(updss,v)
        con.commit()

        print("Item Added to Cart")

    print("Option 1: Add more items to the cart")
    print("Option 2: Checkout")
    print("Option 3: Check total discount")

    qu=int(input("Enter Option Number: "))

    if qu==1:
        #calling function cart within itself
        cart()

    elif qu==2:
        #calling functions checkout
        checkout()

    elif qu==3:
        yo="select sum(Discount) from Cart"
        cursor.execute(yo)
        xo=cursor.fetchone()[0]
        disco=xo

        print("You have gotten a discount of ",disco,"so far")

        zo="select sum(Price) from Cart"
        cursor.execute(zo)
        mew=cursor.fetchone()[0]
        prii=mew

        if prii<500:
            wow=500-prii
            print("Shop for ",wow," more and get 2.5% off your bill")
        elif prii>500 and prii<1000:
            wow=1000-prii
            print("Shop for ",wow," more and get 5% off your bill")
        elif prii>1000 and prii<1500:
            wow=1500-prii
            print("Shop for ",wow," more and get 7.5% off your bill")
        elif prii>1500 and prii<2000:
            wow=2000-prii
            print("Shop for ",wow," more and get 10% off your bill")

        print("Option 1: Continue to add items to cart: ")
        print("Option 2: Checkout")

        opt=int(input("Enter Option Number: "))

        if opt==1:
            cart()
        if opt==2:
            checkout()
            
        


#main program loop
while True:

    print("Option 1: Store Employee")
    print("Option 2: Customer")
    print("Option 3: Exit")

    n=int(input("Enter Option Number: "))

    if n==1:
        print("Option 1: Add Stock")
        print("Option 2: Update Stock")
        print("Option 3: Delete Stock")
        print("Option 4: View Customers")

        a=int(input("Enter Option Number: "))

        if a==1:
            cd=int(input("Enter Product Code: "))
            nm=input("Enter Product Name: ")
            qty=int(input("Enter Product Quantity: "))
            price=int(input("Enter Price of Product: "))
            dis=int(input("Enter Discount: "))
            insert="insert into StoreStock values(%s,%s,%s,%s,%s)"
            val=(cd,nm,qty,price,dis)
            cursor.execute(insert, val)
            print("Stock Added")
            con.commit()
            cursor.execute("select*from StoreStock")
            res=cursor.fetchall()

            #using prettytable for formatting
            table=PrettyTable()
            table.field_names=[desc[0] for desc in cursor.description]
            for j in res:
                table.add_row(j)
            print(table)


        if a==2:
            w=input("Enter Column you would like to change: ")
            x=input("Enter Field of Reference: ")
            y=input("Enter Reference Value: ")
            z=input("Enter New Value: ")
            update="update StoreStock set {}=%s where {}=%s".format(w,x)
            cursor.execute(update, (z,y))
            print("Stock Updated")
            con.commit()
            cursor.execute("select*from StoreStock")
            res=cursor.fetchall()

            #using prettytable for formatting
            table=PrettyTable()
            table.field_names=[desc[0] for desc in cursor.description]
            for j in res:
                table.add_row(j)
            print(table)
                
                

        if a==3:
            l=input("Enter reference column: ")
            m=input("Enter reference value: ")
            delete="delete from StoreStock where {}=%s".format(l)
            cursor.execute(delete, (m,))
            print("Record Deleted")
            con.commit()
            cursor.execute("select * from StoreStock")
            z=cursor.fetchall()

            #using prettytable for formatting
            table = PrettyTable()
            table.field_names = [desc[0] for desc in cursor.description]
            for k in z:
                table.add_row(k)
            print(table)



        if a==4:
            sels="select*from Customer"
            cursor.execute(sels)
            m=cursor.fetchall()

            #using pprettytable for formatting
            table=PrettyTable()
            table.field_names = [desc[0] for desc in cursor.description]
            for i in m:
                table.add_row(i)
            print(table)



    if n==2:
        print("Option 1: View Products")
        print("Option 2: View Special Offers")
        print("Option 3: Add Product to Cart & Checkout")

        b=int(input("Enter Option Number: "))

        if b==1:
            select="select*from StoreStock"
            cursor.execute(select)
            result=cursor.fetchall()

            #using prettytable for formatting
            table=PrettyTable()
            table.field_names=[desc[0] for desc in cursor.description]
            for t in result:
                table.add_row(t)
            print(table)

        if b==2:
            print("Welcome to Special Offers")
            
            print("Shop for Rupees 500 or more to get 2.5% off the discounted bill")
            print("Shop for Rupees 1000 or more to get 5% off the discounted bill")
            print("Shop for Rupees 1500 or more to get 7.5% off the discounted bill")
            print("Shop for Rupees 2000 or more to get 10% off the discounted bill")


        if b==3:
            cart()
           

    if n==3:
        break

#end of program.

 
            
           
            
