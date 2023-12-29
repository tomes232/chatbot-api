#from semantic_search import gen_text_embed, get_text

#from distilbert import get_answer

from transformers import pipeline

from app.load import FileJson

import os

from openai import OpenAI

#from mongo import get_collection


# TODO - expand this section to allow for multiple files

# def get_bot_response(userText:str):
#     embeddings_dataset, tokenizer, model = gen_text_embed()
#     text_dict = get_text(userText, embeddings_dataset, tokenizer, model)

#     score = 0
    
#     #iterate throught the text and filename to find the max score from get_answer
#     for i in  range(len(text_dict['text'])):
#         answer = get_answer(userText, text_dict['text'][i])
#         if answer['score'] > score:
#             score = answer['score']
#             answer = answer['answer']
#             filename = text_dict['filename'][i]

#     return { str(filename) : str(answer['answer']) }

                                       

def answer_resume(userText:str):

    resume = FileJson('resume.json', load=True)
    # print (resume.get_dict()["doc"]["text"])

    model_checkpoint = "huggingface-course/bert-finetuned-squad"
    question_answerer = pipeline("question-answering", model=model_checkpoint)

    question = userText

    return question_answerer(context=resume.get_dict()["doc"]["text"], question=question)


    

