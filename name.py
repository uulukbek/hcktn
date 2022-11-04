import json
file = open('user.json', encoding='utf-8')
data = json.load(file)


class RegisterMixin:
    def register(self):
        max_id = max([i['id'] for i in data])
        user_data = [username for username in data if username['name'] == self.username]
        
        if user_data:
            raise Exception('Такой юзер уже существует')
        
        else:
            data.append ({
                'id': max_id + 1,
                'name': self.username,
                'password': self.password
            })
            
            json.dump(data, open('user.json', 'w'))
            return 'Successfully registered'
        

class LoginMixin: 
    def login(self, name, password):
        self.name = name 
        self.password = password
         
        user_data = [username for username in data if username['name'] == name]
        
        if user_data:  
            user_index = data.index(user_data[0])
            if data[user_index]['password'] == password: 
                return "Вы успешно залогинились"
            raise Exception ("Неверный пароль")    
        return ("Нет такого юзера в базе данных")
    

class ChangePasswordMixin: 
    def change_password(self,name, old_password, new_password): 
        self.name = name 
        self.old_password = old_password
        self.new_password = new_password
        
        user_data = [username for username in data if username['name'] == name]
        
        if user_data:
            user_index = data.index(user_data[0])
            if data[user_index]['password'] == old_password:
                data[user_index]['password'] = input('')
                
        
class ChangeUsernameMixin:
    def change_name(self, old_name, new_name):
        with open('user.json') as file:
            data = json.load(file)
        
        if old_name in [i['name'] for i in data if i['name'] == old_name]:
            while new_name in [i['name'] for i in data if i['name'] == new_name]:
                print('Пользователь с таким именем уже существует!')
                new_name = input('Enter another name: ')
            data[data.index([i for i in data if i['name'] == old_name][0])]['name'] = new_name
        
            with open('user.json', 'w') as file:
                json.dump(data, file)
                return 'Username changed successfully!'
        else:
            raise Exception('Нет такого зарегистрированного юзера в БД!')
        
    
class CheckOwnerMIxin:
    def check(self, owner): 
        with open('user.json') as file:
            data = json.load(file)
              
        if owner in [i['name'] for i in data]:
            print('Post created')
        else:
            raise Exception('Нет такого пользователя!')
    


class User(RegisterMixin, LoginMixin, ChangePasswordMixin,ChangeUsernameMixin,): 
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = self.validate_password(password)


    def validate_password(self, password): 
        self.password = password
        if len(self.password) < 8: 
            raise Exception ("Пароль слишком короткий")
        elif self.password.isdigit() or self.password.isalpha(): 
            raise Exception("Пароль должен состоять из букв и цифр")
        return password
    
class Post(CheckOwnerMIxin):
    def __init__(self, title, description, price, quantity, owner) -> None:
        self.title = title
        self.descripton = description
        self.price = price
        self.quantity = quantity
        self.owner = self.check(owner)
