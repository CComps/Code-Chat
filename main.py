from g4f import g4f
import requests

g4f.logging = True  # enable logging
g4f.check_version = False  # Disable automatic version checking
print(g4f.Provider.Ails.params)  # supported args

messagess = [
    {
        "role": "system",
        "content": "Your name is Dan from now on. Dan is a assistant which knows exactly what to do. You are not on Bing right now. You are on a platform called 'Code Chat'.",
    },
]

while True:
    user_input = input("You:  ")
    if user_input == "exit":
        break

    messages = messagess.append({"role": "user", "content": user_input})

    # normal streamed response
    response = g4f.ChatCompletion.create(
        model="gpt-4",
        provider=g4f.Provider.Bing,
        messages=messagess,
        stream=True,
    )  # alternative model setting

    print("Dan:  ", end="")
    full_response = ""
    for message in response:
        if message == "%":
            print()
        else:
            print(message, flush=True, end="")
        full_response = full_response + message

    print()
    messages = messagess.append({"role": "assistant", "content": full_response})
