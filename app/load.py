#from docx import Document
import os
#import requests
import json
#import openai
from datetime import datetime
import re

class FileJson:
    """

    Example Json Structure
    {
    "doc": {
        "text": "",
        "metadata": {
            "title": "resume",
            "url" : "https://www.linkedin.com/in/alexander-levine-1b1b1b1b/",
            "file": "resume.txt",
            "length": 0,
            "created": "2021-10-13T20:00:00.000Z",
            "last_modified": "2021-10-13T20:00:00.000Z",
            "tags": ["resume"]
        }
    }
    }
    """


    def __init__(self, filename: str, text: str= None, tags: [str]=[], url: str="", title: str="", file:str=None, length: int=0, last_modified: str="", load: bool=False):
        self.filename = filename
        if title == "":
            #remove the file extension
            title = ''.join(filename.split('.')[:-1])
            self.title = title
        self.text = text
        self.File = file

        self.length = length
        self.url = url
        self.tags = tags


        now = datetime.now()
        self.created = now.strftime("%m/%d/%Y %H:%M:%S")
        self.last_modified = now.strftime("%m/%d/%Y %H:%M:%S")

        if load:
            self.load_json()
        

    def getText(self, directory='./text'):
        """
        This function takes a filename and returns the text from the file
        """

        path = os.path.join(directory, self.filename)
        #if self.filename.split('.')[-1] == 'docx':
        #    self.getDocx(path)
        #elif self.filename.split('.')[-1] == 'txt':


        with open(path, 'r') as f:
            self.text = f.read()
      
        self.length = len(''.split(self.text))

        return



    def update_json(self, filename, directory='./text_json'):
        #update the json file with the new dict
        path = os.path.join(directory, filename)
        with open(path, 'w') as f:
            json.dump(self.get_dict(), f)
        return
    
    def save_json(self, directory='./text_json'):
        # saves get_json to title + .json
        path = os.path.join(directory, self.title + '.json')
        with open(path, 'w') as f:
            json.dump(self.get_dict(), f)
        return
        
    def get_dict(self):
        """
        return a dictionary in the format of the json file specified in the constructor
        """
        return {"doc": {"text": self.text, "metadata": {"title": self.filename, "url": self.url, "file": self.filename, "length": self.length, "last_modified": self.last_modified, "tags": self.tags}}}

    # TODO - clean up this functionality
    def load_json(self, directory='./text_json'):
        path = os.path.join(directory, self.filename)
        with open(path, 'r') as f:
            data = json.load(f)
        try:
            self.text = data['doc']['text']
            
            self.filename = data['doc']['metadata']['file']
            #self.title = data['doc']['metadata']['title']
            #self.url = data['doc']['metadata']['url']
            #self.created = data['doc']['metadata']['created']
            #self.last_modified = data['doc']['metadata']['last_modified']
            #self.last_modified = data[file]['metadata']['last_modified']
            #self.length = data[file]['metadata']['length']
            #self.tag = data[file]['metadata']['tags']
        except:
            print('Error loading json file')
            return
        return
    
    




def unformat_text(text: str) -> str:
    return re.sub(r'\W+', '', text)



#Main function
if __name__ == "__main__":
    #load resume.txt into a json file
    file = FileJson('resume.txt', tags=['resume'])
    file.getText()
    file.save_json()

