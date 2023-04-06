from dotenv import load_dotenv
import openai
import os

#Load env vars
# load_dotenv()

import sys


def resource_path(relative_path):
  """ Get absolute path to resource, works for dev and for PyInstaller """
  try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    base_path = sys._MEIPASS
  except Exception:
    base_path = os.path.abspath(".")

  return os.path.join(base_path, relative_path)

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "files/api-key.txt"
# abs_file_path = os.path.join(script_dir, rel_path)
abs_file_path = resource_path(rel_path)

with open(abs_file_path) as f:
  # authenticate openai
  api_key=f.readline()
  openai.api_key = api_key

# print(api_key)
# openai.api_key = api_key


def generate_text_by_keywords(topic: str, keywords: str, language: str, min_word_count: int):
  intro_word_count = 0.2*min_word_count
  body_word_count=0.6*min_word_count
  conclusion_word_count=0.2*min_word_count

  blog_intro = generate_text("Write the opening to a personal blog page about " + topic+ " that includes the keyword(s) (but is not soley focused on): " + keywords+ ". The blog must be in the language: " + language+". The blog must be around the word count: "+str(intro_word_count)+". You do not need to introduce the blog itself, just open the post. Do not say 'welcome to my blog'.")
  blog_body = generate_text("Write the body section of a personal blog for the introduction: '" +blog_intro +"'. The blog body must be about " + topic+ " that includes the keyword (but is not soley focused on): " + keywords+ ". The blog must be in the language: " + language+". The blog must be around the word count: "+str(body_word_count))
  blog_conclusion = generate_text("Write the conclusion section of a personal blog, without saying 'in conclusion' or anything similar, for the introduction: '" +blog_intro +"'. The blog body must be about " + topic+ " that includes the keyword (but is not soley focused on): " + keywords+ ". The blog must be in the language: " + language+". The blog must be around the word count: "+str(conclusion_word_count))
  
  headers_list=generate_headers(blog_body).split('\n')
  
  blog_body_list=blog_body.split('\n\n')
  blog_body_completed =""

  # add header onto each body paragraph
  for index, para in enumerate(blog_body_list):
    header=""
    if len(headers_list)>index:
      header = "<h2>"+headers_list[index]+"</h2>"
    blog_body_completed+=(header+"\n"+para+"\n\n")


  return blog_intro+'\n\n'+blog_body_completed+blog_conclusion

def generate_text_by_title(title: str, language: str, min_word_count: int):
  intro_word_count = 0.2*min_word_count
  body_word_count = 0.6*min_word_count
  conclusion_word_count = 0.2*min_word_count

  blog_intro = generate_text("Write the opening to a personal blog page on the title " + title+ ". The blog must be in the language: " + language+". The blog must be around the word count: "+str(intro_word_count)+". You do not need to introduce the blog itself, just open the post. Do not say 'welcome to my blog'.")
  blog_body = generate_text("Write the body section of a personal blog for the introduction: '" +blog_intro +"'. The blog body must be on the title " + title+ ". The blog must be in the language: " + language+". The blog must be around the word count: "+str(body_word_count))
  blog_conclusion = generate_text("Write the conclusion section of a personal blog, without saying 'in conclusion' or anything similar, for the introduction: '" +blog_intro +"'. The blog body must be about " + title+". The blog must be in the language: " + language+". The blog must be around the word count: "+str(conclusion_word_count))
  
  headers_list=generate_headers(blog_body).split('\n')
  
  blog_body_list=blog_body.split('\n\n')
  blog_body_completed =""

  # add header onto each body paragraph
  for index, para in enumerate(blog_body_list):
    header =""
    if index < len(headers_list):
      header = "<h2>"+headers_list[index].replace('-','')+"</h2>"

    blog_body_completed+=(header+"\n"+para+"\n\n")

  return blog_intro+'\n\n'+blog_body_completed+blog_conclusion

def generate_headers(blog_body):
  return generate_text("create a list (NOT NUMBERED) of short header titles for each main paragraph seperated by a line with no other text for each paragraph (seperated by a line) in the blog body. Do not include anything except the header titles. MAKE SURE THAT IT IS ONLY THE ONE-LINER OF THE HEADER TITLE. Make sure that the number of headers matches the number of paragraphs: '"+blog_body+"'")

def generate_text(content):
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a blog writer. You have a nice personal touch on your writings and share your own opinions fluidly"},
        {"role": "user", "content": content}
      ]
  )
  return response['choices'][0]['message']['content']

