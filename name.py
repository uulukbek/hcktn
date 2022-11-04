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
        self.old_name = old_name
        self.new_name = new_name
        
        user_data = [username for username in data if username['name'] == old_name]
        
        if user_data:
            newName = [username for username in data if username['name'] == old_name]
            if newName: 
                raise Exception("Пользователь с таким именем уже существует, попробуйте еще раз!")
        else: 
            raise Exception("Нет такого зарегистрированного юзера в базе данных!")



class User(RegisterMixin, LoginMixin, ChangePasswordMixin): 
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
    
 
obj = User("Nurik", "YAnetakoizadrotkakya1")
obj2 = User("Danchik", "Fkljflsjdflr44343")
print(obj.register())
print(obj2.register())