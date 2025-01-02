import google.generativeai as genai
from tkinter import TclError
import customtkinter
import customtkinter as ctk 
from customtkinter import *
import json 
import time 
import datetime 
import pytz 
import os 


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

root2 = customtkinter.CTk()
root2.geometry("800x800")
root2.title("CTk AI GUI")

#Global variables 
input_counter = 0 
current_time_seconds = time.time()
utc_time = datetime.datetime.fromtimestamp(current_time_seconds, tz=pytz.utc)
est = pytz.timezone('US/Eastern')
est_time = utc_time.astimezone(est)
formatted_time = est_time.strftime("%I:%M:%S %p")
small_label = None
show_chats = None
settings_label = None


#========= Start up settings ================
file_path = os.path.join("CTk_AI_GUI", "saved_chats", "settings.json")

os.makedirs(os.path.dirname(file_path), exist_ok=True)

try:
    with open(file_path, "r") as file:
        settings_data = json.load(file)
except FileNotFoundError:
    settings_data = [] 
except json.JSONDecodeError:
    settings_data = []  

if settings_data and isinstance(settings_data, list) and isinstance(settings_data[0], dict):
    first_setting = settings_data[0]
    selected_text_color = first_setting.get("text_color", "#00FF00") 
    memory_toggle = first_setting.get("remember_chats", False)  
else:
    selected_text_color = "#00FF00"  
    memory_toggle = False  


def generate_prompt_with_memory(user_input):
    global memory_toggle, chats_data, full_prompt

    ai_start_prompt = "You are a friendly AI assistant, this is a start prompt meant to inform you of the tone you should take. Your goal is to be helpful, friendly, and informative. Now you are going to be given a prompt reminding you of previous chats with the user."
    memory_prompt = ""

    if memory_toggle:
        try:
            with open(file_path, "r") as file:
                chats_data = json.load(file)
        except FileNotFoundError:
            chats_data = []  
        except json.JSONDecodeError:
            chats_data = [] 

        if chats_data:
            memory_prompt = "\n".join(
                [f"User: {chat.get('user_response', 'No user input found')}\nGemini: {chat.get('ai_response', 'No response found')}"
                 for chat in chats_data]
            )

    full_prompt = f"{ai_start_prompt}\nHere is a conversation history with the user:\n{memory_prompt}\nUser: {user_input}\nGemini:"

    return full_prompt

#==================

app_canvas2 = customtkinter.CTkCanvas(root2, width=800, height=800)
app_label2 = customtkinter.CTkLabel(root2, text="LLM Terminal", text_color=selected_text_color,font=("Cascadia Code", 25),pady=20)
app_label2.grid(row=0, column=0)


user_input_var = StringVar()
app_textbox2 = customtkinter.CTkEntry(root2, textvariable=user_input_var, text_color= selected_text_color,font=("Cascadia Code",15),placeholder_text="Enter message")
app_textbox2.grid(row=1,column=0, sticky=EW, padx=10, pady=10)


def gemini_call():
    global response, app_textbox2, user_response, selected_text_color, memory_toggle, full_prompt

    user_response = app_textbox2.get()
    genai.configure(api_key="enter-API-key-here") #This is sensitive data, please be weary of who you share this with! 
    model = genai.GenerativeModel("gemini-1.5-flash")

    if memory_toggle:
        full_prompt = generate_prompt_with_memory(user_response)
    else:
        full_prompt = f"User: {user_response}\nGemini:"
    response = model.generate_content(full_prompt)
    gemini_response(response.text)

def send_message():
    gemini_call()
    app_textbox2.delete(0, END)

app_button2 = customtkinter.CTkButton(root2, font=("Cascadia Code", 15),text="Send", fg_color="gray", hover_color="lightgray",height=30,command=send_message)
app_button2.grid(row=2, column=0, sticky=EW, padx=10, pady=10)

gemini_label2 = customtkinter.CTkLabel(root2, font=("Cascadia Code",20),text_color=selected_text_color,text="AI Output:", pady=5, width=800)
gemini_label2.grid(row=3, column=0, sticky=EW)

gemini_output2 = ctk.CTkTextbox(root2, width=700, height=500, text_color=selected_text_color, fg_color="gray10",font=("Cascadia Code", 15),state="disabled", wrap="word")
gemini_output2.grid(row=4, column=0, columnspan=2, pady=10, padx=20)


def gemini_response(response_text):
    save_chats()
    gemini_output2.configure(state="normal")  
    gemini_output2.delete("1.0", ctk.END) 
    gemini_output2.insert("1.0", response_text) 
    gemini_output2.configure(state="disabled")



def save_chats():
    global input_counter, user_input_var, response, user_response, formatted_time, chats_data, file_path
    input_counter += 1 

    file_path = os.path.join("CTk_AI_GUI", "saved_chats", "chats.json")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    chat_entry = {
        "user_response": user_response, 
        "ai_response": response.text, 
        "timestamp": formatted_time,
        "timezone": "EST"
    }

    try:
        with open(file_path, "r") as file:
            chats_data = json.load(file)
    except FileNotFoundError:
        chats_data = []  

    chats_data.append(chat_entry)

    with open(file_path, "w") as file:  
        json.dump(chats_data, file, indent=4)
        
    print(f"Saved chat: {chat_entry}")

def clear_saved_chats():
    global chats_data, file_path
    try:
        with open(file_path, "w") as file:
            json.dump([], file, indent=4)
    except FileNotFoundError:
        print("No data to delete.")


isclicked = 0
root3 = None 
root4 = None 
def on_option_click(choice):
    global isclicked, root3, chats_data, file_path, root4, settings_label, small_label, show_chats, switch_var
    print(f"Option clicked {choice}")
    isclicked += 1

    file_path = os.path.join("CTk_AI_GUI", "saved_chats", "chats.json")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    if choice == "Quit":
        root2.destroy()
    elif choice == "Past Chats" and isclicked == 1:
        if root3 is None or not root3.winfo_exists():
            isclicked -= 1
            root3 = ctk.CTkToplevel(root2)
            root3.geometry("300x500")
            root3.title("Chat History")

            small_label = ctk.CTkLabel(root3, text="Past Chats", font=("Cascadia Code", 20, "underline"), text_color=selected_text_color)
            small_label.grid(row=0, column=0, pady=10)
            try:
                with open(file_path, "r") as file:
                    chats_data = json.load(file)
            except FileNotFoundError:
                chats_data = [] 

            show_chats = ctk.CTkTextbox(root3, wrap="word",  width=300, height=400, text_color=selected_text_color, fg_color="gray10")
            formatted_chats = ""
            for chat in chats_data:
                formatted_chats += f"User: {chat['user_response']}\nGemini: {chat['ai_response']}\nTimestamp:{chat['timestamp']}\nTimezone:{chat['timezone']}\n"

            show_chats.insert("1.0", formatted_chats)
            show_chats.grid(row=3,column=0)
    
    elif choice =="Past Chats" and isclicked > 1:
        pass

    elif choice =="Settings" and isclicked == 1: 
        if root4 is None or not root4.winfo_exists():
            isclicked -=1 
            root4 = ctk.CTkToplevel(root2)
            root4.geometry("300x500")
            root4.title("App Settings")

            settings_label = ctk.CTkLabel(root4, text="Settings", font=("Cascadia Code", 25), text_color=selected_text_color, pady=10)
            settings_label.grid(row=0, column=0)

            clear_chats = ctk.CTkButton(root4, text="Clear Chats", fg_color="gray", hover_color="lightgray", command=clear_saved_chats)
            clear_chats.grid(row=1, column=0, pady=5)

            red_color_var = customtkinter.StringVar(value="red")
            green_color_var = customtkinter.StringVar(value="green")
            blue_color_var = customtkinter.StringVar(value="blue")
            purple_color_var = customtkinter.StringVar(value="purple")
            text_colors = ctk.CTkOptionMenu(root4, values=["Text Color","red", "green", "blue", "purple"], fg_color="gray", button_hover_color="lightgray", command=switch_color)
            text_colors.grid(row=2, column=0, pady=5)

            switch_var = customtkinter.StringVar(value="on" if memory_toggle else "off")
            switch = customtkinter.CTkSwitch(root4, text="Remember Chats", command=change_in_settings, variable=switch_var, onvalue="on", offvalue="off")
            switch.grid(row=3, column=0)




def change_in_settings():
    global selected_text_color, memory_toggle, switch_var

    memory_toggle = switch_var.get() == "on"

    file_path = os.path.join("CTk_AI_GUI", "saved_chats", "settings.json")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    settings_change = {
        "text_color": selected_text_color, 
        "remember_chats": memory_toggle
    }
    try:
        with open(file_path, "r") as file:
            settings_data = json.load(file)
    except FileNotFoundError:
        settings_data = []  

    updated = False
    for setting in settings_data:
        if "text_color" in setting:  
            setting["text_color"] = settings_change["text_color"]
            setting["remember_chats"] = settings_change["remember_chats"]
            updated = True
            break
    if not updated:
        settings_data.append(settings_change)

    with open(file_path, "w") as file:
        json.dump(settings_data, file, indent=4)

    reload_settings()


def reload_settings():
    global selected_text_color, memory_toggle, switch_var

    file_path = os.path.join("CTk_AI_GUI", "saved_chats", "settings.json")

    try:
        with open(file_path, "r") as file:
            settings_data = json.load(file)
    except FileNotFoundError:
        settings_data = []

    if settings_data and isinstance(settings_data[0], dict): 
        first_setting = settings_data[0]
        selected_text_color = first_setting.get("text_color", "#00FF00")  
        memory_toggle = first_setting.get("remember_chats", False)  

    if 'switch_var' in globals():
            switch_var.set("on" if memory_toggle else "off")
            
            if root4 and root4.winfo_exists():
                for child in root4.winfo_children():
                    if isinstance(child, customtkinter.CTkSwitch):
                        if memory_toggle:
                            child.select()
                        else:
                            child.deselect()

    apply_settings()

    
def switch_color(color):
    global selected_text_color
    if color == "red":
        selected_text_color = "red"
    elif color =="green":
        selected_text_color = "#00FF00"
    elif color =="blue":
        selected_text_color = "blue"
    elif color == "purple":
        selected_text_color = "purple"
    change_in_settings()


def apply_settings():
    global selected_text_color, small_label

    if app_label2:
        app_label2.configure(text_color=selected_text_color)
    if gemini_label2:
        gemini_label2.configure(text_color=selected_text_color)
    if gemini_output2:
        gemini_output2.configure(text_color=selected_text_color)
    if app_textbox2:
        app_textbox2.configure(text_color=selected_text_color)


    try:
        if 'settings_label' in globals() and settings_label and root4 and root4.winfo_exists():
            settings_label.configure(text_color=selected_text_color)
    except (AttributeError, TclError):
        pass

    try:
        if 'small_label' in globals() and small_label and root3 and root3.winfo_exists():
            small_label.configure(text_color=selected_text_color)
    except (AttributeError, TclError):
        pass

    try:
        if 'show_chats' in globals() and show_chats and root3 and root3.winfo_exists():
            show_chats.configure(text_color=selected_text_color)
    except (AttributeError, TclError):
        pass


app_menu_button_var = customtkinter.StringVar(value="Past Chats")
app_menu_button_var2 = customtkinter.StringVar(value="Quit")
app_menu_button = customtkinter.CTkOptionMenu(root2, fg_color="#333333", button_color="gray",  button_hover_color="lightgray",values=["Settings","Past Chats", "Quit"], variable=app_menu_button_var, command=on_option_click)
app_menu_button.place(x=650, y=10)


root2.mainloop()

