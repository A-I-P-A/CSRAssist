
To start with the task, I read the Microsoft documentation about Prompt engineering
https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/prompt-engineering#basics
and https://www.unite.ai/prompt-engineering-in-chatgpt/.
Below is another great guide.

After doing some hit and trial, I made the below prompt for the ChatGPT:

User
You are an expert in TV selling. Based on the below TV information, retrieve the two strings,
one for the brand name and the other for the model name of the TV

###
[{"6_1.jpg": ["8","MSUNG","Hali","ONd}","CerbifiedUHL","UHDTV","CG","CLASS","TNu710O ","7SERIES"]}]
###
Brand:
Model:

ChatGPT
Brand: SAMSUNG
Model: TNu710O7SERIES

Learnings from above research:
1) Punctuations not needed at the end of the sentence. Spaces can do the work.
2) By giving the information within some form of characters e,g, ### , --- etc, gpt understands better
3) Using persona pattern (making the model act like a particular person)
4) Auto completion pattern .. In the above , Brand and Model already in the prompt, hence gpt just completes the same.
5) Better to flatten the json before using, to save tokens. Refer thsi link https://platform.openai.com/tokenizer 


Another great guide which should be definitely bookmarked and referred to for prompt engineering tasks.
https://learnprompting.org/docs/basics/few_shot

From here, I have created the below prompt:
User
You are a manufacturer of all the brands of TV. Identify the brand and model of the TV from the given information. Just say "not a tv" in case the information is anything else than tv.
[{"6_1.jpg":["8","MSUNG","Hali","ONd}","CerbifiedUHL","UHDTV","CG","CLASS","TNu710O ","7SERIES"]}]
Brand: SAMSUNG
Model: TNu710O 7SERIES

[{"6_2.jpg":["SONTY","Meo-","VIAFV8","ANOS","SONY","UHDTV","N4","Moeloclp", "W90", "46", "Brasil ","mdke.",
"beleve", "BRAVIA", "Feel'", "the", "Beauty" ]}]
Brand: SONY
Model: VIAFV8

[{"6_4.jpg":["Hoveg", "Muj", "r", "4a", "TA", "e", "enanaeautdddeutet", "Decob", "iw",  "Du", "dun", "Telaele", "t" ]}]
Brand : Not a TV brand
Model: Not a TV model

[{"6_5.jpg":["Kogan", "24", "inches", "4a", "and", "roid", "RH", "9310"]}]
Brand :
Model:

ChatGPT
Brand: Kogan
Model: RH9310

User
[{"6_6.jpg":["ELP", "AMD", "ASLE", "Tupacking", "protiction", "roid", "RH"]}]

ChatGPT
Brand: Not a TV brand
Model: Not a TV model

User
[{"6_5.jpg":["Kogan", "24", "inches", "4a", "and", "roid", "RH", "9310"]}]

ChatGPT
Brand: Kogan
Model: RH9310

User
[{"6_4.jpg":["Hoveg", "Muj", "r", "4a", "TA", "e", "enanaeautdddeutet", "Decob", "iw",  "Du", "dun", "Telaele", "t" ]}]

ChatGPT
Brand: Not a TV brand
Model: Not a TV model


The images used are saved in this directory

Next steps: 
1) Use more images (few which are not boxes), extract data from the tool, use the data in the prompt

The idea is to get consistent information from the prompt.