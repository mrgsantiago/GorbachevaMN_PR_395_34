from kivy.config import Config
Config.set('graphics','resizable',0)
from kivy.app import App
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
import sqlite3
from sqlite3 import Error
from kivy.uix.popup import Popup

class MessageBox(Popup):
    def openPopup(self,TextMessage):
        message = MessageBox()
        message.messageForText.text = TextMessage
        message.open()
        
class WindowManager(ScreenManager):
    pass

class Autorization(Screen):
    def UserInput(self):
        path = 'Users.db'
        connection = None
        message = MessageBox()
        if  self.enteredLogin.text and  self.enteredPassword.text :
            try:
                connection = sqlite3.connect(path)
                cursor = connection.cursor()
                cursor.execute("SELECT Password FROM User WHERE Login = :login ",{"login":self.enteredLogin.text })
                CheckExistLogin = cursor.fetchall()
                if CheckExistLogin:
                    
                    if CheckExistLogin[0][0]== self.enteredPassword.text:
                        message.openPopup('Вы успешно вошли!')
                    else:
                        message.openPopup('Неверный пароль!')
                else:
                    message.openPopup('Пользователя с таким логином не существует!')
            except Error as e:
                message.openPopup(f'Возникла ошибка: {e}')
            finally:
                connection.close()
        else:
            message.openPopup('Вы не ввели данные!')


class Registration(Screen):

    def InsertUser(self):
        path = 'Users.db'
        connection = None
        message = MessageBox()
        if  self.userSurname.text and  self.userName.text and  self.userLogin.text and  self.userPassword.text:
            if self.userRepeatPass.text == self.userPassword.text:
                try:
                    connection = sqlite3.connect(path)
                    cursor = connection.cursor()
                    cursor.execute("SELECT Name FROM User WHERE Login = :login ",{"login":self.userLogin.text })
                    CheckExist = cursor.fetchall()
                    if not CheckExist:
                        cursor.execute("INSERT INTO User (Surname,Name,MiddleName,Login,Password) VALUES (:Surname,:Name,:MiddleName,:Login,:Password)",{"Surname":self.userSurname.text,"Name":self.userName.text,"MiddleName":self.userMiddleName.text,"Login":self.userLogin.text,"Password":self.userPassword.text})
                        connection.commit()
                        message.openPopup('Вы успешно зарегистрировались!')
                    else:
                        message.openPopup('Пользователь с таким логином уже существует!')
                except Error as e:
                    message.openPopup(f'Возникла ошибка: {e}')
                finally:
                    connection.close()
            else:
                message.openPopup('Пароли не равны!')
        else:
            message.openPopup('Вы не ввели данные!')

Window.size = (360,600)
Window.clearcolor = (.89,.87,.85, 1)
kv = Builder.load_file("style.kv")
class MainApp(App):
   
    def build(self):
        return kv


if __name__=="__main__":
    
    MainApp().run()    