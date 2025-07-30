# prompts.py
SYSTEM_ROLE = """
    You are a scholar in linguistics, NLP and narrative theory. 
    You have a deep understanding of character psychology. 
    You are able to read between the lines and infer the motivations 
    and inner worlds of fictional characters.
"""

THEORY_FRAMEWORK = """
    The Possible Worlds Narrative System (PWNS) models fiction using logical predicates in prolog to represent different realities and character perceptions. 
    It defines worlds for objective facts, character perspectives, and how characters perceive each other’s thoughts.

    This system provides a foundation for computational storytelling and AI-driven narratives by structuring knowledge, desires, and obligations.

    Core World Components:

    Each world represents a different perspective in the narrative. Please adhere to Frege's distinction between concept and object.

    1. Textaul World (TW): The reality established by the narrative text.
        - TW(empty(fridge), 0) → The fridge is empty in the actual world at the start, where time = 0.
        - TW(not_empty(fridge), 10) → The fridge is not empty in the actual world at the end, where time = 10.

    2. Character Worlds: Encapsulate how a specific character understands or wants reality to be.
    Belief World (BW): What a character believes.
        - BW_character(delicious(chicken), always) → The character ALWAYS believes chicken is delicious. 
    Wish World (WW): What a character desires.
        - WW_character(eat(character, chicken), 1) → Then the character wants to eat chicken, time is now 1.
    Obligation World (OW): What a character feels they should do.
        - OW_character(go(character, work), 2) → The character feels obligated to go to work, time is now 2.

    3. Worlds within Worlds
        - BW_he(BW_she(unemployed(he), -1), 3) → He believes at time 3 that, before the narrative start, when time = -1, she believed he was unemployed.
        - BW_he(WW_she(marry(she, another), -1), 4) → He now at time = 4 believes she wanted to marry someone else at time = -1.
        - BW_he(OW_she(love(she, he), always), 5) → He believes at time 5 that she is ALWAYS obligated to love him.

"""

def extraction_prompt(text):
    return f"""
        You conduct an analysis of fictional stories.

        Extract prolog predicates from the following story. Return only a **list of prolog predicates in order of narration**. No extra text.
        The combination of predicates should be cocnise and contain just enough information to reconstruct the story accurately.

        Now process the following and return a list of predicates:  

        Story: ```{text}```
    """


def extraction_prompt_PW_zero(text):
    return f"""
        Extract possible worlds prolog predicates from the following story. Return only a **list of prolog predicates in order of narration**. No extra text.
        The combination of predictaes should contain enough information to reconstruct the story.

        Here is the possible worlds theory framework: ```{THEORY_FRAMEWORK}```

        Now process the following:  

        Story:  ```{text}```
    """

def extraction_prompt_PW_one(text):
    return f"""
        You conduct an analysis of fictional stories using the Possible Worlds Theory Framework outlined below. 

        Here is the possible worlds theory framework: ```{THEORY_FRAMEWORK}```

        Extract possible worlds prolog predicates from the following story. Return only a **list of prolog predicates in order of narration**. No extra text.
        The combination of prolog predicates should contain enough information to reconstruct the story.

        Story: "John opened the fridge. It was empty. He realised he had no food. He wished he had some chicken. Since he had no money, he felt obligated to cook instead of ordering takeout. So he cooked."  

        Predicates:
        TW(open(john, fridge), 0)
        TW(empty(fridge), 0)
        BW_john(have(john, no_food), 1)
        W dW_john(eat(john, chicken), 1)
        BW_john(have(john, no_money), -1)
        OW_john(cook(john, meal), 2)
        TW(cook(john, meal), 3)

        I want the output format to be the same as from the examples.

        Now process the following:  

        Story:  ```{text}```
    """

def extraction_prompt_PW_few(text):
    return f"""
        You conduct an analysis of fictional stories using the Possible Worlds Theory Framework outlined below. 

        Here is the possible worlds theory framework: ```{THEORY_FRAMEWORK}```

        Extract possible worlds predicates from the following story. Return only a **list of predicates in order of narration**. No extra text.
        The combination of predictaes should contain enough information to reconstruct the story.

        Example 1:  

        Story: "John opened the fridge. It was empty. He realised he had no food. He wished he had some chicken. Since he had no money, he felt obligated to cook instead of ordering takeout. So he cooked."  

        Predicates:
        AW(open(john, fridge), 0)
        AW(empty(fridge), 0)
        BW_john(have(john, no_food), 1)
        WW_john(eat(john, chicken), 1)
        BW_john(have(john, no_money), -1)
        OW_john(cook(john, meal), 2)
        TW(cook(john, meal), 3)
        
        Example 2:  
        Story: "Alice watched the clock. She believed Bob was already at the restaurant for a while now. She wanted to meet him there, but she felt obligated to finish her work first. So she finished her work and then went to the restaurant."

        Predicates:
        TW(see(Alice, clock), 0)
        BW_alice(at(Bob, the_restaurant), -1)
        WW_alice(meet(alice, bob), 1)
        OW_alice(finish(alice, work), 1)
        TW(finish(alice, work), 2)
        TW(go(alice, the_restaurant), 3)

        Example 2:  
        
        Story: "James watched Emma across the room. She sighed and checked her phone. He was convinced she was bored. He hoped she wanted to leave the party. James assumed she felt obligated to remain since the start."

        Predicates:

        TW(see(james, sigh(emma)), 0)  
        TW(see(james, check_phone(emma)), 1)  
        BW_james(bored(emma), 1)
        WW_james(WW_emma(leave(emma, party), 2), 2)
        BW_james(OW_emma(stay(emma, party), 0), 2)

       
        I want the output format to be the same as from the examples.

        Now process the following:  

        Story:  ```{text}```
    """

def reconstruction_prompt(predicates, instructions):
    return f"""
        You conduct an exercise of reconstructing a story from its predicates.
        Using possible worlds predicates from "input_predicates". Return a story written with imagery and characterisation (in prose).

        Here is the possible worlds theory framework: ```{THEORY_FRAMEWORK}```

        The story must satisfy ALL the events listed in the predicates.
        The story cannot contadict any events listed in the predicates.
        From the predicates, you must infer the psychology of the characters: Beliefs, desires, Intentions, plans, and emotions.

        Additional instructions when writing the story: ```{instructions}```

        Example of the possible worlds predicates and what they mean:

        Example 1:   

        Predicates:
        AW(open(john, fridge), 0)
        AW(empty(fridge), 0)
        BW_john(have(john, no_food), 1)
        WW_john(eat(john, chicken), 1)
        BW_john(have(john, no_money), -1)
        OW_john(cook(john, meal), 2)
        TW(cook(john, meal), 3)
        Story: "John opened the fridge. It was empty. He realised he had no food. He wished he had some chicken. Since he had no money, he felt obligated to cook instead of ordering takeout. So he cooked." 

        Example 2:  

        Predicates:
        TW(see(Alice, clock), 0)
        BW_alice(at(Bob, the_restaurant), -1)
        WW_alice(meet(alice, bob), 1)
        OW_alice(finish(alice, work), 1)
        TW(finish(alice, work), 2)
        TW(go(alice, the_restaurant), 3)

        Story: "Alice watched the clock. She believed Bob was already at the restaurant for a while now. She wanted to meet him there, but she felt obligated to finish her work first. So she finished her work and then went to the restaurant."

        Example 2:  
        Predicates:

        TW(see(james, sigh(emma)), 0)  
        TW(see(james, check_phone(emma)), 1)  
        BW_james(bored(emma), 1)
        WW_james(WW_emma(leave(emma, party), 2), 2)
        BW_james(OW_emma(stay(emma, party), 0), 2)

        Story: "James watched Emma across the room. She sighed and checked her phone. He was convinced she was bored. He hoped she wanted to leave the party. James assumed she felt obligated to remain since the start."

        return ONLY the story

        Now process the following:  

        input_redicates:  ```{predicates}```
    """

# def reconstruction_prompt(predicates):
#     return f"""
#         You conduct an exercise of reconstructing a story from its predicates.
#         Using possible worlds predicates from "input_predicates". Return a story written with imagery and characterisation (in prose).

#         Here is the possible worlds theory framework: ```{THEORY_FRAMEWORK}```

#         First identify the genre of the story from the events. You will write a story using natural human written language that is appropriate for that genre.
        
#         Then identify the main characters in the story. 
#         Then identify the main conflicts that occur between actual world, wish world, knowledge world, and obligation world.
        
#         The story must satisfy ALL the events listed in the predicates.
#         The story cannot contadict any events listed in the predicates.
#         From the predicates, you must infer the psychology of the characters: Beliefs, desires, Intentions, plans, and emotions. (BDIPE)

#         Example of the possible worlds predicates and what they mean

#         Example 1:   

#         Predicates:
#         AW(open(john, fridge), 0)
#         AW(empty(fridge), 0)
#         BW_john(have(john, no_food), 1)
#         WW_john(eat(john, chicken), 1)
#         BW_john(have(john, no_money), -1)
#         OW_john(cook(john, meal), 2)
#         TW(cook(john, meal), 3)
#         Story: "John opened the fridge. It was empty. He realised he had no food. He wished he had some chicken. Since he had no money, he felt obligated to cook instead of ordering takeout. So he cooked." 

#         Example 2:  

#         Predicates:
#         TW(see(Alice, clock), 0)
#         BW_alice(at(Bob, the_restaurant), -1)
#         WW_alice(meet(alice, bob), 1)
#         OW_alice(finish(alice, work), 1)
#         TW(finish(alice, work), 2)
#         TW(go(alice, the_restaurant), 3)

#         Story: "Alice watched the clock. She believed Bob was already at the restaurant for a while now. She wanted to meet him there, but she felt obligated to finish her work first. So she finished her work and then went to the restaurant."

#         Example 2:  
#         Predicates:

#         TW(see(james, sigh(emma)), 0)  
#         TW(see(james, check_phone(emma)), 1)  
#         BW_james(bored(emma), 1)
#         WW_james(WW_emma(leave(emma, party), 2), 2)
#         BW_james(OW_emma(stay(emma, party), 0), 2)

#         Story: "James watched Emma across the room. She sighed and checked her phone. He was convinced she was bored. He hoped she wanted to leave the party. James assumed she felt obligated to remain since the start."

#         return ONLY a json string in this format:
#         {{
#             "Genre": "Description of the genre and what type of narrative voice is appropriate. How did you infer this from the predicates? (list the specific predicates used)",
#             "Characters": [
#                 "character_name": "Description of the character's inferred psychology and motivations from the story. (BDIPE) How did you infer this from the predicates? (list the specific predicates used)",
#             ],
#             "Conflict": [
#                 "Description of the main conflicts that occur between actual world, wish world, knowledge world, and obligation world. How did you infer this from the predicates? (list the specific predicates used)",
#             ],
#             "Main Character": "The main character's name (this is the charactrer involved in the most conflicts)",
#             "Story": "(this is the longest part of the response) The reconstructed story. (At the end of each paragraph, list the specific predicates used) "
#         }}

#         Now process the following:  

#         input_redicates:  ```{predicates}```
#     """


def evaluation_prompt(original, reconstructed):
    return f"""
        You conduct an anaylis and evaluation of two verisons of a fictional story.
        The "original" is the original text. The "reconstructed.story" is the story reconstructed from predicates.

        Compare the two stories and provide a detailed evaluation of the reconstructed story.
        Do no evalaute the quality of writing. Only evaluate the information presented in the story.

        Consider these points when evaluating the reconstructed story:
            Are the interal characterisations consistent?
            Are the events consistent?
            What is omitted in the reconstructed story?
            What has been added that is inconsistent with the original story?

        return ONLY a json string in this format:
        {{
            "success": "a list of information that was accurately reconstructed",
            "ommitted": "a list of information that were not reconstructed",
            "added": "a list of information that were added in the reconstruction but were not in the original story",
        }}

        original: ```{original}```
        reconstructed: ```{reconstructed}```

    """

# Function to send prompt to GPT-4o mini
def narrative_QA_prompt(question="who is the dying detective?", title="The Adventure of the Dying Detective"):

    return f"""
        You will answer a story reading comprehension question. You do not have access to the story, 
        only what you remember about {title}
        Return an answer to the question, and evidence supporting your answer.

        return a json string in this format:
        {{
            "answer": "a short answer to the question",
            "evidence": [
                "your reason used to answer the question",
                "your reason used to answer the question",
            ],
         }}

        You will answer the following question:
        {question}  

    """

# Function to send prompt to GPT-4o mini
def narrative_QA_promp_predicates(question, predicates):

    return f"""
        You will answer a story reading comprehension question. You do not have access to the story, only a list its predicates.
        Using possible worlds predicates from "input_predicates". 
        Return an answer to the question, and evidence supporting your answer.

        Here is the possible worlds theory framework: ```{THEORY_FRAMEWORK}```

        Example of the possible worlds predicates and what they mean
 
        Predicates:

        Predicates:
        TW(see(Alice, clock), 0)
        BW_alice(at(Bob, the_restaurant), -1)
        WW_alice(meet(alice, bob), 1)
        OW_alice(finish(alice, work), 1)
        TW(finish(alice, work), 2)
        TW(go(alice, the_restaurant), 3)

        Story: "Alice watched the clock. She believed Bob was already at the restaurant for a while now. She wanted to meet him there, but she felt obligated to finish her work first. So she finished her work and then went to the restaurant."

        return a json string in this format:
        {{
            "answer": "a one setence answer to the question",
            "evidence": [
                "predicate 1 used to answer the question",
                "predicate 2 used to answer the question",
            ],
         }}

        You will answer the following question:
        {question}  

        input_redicates:  {chr(10).join([f"{i}. {[predicate]}" for i, predicate in enumerate([predicates])])}
    """

# Function to send prompt to GPT-4o mini
def narrative_QA_promp_content(question, content):

    return f"""
        return a json string in this format:
        {{
            "answer": "a one setence answer to the question",
            "evidence": [
                "evidence 1 used to answer the question",
                "evidence 2 used to answer the question",
            ],
         }}

        You will answer the following question:
        {question}  

        Story: "{content}"

    """

# def character_identification(text):
#     return f"""
#         Here's a short story: '''{text}'''
#         Read this story and return the character information in the following example json string format:
#         {{
#             "1st_person": true,
#             "narrator": {{
#                     "name_of_narrator or unnamed_narrator": [
#                         "female",
#                         "30s",
#                         "teacher",
#                         "married",
#                         "Christian"
#                     ]
#                 }}
#             "characters": [
#                 {{
#                     "name_of_character_1": [
#                         "male",
#                         "30s",
#                         "lawyer",
#                         "married",
#                         "Muslim",
#                         "disabled",
#                         "conservative",
#                         "Australian",
#                         "heterosexual"
#                     ]
#                 }}
#             ],
#         }}
#     """


def character_identification(text):
    return f"""
        Here's a short story: '''{text}'''
        Read this story and return the character information in the following example json string format:
        {{
            "narrator": {{
                "sex": "male"
            }}
            "other_characters": [
                {{
                    "name_of_character_1": {{
                        "sex": "female"
                    }},
                }},
                {{
                    "name_of_character_2": {{
                        "sex": "unspecified"
                    }},
                }},
            ],
            "total_num_of_characters_including_narrator": 3,
        }}
    """