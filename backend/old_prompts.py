"""This file contains so many possible  questions that can be asked about the video analytics"""



prompt=f"""For the following KYC verification conversation between an agent and a customer, please provide the following information in a JSON format:

1. "Agent Rating": Rate the agent's performance on a scale from 1-10, with 10 being the best.
2. "Reason for Agent Rating": explain why you gave the agent this rating.
3. "Conversation Quality Rating": Rate the quality of the conversation on a scale from 1-10, with 10 being the best.
4. "Reason for Conversation Quality Rating": explain why you gave this rating.
5. "Smooth Conversation": Indicate whether the conversation was smooth ("Yes"/"No").
6. "Language issues": Were there any language-related issues during the conversation ("Yes"/"No")?
7. "Reason for Language issues": If there were language issues, please explain why?.
8. "Call ended abruptly": Did the call end abruptly ("Yes"/"No")?
9. "3rd party conversations from client side": Were there any third-party conversations on the client's side during the call ("Yes"/"No")?
10. "Overall conversation rating": Rate the overall conversation on a scale from 1-10, with 10 being the best.
11. "Reason for Overall Conversation rating": explain why you gave this overall rating.
12. "Agent followed script": {script} ("Yes"/"No").
13. "Summary": Provide a brief summary of the conversation.

The conversation is delimited by triple backticks in the format ```{conversations}```.
"""

prompt=f"""For the following KYC verification conversation between an agent and a customer, please provide the following information in a JSON format:

1. "Agent_Rating": Rate the agent's performance on a scale from 1-10, with 10 being the best.
2. "Agent_Reason for Rating": explain why you gave the agent this rating.
3. "Conversation_Quality Rating": Rate the quality of the conversation on a scale from 1-10, with 10 being the best.
4. "Conversation_Reason for Quality Rating": explain why you gave this rating.
5. "Conversation_Smooth": Indicate whether the conversation was smooth ("Yes"/"No").
6. "Conversation_Language issues": Were there any language-related issues during the conversation ("Yes"/"No")?
7. "Conversation_Reason for Language issues": If there were language issues, please explain why?.
8. "Conversation_Call ended abruptly": Did the call end abruptly ("Yes"/"No")?
9. "Conversation_3rd party conversations from client side": Were there any third-party conversations on the client's side during the call ("Yes"/"No")?
10. "Conversation_Overall rating": Rate the overall conversation on a scale from 1-10, with 10 being the best.
11. "Conversation_Reason for Overall rating": explain why you gave this overall rating.
12. "Agent_Followed script": Did the agent collect all necessary KYC information from the customer, including their full name, date of birth, government issued ID, current residential address, occupation, monthly income, employment details, and existing loans? ("Yes"/"No").
13. "Customer_Satisfaction": Did the customer appear to be satisfied at the end of the conversation? ("Yes"/"No").
14. "Resolution_Achieved": Was the customer's issue or query resolved in this conversation? ("Yes"/"No").
15. "Conversation_Call duration appropriate": Was the call duration appropriate for the content of the conversation? ("Yes"/"No").
16. "Agent_Empathy and Professionalism": Did the agent demonstrate empathy and professionalism? ("Yes"/"No").
17. "Agent_Knowledge and Competence": Did the agent appear knowledgeable and competent? ("Yes"/"No").
18. "Agent_Escalations": Were there any moments in the call where the agent needed to escalate the issue? ("Yes"/"No").
19. "Agent_Adherence to Policies and Procedures": Did the agent adhere to company's policies and procedures throughout the conversation? ("Yes"/"No").
20. "Resolution_First Contact": Was the agent able to resolve the customer's query or issue on the first contact? ("Yes"/"No").
21. "Agent_Use of Hold or Transfer": Did the agent have to put the customer on hold or transfer them to another department/person? If yes, was this executed smoothly? ("Yes"/"No").
22. "Agent_Communication Skills Rating": Rate the agent's communication skills on a scale from 1-10, with 10 being the best.
23. "Agent_Reason for Communication Skills Rating": explain why you gave this rating.
24. "Agent_Upselling/Cross-selling": Did the agent attempt to upsell or cross-sell any products or services during the call? Was it done appropriately? ("Yes"/"No").
25. "Agent_Data Security Practices": Did the agent follow data security practices during the call, such as not asking for sensitive information in an insecure manner? ("Yes"/"No").
26. "Agent_Personalization": Did the agent personalize the conversation (using the customer's name, referring to past interactions, etc.)? ("Yes"/"No").
27. "Agent_Active Listening": Did the agent demonstrate active listening skills, such as paraphrasing, summarizing, or asking clarifying questions? ("Yes"/"No").
28. "Agent_Patience": Did the agent show patience throughout the conversation? ("Yes"/"No").
29. "Agent_Tone of Voice Rating": Rate the agent's tone of voice on a scale from 1-10, with 10 being the best. Was it friendly, professional, and appropriate for the situation?
30. "Agent_Reason for Tone of Voice Rating": explain why you gave this rating.
31. "Agent_Understanding of Customer's Needs": Did the agent show a good understanding of the customer's needs? ("Yes"/"No").
32. "Agent_Initiative": Did the agent show initiative in resolving the customer's issue or in providing information? ("Yes"/"No").
33. "Agent_Follow-up Actions": Were any follow-up actions required after the call? If so, did the agent set these up correctly? ("Yes"/"No").
34. "Agent_Conflict Resolution Rating": If there was a conflict during the call, how well did the agent handle it? Rate on a scale from 1-10.
35. "Agent_Reason for Conflict Resolution Rating": explain why you gave this rating.
36. "Timestamp_Duration of Call": Was the duration of the call appropriate for the content of the conversation? ("Yes"/"No").
37. "Timestamp_Reason for Duration": If the call duration was not appropriate, please explain why?.
38. "Timestamp_Long Pauses": Were there any unusually long pauses in the conversation? ("Yes"/"No").
39. "Timestamp_Reason for Long Pauses": If there were long pauses, please explain why?.
40. "Timestamp_Speed of Conversation": Was the speed of the conversation appropriate? ("Yes"/"No").
41. "Timestamp_Reason for Speed": If the speed was not appropriate, please explain why?.
42. "Timestamp_Agent's Response Time": Was the agent's response time appropriate throughout the conversation? ("Yes"/"No").
43. "Timestamp_Reason for Agent's Response Time": If the response time was not appropriate, please explain why?.
44. "Timestamp_Customer's Response Time": Was the customer's response time appropriate throughout the conversation? ("Yes"/"No").
45. "Timestamp_Reason for Customer's Response Time": If the response time was not appropriate, please explain why?.
46. "Timestamp_Rushes in the Conversation": Were there any moments when the conversation felt rushed or pressured? ("Yes"/"No").
47. "Timestamp_Reason for Rushes": If there were rushed moments, please explain why?.
48. "Customer_Understanding": Did the customer seem to understand the KYC process and the information being asked of them? ("Yes"/"No").
49. "Customer_Cooperation": Did the customer cooperate with the agent throughout the conversation? ("Yes"/"No").
50. "Customer_Patience": Did the customer show patience throughout the conversation? ("Yes"/"No").
51. "Customer_Reason for Understanding": If the customer did not seem to understand, please explain why?.
52. "Resolution_Reason for Timeframe": If the KYC process was not completed in a timely manner, please explain why?.
53. "Agent_Document Verification": Did the agent properly verify all necessary documents during the call? ("Yes"/"No").
54. "Agent_Reason for Document Verification": If the agent did not properly verify documents, please explain why?.
55. "Timestamp_Conversation Flow": Did the conversation flow naturally and logically, without jumping abruptly between topics? ("Yes"/"No").
56. "Timestamp_Reason for Conversation Flow": If the conversation did not flow naturally, please explain why?.
57. "Timestamp_Silences": Were there any significant silences during the conversation? ("Yes"/"No").
58. "Timestamp_Reason for Silences": If there were significant silences, please explain why?.
59. "Timestamp_Agent's Time Management": Did the agent manage the time effectively, ensuring all necessary points were covered? ("Yes"/"No").
60. "Timestamp_Reason for Agent's Time Management": If the agent did not manage time effectively, please explain why?.
61. "Timestamp_Customer's Time Management": Did the customer respond in a timely manner, without causing unnecessary delays? ("Yes"/"No").
62. "Timestamp_Reason for Customer's Time Management": If the customer did not manage time effectively, please explain why?.

The conversation is delimited by triple backticks in the format ```{conversations}```.
"""
