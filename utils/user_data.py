import json

class UserData:
    def __init__(self, uid):
        self.uid = uid
        self.u_name = "IW Citizen"
        #self.u_avatar = "https://cdn.discordapp.com/attachments/1096933532032581693/1176470799008399450/iw_logo.png"
        self.u_achv = "Newcomer"
        self.u_lv = 1
        self.u_from = "🌏 Earth"
        self.u_home = "🏠 IW"
        self.u_joindate = 0
        self.u_fame = 0
        self.u_tech = "🔹"
        self.u_blc = 1000 # Ira

    def get(self):
        user_data = self._load_data()
        if str(self.uid) in user_data:
            user = user_data[str(self.uid)]
            for key, value in vars(self).items():
                setattr(self, key, user.get(key, value))
        else:
            # Nếu uid không có trong dữ liệu, lưu giá trị mặc định vào file
            user_data[str(self.uid)] = {key: value for key, value in vars(self).items()}
            self._save_data(user_data)

    def set(self, variable, new_value):
        if variable in self.__dict__:
            setattr(self, variable, new_value)
            user_data = self._load_data()
            if str(self.uid) in user_data:
                user_data[str(self.uid)][variable] = new_value
            else:
                # Nếu uid không tồn tại, tạo một bản ghi mới
                user_data[str(self.uid)] = {variable: new_value}
            self._save_data(user_data)

    def update(self, variable, value):
        self.get()  # Load existing data
        if variable in self.__dict__:
            current_value = getattr(self, variable)
            setattr(self, variable, current_value + value)
            user_data = self._load_data()
            if str(self.uid) in user_data:
                user_data[str(self.uid)][variable] = current_value + value
            else:
                # Nếu uid không tồn tại, tạo một bản ghi mới
                user_data[str(self.uid)] = {variable: current_value + value}
            self._save_data(user_data)

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
#uid = 123456789  # Replace with the actual user ID
#user_instance = UserData(uid)

# Get user data
#user_instance.get()
#print(f"User ID: {uid}, Joindate: {user_instance.u_joindate}, ITR: {user_instance.u_itr}, Balance: {user_instance.u_blc}")

# Update and save data
#user_instance.update('u_itr', 10)
#user_instance.update('u_blc', -5)

# Get and print updated data
#user_instance.get()
#print(f"User ID: {uid}, Joindate: {user_instance.u_joindate}, ITR: {user_instance.u_itr}, Balance: {user_instance.u_blc}")
