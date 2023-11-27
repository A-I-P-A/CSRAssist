
# 1. Introduction
In this document, I explore prompt engineering techniques for training ChatGPT to identify TV brands and models from given information.
The goal is to improve the model's accuracy and consistency in extracting relevant details.
I discuss learnings from previous experiments and provide a step-by-step guide for crafting effective prompts.

# 2. Initial Research
To start with the task, I read the Microsoft documentation on Prompt engineering
https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/prompt-engineering#basics
and found additional insights here: https://www.unite.ai/prompt-engineering-in-chatgpt/.

After several iterations, I identified the below pattern that improve prompt understanding.
## Example
User

You are an expert in TV selling. Based on the below TV information, retrieve the two strings,
one for the brand name and the other for the model name of the TV
###[{"6_1.jpg": ["8","MSUNG","Hali","ONd}","CerbifiedUHL","UHDTV","CG","CLASS","TNu710O ","7SERIES"]}]###
Brand:
Model:

ChatGPT
Brand: SAMSUNG
Model: TNu710O7SERIES


# 3. Learnings from above research
1) **Punctuations** not needed at the end of the sentence. Spaces can do the work.
2) **Delimiting Pattern** Using some form of characters e,g, ### , --- etc, gpt understands better.
3) **Persona Pattern** Making the model act like a specific person.
4) **Auto completion Pattern** Including relevant information in the prompt aids the model in completing tasks.
     In the above, Brand and Model were already in the prompt, hence GPT understood that it has to complete the same.
5) **JSON Flattening** This is done to save tokens. Refer this link https://platform.openai.com/tokenizer to calculate number of tokens.

# 4. Recommended Guide
Another great guide which should be definitely bookmarked and referred to for prompt engineering tasks.
https://learnprompting.org/docs/basics/few_shot

# 5. Updated Prompt
Building on the learnings, I refined the prompt. The idea is to get consistent information from the prompt.

## Examples
I provide examples of prompts and model responses using different TV information. The model successfully 
identifies TV brands and models _while handling cases where the information does not correspond to a TV_.

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

# 6. Next steps
The next steps involve expanding the dataset with more images (need not be boxes), extracting data from the tool,
   incorporating it into the prompt. The aim is to further enhance the model's ability to provide consistent information.

 **Note: The images used are saved in this directory**

 **Note: Please refer the task https://github.com/orgs/A-I-P-A/projects/1/views/1?pane=issue&itemId=45287557 for the screenshots of the above prompts.** 