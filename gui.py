import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import tksvg as svg
from tkinter import ttk 
from tkinter import filedialog
import os
import socket
import threading
import subprocess
from tkinter import scrolledtext
from tkinter import messagebox
import pyrebase
import time



# firebase config
config = {
    "apiKey": "AIzaSyBlfTCr9XVUtSb2g8NQOe3XbLa_3Gs_REo",
    "authDomain": "dc-connect-b1869.firebaseapp.com",
    "projectId": "dc-connect-b1869",
    "storageBucket": "dc-connect-b1869.appspot.com",
    "messagingSenderId": "55035675965",
    "appId": "1:55035675965:web:a2ce1e11722c6a6889f154",
    "measurementId": "G-9X36Q0NSL7",
    "databaseURL": "https://dc-connect-b1869-default-rtdb.europe-west1.firebasedatabase.app/",
}


# storage_config = {
#     "apiKey": "AIzaSyBlfTCr9XVUtSb2g8NQOe3XbLa_3Gs_REo",
#     "authDomain": "dc-connect-b1869.firebaseapp.com",
#     "projectId": "dc-connect-b1869",
#     "storageBucket": "dc-connect-b1869.appspot.com",
#     "messagingSenderId": "55035675965",
#     "appId": "1:55035675965:web:a2ce1e11722c6a6889f154",
#     "measurementId": "G-9X36Q0NSL7",
#     "databaseURL": "https://console.firebase.google.com/u/0/project/dc-connect-b1869/storage/dc-connect-b1869.appspot.com/files",
# }

firebase = pyrebase.initialize_app(config)
database = firebase.database()
auth = firebase.auth()


# main tkinter gui configs
root = ctk.CTk()
root.geometry("1200x600")
root.title(" DC-Connect")

dark_gray = "#121212"
medium_gray = "#1f1b24"
font = ("Arial", 20)
fontSmall = ("Georgia", 15)
menuBtnFont = ("Candara", 18)

global currentFrame
global usersSectProf
global usersSectProfPhotoImg
global usersSectProfLogin
global usersSectProfPhotoImLogin
usersSectProf = Image.open("profile\dummy.jpg")
usersSectProfPhotoImg = ImageTk.PhotoImage(usersSectProf)


HOST = '127.0.0.1'
PORT = 1234
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def Chat():
    globals()["currentFrame"].destroy()
    chatCont = ctk.CTkFrame(master=mainCont)
    chatCont.grid_rowconfigure(0, weight=2)
    chatCont.grid_rowconfigure(0, weight=1)
    chatCont.grid_columnconfigure(0, weight=1)
    chatCont.grid(row=0, column=0, sticky="news", pady=15, padx=15)

    globals()["currentFrame"] = chatCont
    global message_box
    message_box = scrolledtext.ScrolledText(master=chatCont, background="#1B071C", font=("Georgia", 20), fg="white")
    message_box.grid(row=0, column=0, sticky="news", padx=40, pady=40)

    bottFrame = ctk.CTkFrame(master=chatCont)
    bottFrame.grid_columnconfigure(0, weight=2)
    bottFrame.grid_columnconfigure(1, weight=1)
    bottFrame.grid_rowconfigure(0, weight=1)
    bottFrame.grid(row=1, column=0, sticky="news",)

    global message_textbox
    message_textbox = ctk.CTkEntry(master=bottFrame, font=("Georgia", 20), placeholder_text="Type your message",width=300)
    message_textbox.grid(row=0, column=0, padx=50, pady=12, sticky="we", )

    message_send = ctk.CTkButton(master=bottFrame, text="Send", font=menuBtnFont, border_width=2,  command=SendMessage,
            border_color=("#65BD67"), corner_radius=10, fg_color=("transparent"), hover_color=("black"),border_spacing=5,
            image=svg.SvgImage(file="white_icons/send.svg"),
            )
    message_send.grid(row=0, column=1, padx=12, pady=12, sticky="e")

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

def ConnToServer():

    # try except block
    try:

        # Connect to the server
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        add_message("[SERVER] Successfully connected to the server")
    except:
        pass
        # messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

    username = 'globals()["EmailAddress"]'
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")
    
    Chat()

    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()


def SendMessage():
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, len(message))
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")


def listen_for_messages_from_server(client):

    while 1:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]
            content = message.split('~')[1]

            add_message(f"[{username}] {content}")
            
        else:
            messagebox.showerror("Error", "Message recevied from client is empty")

def CheckInternetConnection():
    host="8.8.8.8"
    port=53
    timeout=3
    
    while True:
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            
            lblWifi.grid(padx=12, pady=50, row=4, column=0, ipadx=28)
            
        except OSError as ex:
            lblNoWifi.grid(padx=12, pady=50, row=4, column=0, ipadx=28)
            
        time.sleep(3)

def Upload():
    if status.get() == 0:
        role = "Donor"
    else:
        role = "Charity Organisation"

    db = firebase.database()
    # storage = firebase.storage()
    data = {
        "Email": EmailAddress,
        "Organisation name": entName.get(),
        "Founder": entFounder.get(),
        "Status": role,
        "entDescription": entDescription.get("0.0", "end"),
    }

    progress()

    try:
        db.child("Users").child(entName.get()).set(data)
        # storage.child("Profiles").child(EmailAddress).set("profile/profile.jpg")
        messagebox.showinfo("Account completed", "Account has been successifuly setup!")
        
        Connect()
    except Exception as e:
        print(e)
        messagebox.showerror("Fail status", "Profile upload failed, try again.")

    progressbar.destroy()

    

def AccInformationViaMenu():
    globals()["currentFrame"].destroy()

    accCont = ctk.CTkFrame(master=mainCont, border_color="#DC70D2", border_width=2,)
    accCont.grid_rowconfigure(0, weight=1)
    accCont.grid_columnconfigure(0, weight=1)
    accCont.grid(row=0, column=0, padx=25, pady=25)

    globals()["currentFrame"] = accCont

    # create the widgets of this frame
    # the 3 Children of the main accCont frame
    global profileFrame
    global canvProfile
    profileFrame = ctk.CTkFrame(master=accCont,)
    profileFrame.grid_rowconfigure(0, weight=1)
    profileFrame.grid_columnconfigure(0, weight=1)
    profileFrame.grid(row=0, column=0, padx=5,)
    

    canvProfile = tk.Canvas(master=profileFrame, width=250, height=250, )
    globals()["usersSectProf"] = globals()["usersSectProf"].resize((250, 250))
    canvProfile.create_image(0,0,anchor="nw", image=globals()["usersSectProfPhotoImg"])
    canvProfile.pack(padx=0, pady=20)

    btnUpload = ctk.CTkButton(master=profileFrame, text="Choose profile picture", font=menuBtnFont, border_width=2,  command=open_file,
        border_color=("#65BD67"), corner_radius=10, fg_color=("transparent"), hover_color=("black"),border_spacing=5,
        image=svg.SvgImage(file="white_icons/upload.svg"),
    )
    btnUpload.pack(padx=5, side="left")

    # charity things!
    charityFrame = ctk.CTkFrame(master=accCont,width =600 )
    charityFrame.grid_rowconfigure((0,1,2,3,), weight=1)
    charityFrame.grid_columnconfigure(0, weight=1)
    charityFrame.grid_columnconfigure(1, weight=2)
    charityFrame.grid(row=0, column=1, sticky="news", padx=20, pady=15)


    # children for the charity frame widget
    lblSidenote = ctk.CTkLabel(master=charityFrame, font=("Arial", 28),text="Input the relevent information to complete your profile", )
    lblSidenote.grid(row= 0, column=0, columnspan=2, padx=12, pady=12)

    global status,entName,entFounder,entDescription
    status =  tk.IntVar(value=0)
    charity = ctk.CTkRadioButton(master=charityFrame, text="Donor",font=font, variable=status, value=0, )
    charity.grid(row=1, column=0,sticky="w", padx=12)
    donor = ctk.CTkRadioButton(master=charityFrame,text="Charity Organisation",font=font, variable=status, value=1)
    donor.grid(row=1, column=1, sticky="we", padx=12, pady=8, columnspan=3)

    lblName = ctk.CTkLabel(master=charityFrame, text="Organisation's Name", font=font)
    lblName.grid(row=2, column=0, sticky="w", padx=12)
    entName = ctk.CTkEntry(master=charityFrame, font=font, width= 30)
    entName.grid(row=2, column=1, sticky="we", padx=12, pady=8, columnspan=3)

    lblFounder = ctk.CTkLabel(master=charityFrame, text="Organisation's Founder", font=font)
    lblFounder.grid(row=3, column=0, sticky="w", padx=12)
    entFounder = ctk.CTkEntry(master=charityFrame, font=font, width= 30)
    entFounder.grid(row=3, column=1, sticky="we", padx=12, pady=8, columnspan=2)

    lblEmail = ctk.CTkLabel(master=charityFrame, text="Organisation's Email Adress", font=font)
    lblEmail.grid(row=4, column=0, sticky="w", padx=12)
    entEmail = ctk.CTkEntry(master=charityFrame, font=font, width= 30, )
    entEmail.insert(0, "globals()['EmailAddress']")
    entEmail.grid(row=4, column=1, sticky="we", padx=12, pady=8, columnspan=2)

    lblDescription = ctk.CTkLabel(master=charityFrame, text="Organisation's Description", font=font)
    lblDescription.grid(row=5, column=0, sticky="w", padx=12)
    entDescription = ctk.CTkTextbox(master=charityFrame, font=font, width= 30)
    entDescription.grid(row=5, column=1, sticky="we", padx=12, pady=8,columnspan=2)

    
    btnUploadProf = ctk.CTkButton(master=charityFrame, text="Upload profile", font=menuBtnFont, border_width=2,  command=Upload,
    border_color=("#65BD67"), corner_radius=10, fg_color=("transparent"), hover_color=("black"),border_spacing=5,
    image=svg.SvgImage(file="white_icons/upload-cloud.svg"),
    )
    btnUploadProf.grid(row=8, column=0, columnspan=2, padx=12, pady=5)
    # waiting for the love
    # summer vibes daloka

def AccInformationViaLogin():
    AccInformationViaMenu()
    globals()["usersSectProfLogin"] = Image.open("profile\dummy.jpg")
    globals()["usersSectProfPhotoImgLogin"] = ImageTk.PhotoImage(globals()["usersSectProfLogin"])
    globals()["usersSectProfLogin"] = globals()["usersSectProfLogin"].resize((250, 250))
    canvProfile.create_image(0,0,anchor="nw", image=globals()["usersSectProfPhotoImgLogin"])

def open_file():
    file_path = filedialog.askopenfilename(initialdir="C:/", title="Select Image", filetypes=[('Image Files', '*.jpg')])
    if file_path is not None:
        img = Image.open(file_path)

        if img is not None:
            curr_directory = os.getcwd()
            os.chdir(curr_directory + "/profile")
            complete_name = os.path.join(os.getcwd(), "profile.jpg")
            img.save(complete_name)
            os.chdir(curr_directory)

    # canvProfile = tk.Canvas(master=profileFrame, width=250, height=250, )
    globals()["usersSectProf"] = Image.open("profile\profile.jpg")
    globals()["usersSectProfPhotoImg"] = ImageTk.PhotoImage(globals()["usersSectProf"])
    globals()["usersSectProf"] = globals()["usersSectProf"].resize((250, 250))
    canvProfile.create_image(0,0,anchor="nw", image=globals()["usersSectProfPhotoImg"])
    # canvProfile.pack(padx=0, pady=20)

def loadConnectProfiles(connCont, row, username,email, description):

    userInfoCont = ctk.CTkFrame(master=connCont, bg_color="#AF76C1", fg_color="#322C34")
    userInfoCont.grid_columnconfigure((0,2), weight=0)
    userInfoCont.grid_columnconfigure(1, weight=1)
    userInfoCont.grid_rowconfigure((1,2,3), weight=1)
    userInfoCont.grid(row=row, column=0, padx=25, pady=5, sticky="we", columnspan=2)

    canvUsersSectProf = tk.Canvas(master=userInfoCont, width=250, height=250,)
    globals()["usersSectProf"] = globals()["usersSectProf"].resize((250, 250))
    canvUsersSectProf.create_image(0,0,anchor="nw", image=globals()["usersSectProfPhotoImg"])
    canvUsersSectProf.grid(row=0, column=0, rowspan=4)

    
    # make the widgets

    lblUsername = ctk.CTkLabel(master=userInfoCont, text=username, font=("Arial", 30))
    lblUsername.grid(row=0, column=1,padx=20,pady=3,sticky="w")

    lblemail = ctk.CTkLabel(master=userInfoCont, text=email, font=("Arial", 18))
    lblemail.grid(row=1, column=1,padx=20,pady=3,sticky="w")
    
    lblCompDescription = ctk.CTkLabel(master=userInfoCont, font=("Arial", 18), text=description, wraplength=700)
    lblCompDescription.grid(row=2, column=1,padx=20,pady=3,sticky="ew", columnspan=3, )
    
    btnDM = ctk.CTkButton(master=userInfoCont, text="Direct message",font=("Candara", 13), border_width=1, command=ConnToServer,
        border_color=("#65BD67"), corner_radius=10, fg_color=("transparent"), hover_color=("black"),border_spacing=5,
        image=svg.SvgImage(file="white_icons/message-circle.svg")
    )
    btnDM.grid(row=3, column=1, pady=1, padx=30,sticky="se" , columnspan=2)

testAccounts = 4
def Connect():

    globals()["currentFrame"].destroy()

    connCont = ctk.CTkScrollableFrame(master=mainCont)
    connCont.grid(row=0, column=0, sticky="news", padx=25, pady=25)
    globals()["currentFrame"] = connCont

    db = firebase.database()
    progress()

    try:
        users = database.child("Users").get()
        # Connect()
    except Exception as e:
        messagebox.showerror("Failure status", "Please check your internet connection.")

    row = 1
    for people in users.each():
        print(people.val())
        print(people.key())
        print(people.val()["Email"])
        

        loadConnectProfiles(globals()["currentFrame"], row, people.key(), people.val()["Email"], people.val()["entDescription"])
        row = row + 1

    progressbar.destroy()

def progress():
    global progressbar
    progressbar = ctk.CTkProgressBar(topBar)
    progressbar.grid(row=0, column=0, padx=20, pady=5, columnspan=3, sticky="news")
    progressbar.configure(mode="indeterminnate")
    progressbar.start()

def Login():
    progress()
    try:
        auth.sign_in_with_email_and_password(entryUsername.get(), entryPass.get())
        messagebox.showinfo("Successiful authentication", "You have been sucessifuly authenticated! \n Please complete your profile. ")
        globals()["EmailAddress"] = entryUsername.get()
        AccInformationViaLogin()
    except Exception as e:
        print(e)
        messagebox.showerror("Failure authentication attempt", "Authentication failed. Invalid username or password")

    progressbar.destroy()

def Signup():
    progress()
    try:
        auth.create_user_with_email_and_password(createUsername.get(), createPass.get())
        messagebox.showinfo("Account created", "Account successifuly created. Please login!")
        signupFrame.destroy()
    # except NewConnectionError as e:
    #     lblError.pack(padx=2, side="right", expand="true")
    except Exception as e:
        print(e)
        messagebox.showerror("Invalid email", "That email address is already in use.")
        
    progress.progressbar.destroy()

def ShowSignup():
    global createUsername, createPass, signupFrame
    signupFrame = ctk.CTkFrame(master=containerLogin, corner_radius=10)
    signupFrame.grid(row=0, column=1,padx= 15, pady=15,sticky="news")

    lblLoginMsg = ctk.CTkLabel(master=signupFrame, text="Signup to DC-Connect", font=("Lucida Console", 30), )
    lblLoginMsg.grid(row=0, column=0, columnspan=2,padx=20,pady=15, sticky="new")

    
    lblUsername = ctk.CTkLabel(master=signupFrame, text="Email: ", font=font,)
    lblUsername.grid(row=1, column=0,padx=20,pady=0,sticky="w")
    createUsername = ctk.CTkEntry(master=signupFrame, width=20, font=font,)
    createUsername.grid(row=2, column=0,padx=20,pady=2, sticky="we", columnspan=2)

    lblPass = ctk.CTkLabel(master=signupFrame, text="Password: ", font=font)
    lblPass.grid(row=3, column=0,padx=20,pady=0,sticky="w")
    createPass = ctk.CTkEntry(master=signupFrame, width=20, font=font)
    createPass.grid(row=4, column=0,padx=20,pady=2, sticky="ew", ipadx=20, columnspan=2)

    btnLogin = ctk.CTkButton(master=signupFrame, text="Signup", font=("Candara", 28), border_width=2, border_color=("#C27EBB"), corner_radius=10, fg_color=("#514854"), hover_color=("black"),border_spacing=5, command=Signup)
    btnLogin.grid(row=5, column=0, pady=20, padx=150, )

root.grid_columnconfigure(0, weight=0)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=1)


# top bar
topBar = ctk.CTkFrame(master=root, height=1)
topBar.grid_rowconfigure(0, weight=1)
topBar.grid_columnconfigure(0, weight=1)
topBar.grid(row=0, column=0, pady=5, padx=5, sticky="new", columnspan= 2)

# side menu
leftMenu = ctk.CTkFrame(master=root, bg_color="#AF76C1", fg_color="#322C34")
leftMenu.grid(row=1, column=0, padx=5, sticky="wens", rowspan=3)

# main container
mainCont = ctk.CTkFrame(master=root,bg_color="#AF76C1", fg_color="#322C34")
mainCont.grid_rowconfigure(0, weight=1)
mainCont.grid_columnconfigure(0, weight=1)
mainCont.grid(row=1, column=1, padx=5, sticky="wens", rowspan=3)

# create the widgets for the top bar
global lblError
lblError = ctk.CTkLabel(master=topBar, text="Connecting, check your network connectivity...", font=font, bg_color="#E3742A",
            image=svg.SvgImage(file="white_icons/alert-octagon.svg")
)

# lblMsg = ctk.CTkLabel(master=topBar, text="DC-Connect", font=font)
# lblMsg.pack(padx=2, pady=8, side="right", expand="true")
# canvTop = tk.Canvas(master=topBar, width=100, height=100,confine="true", background="dark gray")
# topImage = Image.open("images\logo.jpeg")
# topImage = topImage.resize((100, 100))
# topPhotoImage = ImageTk.PhotoImage(topImage)
# canvTop.create_image(0,0,anchor="nw", image=topPhotoImage)
# canvTop.pack(side="left", padx=12)

# progress()

# create side menu items
btnConnect = ctk.CTkButton(master=leftMenu, text="Connect", font=menuBtnFont, command=Connect, border_width=2, border_color=("#C27EBB"), corner_radius=10, fg_color=("#514854"), hover_color=("black"),border_spacing=5,)
btnConnect.grid(padx=12, pady=30, row=0, column=0, ipadx=28)

btnChat = ctk.CTkButton(master=leftMenu, text="Chat", font=menuBtnFont, border_width=2, border_color=("#C27EBB"), corner_radius=10, fg_color=("#514854"), hover_color=("black"),border_spacing=5, command=Chat)
btnChat.grid(padx=12, pady=30, row=1, column=0, ipadx=28)

btnAcc = ctk.CTkButton(master=leftMenu, text="My Account", font=menuBtnFont, border_width=2, border_color=("#C27EBB"), corner_radius=10, fg_color=("#514854"), hover_color=("black"),border_spacing=5, command=AccInformationViaMenu)
btnAcc.grid(padx=12, pady=30, row=2, column=0, ipadx=10)

btnLogout = ctk.CTkButton(master=leftMenu, text="Logout", font=menuBtnFont, border_width=2, border_color=("#C27EBB"), corner_radius=10, fg_color=("#514854"), hover_color=("black"),border_spacing=5,)
btnLogout.grid(padx=12, pady=30, row=3, column=0, ipadx=28)

# login container and widgets.
containerLogin = ctk.CTkFrame(master=mainCont, corner_radius=10, border_color="#DC70D2", border_width=2,)
containerLogin.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)
containerLogin.grid_columnconfigure((0,1), weight=1)
containerLogin.grid_columnconfigure(1, weight=0)
containerLogin.grid(row=0, column=0, padx=5,)
    # contents
canvLogin = tk.Canvas(master=containerLogin, width=500, height=500,confine="true", background="dark gray")
loginImage = Image.open("images\logo0.jpeg")
loginImage = loginImage.resize((500, 500))
loginPhotoImage = ImageTk.PhotoImage(loginImage)
canvLogin.create_image(0,0,anchor="nw", image=loginPhotoImage)

canvLogin.grid(row=0, column=0,padx= 15, pady=15,sticky="news")
miniContLogin = ctk.CTkFrame(master=containerLogin, corner_radius=10,)
miniContLogin.grid(row=0, column=1,padx= 15, pady=15,sticky="news")


lblLoginMsg = ctk.CTkLabel(master=miniContLogin, text="Login to DC-Connect", font=("Lucida Console", 30), )
lblLoginMsg.grid(row=0, column=0, columnspan=2,padx=20,pady=15, sticky="new")

global entryUsername, entryPass, EmailAddress 
lblUsername = ctk.CTkLabel(master=miniContLogin, text="Email: ", font=font)
lblUsername.grid(row=1, column=0,padx=20,pady=0,sticky="w")
entryUsername = ctk.CTkEntry(master=miniContLogin, width=20, font=font, )
entryUsername.grid(row=2, column=0,padx=20,pady=2, sticky="we", columnspan=2)

lblPass = ctk.CTkLabel(master=miniContLogin, text="Password: ", font=font)
lblPass.grid(row=3, column=0,padx=20,pady=0,sticky="w")
entryPass = ctk.CTkEntry(master=miniContLogin, width=20, font=font)
entryPass.grid(row=4, column=0,padx=20,pady=2, sticky="ew", ipadx=20, columnspan=2)

btnLogin = ctk.CTkButton(master=miniContLogin, text="Login", font=("Candara", 28), border_width=2, border_color=("#C27EBB"), corner_radius=10, fg_color=("#514854"), hover_color=("black"),border_spacing=5, command=Login)
btnLogin.grid(row=5, column=0, pady=20, padx=150, )

sepLogin = ttk.Separator(master=miniContLogin, orient='horizontal',)
sepLogin.grid(row=6, column=0, sticky="we", padx=0, columnspan=2)

lblLoginInfo = ctk.CTkLabel(master=miniContLogin, text="New to DC-Connenct?", font=font)
lblLoginInfo.grid(row=7, column=0,padx=20,pady=12,sticky="w")
btnNew = ctk.CTkButton(master=miniContLogin, text="Signup with Google", font=menuBtnFont, border_width=2, command=ShowSignup,
        border_color=("#65BD67"), corner_radius=10, fg_color=("transparent"), hover_color=("black"),border_spacing=5,
        image=svg.SvgImage(file="white_icons/user-plus.svg")
        )
btnNew.grid(row=8, column=0, pady=5, padx=20, sticky="w" )
btnNew = ctk.CTkButton(master=miniContLogin, text="Facebook",font=menuBtnFont, border_width=2,
        border_color=("#65BD67"), corner_radius=10, fg_color=("transparent"), hover_color=("black"),border_spacing=5,
        image=svg.SvgImage(file="white_icons/facebook.svg")
    )
btnNew.grid(row=9, column=0, pady=2, padx=20, sticky="we")

btnNew = ctk.CTkButton(master=miniContLogin, text="Twitter",font=menuBtnFont, border_width=2, 
        border_color=("#65BD67"), corner_radius=10, fg_color=("transparent"), hover_color=("black"),border_spacing=5,
        image=svg.SvgImage(file="white_icons/twitter.svg",)
        )
btnNew.grid(row=10, column=0, pady=0, padx=20, sticky="we",)

globals()["currentFrame"] = containerLogin

# setup the check internet thread
lblNoWifi = ctk.CTkLabel(master=leftMenu,text=" ", image=svg.SvgImage(file="images/wifi-off.svg"),)
lblWifi = ctk.CTkLabel(master=leftMenu,text=" ", image=svg.SvgImage(file="images/wifi.svg"),)

internet_thread = threading.Thread(target=CheckInternetConnection)
internet_thread.daemon = True
internet_thread.start()


root.mainloop()


