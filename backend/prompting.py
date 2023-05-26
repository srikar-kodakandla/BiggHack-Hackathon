import re
import pandas as pd
import numpy as np
import openai
from tqdm.auto import tqdm
import openai

agent_video_path='input/agent.mp4'
customer_video_path='input/customer.mp4'


class ChatGPT:  
    def __init__(self, api_key): 
        self.api_key = api_key
        openai.api_key = self.api_key
        self.conversation_history = [
            {"role": "system", "content": "Start of the conversation."}
        ]

    def ask(self, question):
        self.conversation_history.append({"role": "user", "content": question})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.conversation_history,
            temperature=0,
        )
        assistant_reply = response.choices[0].message["content"]
        self.conversation_history.append({"role": "assistant", "content": assistant_reply})
        return assistant_reply

api_key="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"

chat = ChatGPT(api_key)

conversations="""00:00	(Speaker A)	Hello Alam, welcome to Credit the Video KYC process for your personal loan application. So can you  
     	           	please confirm your full name and date of birth?                                                    
00:13	(Speaker B)	Hi ma'am, my name is Alam is on 21st November 1990.                                                 
00:24	(Speaker A)	So so can you please show me your government issued ID document such as passport, driving license,  
     	           	other card or a Pan card?                                                                           
00:33	(Speaker B)	Yes, of course I have driving license, I can show you.                                              
00:42	(Speaker A)	Okay, can you please confirm your current residential address and contact details?                  
00:48	(Speaker B)	Yes, sure it is. Door number two. Double 1214 Main Road Seven, cross Kudi Ali, Bangalore.           
00:59	(Speaker A)	So what is your occupation and monthly income?                                                      
01:03	(Speaker B)	Yeah, so I work as a sales executive and my monthly salary is 30,000.                               
01:12	(Speaker A)	So have you ever declared bankruptcy or had any outstanding debt in the past? No okay, have you ever
     	           	been convicted of any financial crimes or frauds? No so can you please provide your employment      
     	           	details such as your company name and designation?                                                  
01:40	(Speaker B)	Yeah, so my company name is Data for Chain Services Private Limited and working as a sales          
     	           	executive.                                                                                          
01:49	(Speaker A)	Okay, can you please provide details of your current or a previous employment including your job    
     	           	title, length of employment and monthly salary?                                                     
02:02	(Speaker B)	Yeah, that is 9000 High tech, Private limited and I was working there as support executive.         
02:09	(Speaker A)	Okay so can you please provide details of your existing loans and debts if any? No okay, so can you 
     	           	please explain the purpose of the loan you are applying for and how you plan to use it?             
02:29	(Speaker B)	So basically, we want to celebrate our kids birthday in Dubai and say you applied.                  
02:38	(Speaker A)	Okay, thank you.  """


script ="Did the agent collect all necessary KYC information from the customer, including their full name, date of birth, government issued ID, current residential address, occupation, monthly income, employment details, and existing loans? "

questions = {
    "Call_Quality": {
        "Reason_for_Call_Completion": "If the call did not complete, please explain why?.",
        "Call_Completion": "Did the call complete, or was it interrupted due to technical or business reasons? ('Yes'/'No')",
        "Reason_for_Call_Quality_Rating": "explain why you gave this rating to the call quality.",
        "Call_Quality_Rating": "Rate the quality of the call on a scale from 1-10, with 10 being the best."
    },
    "Agent_Performance": {
        "Agent_Adherence_to_Script": "Did the agent collect all necessary KYC information from the customer, including their full name, date of birth, government issued ID, current residential address, occupation, monthly income, employment details, and existing loans? ('Yes'/'No')",
        "Reason_for_Agent_Adherence": "If the agent did not adhere to the script, please explain why?.",
        "Agent_Empathy_and_Professionalism": "Did the agent demonstrate empathy and professionalism? ('Yes'/'No')",
        "Agent_Understanding_of_Customer": "Did the agent show a good understanding of the customer's needs? ('Yes'/'No')",
        "Agent_Rating": "Rate the agent's performance on a scale from 1-10, with 10 being the best.",
        "Reason_for_Agent_Rating": "explain why you gave this rating to the agent's performance."
    },
    "Customer_Behavior": {
        "Reason_for_Customer_Cooperation": "If the customer did not cooperate, please explain why in english text",
        "Customer_Cooperation": "Did the customer cooperate with the agent throughout the conversation? ('Yes'/'No')",
        "Reason_for_Customer_Understanding": "If the customer did not seem to understand, please explain why in english text",
        "Customer_Understanding": "Did the customer seem to understand the KYC process and the information being asked of them? ('Yes'/'No')",
        "Customer_Rating": "Rate the customer's behavior on a scale from 1-10, with 10 being the best.",
        "Reason_for_Customer_Rating": "explain why you gave this rating to the customer's behavior in english text"
    },
    "Third_Party_Interference": {
        "Reason_for_Third_Party_Interference": "If there was third-party interference, please explain why in english text.",
        "Third_Party_Presence": "Was there any evidence of a third party interfering or prompting the customer during the call? ('Yes'/'No')"
    },
    "Conversation_Analysis": {
        "Reason_for_Conversation_Flow": "If the conversation did not flow naturally, please explain why in english text.",
        "Conversation_Flow": "Did the conversation flow naturally and logically, without jumping abruptly between topics? ('Yes'/'No')",
        "Reason_for_Conversation_Frustration": "If there was any indication of frustration, please explain why in english text.",
        "Conversation_Frustration": "Did any part of the conversation indicate frustration either from the agent or the customer? ('Yes'/'No')"
    },
    "Security_Checks": {
        "Reason_for_liveness_Check": "If a liveness check was not conducted, please explain why in english text.",
        "liveness_Check": "Was a liveness check conducted with a security check? ('Yes'/'No')",
        "Reason_for_Random_Number_Security_Check": "If a random number security check was not conducted, please explain why in english text.",
        "Random_Number_Security_Check": "Was a security check done using a random number where the client needs to say the random number? ('Yes'/'No')"
    },
    "Document_Verification": {
        "Reason_for_Document_Verification": "If the agent did not properly verify documents, please explain why in english text.",
        "Document_Verification": "Did the agent properly verify all necessary documents during the call? ('Yes'/'No')"
    },
    "Timestamp_Analysis": {
        "Reason_for_Call_Duration": "If the call duration was not appropriate, please explain why in english text.",
        "Duration_of_Call": "Was the duration of the call appropriate for the content of the conversation? ('Yes'/'No')",
        "Reason_for_Long_Pauses": "If there were long pauses, please explain why in english text.",
        "Long_Pauses": "Were there any unusually long pauses in the conversation? ('Yes'/'No')",
        "Reason_for_Speed": "If the speed was not appropriate, please explain why in english text.",
        "Speed_of_Conversation": "Was the speed of the conversation appropriate? ('Yes'/'No')"
    },
    
    "Image_Context_Changes": {
        "Image_Context_Changes": "Did the image descriptions indicate any significant changes in the environment or context during the conversation? ('Yes'/'No')",
        "Reason_for_Context_Changes": "If there were significant changes, please explain in short english summary"
    },
    "Non_Verbal_Cues": {
        "Non_Verbal_Cues": "Did the image descriptions indicate any non-verbal cues (gestures, expressions) from the customer or agent that impacted the conversation? ('Yes'/'No')",
        "Reason_for_Non_Verbal_Cues": "If there were non-verbal cues, please explain in short english summary"
    },
    "Third_Party_Presence_Image": {
        "Third_Party_Presence_Image": "Did the image descriptions suggest the presence of a third party that may have influenced the conversation? ('Yes'/'No')",
        "Reason_for_Third_Party_Presence_Image": "If there was evidence of third-party presence, please explain in short english summary"
    },
    "Technical_Issues_Image": {
        "Technical_Issues_Image": "Did the image descriptions suggest any technical issues (e.g., poor lighting, low video quality) that may have affected the conversation? ('Yes'/'No')",
        "Reason_for_Technical_Issues_Image": "If there were technical issues, please explain in short english summary"
    },
    "Distractions_Image": {
        "Distractions_Image": "Did the image descriptions suggest any distractions in the customer's or agent's environment? ('Yes'/'No')",
        "Reason_for_Distractions_Image": "If there were distractions, please explain in short english summary"
    },
    "Image_Context_Contribution": {
        "Image_Context_Contribution": "Overall, did the image descriptions contribute significant additional information to understanding the conversation? ('Yes'/'No')",
        "Reason_for_Image_Context_Contribution": "If the image descriptions contributed significantly, please explain in short english summary"
    }
    
}



def questions_to_prompt(questions, image_description_agent,image_description_customer, analytics):
    prompt = ""
    i = 1
    for category, question_dict in questions.items():
        prompt += f"For the following KYC verification conversation and corresponding image descriptions (provided every 5 seconds) between an agent and a customer, please provide the following information in a JSON format:\n\n"
        for question_key, question in question_dict.items():
            prompt += f"{i}. '{question_key}': '{question}'\n"
            i += 1
        prompt += f"The conversation is delimited by triple backticks in the format ```{conversations}```.\n\n"
        prompt += f"The image descriptions are provided for agent as follows: ```{image_description_agent}```. Note that these descriptions are given for every few seconds of the video.\n\n"
        prompt += f"The image descriptions are provided for customer as follows: ```{image_description_customer}```. Note that these descriptions are given for every few seconds of the video.\n\n"
        prompt += f"{analytics}.\n\n"
    return prompt

from tqdm.auto import tqdm
from time import sleep


from image_to_text import generate_video_summary
image_summary_customer=generate_video_summary(customer_video_path)
image_summary_agent=generate_video_summary(agent_video_path)

from emotion_video_detection import main_function
emotions_video_customer=main_function(customer_video_path)
emotions_video_agent=main_function(agent_video_path)

from emotion_detection_audio import main_video
emotions_audio_customer=main_video(customer_video_path)
#emotions_audio_agent=main_video(agent_video_path)


from check_video_quality import check_quality
check_quality_customer=check_quality(customer_video_path)
check_quality_agent=check_quality(agent_video_path)

def round_values(d):
    for k, v in d.items():
        if isinstance(v, float):
            d[k] = round(v, 2)
        elif isinstance(v, dict):
            round_values(v)
    return d


analytics_prompt = f"""I am giving you the anylitics of the image during the conversation use this information also to answer the questions:
The customer video is divided in to 10 chunks where each chunk i calculated the number of people in the video It is as follows {list(emotions_video_customer['people_count'].values())
} In the same way agent video is divided in to 10 chunks where each chunk i calculated the number of people in the video It is as follows {list(emotions_video_agent['people_count'].values())}

In the same way video sentiment was calculated for the agent. In each chunk i am classifying each chunk in to top two sentiments,It is as followes {list(emotions_video_agent['final_emotion'].values())}
In the same way video sentiment was calculated for the customer. In each chunk i am classifying each chunk in to top two sentiments,It is as followes {list(emotions_video_customer['final_emotion'].values())}
In the same way Complete video sentiment was calculated for the customer. It is as follows {round_values(emotions_video_customer["score_comparisons"].set_index('Human Emotions').to_dict()["Emotion Value from the Video"])}
In the same way Complete video sentiment was calculated for the agent.It counts the number of frames with different emotions, i scaled it with minmax. It is as follows {round_values(emotions_video_agent["score_comparisons"].set_index('Human Emotions').to_dict()["Emotion Value from the Video"])}
In the same way audio sentiment was calculated for the customer. It is as follows {list(emotions_audio_customer['emotion_for_chunks'].values())} These sentiments are calculated for each chunk of the video. where a video is divided in to 10 chunks.
The video and audio quality of agent was calculated where 0 is worest and 1 is good. It is as follows {round_values(check_quality_agent)} These sentiments are calculated for each chunk of the video. where a video is divided in to 10 chunks.
Use this information to answer  the questions that were asked. Don't give analytics in the answer. 
"""

chat = ChatGPT(api_key)

short_summary=chat.ask(f"The given text is the conversation between KYC Agent and the customer.write a short summary in bullet points on {conversations}")

all_category_outputs=dict()
all_category_outputs['Short_Summary']=dict()
all_category_outputs['Short_Summary']["short_summary"]=short_summary

count=0

for category in tqdm(questions.keys()):
    print(category)
    ask_prompt = questions_to_prompt({category:questions[category]}, image_summary_customer, image_summary_agent, analytics_prompt)
    chat = ChatGPT(api_key)
    output=chat.ask(ask_prompt)
    all_category_outputs[category]=output
    sleep(20) #### This is to avoid the limit error from the ChatGPT API 
    

pd.DataFrame(all_category_outputs).T

df = pd.DataFrame(all_category_outputs).transpose()

df.index.name = 'Category of the Question'
df["Question"]=questions
df.columns.name = None

df.to_csv('Final_output.csv')   



###############################################################################################################
###############################################################################################################
###############################################################################################################
###############################################################################################################
###############################################################################################################
###############################################################################################################

####################This is the code for the chatbot###########################################################
#################### Ask any question which is related to  the conversation between agent and customer #########

def chatbot(question, image_description_agent,image_description_customer, analytics):
    prompt = ""
    prompt += f"For the following KYC verification conversation and corresponding image descriptions (provided every 5 seconds) between an agent and a customer, if possible,please provide the following information in a JSON format:\n\n"
    prompt+=question
    prompt += f"The conversation is delimited by triple backticks in the format ```{conversations}```.\n\n"
    prompt += f"The image descriptions are provided for agent as follows: ```{image_description_agent}```. Note that these descriptions are given for every few seconds of the video.\n\n"
    prompt += f"The image descriptions are provided for customer as follows: ```{image_description_customer}```. Note that these descriptions are given for every few seconds of the video.\n\n"
    prompt += f"{analytics}.\n\n"
    chat = ChatGPT(api_key)
    answer = chat.ask(prompt)
    return answer

if __name__ == "__main__":

    your_question=""" What is the color of the shirt that the person wore in the video?"""
    your_question= """what is the customer gender? """
    your_question= """what is the customer age? and why did you gave that age ?  """
    your_question= """is the customer wearing a mask?"""
    your_question=""" give me the short summary of the conversation?"""
    your_question="""Did the image descriptions suggest any technical issues (e.g., poor lighting, low video quality) that may have affected the conversation? ('Yes'/'No')"""

    your_question="""How was the agent behaviour towards the customer?"""


    your_question="""Is there any third party interference? First tell me the reason and then tell me the answer"""
    answer=chatbot(your_question, image_summary_customer, image_summary_agent, analytics_prompt)
    print(answer)
