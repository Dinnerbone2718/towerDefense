import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
import socket
import time
import uuid


script_dir = os.path.dirname(os.path.abspath(__file__))
prefix = f"{script_dir}/"

# Path to your service account key file
service_account_key = f"{prefix}towerdefense-ce12a-firebase-adminsdk-pz797-cafdf36b1a.json"

# Initialize the Firebase Admin SDK
cred = credentials.Certificate(service_account_key)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://towerdefense-ce12a-default-rtdb.firebaseio.com/'
})

# Function to write user data to Firebase
def writeUserData(user_id, host, time, data,):
    ref = db.reference(f'Lobby1/{user_id}')
    ref.set({
        'host': host,
        'time': time,
        'data': data
    })
    print('User data written successfully!')

# Function to read user data from Firebase
def readUserData(user_id):
    ref = db.reference(f'Lobby1/{user_id}')
    data = ref.get()
    if data:
        return data
    else:
        print('No data available for user:', user_id)


def removeUserData(user_id):
    ref = db.reference(f'Lobby1/{user_id}')
    ref.delete()  # Deletes the node for the specified user
    print(f'User {user_id} removed from the database successfully!')


def removeAFK():
    ref = db.reference('Lobby1') 
    data = ref.get()  
    
    if data:  
        for key, value in data.items():
            if isinstance(value, dict) and "time" in value and time.time() - value["time"] > 10:
                ref.child(key).delete() 


#writeUserData(uuid.uuid4(), False, time.time(), "N/A")

print(readUserData("593ebe7b-adc1-499d-98ef-2775b7f47a16")["host"])