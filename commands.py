import pyrebase

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

firebase = pyrebase.initialize_app(config)
database = firebase.database()

data = {"name": "dee",
        "age": 44,
        "degree": "computer science",
        "college": "NUST"
    }

# database.child("Users").child("Comp2").set(data)

# try:
#     database.child("Users").child("Comp2").set(data)
#     query = database.child("Users").get()
# except Exception as e:
#     print(e)


# query.each()
users = database.child("Users").get()
for people in users.each():
    print(people.val())
    print(people.key())
    print(people.val()["Email"])

