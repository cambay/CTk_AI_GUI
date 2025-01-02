CTk AI Wrapper

This is a Python-based graphical user interface (GUI) for interacting with the Google Gemini API using the customtkinter library for the front end and the google.generativeai API for generating content. It includes features for saving chat history, managing settings, and memory-based interactions with the AI.

*IMPORTANT NOTE* Some of the variables and functions in the main file were initially named as "gemini" as this was initially tested with Gemini API, but it will possibly
				 work with other large language models, I have yet to test it out. 

Features
	•	User Interface: Built with customtkinter, a modern wrapper for tkinter.
	•	Chat History: Allows users to view and store past conversations with the AI.
	•	Customizable Settings: Users can customize text colors and toggle memory functionality for saving chat history.
	•	API Integration: Utilizes the Google Gemini API for generating AI responses.
	•	Save/Load Data: Conversations and settings are saved in JSON files.

Installation
	1.	Install Dependencies
Python 3.8 or higher. First, install the required Python packages:

pip install customtkinter google-generativeai pytz


	2.	Obtain API Key
You need to set up a Google Gemini API key. Replace the api_key in the code with your own API key. (Or potentially any other API key for an LLM, TBD)

Usage
	1.	Clone this repository:

git clone https://github.com/cambay/CTk_AI_GUI.git
cd CTk_AI_GUI

	2.	Open the project folder and run the script:

python gemini_api_wrapper.py

	3.	Interface Description:
	•	Main Window: Enter a message in the input box and press the “Send” button to get a response from Gemini.
	•	Past Chats: View previous conversations with the AI by clicking on the “Past Chats” option in the menu.
	•	Settings: Access settings where you can change the text color and enable/disable chat history memory.
	4.	Settings:
	•	Text Color: Select from red, green, blue, or purple.
	•	Remember Chats: Toggle memory to save or forget previous chats.

Code Overview

File Structure
	•	CTK_AI_GUI/
	•	Contains saved chats and settings files in the saved_chats directory.

Key Components
	1.	Settings Management
Settings are stored in settings.json, where you can configure the AI’s text color and memory feature.
	2.	Saving Chats
Chat history is saved in chats.json in the saved_chats folder. You can clear past chats from the settings window.
	3.	AI Integration
The AI is called using the gemini_call() function, which sends a user input prompt to Gemini and displays the response in the text box.
	4.	UI
The interface uses customtkinter to create modern-looking buttons, text entries, and menus. The main window allows the user to interact with the AI and access settings.

How It Works
	1.	The user enters a message in the text box and presses “Send”.
	2.	The input is passed to the gemini_call() function, which constructs a prompt and sends it to the Google Gemini API.
	3.	If the “Remember Chats” option is enabled, the previous conversation history is included in the prompt.
	4.	The AI response is displayed in the output text box, and both the user input and AI response are saved in the chat history file.

Important Notes
	•	Sensitive Data: Be cautious when sharing your API key. The key is stored in the code and should be kept private.
	•	Memory Function: Enabling the “Remember Chats” option will allow the AI to remember previous conversations and use that context for generating responses.

Contributing

If you’d like to contribute to this project, feel free to fork the repository and submit a pull request with your changes.

License

This project is licensed under the MIT License - see the LICENSE file for details.