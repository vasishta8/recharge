#importing necessities
from tkinter import *
from tkinter import messagebox, font, ttk
from datetime import datetime
from PIL import Image, ImageTk
import pyglet
import mysql.connector
import os

#setting up root variables
global sqluser, sqlpass, mydb
while True:
    try:
        sqluser = input("Enter your MySQL username:")
        sqlpass = input("Enter your MySQL password:")
        mydb = mysql.connector.connect(host="localhost", user=sqluser, password=sqlpass)
        mydb.disconnect()
        break
    except Exception as e:
        print("Invalid username or password. Please try again.")
root = Tk()
root.geometry("1280x720")
root.title("Recharge")
ico=Image.open(r"assets\icons\icon.png")
icon = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, icon)
root.configure(background = "black")
pyglet.options['win32_gdi_font'] = True


#importing assets
pyglet.font.add_file(r"assets\fonts\KronaOne-Regular.ttf")
explore_image = PhotoImage(file=r"assets\icons\explore.png")
shop_background = PhotoImage(file=r"assets\backgrounds\shop_background.png")
icon_white = PhotoImage(file=r"assets\icons\icon_white.png")
search_image = PhotoImage(file=r"assets\icons\search.png")
login_background=PhotoImage(file=r"assets\backgrounds\login_background.png")
background = PhotoImage(file=r"assets\backgrounds\background.png")
login_image = PhotoImage(file=r"assets\icons\login.png")
back_image = PhotoImage(file=r"assets\icons\back.png")
signup_image = PhotoImage(file=r"assets\icons\signup.png")
admin_image = PhotoImage(file=r"assets\icons\admin.png")
addtocart_image = PhotoImage(file=r"assets\icons\addtocart.png")
cart_image = PhotoImage(file=r"assets\icons\cart.png")
visa_image = PhotoImage(file=r"assets\icons\visa.png")

#initialising required variables
Brand_List = []
cust_details = []
cart_list = []

#creating the class and functions for phones
def phone_resize(image):
    image = Image.open(image)
    photo_image = ImageTk.PhotoImage(image)
    image = ImageTk.getimage(photo_image)
    imagex, imagey = photo_image.width(), photo_image.height()
    newx, newy = imagex/imagey*432, 432
    image = image.resize((int(newx),int(newy)))
    image = image.convert("RGBA")
    photo_image = ImageTk.PhotoImage(image)
    return photo_image

#creating the function for password visibility
visiblity_check = False
def passee(entry):
    global visiblity_check
    if visiblity_check:
        entry.config(show="*")
        visiblity_check = False
    else:
        entry.config(show="")
        visiblity_check = True

see=Image.open(r"assets\icons\eye.png")
resized=see.resize((25,25))
newsee=ImageTk.PhotoImage(resized)

#creating the database
#module to create database connection and to create tables in mysl for cs project
import mysql.connector

def Create_Database():
    global mydb,c, sqluser, sqlpass
    mydb = mysql.connector.connect(host="localhost", user=sqluser, password=sqlpass)
    c = mydb.cursor()
    c.execute('SHOW DATABASES')
    i = ('rechargemobiles',)
    databases=c.fetchall()
    if i in databases:
        c.execute('USE rechargemobiles')
    else:
        c.execute('CREATE DATABASE rechargemobiles')
        c.execute('USE rechargemobiles')

def Create_Tables():
    global mydb,c,check
    check=[False,False,False]
    c.execute('SHOW TABLES')
    tables=c.fetchall()
    table_list=[('admin',), ('customer',), ('dealer',), ('purchaselog',), ('stock',)]
    if tables!=table_list:
        #creating tables
        c.execute("CREATE TABLE Dealer( DealerID char(5) primary key, DealerName varchar(50) not null, DealerAddress varchar(150), DealerNumber char(10), DealerBrand varchar(30) not null);")
        c.execute("CREATE TABLE Stock(PhoneID char(5), PhoneModel varchar(40), DealerID char(5) not null, PhoneCP double(8,2) not null, PhoneSP double(8,2) not null, PhoneManufacturer varchar(30), PhoneCountry varchar(30), PhoneWeight int(3), PhoneGen varchar(20), PhoneOS varchar(20), PhoneScreen varchar(20), PhoneRAM varchar(8), PhoneROM varchar(8), PhoneDimensions varchar(40), PhoneColour varchar(15), PhoneEssentials varchar(150), PhoneCount int(2) not null, PhoneImage varchar(150));")            
        c.execute("CREATE TABLE Customer(CustomerID char(5) primary key, CustomerEmail varchar(50), CustomerPassword varchar(16) not null, CustomerName varchar(30) not null, CustomerAddress varchar(150), CustomerNumber char(10), Totalamountspent double(9,2));")
        c.execute("CREATE TABLE Admin(AdminID char(5) primary key, AdminPassword varchar(16) not null, AdminName varchar(30) not null);")
        c.execute("CREATE TABLE PurchaseLog(PurchaseID char(5) primary key, OrderID char(5) NOT NULL, PurchaseDate date, PhoneID char(5) not null, PhoneModel varchar(40), CustomerID char(5) not null, DealerID char(5) not null, PaymentMode varchar(30), PurchaseProfit double(8,2));")
        #adding keys
        c.execute("ALTER TABLE Stock ADD PRIMARY KEY (PhoneID, Phonemodel);")
        c.execute("ALTER TABLE Stock ADD FOREIGN KEY (DealerID) REFERENCES Dealer(DealerID);")
        c.execute("ALTER TABLE PurchaseLog ADD FOREIGN KEY (DealerID) REFERENCES Dealer(DealerID);")
        #inserting values
        #dealer
        c.execute("INSERT INTO Dealer(DealerID, DealerName, DealerAddress, DealerNumber, DealerBrand) VALUES('DI101', 'Savitri Mobiles','Kalbadevi, Mumbai','9345765362','Xiaomi');")
        c.execute("INSERT INTO Dealer(DealerID, DealerName, DealerAddress, DealerNumber, DealerBrand) VALUES('DI102', 'Infrix Technologies', 'Okhla Industrial Area, New Delhi','9964823461', 'OnePlus');")
        c.execute("INSERT INTO Dealer(DealerID, DealerName, DealerAddress, DealerNumber, DealerBrand) VALUES('DI103', 'Incezzance Pvt Ltd', 'Secunderabad, Hyderabad', '6789686372', 'Samsung');")
        c.execute("INSERT INTO Dealer(DealerID, DealerName, DealerAddress, DealerNumber, DealerBrand) VALUES('DI104', 'Fujitas Mobiles Ltd', 'Chembur, Mumbai', '9940257346', 'Huawei');")
        c.execute("INSERT INTO Dealer(DealerID, DealerName, DealerAddress, DealerNumber, DealerBrand) VALUES('DI105', 'Frixion Technologies', 'Jasola Vihar, New Delhi', '9375936534', 'Apple');")
        c.execute("INSERT INTO Dealer(DealerID, DealerName, DealerAddress, DealerNumber, DealerBrand) VALUES('DI106', 'Jashant Mobiles', 'Patel Nagar, Gurgaon', '9056464542', 'Google');")
        c.execute("INSERT INTO Dealer(DealerID, DealerName, DealerAddress, DealerNumber, DealerBrand) VALUES('DI107', 'Finnora Pvt Ltd', 'Seagehalli, Bengaluru', '6787543654', 'Oppo');")
        c.execute("INSERT INTO Dealer(DealerID, DealerName, DealerAddress, DealerNumber, DealerBrand) VALUES('DI108', 'Fonezone Mobiles', 'Sowcarpet, Chennai','7856543421', 'LG');")
        c.execute("INSERT INTO Dealer(DealerID, DealerName, DealerAddress, DealerNumber, DealerBrand) VALUES('DI109', 'Parvat Technologies', 'Nimak Mandi, Amritsar', '9970987657', 'Vivo');")
        c.execute("INSERT INTO Dealer(DealerID, DealerName, DealerAddress, DealerNumber, DealerBrand) VALUES('DI110', 'Jazzato Pvt Ltd', 'Nungambakkam, Chennai', '6383786452', 'Nokia'); ")
        #admin
        c.execute("INSERT INTO Admin(AdminID, AdminPassword, AdminName) VALUES('AI101', 'CSProject1','Aashrith');")
        c.execute("INSERT INTO Admin(AdminID, AdminPassword, AdminName) VALUES('AI102', 'CSProject2', 'Vasishta');")
        c.execute("INSERT INTO Admin(AdminID, AdminPassword, AdminName) VALUES('AI103', 'CSProject3', 'Pranav');")
        #customer (dummy customers for immediate use of login functionality)
        c.execute("INSERT INTO Customer(CustomerID, CustomerEmail, CustomerPassword, CustomerName, CustomerAddress, CustomerNumber, Totalamountspent) VALUES('CI101', 'adam@gmail.com', 'pass101', 'Adam', 'No.24, Ramapuram, Chennai', '9864753652', 0.00);")
        c.execute("INSERT INTO Customer(CustomerID, CustomerEmail, CustomerPassword, CustomerName, CustomerAddress, CustomerNumber, Totalamountspent) VALUES('CI102', 'babu@gmail.com', 'pass102', 'Babu', 'No.12, R.A. Puram, Chennai', '9076368233',0.00);")
        c.execute("INSERT INTO Customer(CustomerID, CustomerEmail, CustomerPassword, CustomerName, CustomerAddress, CustomerNumber, Totalamountspent) VALUES('CI103', 'chris@gmail.com', 'pass103', 'Chris', 'No/09, Vinay Vihar, New Delhi', '9084863746',0.00);") 
        #stock (may be modified)
        c.execute("INSERT INTO Stock(PhoneID, PhoneModel, DealerID,PhoneCP,PhoneSP,PhoneManufacturer,PhoneCountry,PhoneWeight,PhoneGen,PhoneOS,PhoneScreen,PhoneRAM,PhoneROM,PhoneDimensions,PhoneColour,PhoneEssentials,PhoneCount,PhoneImage) VALUES('PI101', 'Redmi Note 11T 5G', 'DI101', 15999.00, 17999.00, 'Xiaomi', 'China', 195, '5G', 'Andriod 11', 'Super AMOLED', '8GB', '128GB', '163.6 x 75.8 x 8.8 mm', 'Teal', '50MP Front Camera, 90hz display, in-display fingerprint sensor', 05, 'assets/phones/pi101.png');")
        c.execute("INSERT INTO Stock(PhoneID, PhoneModel, DealerID,PhoneCP,PhoneSP,PhoneManufacturer,PhoneCountry,PhoneWeight,PhoneGen,PhoneOS,PhoneScreen,PhoneRAM,PhoneROM,PhoneDimensions,PhoneColour,PhoneEssentials,PhoneCount,PhoneImage) VALUES('PI102', 'OnePlus Nord CE 5G', 'DI102', 22999.00, 24999.00, 'OnePlus','China', 170, '5G', 'Android 11', 'Fluid AMOLED', '12GB', '256GB', '159.2 x 73.5 x 7.9 mm', 'Grey', '64 MP Front Camera, 90hz display, in display fingerprint sensor', 03, 'assets/phones/pi102.png');")
        c.execute("INSERT INTO Stock(PhoneID, PhoneModel, DealerID,PhoneCP,PhoneSP,PhoneManufacturer,PhoneCountry,PhoneWeight,PhoneGen,PhoneOS,PhoneScreen,PhoneRAM,PhoneROM,PhoneDimensions,PhoneColour,PhoneEssentials,PhoneCount,PhoneImage) VALUES('PI103', 'Samsung Galaxy A22 5G', 'DI103', 15999.00, 17499.00, 'Samsung', 'South Korea', 203, '5G', 'Android 11', 'TFT', '8GB', '128GB', '167.2 x 76.4 x 9 mm', 'Mint Green', '48MP Front Camera, 90hz display, side-mounted fingerprint sensor', 04, 'assets/phones/pi103.png');")
        c.execute("INSERT INTO Stock(PhoneID, PhoneModel, DealerID,PhoneCP,PhoneSP,PhoneManufacturer,PhoneCountry,PhoneWeight,PhoneGen,PhoneOS,PhoneScreen,PhoneRAM,PhoneROM,PhoneDimensions,PhoneColour,PhoneEssentials,PhoneCount,PhoneImage) VALUES('PI104', 'VIVO V23 5G', 'DI109', 29999.00, 32999.00, 'Vivo', 'China', 179, '5G', 'Android 12', 'AMOLED', '12GB', '256GB', '157.2 x 72.4 x 7.6 mm', 'Rose Gold', '64MP Front Camera, 90hz display, optical fingerprint sensor', 02, 'assets/phones/pi104.png');")
        c.execute("INSERT INTO Stock(PhoneID, PhoneModel, DealerID,PhoneCP,PhoneSP,PhoneManufacturer,PhoneCountry,PhoneWeight,PhoneGen,PhoneOS,PhoneScreen,PhoneRAM,PhoneROM,PhoneDimensions,PhoneColour,PhoneEssentials,PhoneCount,PhoneImage) VALUES('PI105', 'Apple iPhone 13 5G', 'DI105', 74999.00, 79999.00, 'Apple', 'USA', 174, '5G', 'IOS 15', 'Super retina OLED', '4GB', '512GB', '146.7 x 71.5 x 7.7 mm', 'Turqoise Blue', '12MP Front Camera with OIS, 120hz display, optical fingerprint sensor', 03, 'assets/phones/pi105.png');")
        c.execute("INSERT INTO Stock(PhoneID, PhoneModel, DealerID,PhoneCP,PhoneSP,PhoneManufacturer,PhoneCountry,PhoneWeight,PhoneGen,PhoneOS,PhoneScreen,PhoneRAM,PhoneROM,PhoneDimensions,PhoneColour,PhoneEssentials,PhoneCount,PhoneImage) VALUES('PI106', 'Samsung Galaxy S22 Ultra 5G', 'DI103', 69999.00, 73999.00, 'Samsung', 'South Korea', 229, '5G', 'Android 12', 'Dynamic AMOLED', '12GB', '1TB', '163.3 x 77.9 x 8.9 mm', 'Burgundy', '108MP Front Camera, 120hz display, ultrasonic fingerprint sensor', 02, 'assets/phones/pi106.png');")
        c.execute("INSERT INTO Stock(PhoneID, PhoneModel, DealerID,PhoneCP,PhoneSP,PhoneManufacturer,PhoneCountry,PhoneWeight,PhoneGen,PhoneOS,PhoneScreen,PhoneRAM,PhoneROM,PhoneDimensions,PhoneColour,PhoneEssentials,PhoneCount,PhoneImage) VALUES('PI107', 'Apple iPhone SE', 'DI105', 39999.00, 42999.00, 'Apple', 'USA', 148, '5G', 'IOS 13', 'Retina IPS LCD', '3GB', '256GB', '138.4 x 67.3 x 7.3 mm', 'Red', '12MP Front Camera with OIS, 60hz display, front-mounted fingerprint sensor', 08, 'assets/phones/pi107.png');")
        c.execute("INSERT INTO Stock(PhoneID, PhoneModel, DealerID,PhoneCP,PhoneSP,PhoneManufacturer,PhoneCountry,PhoneWeight,PhoneGen,PhoneOS,PhoneScreen,PhoneRAM,PhoneROM,PhoneDimensions,PhoneColour,PhoneEssentials,PhoneCount,PhoneImage) VALUES('PI108', 'Huawei Nova 9', 'DI104', 29999.00, 35999.00, 'Huawei', 'China', 175, '5G', 'HarmonyOS 2.0', 'OLED', '8GB', '256GB', '160 x 73.7 x 7.8 mm', 'Starry Blue', '50MP Front Camera, 120hz display, in-display fingerprint sensor', 02, 'assets/phones/pi108.png');")
        c.execute("INSERT INTO Stock(PhoneID, PhoneModel, DealerID,PhoneCP,PhoneSP,PhoneManufacturer,PhoneCountry,PhoneWeight,PhoneGen,PhoneOS,PhoneScreen,PhoneRAM,PhoneROM,PhoneDimensions,PhoneColour,PhoneEssentials,PhoneCount,PhoneImage) VALUES('PI109', 'Oppo A76', 'DI107', 23999.00, 26999.0, 'Oppo', 'China', 189 , '5G', 'Android 11', 'IPS LCD', '6GB', '128GB', '164.4 x 75.7 x 8.4 mm', 'Glowing Blue', '13MP Front Camera, 90hz display, in-display fingerprint sensor', 03, 'assets/phones/pi109.png');")
        c.execute("INSERT INTO Stock(PhoneID, PhoneModel, DealerID,PhoneCP,PhoneSP,PhoneManufacturer,PhoneCountry,PhoneWeight,PhoneGen,PhoneOS,PhoneScreen,PhoneRAM,PhoneROM,PhoneDimensions,PhoneColour,PhoneEssentials,PhoneCount,PhoneImage) VALUES('PI110', 'Nokia G20', 'DI110', 16999.00, 18999.00, 'Nokia', 'Finland', 190, '5G', 'Android 11', 'IPS LCD', '4GB', '128GB', '164.6 x 75.9 x 8.5 mm', 'Dark Blue', '50MP Front Camera, 90hz display, side-mounted fingerprint sensor', 04, 'assets/phones/pi110.png');")
        mydb.commit()
    global instanceStock
    instanceStock = {}
    c.execute("SELECT PhoneID, PhoneCount FROM stock;")
    curstock = c.fetchall()
    for item in curstock:
        instanceStock[item[0]] = item[1]

def Delete_Database(p):
    global mydb,c, sqluser, sqlpass
    mydb = mysql.connector.connect(host="localhost", user=sqluser, password=sqlpass)
    c = mydb.cursor()
    if p==False:
        c.execute("DROP DATABASE rechargemobiles")
        return True
    else:
        return True

Create_Database()
Create_Tables()

#creating a class for the phones
class Phone:

    def __init__(self, details):
        #name, image, price, manufacturer, country, weight, gen, dimensions, screen, ram, rom, colour, stock
        self.details = details
        self.name = details[0]
        self.image = phone_resize(details[1])
        self.price = details[2]
        self.manufacturer = details[3]
        self.country = details[4]
        self.weight = details[5]
        self.gen = details[6]
        self.dimensions = details[7]
        self.screen = details[8]
        self.ram = details[9]
        self.rom = details[10]
        self.colour = details[11]
        self.essentials = details[12]
        self.stock = details[13]
        self.id = details[14]
        self.width = self.image.width()
        self.height = self.image.height()
        self.specs = self.manufacturer+"\n"+self.country+"\n"+str(self.weight)+" gm\n"+self.gen+"\n"+self.dimensions+"\n"+self.screen+"\n"+self.ram+" RAM\n"+self.rom+" Storage\n"+self.colour

    def forget_frame(self):
        self.frame.pack_forget()
        shop_frame.pack(expand=TRUE, fill=BOTH)

    def place_frame(self):
        self.frame = Frame(root, width=1280, height=720)
        self.frame.pack(side=LEFT, fill=BOTH, expand=YES)
        self.canvas = Canvas(self.frame, width=1280, height=720, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=YES)
        self.canvas.create_image(0,0, image=background, anchor=NW)
        self.canvas.create_image(128,144,image=self.image, anchor=NW)
        self.canvas.create_text(160+self.width, 180, text=self.name+"\n₹"+str(self.price)+"0", fill="white", font=("Krona One", 25), anchor=NW)
        self.canvas.create_text(160+self.width, 290, text=self.specs, fill="white", font=("Krona One", 15), anchor=NW)
        essentials_list = self.essentials.split(", ")
        delimiter = "\n"
        self.essentials = delimiter.join(essentials_list)
        self.canvas.create_text(825, 290, text=self.essentials, fill="white", font=("Krona One", 15), anchor=NW)
        if self.stock > 0:
            Button(self.canvas, fg="#ffffff", bg="black", text="ADD TO CART", font=("Krona One", 15), image=cart_image, compound="left", bd=0, command=lambda:self.add_to_cart()).place(relx=0.4, rely=0.85, relwidth=0.2, relheight=0.1)
        else:
            self.canvas.create_text(512, 630, text="OUT OF STOCK", fill="white", font=("Krona One", 15), anchor="nw")
        Button(self.canvas, image=back_image, bg="black", bd=0, highlightthickness=0, command=lambda:self.forget_frame()).place(relx=0.93375, rely=0.02, relwidth=0.05625, relheight=0.1)
#relx=0.4, rely=0.85
    def add_to_cart(self):
        global cart_list
        if (instanceStock[self.id] > 0):
            cart_list.append([self.name, self.price, self.image, self.id])
            instanceStock[self.id] -= 1
            self.forget_frame()
            messagebox.showinfo("Recharge", self.name+" has been added to your cart!")
        else:
            self.forget_frame()
            messagebox.showinfo("Recharge", self.name+" was not added to your cart, as there is not enough stock for your purchase needs.")

#function for general usage
def General_Data(usage,*fields):
    global cust_details,sqluser, sqlpass
    dbo=mysql.connector.connect(host="localhost", user=sqluser, password=sqlpass, database='rechargemobiles')
    c=dbo.cursor()
    if usage== 'Login':
        #fields = [Email, Password]
        values= [fields[0],fields[1]]
        c.execute("SELECT CustomerEmail, CustomerPassword, CustomerID, CustomerName, CustomerNumber, CustomerAddress, TotalAmountSpent FROM Customer;")
        details = c.fetchall()
        for data in details:
            if data[0] == values[0].lower() and data[1] == values[1]:
                messagebox.showinfo("Recharge", "Login successful!")
                login_email_entry.delete(0, END)
                login_password_entry.delete(0, END)
                cust_details = data[3:4]+data[0:1]+data[4:6]+data[2:3]
                login_frame.pack_forget()
                shop_frame.pack(fill=BOTH, expand=TRUE)
                return
        messagebox.showerror("Recharge", "Incorrect email or password, login failed.")
        return 

    elif usage=='Signup':
        #fields = [Name, Email, MobileNumber, Address, Password, ConfirmPassword]
        c.execute('SELECT CustomerID FROM Customer;')
        Customers = c.fetchall()
        n = len(Customers) + 1
        emailCheck = True
        CustomerID = 'CI' + str(100+n)
        TotalAmountSpent = 0
        values=[CustomerID,fields[0],fields[1],fields[2],fields[3],fields[4],TotalAmountSpent]
        c.execute('SELECT CustomerEmail FROM Customer;')
        Emails = c.fetchall()
        for Email in Emails:
            if (fields[1],) == Email:
                emailCheck = False
                break
        if fields[4] == fields[5] and fields[2].isnumeric() and len(fields[2]) == 10 and (fields[0].replace(" ", "")).isalpha() and emailCheck:
            sqlcommand = "INSERT INTO Customer(CustomerID, CustomerName, CustomerEmail, CustomerNumber, CustomerAddress, CustomerPassword, TotalAmountSpent) VALUES(%s, %s, Lower(%s), %s, %s, %s, %s);"            
            try:
                c.execute(sqlcommand,values)
                dbo.commit()
                messagebox.showinfo("Recharge", "Signup successful! Welcome to Recharge!")
                signup_name_entry.delete(0, END)
                signup_email_entry.delete(0, END)
                signup_phone_entry.delete(0, END)
                signup_address_entry.delete(0, END)
                signup_password_entry.delete(0, END)
                signup_passwordconfirm_entry.delete(0, END)
                cust_details = values[1:5]
                cust_details.append(CustomerID)
                signup_frame.pack_forget()
                shop_frame.pack(fill=BOTH, expand=TRUE)
                return
            except:
                dbo.rollback()
                messagebox.showerror("Recharge", "Signup failed, recheck the credentials.")
                return
        else:

            messagebox.showerror("Recharge", "Signup failed, recheck the credentials.")
            return 

    elif usage=='PhoneDetails':
        #fields = PhoneID
        values = (fields[0],)
        c.execute('SELECT PhoneID FROM Stock;')
        phones = c.fetchall()
        for phone in phones:
            if phone ==  values:
                try:
                    sqlcommand = "SELECT * FROM Stock WHERE PhoneID = %s;"
                    c.execute(sqlcommand,values)
                    dbo.commit()
                    commandcheck = True
                    phones = c.fetchone()
                    details = list(phones)
                    #details = [PhoneID, PhoneModel, DealerID, PhoneCP, PhoneSP, PhoneManufacturer, PhoneCountry, PhoneWeight, PhoneGen, PhoneOS, PhoneScreen, PhoneRAM, PhoneROM, PhoneDimensions, PhoneColour, PhoneEssentials, PhoneCount]
                    return commandcheck, details
                except:
                    dbo.rollback()
                    commandcheck = False
                    return commandcheck
            else:
                check = False
        if check == False:
            display_text = 'Phone Does Not Exist'
            return check, display_text

    elif usage == "PhoneDiff":
            c.execute('SELECT PhoneModel, PhoneImage, PhoneSP, PhoneID FROM Stock;')
            phones = c.fetchall()
            return phones

    elif usage == "PhoneClick":
        global phone_list, phone_details, click_check
        phone_id = phone_list[fields[0]][3]
        c.execute('SELECT PhoneID, PhoneModel, PhoneImage, PhoneSP, PhoneManufacturer, PhoneCountry, PhoneWeight, PhoneGen, PhoneDimensions, PhoneScreen, PhoneRAM, PhoneROM, PhoneColour, PhoneEssentials, PhoneCount from STOCK;')
        phones = c.fetchall()
        for phone in phones:
            if phone[0] == phone_id:
                phone_details = phone[1:len(phone)]+phone[0:1]
        shop_frame.pack_forget()
        global phone_clicked
        phone_clicked = Phone(list(phone_details))
        phone_clicked.place_frame()
    c.close()
    dbo.close()

#function for the admin portal
def Admin(usage, *fields):
    global sqluser, sqlpass
    import mysql.connector
    dbo=mysql.connector.connect(host="localhost", user=sqluser, password=sqlpass, database='rechargemobiles')
    c=dbo.cursor()
    global Capital, Brand_List
    if usage=='Admin Login':
        #fields = [AdminID, AdminPassword]
        values= [fields[0],fields[1]]
        c.execute("SELECT AdminID, AdminPassword FROM Admin;")
        details = c.fetchall()
        for data in details:
            if data[0] == values[0] and data[1] == values[1]:
                login=True
                return login
            else:
                login=False
                display_text= "Admin ID or Password, please input again"
                return login,display_text

    elif usage == 'Add Admin':
        #using confirm password for this as well, it's there in fields[3]
        # fields = [AdminPassword, AdminName, Confirm_Password]
        c.execute('SELECT AdminID FROM Admin')
        details = c.fetchall()
        n = len(details) + 1
        AdminID = 'AI' + str(100+n)
        values = (AdminID, fields[0], fields[1])
        if fields[0] == fields[2]:
            sqlcommand = 'INSERT INTO Admin(AdminID, AdminPassword, AdminName) VALUES(%s,%s,%s);'
            try:
                c.execute(sqlcommand,values)
                dbo.commit()
                commandcheck = True
                return commandcheck, AdminID
            except:
                dbo.rollback()
                commandcheck = False
                return commandcheck
        else:
            check = False
            display_text = "Entered and Confirmed passwords don't match"
            return check, display_text
            
    elif usage == 'Remove Admin':
        #fields = AdminID
        values = (fields[0],)
        c.execute('SELECT AdminID FROM Admin;')
        details = c.fetchall()
        rows = c.rowcount
        for admin in details:
            if admin == values:
                try:
                    sqlcommand = 'DELETE FROM Admin WHERE AdminID = %s;'
                    c.execute(sqlcommand,values)
                    dbo.commit()
                    commandcheck = True
                    return commandcheck
                except:
                    dbo.rollback()
                    commandcheck = False
                    return commandcheck
            else:
                check = False
        if check ==  False:
            display_text = 'AdminID entered does not exist'
            return check, display_text

    elif usage == 'View Admins':
        #display admin names and IDs only, no extra values in Fields
        #returned in a list to be displayed on output text box or labels
        c.execute('SELECT AdminName,AdminID FROM Admin;')
        rows = c.rowcount
        if rows != 0:
            details = c.fetchall()
            check = True
            #details is a list of tuples each of which contain AdminName and AdminID from each row
            return check, details
        else:
            display_text = 'No admins, kindly remodify code to add atleast one admin'
            check = False
            return check, display_text

    elif usage == 'View PurchaseLog':
        c.execute('SELECT * FROM purchaselog;')
        details = c.fetchall()
        if len(details) != 0:
            check = True
            return check, details
        else:
            display_text = 'Purchase Log Empty'
            check = False
            return check, display_text

    # elif usage == 'View Customer Details':
    #     c.execute('SELECT * FROM Customer;')
    #     rows = c.rowcount
    #     if rows != 0:
    #         details = c.fetchall()
    #         check = True
    #         return check, details
    #     else:
    #         display_text = 'No Customers'
    #         check = False
    #         return check, display_text

    # elif usage == 'View Dealer Details':
    #     c.execute('SELECT * FROM Dealer;')
    #     rows = c.rowcount
    #     if rows != 0:
    #         details = c.fetchall()
    #         check = True
    #         return check, details
    #     else:
    #         display_text = 'No Dealers'
    #         check = False
    #         return check, display_text
        
    # elif usage == 'View Stock':
    #     c.execute('SELECT * FROM Stock;')
    #     rows = c.rowcount
    #     if rows != 0:
    #         details = c.fetchall()
    #         check = True
    #         return check, details
    #     else:
    #         display_text = 'Stock Empty'
    #         check = False
    #         return check, display_text

    elif usage == 'Add Dealer':
        # fields = [DealerName, DealerAddress, DealerNumber, DealerBrand]
        c.execute('SELECT DealerID FROM Dealer;')
        details  =  c.fetchall()
        n = len(details) + 1
        DealerID = 'DI' + str(100+n)
        values = (DealerID, fields[0], fields[1], fields[2], fields[3])
        try:
            sqlcommand = 'INSERT INTO Dealer(DealerID, DealerName, DealerAddress, DealerNumber, DealerBrand) VALUES(%s, %s, %s, %s, %s);'
            c.execute(sqlcommand, values)
            dbo.commit()
            Brand_List.append(values[4])
            commandcheck  = True
            return commandcheck, DealerID
        except:
            dbo.rollback()
            commandcheck = False
            return commandcheck

    elif usage == 'Remove Customer':
        #fields = CustomerID
        values = (fields[0],)
        c.execute('SELECT CustomerID FROM Customer;')
        details = c.fetchall()
        for customer in details:
            if customer == values:
                try:
                    sqlcommand = 'DELETE FROM Customer WHERE CustomerID = %s;'
                    c.execute(sqlcommand,values)
                    dbo.commit()
                    commandcheck = True
                    return commandcheck
                except Exception as e:
                    dbo.rollback()
                    commandcheck = False
                    return commandcheck
            else:
                check = False
        if check == False:
            display_text = 'CustomerID entered does not exist'
            return check, display_text

    elif usage == 'Add Phonecount':
        #fields = [PhoneID, No of phones added]
        values = (fields[0],)
        c.execute('SELECT PhoneID FROM Stock;')
        details = c.fetchall()
        for phone in details:
            if phone == values:
                try:
                    value = (fields[1],fields[0])
                    sqlcommand = 'UPDATE Stock SET PhoneCount = (PhoneCount + %s) WHERE PhoneID = %s;'
                    c.execute(sqlcommand,value)
                    dbo.commit()
                    value = (fields[0],)
                    sqlcommand = 'SELECT PhoneCount, PhoneCP FROM Stock WHERE PhoneID = %s;'
                    c.execute(sqlcommand,value)
                    details = c.fetchone()
                    Capital-= int(details[1])
                    commandcheck = True
                    return commandcheck
                except:
                    dbo.rollback()
                    commandcheck = False
                    return commandcheck
            else:
                check = False
        if check == False:
            display_text = 'Phone not found'
            return check, display_text

    elif usage == 'Modify Selling Price':
        #fields = [PhoneID, NewPhoneSP]
        values = (fields[1], fields[0])
        c.execute('SELECT PhoneID FROM Stock;')
        phones = c.fetchall()
        for phone in phones:
            if phone == (values[1],):
                try:
                    sqlcommand = 'UPDATE Stock SET PhoneSP = %s WHERE PhoneID = %s;'
                    c.execute(sqlcommand,values)
                    dbo.commit()
                    commandcheck = True
                    return commandcheck
                except:
                    dbo.rollback()
                    commandcheck = False
                    return commandcheck
            else:
                check = False
        if check == False:
            display_text = 'PhoneID entered does not exist'
            return check, display_text

    elif usage == 'Add New Model':
        #fields = [PhoneModel, DealerID, PhoneCP, PhoneSP, PhoneManufacturer, PhoneCountry, PhoneWeight, PhoneGen, PhoneOS, PhoneScreen, PhoneRAM, PhoneROM, PhoneDimensions, PhoneColour, PhoneEssentials, PhoneCount, PhoneImage]
        c.execute('SELECT PhoneID FROM Stock;')
        phones = c.fetchall()
        n = len(phones) + 1
        PhoneID = 'PI' + str(100+n)
        values = (PhoneID, fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6], fields[7], fields[8], fields[9], fields[10], fields[11], fields[12], fields[13], fields[14], fields[15], fields[16])  
        try:
            sqlcommand = 'INSERT INTO Stock(PhoneID, PhoneModel, DealerID,PhoneCP,PhoneSP,PhoneManufacturer,PhoneCountry,PhoneWeight,PhoneGen,PhoneOS,PhoneScreen,PhoneRAM,PhoneROM,PhoneDimensions,PhoneColour,PhoneEssentials,PhoneCount, PhoneImage) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
            c.execute(sqlcommand,values)
            dbo.commit()
            commandcheck = True
            return commandcheck, PhoneID
        except Exception as e:
            dbo.rollback()
            commandcheck = False
            return commandcheck
            
    elif usage == 'Remove Model':
        #fields = PhoneID
        values  = (fields[0],)
        c.execute('SELECT PhoneID FROM Stock;')
        phones = c.fetchall()
        for phone in phones:
            if phone == values:
                try:
                    sqlcommand = 'DELETE FROM Stock WHERE PhoneID = %s;'
                    c.execute(sqlcommand,values)
                    dbo.commit()
                    commandcheck = True
                    return commandcheck
                except:
                    dbo.rollback()
                    commandcheck = False
                    return commandcheck
            else:
                check = False
        if check == False:
            display_text = 'PhoneID entered does not exist'
            return check, display_text
    c.close()
    dbo.close()

#function to destroy and create the checkout page on updating 
def checkoutFrame_Create():
    global checkout_frame, cart_list, cust_details, v, search_entry
    def checkout_visa():
        Label(checkout_frame, text="You shall be redirected shortly to the VISA checkout gateway.", font=("Krona One", 9), fg="white", bg="black").place(relx=0.5, rely=0.6, relwidth=0.4, relheight=0.1)
    def checkout_cod():
        Label(checkout_frame, text="₹"+str(cost)+"0 should be paid on delivery by cash.", font=("Krona One", 10), fg="white", bg="black").place(relx=0.5, rely=0.6, relwidth=0.4, relheight=0.1)
    def checkout_netbank():
        Label(checkout_frame, text="You shall be redirected shortly to the netbanking gateway.", font=("Krona One", 10), fg="white", bg="black").place(relx=0.5, rely=0.6, relwidth=0.4, relheight=0.1)    
    def checkout_card():
        Label(checkout_frame, text="You shall be redirected shortly to the card payment gateway.", font=("Krona One", 9), fg="white", bg="black").place(relx=0.5, rely=0.6, relwidth=0.4, relheight=0.1)
    def checkout_end():
        global cust_details, cart_list, v, search_entry
        if v.get() == "1":
            messagebox.showerror("Recharge", "Purchase Failed, please choose a method of transaction.")
        else:
            messagebox.showinfo("Recharge", "Purchase Complete, your new devices are Recharging your way!")
            currentOrder = Checkout(v.get(), False, cart_list[0][3], cust_details[4])
            if len(cart_list)>1:
                for x in range(1,len(cart_list)):
                    Checkout(v.get(), True, cart_list[x][3], cust_details[4], currentOrder)
            Page_Movement(10)
            cust_details = []
            cart_list = []
            search_entry.delete(0, END)
            phone_list = General_Data("PhoneDiff")
    def Remove_Cart(fields):
        # cart_list.append([self.name, self.price, self.image, self.id])
        global cart_list, instanceStock
        try:
            cart_list.pop(fields)
            instanceStock[cart_list[fields][3]] += 1
        except:
            pass
        checkoutFrame_Create()          

    for widget in checkout_frame.winfo_children():
        widget.destroy()    
    Label(checkout_frame, image=background).place(x=0,y=0, relwidth=1, relheight=1)
    Label(checkout_frame, text="ACTIVE CART", font=("Krona One", 25), fg="white", bg="black").place(relx=0.1, rely=0.1, relwidth=0.3, relheight=0.1)
    cost = 0
    v = StringVar(root, "1")
    if len(cart_list) != 0 and len(cust_details) != 0:
        for i in range(len(cart_list)):
            Label(checkout_frame, text=cart_list[i][0]+" PRICE: ₹"+str(cart_list[i][1])+"0", font=("Krona One", 10), fg="white", bg="black").place(relx=0.05, rely=0.2+0.4*cart_list.index(cart_list[i])/len(cart_list), relwidth=0.3, relheight=0.4/len(cart_list))
            Button(checkout_frame, text="REMOVE\n FROM CART", font=("Krona One", 8), fg="white", bg="black", command=lambda j=i:Remove_Cart(j), bd=0, highlightthickness=0).place(relx=0.35, rely=0.2+0.4*cart_list.index(cart_list[i])/len(cart_list), relwidth=0.1, relheight=0.4/len(cart_list))
            cost += cart_list[i][1]
        Label(checkout_frame, text="TOTAL COST: ₹"+str(cost)+"0", font=("Krona One", 15), fg="white", bg="black").place(relx=0.1, rely=0.6, relwidth=0.3, relheight=0.1)
        Label(checkout_frame, text="NAME: "+cust_details[0], font=("Krona One", 12), anchor="w", fg="white", bg="black").place(relx=0.5, rely=0.1, relwidth=0.4, relheight=0.05)
        Label(checkout_frame, text="EMAIL: "+cust_details[1], font=("Krona One", 12), anchor="w", fg="white", bg="black").place(relx=0.5, rely=0.15, relwidth=0.4, relheight=0.05)
        Label(checkout_frame, text="PHONE NUMBER: "+cust_details[2], font=("Krona One", 12), anchor="w", fg="white", bg="black").place(relx=0.5, rely=0.2, relwidth=0.4, relheight=0.05)
        Label(checkout_frame, text="ADDRESS: "+cust_details[3], font=("Krona One", 12), anchor="w", fg="white", bg="black", wraplength=512, justify=LEFT, width=512).place(relx=0.5, rely=0.25, relwidth=0.4)
        Label(checkout_frame, text="PAYMENT OPTIONS", font=("Krona One", 25), fg="white", bg="black").place(relx=0.5, rely=0.4, relwidth=0.4, relheight=0.1)
        Radiobutton(checkout_frame, image=visa_image, variable=v, value="VISA", indicator=0, fg="white", bg="black", command=checkout_visa).place(relx=0.5, rely=0.5, relwidth=0.1, relheight=0.1)
        Radiobutton(checkout_frame, text="CREDIT/DEBIT\n CARD", font=("Krona One", 10), variable=v, value="Credit/Debit Card", indicator=0, fg="white", bg="black", command=checkout_card).place(relx=0.6, rely=0.5, relwidth=0.1, relheight=0.1)
        Radiobutton(checkout_frame, text="NETBANKING", variable=v, value="Netbanking", indicator=0, font=("Krona One", 10), fg="white", bg="black", command=checkout_netbank).place(relx=0.7, rely=0.5, relwidth=0.1, relheight=0.1)
        Radiobutton(checkout_frame, text="CASH\n ON DELIVERY", variable=v, value="Cash on Delivery", indicator=0, font=("Krona One", 10), fg="white", bg="black", command=checkout_cod).place(relx=0.8, rely=0.5, relwidth=0.1, relheight=0.1)
        Button(checkout_frame, text="COMPLETE PURCHASE", font=("Krona One", 15), fg="white", bg="black", bd=0, highlightthickness=0, command=checkout_end).place(relx=0.35, rely=0.8, relwidth=0.3, relheight=0.1)
        Button(checkout_frame, image=back_image, bg="black", bd=0, highlightthickness=0, command=lambda:Page_Movement(8)).place(relx=0.93375, rely=0.02, relwidth=0.05625, relheight=0.1)

    elif len(cart_list) == 0 and len(cust_details) != 0:
        Label(checkout_frame, text="NO ITEMS IN CART", fg="white", bg="black", font=("Krona One", 14)).place(relx=0.1, rely=0.35, relwidth=0.3, relheight=0.1)
        Label(checkout_frame, text="TOTAL COST: ₹"+str(cost), font=("Krona One", 15), fg="white", bg="black").place(relx=0.1, rely=0.6, relwidth=0.3, relheight=0.1)
        Label(checkout_frame, text="NAME: "+cust_details[0], font=("Krona One", 12), anchor="w", fg="white", bg="black").place(relx=0.5, rely=0.1, relwidth=0.4, relheight=0.05)
        Label(checkout_frame, text="EMAIL: "+cust_details[1], font=("Krona One", 12), anchor="w", fg="white", bg="black").place(relx=0.5, rely=0.15, relwidth=0.4, relheight=0.05)
        Label(checkout_frame, text="PHONE NUMBER: "+cust_details[2], font=("Krona One", 12), anchor="w", fg="white", bg="black").place(relx=0.5, rely=0.2, relwidth=0.4, relheight=0.05)
        Label(checkout_frame, text="ADDRESS: "+cust_details[3], font=("Krona One", 12), anchor="w", fg="white", bg="black", wraplength=512, justify=LEFT, width=512).place(relx=0.5, rely=0.25, relwidth=0.4)
        Button(checkout_frame, image=back_image, bg="black", bd=0, highlightthickness=0, command=lambda:Page_Movement(8)).place(relx=0.93375, rely=0.02, relwidth=0.05625, relheight=0.1)

#function for the shop page
def shopFrame_Create():
    global search_term, search_entry
    def searchPhones():
        global phone_list, search_term, search_entry
        phone_list = []
        search_term = search_entry.get()
        for phone in main_list:
            phone_name = phone[0].lower()
            if phone_name.find(search_term.lower()) != -1:
                phone_list.append(phone)
        for widget in shop_frame.winfo_children():
            widget.destroy()
        shopFrame_Create()
    Label(shop_frame, image=shop_background).place(x=0, y=0, relwidth=1, relheight=1)
    if len(phone_list) > 4:
        shop_canvas = Canvas(shop_frame, borderwidth=0, highlightthickness=0)
        shop_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        def on_scroll(event):
            x, y = shop_canvas.canvasx(0), shop_canvas.canvasy(0)
            shop_scrollableframe.create_image(x,y, image=shop_background, anchor="nw")
            shop_scrollableframe.create_image(5,5, image=icon_white, anchor="nw")
        my_scrollbar = ttk.Scrollbar(shop_frame, orient=VERTICAL, command=shop_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=BOTH)
        shop_canvas.configure(yscrollcommand=my_scrollbar.set)
        shop_canvas.bind("<Configure>", lambda e: shop_canvas.configure(scrollregion = shop_canvas.bbox("all")))
        shop_canvas.create_image(0,0, image=shop_background, anchor="nw")
        shop_scrollableframe = Canvas(shop_canvas, background="black", width=1280, height=720, borderwidth=0, highlightthickness=0)
        shop_scrollableframe.pack(fill=BOTH,expand=TRUE)
        shop_scrollableframe.create_image(0,0, image=shop_background, anchor="nw")
        shop_scrollableframe.create_image(5,5, image=icon_white, anchor="nw")
        search_entry = Entry(shop_scrollableframe, bg="black", fg="white", font=("Krona One", 14), bd=2, highlightthickness=2)
        search_entry.insert(0, search_term)
        search_entry.place(relx=0.1, y=11, relwidth=0.445, height=72)
        Button(shop_scrollableframe, image=search_image, bg="black", bd=0, highlightthickness=0, command=lambda: searchPhones()).place(relx=0.545, y=11, relwidth=0.05625, height=72)
        Button(shop_scrollableframe, text="PROCEED TO \nCHECKOUT", image=cart_image, font=("Krona One", 12), fg="white", bg="black", compound="left", bd=0, highlightthickness=0, command=lambda:Page_Movement(7)).place(relx=0.615, y=11, relwidth=0.175, height=72)
        Button(shop_scrollableframe, text="END EXPLORING \nSESSION", image=explore_image, font=("Krona One", 12), fg="white", bg="black", compound="left", bd=0, highlightthickness=0, command=lambda:Page_Movement(9)).place(relx=0.8,y=11, relwidth=0.175, height=72)
        shop_canvas.create_window((0,0), window=shop_scrollableframe, anchor="nw")
        shop_scrollableframe.bind("<Configure>", on_scroll, "+")
        shop_scrollableframe.grid_rowconfigure(1, minsize=125)
        image_list = []
        for x in range(len(phone_list)):
            image = Image.open(phone_list[x][1])
            photo_image = ImageTk.PhotoImage(image)
            imagex, imagey = photo_image.width(), photo_image.height()
            newx, newy = imagex/imagey*120, 120
            image = image.resize((int(newx),int(newy)))
            final_image = ImageTk.PhotoImage(image)
            image_list.append(final_image)
        for x in range(len(phone_list)):
            phoneButton = Button(shop_scrollableframe, text="   "+phone_list[x][0]+"\n   ₹"+str(phone_list[x][2])+"0", font=("Krona One",12), image=image_list[x], compound="left",  width=1024, height=144, fg="white", bg="black", highlightthickness=0, bd=0, anchor="w", justify="left", command=lambda j=x: General_Data("PhoneClick", j))
            phoneButton.grid(row=x+2, column=1, padx=128, pady=2)
            phoneButton.image = image_list[x]
        shop_canvas.configure(scrollregion = shop_canvas.bbox("all"))

    elif len(phone_list) == 0:
        shop_canvas = Canvas(shop_frame, background="black", width=1280, height=720, borderwidth=0, highlightthickness=0)
        shop_canvas.pack(expand=TRUE, fill=BOTH)
        shop_canvas.create_image(0,0, image=shop_background, anchor="nw")
        shop_canvas.create_image(5,5, image=icon_white, anchor="nw")
        shop_canvas.create_text(500, 350, text="No phones found!", font=("Krona One", 16), fill="white", anchor="nw")
        search_entry = Entry(shop_canvas, bg="black", fg="white", font=("Krona One", 14), bd=2, highlightthickness=2)
        search_entry.insert(0, search_term)
        search_entry.place(relx=0.1, y=11, relwidth=0.445, height=72)     
        Button(shop_canvas, image=search_image, bg="black", bd=0, highlightthickness=0, command=lambda: searchPhones()).place(relx=0.545, y=11, relwidth=0.05625, height=72)   
        Button(shop_canvas, text="PROCEED TO \nCHECKOUT", image=cart_image, font=("Krona One", 12), fg="white", bg="black", compound="left", bd=0, highlightthickness=0, command=lambda:Page_Movement(7)).place(relx=0.615, y=11, relwidth=0.175, height=72)
        Button(shop_canvas, text="END EXPLORING \nSESSION", image=explore_image, font=("Krona One", 12), fg="white", bg="black", compound="left", bd=0, highlightthickness=0, command=lambda:Page_Movement(9)).place(relx=0.8,y=11, relwidth=0.175, height=72)

    else:
        image_list = []
        for x in range(len(phone_list)):
            image = Image.open(phone_list[x][1])
            photo_image = ImageTk.PhotoImage(image)
            imagex, imagey = photo_image.width(), photo_image.height()
            newx, newy = imagex/imagey*120, 120
            image = image.resize((int(newx),int(newy)))
            final_image = ImageTk.PhotoImage(image)
            image_list.append(final_image)
        shop_canvas = Canvas(shop_frame, background="black", width=1280, height=720, borderwidth=0, highlightthickness=0)
        shop_canvas.pack(fill=BOTH, expand=TRUE)
        shop_canvas.grid_rowconfigure(1, minsize=125)
        shop_canvas.create_image(0,0, image=shop_background, anchor="nw")
        shop_canvas.create_image(5,5, image=icon_white, anchor="nw")
        search_entry = Entry(shop_canvas, bg="black", fg="white", font=("Krona One", 14), bd=2, highlightthickness=2)
        search_entry.insert(0, search_term)
        search_entry.place(relx=0.1, y=11, relwidth=0.445, height=72)
        Button(shop_canvas, image=search_image, bg="black", bd=0, highlightthickness=0, command=lambda: searchPhones()).place(relx=0.545, y=11, relwidth=0.05625, height=72)
        Button(shop_canvas, text="PROCEED TO \nCHECKOUT", image=cart_image, font=("Krona One", 12), fg="white", bg="black", compound="left", bd=0, highlightthickness=0, command=lambda:Page_Movement(7)).place(relx=0.615, y=11, relwidth=0.175, height=72)
        Button(shop_canvas, text="END EXPLORING \nSESSION", image=explore_image, font=("Krona One", 12), fg="white", bg="black", compound="left", bd=0, highlightthickness=0, command=lambda:Page_Movement(9)).place(relx=0.8,y=11, relwidth=0.175, height=72)
        for x in range(len(phone_list)):
            phoneButton = Button(shop_canvas, text="   "+phone_list[x][0]+"\n   ₹"+str(phone_list[x][2])+"0", font=("Krona One",12), image=image_list[x], compound="left",  width=1024, height=144, fg="white", bg="black", highlightthickness=0, bd=0, anchor="w", justify="left", command=lambda j=x: General_Data("PhoneClick", j))
            phoneButton.grid(row=x+2, column=1, padx=128, pady=2)
            phoneButton.image = image_list[x]

#function for the checkout page
def Checkout(PaymentMode, sameorder ,*fields):
    global Capital,sqluser, sqlpass
    dbo=mysql.connector.connect(host="localhost", user=sqluser, password=sqlpass, database='rechargemobiles')
    c=dbo.cursor()
    #fields = [PhoneID, CustomerID, OrderID(if order is same)]
    c.execute('SELECT PurchaseID FROM PurchaseLog;')
    purchases = c.fetchall()
    n = len(purchases) + 1
    PurchaseID = 'LI' + str(100 + n)
    if sameorder == False:
        c.execute('SELECT OrderID FROM PurchaseLog;')
        orders = c.fetchall()
        if len(orders) != 0:
            n = orders[len(orders)-1]
            OrderID = 'OI' + str(int(n[0][2:len(n[0])])+1)
        else:
            OrderID = 'OI101'
    else:
        OrderID = fields[2]
    PurchaseDate = datetime.today().strftime('%Y-%m-%d')
    PhoneID = (fields[0],)
    sqlcommand = 'SELECT DealerID FROM Stock WHERE PhoneID = %s;'
    c.execute(sqlcommand, PhoneID)
    Dealer= c.fetchone()
    DealerID = Dealer[0]
    sqlcommand = 'SELECT PhoneCP, PhoneSP, PhoneModel FROM Stock WHERE PhoneID = %s;'
    c.execute(sqlcommand,PhoneID)
    PhoneCosts = c.fetchone()
    CustomerID = (fields[1],)
    sqlcommand = 'SELECT CustomerName FROM Customer WHERE CustomerID = %s;'
    c.execute(sqlcommand,CustomerID)
    customer = c.fetchone()
    CustomerName = customer[0]
    PurchaseProfit = PhoneCosts[1] - PhoneCosts[0]
    PhoneModel = PhoneCosts[2]
    PhoneID = fields[0]
    CustomerID = fields[1]
    #insertion
    try:
        values = (PurchaseID, OrderID, PurchaseDate, PhoneID, PhoneModel, CustomerID, DealerID, PaymentMode, PurchaseProfit)
        sqlcommand = 'INSERT INTO PurchaseLog(PurchaseID, OrderID, PurchaseDate, PhoneID, PhoneModel, CustomerID, DealerID, PaymentMode, PurchaseProfit) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);' 
        c.execute(sqlcommand,values)
        dbo.commit()
        commandcheck = True
    except:
        dbo.rollback()
        commandcheck = False
    if commandcheck == True:
        values = (PhoneCosts[1], CustomerID)
        sqlcommand = 'UPDATE Customer SET TotalAmountSpent = TotalAmountSpent + %s WHERE CustomerID = %s;'
        c.execute(sqlcommand,values)
        dbo.commit()
        values = (fields[0],)
        sqlcommand = 'UPDATE Stock SET PhoneCount = PhoneCount-1 WHERE PhoneID = %s;'
        c.execute(sqlcommand, values)
        dbo.commit()
        return OrderID
    else:
        display_text = 'input error, something went wrong with the input or the code, please check'
        return commandcheck, display_text
    
#function to move between pages
def Page_Movement(usage):
    if usage == 1:
        entry_frame.pack_forget()
        select_frame.pack(expand=TRUE, fill=BOTH)
    elif usage == 2:
        select_frame.pack_forget()
        entry_frame.pack(expand=TRUE, fill=BOTH)
    elif usage == 3:
        select_frame.pack_forget()
        login_frame.pack(expand=TRUE, fill=BOTH)
    elif usage == 4:
        login_frame.pack_forget()
        select_frame.pack(expand=TRUE, fill=BOTH)
    elif usage == 5:
        select_frame.pack_forget()
        signup_frame.pack(expand=TRUE, fill=BOTH)
    elif usage == 6:
        signup_frame.pack_forget()
        select_frame.pack(expand=TRUE, fill=BOTH)
    elif usage == 7:
            shop_frame.pack_forget()
            checkoutFrame_Create()
            checkout_frame.pack(expand=TRUE, fill=BOTH)
    elif usage == 8:
        checkout_frame.pack_forget()
        shop_frame.pack(expand=TRUE, fill=BOTH)
    elif usage == 9:
        shop_frame.pack_forget()
        entry_frame.pack(expand=TRUE, fill=BOTH)
    elif usage == 10:
        checkout_frame.pack_forget()
        entry_frame.pack(expand=TRUE, fill=BOTH)
    elif usage == 11:
        entry_frame.pack_forget()
        framehome.pack(expand=TRUE, fill=BOTH)

#function for making the logo a transparent image of needed size
def transp_image(image):
    image = ImageTk.getimage(image)
    photo_image = ImageTk.PhotoImage(image)
    imagex, imagey = photo_image.width(), photo_image.height()
    newx, newy = imagex/imagey*83, 83
    image = image.resize((int(newx),int(newy)))
    image = image.convert("RGBA")
    photo_image = ImageTk.PhotoImage(image)
    return photo_image

#entry frame
entry_frame = Frame(root, width=1280, height=720, background="black")
entry_frame.pack()
Label(entry_frame, image=login_background).place(x=0,y=0,relwidth=1,relheight=1)
Button(entry_frame, text=" START EXPLORING", image=explore_image, font=("Krona One", 24), fg="white", bg="black", compound="left", bd=0, command=lambda:Page_Movement(1)).place(relx=0.3, rely=0.55, relwidth=0.4, relheight=0.1)
Button(entry_frame, text=" ADMIN\n PORTAL", image=admin_image, font=("Krona One",12), fg="white", bg="black",  compound="left", bd=0, command=lambda:Page_Movement(11)).place(relx=0.865, rely=0.883, relwidth=0.125, relheight=0.1)

#select frame
select_frame = Frame(root, width=1280, height=720, background="black")
Label(select_frame, image=background).place(x=0,y=0,relwidth=1,relheight=1)
Button(select_frame, text="LOGIN", image=login_image, compound="left", font=("Krona One", 18), fg="white", bg="black", bd=0, highlightthickness=0, command=lambda:Page_Movement(3)).place(relx=0.4, rely=0.4, relwidth=0.2, relheight=0.1)
Button(select_frame, text="SIGN UP", image=signup_image, font=("Krona One", 18), fg="white", bg="black", compound="left", bd=0, highlightthickness=0, command=lambda:Page_Movement(5)).place(relx=0.4, rely=0.5, relwidth=0.2, relheight=0.1)
Button(select_frame, image=back_image, bg="black", bd=0, highlightthickness=0, command=lambda:Page_Movement(2)).place(relx=0.93375, rely=0.02, relwidth=0.05625, relheight=0.1)

#login frame
login_frame = Frame(root, width=1280, height=720, background="black")
Label(login_frame, image=background).place(x=0,y=0,relwidth=1,relheight=1)
Label(login_frame, text="EMAIL ADDRESS", font=("Krona One",15), fg="white", bg="black", highlightthickness=0, bd=0).place(relx=0.3, rely=0.33, relwidth=0.2, relheight=0.04)
Label(login_frame, text="PASSWORD", font=("Krona One",15), fg="white", bg="black", highlightthickness=0, bd=0).place(relx=0.3, rely=0.43, relwidth=0.2, relheight=0.04)
Button(login_frame, image=back_image, bg="black", bd=0, highlightthickness=0, command=lambda:Page_Movement(4)).place(relx=0.93375, rely=0.02, relwidth=0.05625, relheight=0.1)
login_email_entry = Entry(login_frame, borderwidth=5, fg="white", bg="black", highlightthickness=2, bd=2)
login_password_entry = Entry(login_frame, show="*", borderwidth=5, fg="white", bg="black", highlightthickness=2, bd=2)
login_email_entry.place(relx=0.5, rely=0.33, relwidth=0.2, relheight=0.04)
login_password_entry.place(relx=0.5, rely=0.43, relwidth=0.2, relheight=0.04)
login_button = Button(login_frame, text="LOGIN", image=login_image, compound="left", font=("Krona One",20), fg="white", bg="black", highlightthickness=0, bd=0, command=lambda:General_Data("Login", login_email_entry.get(), login_password_entry.get())).place(relx=0.4, rely=0.5, relwidth=0.2, relheight=0.1)

butsee=Button(login_frame,image=newsee, command= lambda: passee(login_password_entry),bd=0, highlightthickness=0)
butsee.place(relx=0.72, rely=0.43)

#signup frame
signup_frame = Frame(root, width=1280, height=720, background="black")
Label(signup_frame, image=background).place(x=0,y=0,relwidth=1,relheight=1)
signup_name_label = Label(signup_frame, text="NAME", font=("Krona One",12), fg="white", bg="black", highlightthickness=0, bd=4).place(relx=0.3, rely=0.18, relwidth=0.2, relheight=0.04)
signup_email_label = Label(signup_frame, text="EMAIL ADDRESS", font=("Krona One",12), fg="white", bg="black", highlightthickness=0, bd=4).place(relx=0.3, rely=0.28, relwidth=0.2, relheight=0.04)
signup_phone_label = Label(signup_frame, text="MOBILE NUMBER", font=("Krona One",12), fg="white", bg="black", highlightthickness=0, bd=4).place(relx=0.3, rely=0.38, relwidth=0.2, relheight=0.04)
signup_address_label = Label(signup_frame, text="ADDRESS", font=("Krona One",12), fg="white", bg="black", highlightthickness=0, bd=4).place(relx=0.3, rely=0.48, relwidth=0.2, relheight=0.04)
signup_password_label = Label(signup_frame, text="PASSWORD", font=("Krona One",12), fg="white", bg="black", highlightthickness=0, bd=4).place(relx=0.3, rely=0.58, relwidth=0.2, relheight=0.04)
signup_passwordconfirm_label = Label(signup_frame, text="CONFIRM PASSWORD", font=("Krona One",12), fg="white", bg="black", highlightthickness=0, bd=4).place(relx=0.3, rely=0.68, relwidth=0.2, relheight=0.04)
signup_name_entry = Entry(signup_frame, borderwidth=5, fg="white", bg="black", highlightthickness=2, bd=2)
signup_email_entry = Entry(signup_frame, borderwidth=5, fg="white", bg="black", highlightthickness=2, bd=2)
signup_phone_entry = Entry(signup_frame, borderwidth=5, fg="white", bg="black", highlightthickness=2, bd=2)
signup_address_entry = Entry(signup_frame, borderwidth=5, fg="white", bg="black", highlightthickness=2, bd=2)
signup_password_entry = Entry(signup_frame, show="*", borderwidth=5, fg="white", bg="black", highlightthickness=2, bd=2)
signup_passwordconfirm_entry = Entry(signup_frame, show="*", borderwidth=5, fg="white", bg="black", highlightthickness=2, bd=2)
signup_name_entry.place(relx=0.5, rely=0.18, relwidth=0.2, relheight=0.04)
signup_email_entry.place(relx=0.5, rely=0.28, relwidth=0.2, relheight=0.04)
signup_phone_entry.place(relx=0.5, rely=0.38, relwidth=0.2, relheight=0.04)
signup_address_entry.place(relx=0.5, rely=0.48, relwidth=0.2, relheight=0.04)
signup_password_entry.place(relx=0.5, rely=0.58, relwidth=0.2, relheight=0.04)
signup_passwordconfirm_entry.place(relx=0.5, rely=0.68, relwidth=0.2, relheight=0.04)
Button(signup_frame, text="SIGN UP", image=signup_image, font=("Krona One",20), compound="left", fg="white", bg="black", highlightthickness=0, bd=0, command=lambda:General_Data("Signup", signup_name_entry.get(), signup_email_entry.get(), signup_phone_entry.get(), signup_address_entry.get(), signup_password_entry.get(), signup_passwordconfirm_entry.get())).place(relx=0.4, rely=0.75, relwidth=0.2, relheight=0.1)
Button(signup_frame, image=back_image, bg="black", bd=0, highlightthickness=0, command=lambda:Page_Movement(6)).place(relx=0.93375, rely=0.02, relwidth=0.05625, relheight=0.1)

butsee=Button(signup_frame,image=newsee, command= lambda: passee(signup_password_entry),bd=0, highlightthickness=0)
butsee.place(relx=0.72, rely=0.58)
butsee=Button(signup_frame,image=newsee, command= lambda: passee(signup_passwordconfirm_entry),bd=0, highlightthickness=0)
butsee.place(relx=0.72, rely=0.68)

# shop frame
main_list = General_Data("PhoneDiff")
phone_list = General_Data("PhoneDiff")
icon_white = transp_image(icon_white)
search_term = ""
shop_frame = Frame(root, width=1280, height=720, background="black")
shopFrame_Create()

#checkout frame
checkout_frame = Frame(root, width=1280, height=720, background="black")
checkoutFrame_Create()


#admin portal
framehome= Frame(root,width=1280,height=720, background="black")
my_labhome = Label(framehome, image=background).place(x=0, y=0, relwidth = 1, relheight = 1)
count = 0
idl=Label(framehome, text="ADMIN ID", font=("Krona One",16),bg='black',fg='white')
idl.place(relx=0.3,rely=0.44)
ehi=Entry(framehome, width=15, bg='black',fg='white', bd = 2, highlightthickness = 2)
ehi.place(relx=0.43, relwidth=0.2,rely=0.44)
count += 1

idp=Label(framehome, text="ADMIN PASSWORD", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
idp.place(relx=0.2,rely=0.52)
ehp=Entry(framehome,  width=15, show='*',bg='black',fg='white', bd = 2, highlightthickness = 2)
ehp.place(relx=0.43, relwidth=0.2,rely=0.52)
count +=1
def back():
    framehome.pack_forget()
    entry_frame.pack(expand=TRUE, fill=BOTH)
    ehp.delete(0, END)
    ehi.delete(0, END)
    
Button(framehome, image=back_image, bg="black", bd=0, highlightthickness=0, command=back).place(relx=0.93375, rely=0.02, relwidth=0.05625, relheight=0.1)

frame= Frame(root,width=1280,height=720, background="black")
img=PhotoImage(file=r'assets/backgrounds/background.png')
my_lab = Label(frame, image=img)
my_lab.place(x=0, y=0, relwidth = 1, relheight = 1)

frame2 =Frame(root,width=1280,height=720, background="black")
img2=PhotoImage(file=r'assets/backgrounds/background.png')
my_label = Label(frame2, image=img2)
my_label.place(x=0, y=0, relwidth = 1, relheight = 1)

frameada= Frame(root,width=1280,height=720, background="black")
imgada=PhotoImage(file=r'assets/backgrounds/background.png')
my_labada = Label(frameada, image=imgada)
my_labada.place(x=0, y=0, relwidth = 1, relheight = 1)

framerem= Frame(root,width=1280,height=720, background="black")
imgrem=PhotoImage(file=r'assets/backgrounds/background.png')
my_labrem = Label(framerem, image=imgrem)
my_labrem.place(x=0, y=0, relwidth = 1, relheight = 1)

frameadd= Frame(root,width=1280,height=720, background="black")
imgadd=PhotoImage(file=r'assets/backgrounds/background.png')
my_labadd = Label(frameadd, image=imgadd)
my_labadd.place(x=0, y=0, relwidth = 1, relheight = 1)

frameremc= Frame(root,width=1280,height=720, background="black")
imgremc=PhotoImage(file=r'assets/backgrounds/background.png')
my_labremc = Label(frameremc, image=imgremc)
my_labremc.place(x=0, y=0, relwidth = 1, relheight = 1)

frameadp= Frame(root,width=1280,height=720, background="black")
imgadp=PhotoImage(file=r'assets/backgrounds/background.png')
my_labadp = Label(frameadp, image=imgadp)
my_labadp.place(x=0, y=0, relwidth = 1, relheight = 1)

framemod= Frame(root,width=1280,height=720, background="black")
imgmod=PhotoImage(file=r'assets/backgrounds/background.png')
my_labmod = Label(framemod, image=imgmod)
my_labmod.place(x=0, y=0, relwidth = 1, relheight = 1)

frameadm= Frame(root,width=1280,height=720, background="black")
imgadm=PhotoImage(file=r'assets/backgrounds/background.png')
my_labadm = Label(frameadm, image=imgadm)
my_labadm.place(x=0, y=0, relwidth = 1, relheight = 1)

framereme= Frame(root,width=1280,height=720, background="black")
imgreme=PhotoImage(file=r'assets/backgrounds/background.png')
my_labreme = Label(framereme, image=imgreme)
my_labreme.place(x=0, y=0, relwidth = 1, relheight = 1)

framecap= Frame(root,width=1280,height=720, background="black")
imgcap=PhotoImage(file=r'assets/backgrounds/background.png')
my_labcap = Label(framecap, image=imgcap)
my_labcap.place(x=0, y=0, relwidth = 1, relheight = 1)

frameplog= Frame(root,width=1280,height=720, background="black")
imgplog=PhotoImage(file=r'assets/backgrounds/background.png')
my_labplog = Label(frameplog, image=imgplog)
my_labplog.place(x=0, y=0, relwidth = 1, relheight = 1)

def close1():
    frame.pack_forget()
    frameada.pack()

    count=0
    idn=Label(frameada, text="ADMIN NAME", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    idn.place(relx=0.26,rely=0.36)
    ehn=Entry(frameada, bg='black',fg='white',bd = 2, highlightthickness = 2)
    ehn.place(relx=0.43, relwidth=0.2,rely=0.36)
    count+=1
    
    pad=Label(frameada, text="ADMIN PASSWORD", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    pad.place(relx=0.2,rely=0.44)
    ep=Entry(frameada,   bg='black',fg='white', show="*", bd = 2, highlightthickness = 2)
    ep.place(relx=0.43, relwidth=0.2,rely=0.44)
    count+=1

    butsee=Button(frameada,image=newsee, command= lambda: passee(ep),bd=0, highlightthickness=0)
    butsee.place(relx=0.65, rely=0.44)
    
    idcp=Label(frameada, text="CONFIRM PASSWORD", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    idcp.place(relx=0.18,rely=0.52)
    ehpc=Entry(frameada,    show='*',bg='black',fg='white', bd = 2, highlightthickness = 2)
    ehpc.place(relx=0.43, relwidth=0.2,rely=0.52)
    count+=1

    butsee=Button(frameada,image=newsee, command= lambda: passee(ehpc),bd=0, highlightthickness=0)
    butsee.place(relx=0.65, rely=0.52)
    
    def check(e1,e2,e3):
        try:
            AdminAddList = Admin('Add Admin', e1, e2, e3)
            if type(AdminAddList) == tuple and AdminAddList[0] == False:
                messagebox.showerror('Recharge', AdminAddList[1])
            elif type(AdminAddList) == tuple and AdminAddList[0] == True:
                messagebox.showinfo('Recharge', 'Successfully added new admin!\nYour Admin ID is ' + str(AdminAddList[1]))
            else:
                messagebox.showerror('Recharge', 'An error occured.')
        except Exception:
            pass
    
    def back():
        frameada.pack_forget()
        frame.pack()
        
    ada=Button(frameada, text="ADD ADMIN", fg='white', bg='black', activebackground='black', padx=35, pady=10, font=('Krona One',12),command= lambda: check(str(ep.get()),str(ehn.get()), str(ehpc.get())),bd=0, highlightthickness=0)
    ada.place(relx=0.44,rely=0.7)
    Button(frameada, image=back_image, bg="black", bd=0, highlightthickness=0, command=back).place(relx=0.93375, rely=0.02, relwidth=0.05625, relheight=0.1)


def close2():
    frame.pack_forget()
    framerem.pack()

    count = 0
    idrem=Label(framerem, text="ENTER ADMIN ID TO BE REMOVED", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    idrem.place(relx=0.33,rely=0.36)
    ehrem=Entry(framerem, bg='black',fg='white', bd = 2, highlightthickness = 2)
    ehrem.place(relx=0.39,rely=0.42, relwidth=0.2)
    count+=1

    def check(e1):
        try:
            AdminRemoveList = Admin('Remove Admin', e1)
            if type(AdminRemoveList) == tuple and AdminRemoveList[0] == False:
                messagebox.showerror('Recharge', AdminRemoveList[1])
            elif type(AdminRemoveList) != tuple and AdminRemoveList == True:
                messagebox.showinfo('Recharge', 'successfully removed admin')
            else:
                messagebox.showerror('Recharge', 'An error occured, check the input.')
        except Exception:
                pass

    def back():
        framerem.pack_forget()
        frame.pack()

    rem=Button(framerem, text="REMOVE ADMIN", fg='white', bg='black', activebackground='black', padx=35, pady=10, font=('Krona One',12), command = lambda: check(str(ehrem.get())),bd=0, highlightthickness=0)
    rem.place(relx=0.4,rely=0.55)
    Button(framerem, image=back_image, bg="black", bd=0, highlightthickness=0, command=back).place(relx=0.93375, rely=0.02, relwidth=0.05625, relheight=0.1)


def close3():
    frame.pack_forget()
    frameadd.pack()

    count = 0  
    iddn=Label(frameadd, text="DEALER NAME", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    iddn.place(relx=0.23,rely=0.36)
    ehdn=Entry(frameadd,   bg='black',fg='white', bd = 2, highlightthickness = 2)
    ehdn.place(relx=0.43, relwidth=0.2,rely=0.36)
    count+=1
    
    idda=Label(frameadd, text="DEALER ADDRESS", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    idda.place(relx=0.22,rely=0.44)
    ehda=Entry(frameadd, bg='black',fg='white', bd = 2, highlightthickness = 2)
    ehda.place(relx=0.43, relwidth=0.2,rely=0.44)
    count+=1
    
    iddnum=Label(frameadd, text="DEALER NUMBER", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    iddnum.place(relx=0.22,rely=0.52)
    ehdnum=Entry(frameadd,   bg='black',fg='white', bd = 2, highlightthickness = 2)
    ehdnum.place(relx=0.43, relwidth=0.2,rely=0.52)
    count+=1
    
    idb=Label(frameadd, text="DEALER BRAND", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    idb.place(relx=0.22,rely=0.6)
    ehb=Entry(frameadd,   bg='black',fg='white', bd = 2, highlightthickness = 2)
    ehb.place(relx=0.43, relwidth=0.2,rely=0.6)
    count+=1

    def check(e1,e2,e3,e4):
        try:
            AdminDAddList = Admin('Add Dealer', e1,e2,e3,e4)
            if type(AdminDAddList) == tuple and AdminDAddList[0] == False:
                messagebox.showerror('Recharge', AdminDAddList[1])
            elif type(AdminDAddList) == tuple and AdminDAddList[0] == True:
                messagebox.showinfo('Recharge', 'Successfully added the new dealer!\nYour new Dealer ID is' + AdminDAddList[1])
            else:
                messagebox.showerror('Recharge', 'An error occured, check the input.')
        except Exception:
            pass
        
    def back():
        frameadd.pack_forget()
        frame.pack()

    add=Button(frameadd, text="ADD DEALER", fg='white', bg='black', activebackground='black', padx=35, pady=10, font=('Krona One',12), command = lambda: check(str(ehdn.get()), str(ehda.get()), str(ehdnum.get()), str(ehb.get())),bd=0, highlightthickness=0)
    add.place(relx=0.4,rely=0.78)
    Button(frameadd, image=back_image, bg="black", bd=0, highlightthickness=0, command=back).place(relx=0.93375, rely=0.02, relwidth=0.05625, relheight=0.1)


def close4():
    frame.pack_forget()
    frameremc.pack()

    count = 0
    idcrem=Label(frameremc, text="ENTER CUSTOMER ID TO BE REMOVED", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    idcrem.place(relx=0.31,rely=0.36)
    ecrem=Entry(frameremc, bg='black',fg='white', bd = 2, highlightthickness = 2)
    ecrem.place(relx=0.39,rely=0.44, relwidth=0.2)
    count+=1
    
    def check(e1):
        try:
            AdminCRemoveList = Admin('Remove Customer', e1)
            if type(AdminCRemoveList) == tuple and AdminCRemoveList[0] == False:
                messagebox.showerror('Recharge', AdminCRemoveList[1])
            elif type(AdminCRemoveList) != tuple and AdminCRemoveList == True:
                messagebox.showinfo('Recharge', 'Successfully removed customer!')
            else:
                messagebox.showerror('Recharge', 'An error occured, check the input.')
        except Exception:
                pass
    
    def back():
        frameremc.pack_forget()
        frame.pack()
  
    remc=Button(frameremc, text="REMOVE CUSTOMER", fg='white', bg='black', activebackground='black', padx=35, pady=10, font=('Krona One',12), command = lambda: check(str(ecrem.get())),bd=0, highlightthickness=0)
    remc.place(relx=0.38,rely=0.55)
    Button(frameremc, image=back_image, bg="black", bd=0, highlightthickness=0, command=back).place(relx=0.93375, rely=0.02, relwidth=0.05625, relheight=0.1)


def close5():
    frame.pack_forget()
    frameadp.pack()

    count = 0
    idpi=Label(frameadp, text="PHONE ID", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    idpi.place(relx=0.3,rely=0.4)
    epi=Entry(frameadp, bg='black',fg='white', bd = 2, highlightthickness = 2)
    epi.place(relx=0.43, relwidth=0.2,rely=0.4)
    count+=1
    
    idpc=Label(frameadp, text="PHONE COUNT", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    idpc.place(relx=0.25,rely=0.48)
    ehpc=Entry(frameadp,   bg='black',fg='white', bd = 2, highlightthickness = 2)
    ehpc.place(relx=0.43, relwidth=0.2,rely=0.48)
    count+=1

    def check(e1,e2):
        try:
            AdminPhoneAddList = Admin('Add Phonecount', e1,e2)
            if type(AdminPhoneAddList) == tuple and AdminPhoneAddList[0] == False:
                messagebox.showerror('Recharge', AdminPhoneAddList[1])
            elif type(AdminPhoneAddList) != tuple and AdminPhoneAddList == True:
                messagebox.showinfo('Recharge', 'Successfully updated phone count!')
            else:
                messagebox.showerror('Recharge', 'An error occured, check the input.')
        except Exception:
                pass

    def back():
        frameadp.pack_forget()
        frame.pack()

    adp=Button(frameadp, text="UPDATE COUNT", fg='white', bg='black', activebackground='black', padx=35, pady=10, font=('Krona One',12), command = lambda: check(str(epi.get()), int(ehpc.get())),bd=0, highlightthickness=0)
    adp.place(relx=0.42,rely=0.6)
    Button(frameadp, image=back_image, bg="black", bd=0, highlightthickness=0, command=back).place(relx=0.93375, rely=0.02, relwidth=0.05625, relheight=0.1)


def close6():
    frame.pack_forget()
    framemod.pack()

    count = 0
    idpid=Label(framemod, text="PHONE ID", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    idpid.place(relx=0.3,rely=0.4)
    epid=Entry(framemod, bg='black',fg='white', bd = 2, highlightthickness = 2)
    epid.place(relx=0.43, relwidth=0.2,rely=0.4)
    count+=1
    
    idnp=Label(framemod, text="NEW PRICE", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    idnp.place(relx=0.29,rely=0.48)
    ehbp=Entry(framemod,   bg='black',fg='white', bd = 2, highlightthickness = 2)
    ehbp.place(relx=0.43, relwidth=0.2,rely=0.48)
    count+=1

    def check(e1,e2):
        try:
            AdminModSellPriceList = Admin('Modify Selling Price', e1,e2)
            if type(AdminModSellPriceList) == tuple and AdminModSellPriceList[0] == False:
                messagebox.showerror('Recharge', AdminModSellPriceList[1])
            elif type(AdminModSellPriceList) != tuple and AdminModSellPriceList == True:
                    messagebox.showinfo('Recharge', 'Successfully modified selling price!')
            else:
                    messagebox.showerror('Recharge', 'An error occured, check the input.')
        except Exception:
                pass
    
    def back():
        framemod.pack_forget()
        frame.pack()

    mod=Button(framemod, text="UPDATE PRICE", fg='white', bg='black', activebackground='black', padx=35, pady=10, font=('Krona One',12), command = lambda: check(str(epid.get()), float(ehbp.get())),bd=0, highlightthickness=0)
    mod.place(relx=0.42,rely=0.6)
    Button(framemod, image=back_image, bg="black", bd=0, highlightthickness=0, command=back).place(relx=0.93375, rely=0.02, relwidth=0.05625, relheight=0.1)


def close7():
    frame.pack_forget()
    frameadm.pack()

    count = 0
    pm=Label(frameadm, text="PHONE MODEL", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    pm.place(relx=0.08,rely=0.13)
    epm=Entry(frameadm,  width=14,   bg='black',fg='white', bd = 2, highlightthickness = 2)
    epm.place(relx=0.29,rely=0.13, relwidth=0.2)
    count+=1
    
    idde=Label(frameadm, text="DEALER ID", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    idde.place(relx=0.11,rely=0.21)
    ede=Entry(frameadm, width=14,  bg='black',fg='white', bd = 2, highlightthickness = 2)
    ede.place(relx=0.29,rely=0.21, relwidth=0.2)
    count+=1
    
    idcp=Label(frameadm, text="PHONE COST PRICE", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    idcp.place(relx=0.03,rely=0.29)
    ehcp=Entry(frameadm,  width=14,   bg='black',fg='white', bd = 2, highlightthickness = 2)
    ehcp.place(relx=0.29,rely=0.29, relwidth=0.2)
    count+=1
    
    idsp=Label(frameadm, text="PHONE SELLING PRICE", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    idsp.place(relx=0.013,rely=0.37)
    ehsp=Entry(frameadm,  width=14,   bg='black',fg='white', bd = 2, highlightthickness = 2)
    ehsp.place(relx=0.29,rely=0.37, relwidth=0.2)
    count+=1
    
    idpm=Label(frameadm, text="PHONE MANUFACTURER", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    idpm.place(relx=0.01,rely=0.45)
    ehpm=Entry(frameadm, width=14,  bg='black',fg='white', bd = 2, highlightthickness = 2)
    ehpm.place(relx=0.29,rely=0.45, relwidth=0.2)
    count+=1

    idpc=Label(frameadm, text="PHONE COUNTRY", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    idpc.place(relx=0.06,rely=0.53)
    ehpc=Entry(frameadm,  width=14, bg='black',fg='white', bd = 2, highlightthickness = 2)
    ehpc.place(relx=0.29,rely=0.53, relwidth=0.2)
    count+=1
    
    idpw=Label(frameadm, text="PHONE WEIGHT (g)", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    idpw.place(relx=0.07,rely=0.61)
    ehpw=Entry(frameadm, width=14, bg='black',fg='white', bd = 2, highlightthickness = 2)
    ehpw.place(relx=0.29,rely=0.61, relwidth=0.2)
    count+=1

    idpg=Label(frameadm, text="PHONE GEN", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    idpg.place(relx=0.54,rely=0.13)
    ehpg=Entry(frameadm, width=18, bg='black',fg='white', bd = 2, highlightthickness = 2)
    ehpg.place(relx=0.74,rely=0.13, relwidth=0.2)
    count+=1
    
    idos=Label(frameadm, text="PHONE OS", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    idos.place(relx=0.55,rely=0.21)
    ehos=Entry(frameadm,  width=18, bg='black',fg='white', bd = 2, highlightthickness = 2)
    ehos.place(relx=0.74,rely=0.21, relwidth=0.2)
    count+=1

    idps=Label(frameadm, text="PHONE SCREEN", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    idps.place(relx=0.54,rely=0.29)
    ehps=Entry(frameadm, width=18, bg='black',fg='white', bd = 2, highlightthickness = 2)
    ehps.place(relx=0.74,rely=0.29, relwidth=0.2)
    count+=1
    
    idpr=Label(frameadm, text="PHONE RAM", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    idpr.place(relx=0.54,rely=0.37)
    ehpr=Entry(frameadm,  width=18, bg='black',fg='white', bd = 2, highlightthickness = 2)
    ehpr.place(relx=0.74,rely=0.37, relwidth=0.2)
    count+=1
    
    idpro=Label(frameadm, text="PHONE ROM", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    idpro.place(relx=0.54,rely=0.45)
    ehpro=Entry(frameadm,  width=18, bg='black',fg='white', bd = 2, highlightthickness = 2)
    ehpro.place(relx=0.74,rely=0.45, relwidth=0.2)
    count+=1
    
    idpd=Label(frameadm, text="PHONE DIMENSIONS", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    idpd.place(relx=0.5,rely=0.53)
    ehpdi=Entry(frameadm, width=18, bg='black',fg='white', bd = 2, highlightthickness = 2)
    ehpdi.place(relx=0.74,rely=0.53, relwidth=0.2)
    count+=1
    
    ipc=Label(frameadm, text="PHONE COLOUR", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    ipc.place(relx=0.52,rely=0.61)
    ehpco=Entry(frameadm,  width=18, bg='black',fg='white', bd = 2, highlightthickness = 2)
    ehpco.place(relx=0.74,rely=0.61, relwidth=0.2)
    count+=1
    
    idpe=Label(frameadm, text="PHONE ESSENTIALS", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    idpe.place(relx=0.5,rely=0.69)
    ehpe=Entry(frameadm, width=18, bg='black',fg='white', bd = 2, highlightthickness = 2)
    ehpe.place(relx=0.74,rely=0.69, relwidth=0.2)
    count+=1
    
    idpco=Label(frameadm, text="PHONE COUNT", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    idpco.place(relx=0.31,rely=0.79)
    ehpcol=Entry(frameadm, width=18, bg='black',fg='white', bd = 2, highlightthickness = 2)
    ehpcol.place(relx=0.49,rely=0.79, relwidth=0.2)
    count+=1

    idppi=Label(frameadm, text="PHONE IMAGE (path)", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    idppi.place(relx=0.26,rely=0.89)
    ehppi=Entry(frameadm, width=18, bg='black',fg='white', bd = 2, highlightthickness = 2)
    ehppi.place(relx=0.49,rely=0.89, relwidth=0.2)
    count+=1

    def check(e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12,e13,e14,e15,e16,e17):
        try:
            AdminAddModelList = Admin('Add New Model', e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12,e13,e14,e15,e16,e17)
            if type(AdminAddModelList) == tuple and AdminAddModelList[0] == False:
                messagebox.showerror('Recharge', AdminAddModelList[1])
            elif type(AdminAddModelList) == tuple and AdminAddModelList[0] == True:
                messagebox.showinfo('Recharge', 'Successfully added new phone model!\nYour new Phone ID is ' + AdminAddModelList[1])
            else:
                messagebox.showerror('Recharge', 'An error occured, check the input.')
        except Exception:
                pass

    def back():
        frameadm.pack_forget()
        frame.pack()

    adm=Button(frameadm, text="ADD MODEL", fg='white', bg='black', activebackground='black', padx=35, pady=10, font=('Krona One',12),command = lambda: check(str(epm.get()), str(ede.get()), float(ehcp.get()), float(ehsp.get()), str(ehpm.get()), str(ehpc.get()), int(ehpw.get()), str(ehpg.get()), str(ehos.get()), str(ehps.get()), str(ehpr.get()), str(ehpro.get()), str(ehpdi.get()), str(ehpco.get()), str(ehpe.get()), int(ehpcol.get()), str(ehppi.get())),bd=0, highlightthickness=0)
    adm.place(relx=0.80,rely=0.85)
    Button(frameadm, image=back_image, bg="black", bd=0, highlightthickness=0, command=back).place(relx=0.93375, rely=0.02, relwidth=0.05625, relheight=0.1)


def close8():
    frame.pack_forget()
    framereme.pack()

    count = 0
    idpeid=Label(framereme, text="ENTER PHONE ID TO BE REMOVED", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0)
    idpeid.place(relx=0.33,rely=0.36)
    ehidpe=Entry(framereme,bg='black',fg='white', bd = 2, highlightthickness = 2)
    ehidpe.place(relx=0.39,rely=0.42, relwidth=0.2)
    count+=1

    def check(e1):
        try:
            AdminRemoveModelList = Admin('Remove Model', e1)
            if type(AdminRemoveModelList) == tuple and AdminRemoveModelList[0] == False:
                messagebox.showerror('Recharge', AdminRemoveModelList[1])
            elif type(AdminRemoveModelList) != tuple and AdminRemoveModelList == True:
                    messagebox.showinfo('Recharge', 'Successfully removed phone model!')
            else:
                    messagebox.showerror('Recharge', 'An error occured, check the input.')
        except Exception:
                pass

    def back():
        framereme.pack_forget()
        frame.pack()

    reme=Button(framereme, text="REMOVE MODEL", fg='white', bg='black', activebackground='black', padx=35, pady=10, font=('Krona One',12),command = lambda: check(str(ehidpe.get())),bd=0, highlightthickness=0)
    reme.place(relx=0.4,rely=0.55)
    Button(framereme, image=back_image, bg="black", bd=0, highlightthickness=0, command=back).place(relx=0.93375, rely=0.02, relwidth=0.05625, relheight=0.1)


def close9():
    global Capital,sqluser, sqlpass
    Capital = 10000000
    dbo = mysql.connector.connect(host="localhost", user=sqluser, password=sqlpass, database="rechargemobiles")
    c = dbo.cursor()
    c.execute("SELECT PhoneID FROM purchaselog;")
    phoneids = c.fetchall()
    for phoneid in phoneids:
        sqlcommand = 'SELECT PhoneSP from Stock where PhoneID = %s;'
        values = phoneid
        c.execute(sqlcommand, phoneid)
        phoneSellprice = c.fetchone()
        Capital += int(phoneSellprice[0])
    c.execute("SELECT PhoneCP, PhoneCount from Stock;")
    values = c.fetchall()
    for value in values:
        Capital -= value[0]*value[1]
    frame.pack_forget()
    framecap.pack()
    if Capital != 0:
        caplab = Label(framecap, text = "Recharge's current capital: ₹"+str(Capital)+"0", font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0).place(relx = 0.2, rely = 0.45, relwidth=0.6, relheight=0.1)
    else:
        caplab = Label(framecap, text = "Recharge's current capital: ₹"+str(Capital), font=("Krona One",16),bg='black',fg='white',bd=0, highlightthickness=0).place(relx = 0.2, rely = 0.45, relwidth=0.6, relheight=0.1)
 

    def back():
        framecap.pack_forget()
        frame.pack()
        
    Button(framecap, image=back_image, bg="black", bd=0, highlightthickness=0, command=back).place(relx=0.93375, rely=0.02, relwidth=0.05625, relheight=0.1)



def close10():
    frame.pack_forget()
    frameplog.pack()
    global sqluser, sqlpass
    dbo=mysql.connector.connect(host="localhost", user=sqluser, password=sqlpass, database='rechargemobiles')
    c = dbo.cursor()
    c.execute('SELECT * from purchaseLog;')
    purchasedetails = c.fetchall()
    purchasecount = len(purchasedetails)
    if purchasecount > 0:
        style = ttk.Style(frameplog)
        style.theme_use('clam')
        style.configure('Treeview', font = ('Krona One', 10), background="black", fieldbackground="black", foreground="white", highlightthickness = 0, borderwidth = 0)
        style.map('Treeview', background =[('active', 'white')], foreground = [('active', 'black')])
        style.configure("Treeview.Heading", font = ('Krona One', 10), background  = 'black' ,fieldbackground = 'black', foreground = 'white')

        tv = ttk.Treeview(frameplog)

        tv['columns']=('PurchaseID', 'OrderID', 'PurchaseDate', 'PhoneID', 'PhoneModel', 'CustomerID', 'DealerID', 'PaymentMode', 'PurchaseProfit')
        tv.column('#0', width=0, stretch=NO)
        tv.column('PurchaseID', anchor=CENTER, width=120)
        tv.column('OrderID', anchor=CENTER, width=90)
        tv.column('PurchaseDate', anchor=CENTER, width=140)
        tv.column('PhoneID', anchor=CENTER, width=90)
        tv.column('PhoneModel', anchor=CENTER, width=300)
        tv.column('CustomerID', anchor=CENTER, width=120)
        tv.column('DealerID', anchor=CENTER, width=90)
        tv.column('PaymentMode', anchor=CENTER, width=150)
        tv.column('PurchaseProfit', anchor=CENTER, width=80)

        tv.heading('#0', text='', anchor=CENTER)
        tv.heading('PurchaseID', text='PurchaseID', anchor=CENTER)
        tv.heading('OrderID', text='OrderID', anchor=CENTER)
        tv.heading('PurchaseDate', text='Purchase Date', anchor=CENTER)
        tv.heading('PhoneID', text='PhoneID', anchor=CENTER)
        tv.heading('PhoneModel', text='Phone Model', anchor=CENTER)
        tv.heading('CustomerID', text='CustomerID', anchor=CENTER)
        tv.heading('DealerID', text='DealerID', anchor=CENTER)
        tv.heading('PaymentMode', text='Payment Mode', anchor=CENTER)
        tv.heading('PurchaseProfit', text='Profit', anchor=CENTER)

        sb = Scrollbar(frameplog, orient=VERTICAL)
        sb.place(x=1235 , y= 120, height = 20)
        tv.config(yscrollcommand=sb.set)
        sb.config(command=tv.yview)

        PurchaseLog = Admin('View PurchaseLog')
        Records = PurchaseLog[1]
        for i in range(0, len(Records)):
            tv.insert(parent='', index=i, iid=i, text='', values=Records[i])
        tv.place(x = 50 , y = 120)

    else:
        Label(frameplog, text="No purchases done so far.", fg="white", bg="black", font=("Krona One", 14), bd=0, highlightthickness=0).place(relx=0.3, rely=0.45, relwidth=0.4, relheight=0.1)

    def back():
        frameplog.pack_forget()
        frame.pack()
        
    Button(frameplog, image=back_image, bg="black", bd=0, highlightthickness=0, command=back).place(relx=0.93375, rely=0.02, relwidth=0.05625, relheight=0.1)

    
def close():
    frame.pack_forget()
    frame2.pack()
    
    def back():
        frame2.pack_forget()
        frame.pack()

    Button(frame2, image=back_image, bg="black", bd=0, highlightthickness=0, command=back).place(relx=0.93375, rely=0.02, relwidth=0.05625, relheight=0.1)


def exit1():
    frame.pack_forget()
    framehome.pack()

Button(frame, image=back_image, bg="black", bd=0, highlightthickness=0, command=exit1).place(relx=0.93375, rely=0.02, relwidth=0.05625, relheight=0.1)

    
my_labm=Label(frame, text="ADMIN PORTAL", font=('Krona One',40),bg='black',fg='white',bd=0, highlightthickness=0)
my_labm.place(relx=0.27,rely=0.05)

my_lab1=Label(frame, text="ADMINS", font=('Krona One',18),bg='black',fg='white',bd=0, highlightthickness=0)
my_lab1.place(relx=0.1, rely=0.45)
mybut1=Button(frame, text="ADD ADMIN", padx=57, pady=5 , font=('Krona One',10),fg='white',bg='black',command=close1,bd=0, highlightthickness=0)
mybut1.place(relx=0.09, rely=0.51)
mybut2=Button(frame, text="REMOVE ADMIN", padx=40, pady=5 , font=('Krona One',10),fg='white',bg='black',command=close2,bd=0, highlightthickness=0)
mybut2.place(relx=0.09, rely=0.57)


my_lab2=Label(frame, text="PRODUCTS", font=('Krona One',18),bg='black',fg='white',bd=0, highlightthickness=0)
my_lab2.place(relx=0.35,rely=0.45)
mybut3=Button(frame, text="ADD NEW MODEL", padx=78, pady=5 , font=('Krona One',10),fg='white',bg='black',command=close7,bd=0, highlightthickness=0)
mybut3.place(relx=0.34, rely=0.51)
mybut4=Button(frame, text="REMOVE EXISTING MODEL", padx=40, pady=5 , font=('Krona One',10),fg='white',bg='black',command=close8,bd=0, highlightthickness=0)
mybut4.place(relx=0.34, rely=0.57)
mybut5=Button(frame, text="ADD PHONE(s)", padx=84, pady=5 , font=('Krona One',10),fg='white',bg='black',command=close5,bd=0, highlightthickness=0)
mybut5.place(relx=0.34, rely=0.63)
mybut6=Button(frame,text="MODIFY SELLING PRICE", padx=50,pady=5, font=("Krona One",10),fg='white',bg='black',command=close6,bd=0, highlightthickness=0)
mybut6.place(relx=0.34, rely=0.69)


my_lab3=Label(frame,text="CUSTOMERS AND DEALERS", font=('Krona One', 14),bg='black',fg='white')
my_lab3.place(relx=0.68,rely=0.45)

mybut7=Button(frame,text="REMOVE CUSTOMERS", padx=78, pady=5, font=("Krona One",10),fg='white',bg='black',command=close4,bd=0, highlightthickness=0)
mybut7.place(relx=0.67,rely=0.51)
mybut8=Button(frame,text="ADD DEALERS", padx=112, pady=5, font=("Krona One",10),fg='white',bg='black',command=close3,bd=0, highlightthickness=0)
mybut8.place(relx=0.67,rely=0.57)

mybut9=Button(frame, text="VIEW CAPITAL", padx=84, pady=5 , font=('Krona One',10),fg='white',bg='black', command = close9,bd=0, highlightthickness=0)
mybut9.place(relx=0.34, rely=0.27)
mybut10=Button(frame, text="VIEW PURCHASE LOG", padx=45, pady=5 , font=('Krona One',10),fg='white',bg='black', command = close10,bd=0, highlightthickness=0)
mybut10.place(relx=0.34, rely=0.21)

butsee=Button(framehome,image=newsee, command= lambda: passee(ehp),bd=0, highlightthickness=0)
butsee.place(relx=0.65, rely=0.52)
    
def login(e1,e2):
    global labsee, ehi, ehp
    if len(e1)==0:
        messagebox.showerror("Recharge", "Please enter your admin ID.")
    elif len(e2)==0:
        messagebox.showerror("Recharge", "Please enter your admin password.")
        
    else:
        AdminLoginList = Admin('Admin Login', e1,e2)
        #adminloginlist can contain commandcheck or a list of commandcheck and display_text
        if type(AdminLoginList) == tuple and AdminLoginList[0] == False:
            messagebox.showerror('Recharge', AdminLoginList[1])
        if AdminLoginList == True:
            messagebox.showinfo("Recharge", "Admin Login succesful!")
            framehome.pack_forget()
            frame.pack()
            ehi.delete(0,'end')
            ehp.delete(0,'end')

my_labh=Label(framehome, text="ADMIN PORTAL", font=('Krona One',40),bg='black',fg='white')
my_labh.place(relx=0.32,rely=0.05)

loginb=Button(framehome, text="LOGIN", image=login_image, compound="left", fg='white', bg='black', activebackground='black', font=('Krona One',18), command= lambda: login(str(ehi.get()), str(ehp.get())),bd=0, highlightthickness=0)
loginb.place(relx=0.44,rely=0.60)

#running the main loop
root.mainloop()
