import re
import bcrypt
import os

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def validEmail(email):
        formatEmail = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(formatEmail, email) is not None
    
    @staticmethod
    def validPassword(password):
        if len(password) < 8:
            return False, "Password must be at least 8 characters!"
        if not re.search(r'[A-Z]', password):  
            return False, "Password must contain uppercase letters!"
        if not re.search(r'[a-z]', password):  
            return False, "Password must contain lowercase letters!"
        if not re.search(r'[0-9]', password): 
            return False, "Password must contain numbers!"
        return True, "Password is valid"

    @staticmethod
    def hashPassword(password):
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


class ManageAuth:
    def __init__(self):
        self.users = self.loadUsers()

    def loadUsers(self):
        users = {}
        try:
            with open('data/Users.txt', 'r') as file:
                for line in file:
                    line = line.strip()
                    if ' | ' in line:
                        parts = line.split(' | ')
                        if len(parts) == 3:
                            username, email, password = parts
                            users[email] = User(username, email, password)
        except FileNotFoundError as e:
            print(f"Users.txt file not found: {e}")
        except Exception as e:
            print(f"Error loading user data: {e}")
        
        print(f"Total users loaded: {len(users)}")
        return users
    
    def saveUsers(self):
        try:
            os.makedirs('data', exist_ok=True)
            with open('data/Users.txt', 'w') as file:
                for user in self.users.values():
                    userData = f"{user.username} | {user.email} | {user.password}\n"
                    file.write(userData)
        except Exception as e:
            print(f"Error saving user data: {e}")