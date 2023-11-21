import json

class UserData:
    def __init__(self, uid):
        self.uid = uid
        self.u_name = "IW Citizen"
        self.u_avatar = ""
        self.u_joindate = 0
        self.u_itr = 0
        self.u_blc = 0

    def get(self):
        user_data = self._load_data()
        if str(self.uid) in user_data:
            user = user_data[str(self.uid)]
            self.u_joindate = user.get('u_joindate', 0)
            self.u_itr = user.get('u_itr', 0)
            self.u_blc = user.get('u_blc', 0)

    def set(self):
        user_data = self._load_data()
        user_data[str(self.uid)] = {
            'u_joindate': self.u_joindate,
            'u_itr': self.u_itr,
            'u_blc': self.u_blc
        }
        self._save_data(user_data)

    def update(self, variable, value):
        self.get()  # Load existing data
        if variable in self.__dict__:
            current_value = getattr(self, variable)
            setattr(self, variable, current_value + value)
            self.set()  # Save updated data

    def _load_data(self):
        try:
            with open('user_files/user_data.json', 'r', encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
        # Create a new file if not found
            with open('user_files/user_data.json', 'w') as file:
                json.dump({}, file, indent=4)
            return {}

    def _save_data(self, data):
        with open('user_files/user_data.json', 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4)

# Example usage:
uid = 123456789  # Replace with the actual user ID
user_instance = UserData(uid)

# Get user data
user_instance.get()
print(f"User ID: {uid}, Joindate: {user_instance.u_joindate}, ITR: {user_instance.u_itr}, Balance: {user_instance.u_blc}")

# Update and save data
user_instance.update('u_itr', 10)
user_instance.update('u_blc', -5)

# Get and print updated data
user_instance.get()
print(f"User ID: {uid}, Joindate: {user_instance.u_joindate}, ITR: {user_instance.u_itr}, Balance: {user_instance.u_blc}")
