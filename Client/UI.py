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
            client._send({'_transfer':{"UserInformations":{'Username':self.user.name,'Message':self.message.text,'Destinator':self.destinator}}})

    def connected_people_list(self,instance):
        if self.connected:
            print("contact selectionné",self.connecteds.text)
            data = client._connectedPeople()
            self.connecteds.values = data.values()


               
    def page_manager(self,instance):
        pages = {'_login':'loginScreen','_contact':"contactScreen",'_send':'sendScreen'}
        sm.current = pages[instance.id]
    
    def contact_selector(self,instance):
        if self.connecteds.text != "Connected Peoples": # on verifie qu'il ai bien selectionner un contact valable dans le spinner
            selected_contact = self.connecteds.text
            print("SELECTED CONTACT:",selected_contact)
            self.page_manager(instance)   
            self.destinator.text = selected_contact 


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
        login_btn = Button(text='Sign In',size_hint=(1,0.2),color=white,background_color=black)
        login_btn.id="_contact"
        self.info = Label(text='',size_hint=(1,0.2),color=white)
        login_btn.bind(on_press=self.login)


        login_layout.add_widget(image)
        login_layout.add_widget(username_container)
        login_layout.add_widget(password_container)
        login_layout.add_widget(login_btn)
        login_layout.add_widget(self.info)

        #adding components to screen 
        _loginScreen.add_widget(login_layout)





        """
                SCREEN FOR CONTACTS
        """
        _contactScreen = Screen(name="contactScreen")
        contact_layout = BoxLayout(orientation='vertical')#size_hint=(0.8,0.6),pos_hint={'center_x':0.5,'center_y':0.5}


        #HEADER
        header_content = BoxLayout(orientation="horizontal",size_hint=(0.6,0.2),pos_hint={'center_x':0.5,'center_y':0.5})

        self.connecteds = Spinner(text="Connected Peoples",values= [],color=blue,background_color=white)#,size_hint=(0.3,0.2)
        self.connecteds.bind(on_press=self.connected_people_list)
 

        select_contact_btn = Button(text="Choisir",background_color=black)#,size_hint=(0.3,0.2)
        select_contact_btn.id = "_send"
        select_contact_btn.bind(on_press=self.contact_selector)

        leave = Button(text="Quit app",color=white,background_color=black)
        leave.id = "_Exit"
        leave.bind(on_press=self.disconnect_from_server)
        
        header_content.add_widget(self.connecteds)
        header_content.add_widget(select_contact_btn)
        header_content.add_widget(leave)

        #BODY
        body_content = BoxLayout(orientation="horizontal")
        L = Label(text='HELLO')
        body_content.add_widget(L)

        # FOOTER
        footer_content = BoxLayout(orientation="horizontal")

        previous_btn = Button(text='Retour au login',size_hint=(1,0.2),color=white,background_color=black)
        previous_btn.id = '_login'
        previous_btn.bind(on_press=self.page_manager)

        footer_content.add_widget(previous_btn)


        # END OF LAYOUT
        contact_layout.add_widget(header_content)
        contact_layout.add_widget(body_content)
        contact_layout.add_widget(footer_content)
        _contactScreen.add_widget(contact_layout)


        """
                SCREEN FOR SENDING MESSAGES
        """
        _sendScreen = Screen(name="sendScreen")


        send_Layout = BoxLayout(orientation="vertical")



        sender_label = Label(text="Envoyer un message",font_size=25)
        self.message = TextInput(text="",multiline=False,font_size=20,size_hint=(1,0.5))
        receiver_label = Label(text="à",font_size=25)
        self.destinator = Label(text="undefined",font_size=25)
        
        send_btn = Button(text='Envoyer',size_hint=(1,0.2),color=white,background_color=black)
        send_btn.bind(on_press=self.send)
        send_info = Label(text='',size_hint=(1,0.2),color=white)

        previous_btn = Button(text='Retour',size_hint=(1,0.2),color=white,background_color=black)
        previous_btn.id = '_contact'
        previous_btn.bind(on_press=self.page_manager)

        send_Layout.add_widget(sender_label)
        send_Layout.add_widget(self.message)
        send_Layout.add_widget(receiver_label)
        send_Layout.add_widget(self.destinator)
        send_Layout.add_widget(previous_btn)

        send_Layout.add_widget(send_btn)
        send_Layout.add_widget(send_info)

        _sendScreen.add_widget(send_Layout)

        """
                __________________________________________________________________________________________________________________________________________________________________
        """


        sm.add_widget(_loginScreen)
        sm.add_widget(_sendScreen)
        sm.add_widget(_contactScreen)

        return sm


UserApp().run()