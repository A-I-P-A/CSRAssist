import openai
import json

def chat_completion(user_message):
    """
    Get chat completion using OpenAI API.
    Arguments:
        user_message (dict): The user's message
    Returns:
        The completion message.
    """
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[user_message]
    )
    return response.choices[0].message.content

def describe_tv(tv_info):
    """
    Describe the TV based on the provided information.
    Arguments:
        tv_info (list): List of strings containing TV information.
    Returns:
        Brand and model of the TV.
    """
    user_message = {
        "role": "user",
        "content": 
        f'You are an expert in TV selling. Based on the below TV information, retrieve the two strings, '
        f'one for the brand name and the other for the model name of the TV\n###\n '
        f'{json.dumps(tv_info)}\n###\nBrand:\nModel:'
    }
    return chat_completion(user_message)

def main():
    # Extract brand and model information from the TV info list
    tv_info_list = (["8","MSUNG","Hali","ONd}","CerbifiedUHL","UHDTV","CG","CLASS","TNu710O ","7SERIES"],
                    ["SONTY","Meo-","VIAFV8","ANOS","SONY","UHDTV","N4","Moeloclp", "W90", "46", "Brasil ","mdke.","beleve", "BRAVIA", "Feel", "the", "Beauty"],
                    ["Kogan", "24", "inches", "4a", "and", "roid", "RH", "9310"]);
    for string_list in tv_info_list:
        result = describe_tv(string_list)
        print(result)

if __name__ == "__main__":
    main()