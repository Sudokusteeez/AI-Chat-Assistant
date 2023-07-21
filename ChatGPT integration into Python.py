import tkinter as tk
import openai

API_Key = open("Ready to upload\API Storage\OpenAI_API.txt", "r").read()


openai.api_key = API_Key

chat_log = []

root = tk.Tk()

def get_user_input():
    global user_message
    user_message = entry.get()
    entry.delete(0, tk.END)

    chat_log.append({"role": "user", "content":user_message})
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = chat_log
    )
    assistant_response = response['choices'][0]['message']['content']
    label.config(text="ChatGPT: " + assistant_response)

    chat_log.append({"role": "assistant", "content": assistant_response})

label = tk.Label(root, text="ChatGPT")
label.pack()

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text="Send", command=get_user_input)
button.pack()

root.mainloop()
        