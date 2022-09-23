from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image




"""
_____________________________________________________________________________________CLIENT SOCKET PART_____________________________________________________________________________________
"""
from Client_Handling import Client_Handling
from User import User 
import sys





running = True



"""

_____________________________________________________________________________________INTERFACE PART_____________________________________________________________________________________ 

"""
white = (1,1,1,1)
red = (1,0,0,1)
black = (0,0,0,0)
green = [0, 1, 0, 1] 
blue = [0, 0, 1, 1] 
purple = [1, 0, 1, 1] 

sm = ScreenManager()
client = Client_Handling()




class UserApp(App):
    def login(self,instance):
        """faire une form validation avec regex"""
        #stocker les users dans un json
        if (len(self.username.text)!=0) and (len(self.password.text)>5):
            self.page_manager(instance)
            self.user = User(self.username.text,self.password.text)
            print(self.user)
            self.registerClient_ToServer()
            
        else: 
            self.info.text = "Infos non valides"

    def connect_to_server(self):
        client._connect_to_server()
        self.connected = True
    
    def registerClient_ToServer(self):
        if self.connected:
            client._send({'_authentification':{"UserInformations":{"Username":self.user.name,"Password":self.user.password}}})
            print("Username envoyé au SERVEUR")
        else:
            print("Not connected")


    def disconnect_from_server(self,instance):
        client._disconnect_from_server(self.user)
        sys.exit()
    
    def send(self,instance):
        # verifier qu'on soit connecter au serveur 
        if self.connected:
            client._send({'_transfer':{"UserInformations":{'Username':self.username.text,'Message':self.message.text,'Destinator':self.destinator.text}}})

    def connected_people_list(self,instance):
        if self.connected:
            data = client._connectedPeople()
            self.connecteds.values = data.values()

               

    def page_manager(self,instance):
        pages = {'_login':'loginScreen','_send':'sendScreen'}
        sm.current = pages[instance.id]


    def build(self):
        #Initialisation des variables 
        self.contacts = []
        self.ids = {}
        self.connected = False
        self.connect_to_server()
        """
                SCREEN FOR LOGIN 
        """
        #Home Screen
        _loginScreen = Screen(name="loginScreen")
        login_layout = BoxLayout(orientation='vertical',size_hint=(0.5,0.6),pos_hint={'center_x':0.5,'center_y':0.5})

        image = Image(source="logo.jfif")
        #USERNAME
        username_container = BoxLayout(orientation='vertical',size_hint=(1,0.2))
        self.username = TextInput(text='User',multiline=False,font_size=20)#background_color=black,foreground_color=white,cursor_color=white,
        
        
        username_container.add_widget(self.username)
  
        #PASSWORD
        password_container = BoxLayout(orientation='vertical',size_hint=(1,0.2))
        self.password = TextInput(text='Password',multiline=False,font_size=20)#background_color=black,foreground_color=white,cursor_color=white,
        
        password_container.add_widget(self.password)

        #SEND BUTTON
        send_btn = Button(text='Sign In',size_hint=(1,0.2),color=white,background_color=black)
        send_btn.id="_send"
        self.info = Label(text='',size_hint=(1,0.2),color=white)
        send_btn.bind(on_press=self.login)


        login_layout.add_widget(image)
        login_layout.add_widget(username_container)
        login_layout.add_widget(password_container)
        login_layout.add_widget(send_btn)
        login_layout.add_widget(self.info)

        #adding components to screen 
        _loginScreen.add_widget(login_layout)





        """
                SCREEN FOR SENDING MESSAGES
        """
        _sendScreen = Screen(name="sendScreen")
        send_layout = BoxLayout(orientation='vertical',size_hint=(0.8,0.6),pos_hint={'center_x':0.5,'center_y':0.5})#pos_hint={'center_x':0.5,'center_y':0.5}

        header_buttons = BoxLayout(orientation="horizontal")

       
        persons = []

        self.connecteds = Spinner(text="Connected Peoples",values= persons,size_hint=(0.3,0.2),color=green,background_color=white)
        self.connecteds.bind(on_press=self.connected_people_list)




        login = Button(text="Quit app",size_hint=(0.3,0.2),color=blue,background_color=white)
        login.id = "_Exit"
        # login.bind(on_press=self.page_manager)
        login.bind(on_press=self.disconnect_from_server)
        header_buttons.add_widget(self.connecteds)
        header_buttons.add_widget(login)


        sender_label = Label(text="Envoyer un message",font_size=25)
        self.message = TextInput(text="",multiline=False,font_size=20,size_hint=(1,0.5))
        receiver_label = Label(text="à",font_size=25)
        self.destinator = TextInput(text="destinataire",multiline=False,font_size=20,size_hint=(1,0.5))
        send_btn = Button(text='Envoyer',size_hint=(1,0.2),color=white,background_color=black)
        send_btn.bind(on_press=self.send)
        self.send_info = Label(text='',size_hint=(1,0.2),color=white)



        send_layout.add_widget(header_buttons)
        # send_layout.add_widget(self.connected_people_list)
        send_layout.add_widget(sender_label)
        send_layout.add_widget(self.message)
        send_layout.add_widget(receiver_label)
        send_layout.add_widget(self.destinator)
        send_layout.add_widget(send_btn)
        send_layout.add_widget(self.send_info)

        _sendScreen.add_widget(send_layout)


        sm.add_widget(_loginScreen)
        sm.add_widget(_sendScreen)




        return sm


UserApp().run()