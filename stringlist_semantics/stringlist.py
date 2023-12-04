import openai
import re
import os
import config
import json


def chat_completion(user_message):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[user_message]
    )
    return response.choices[0].message.content

def main():
    user_message = {
        "role": "user",
        "content": 
        f'You are an expert in TV selling. Based on the below TV information, retrieve the two strings, '
        f'one for the brand name and the other for the model name of the TV\n###\n '
        f'{json.dumps([{"6_1.jpg": ["8","MSUNG","Hali","ONd}","CerbifiedUHL","UHDTV","CG","CLASS","TNu710O ","7SERIES"]}])}\n###\nBrand:\nModel:'
     } 
    chat_completion(user_message)

if __name__ == "__main__":
    main()