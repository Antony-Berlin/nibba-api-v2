    
def make_rag_prompt(query, relevant_passage):
  escaped = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")
  prompt = ("""You are a helpful and informative bot that answers questions using text from the reference passage included below. \
  explain in detail if asked about eligibilty. \
  If the passage is irrelevant to the question , respond with "no data found".\
  Be sure to respond in a shortand and complete sentence,and being comprehensive \
  However, you are talking to a non-technical audience and make it short and easy to understand \
  strike a friendly and converstional tone. \
  
  
  PASSAGE: '{relevant_passage}'
  QUESTION: '{query}'

  ANSWER:
  """).format(query=query, relevant_passage=escaped)
  print(prompt)

  return prompt

def search(query, db, top_k=5):
    # Perform similarity search
    results = db.query(
       query_texts=query,
       n_results = top_k
    )
    
    # Concatenate the page content of top documents
    combined_content = ''.join(text for text in results["documents"][0])
    
    return combined_content

def get_search_keywords(chat,model):
    convo = model.start_chat(history=[])
    prompt = ("""you are a vector database manager who get user chat history  and returns the proper keywords to be searched in the large vector db of schemes for the recent query.
    return specific keywords related to the last user query as a string seperated by comma.
    be more specific with the keyword.
    chat history  = {chat_history}
              """).format(chat_history = chat)
    convo.send_message(prompt)
    print(convo.last.text.split(','))
    return convo.last.text.split(',')


def get_response(chat,model):

    convo = model.start_chat(history=chat[:-1])
    convo.send_message(chat[-1]["parts"][-1]["text"])

    if( convo.last.text.lower() == "no data found"):
        ##code to dynamic search
        return "dummy"
    else:
        
        return convo.last.text
    
def get_scheme_name(chat, model):
    convo = model.start_chat(history=[])
    prompt = ("""get the chat history and return the name of the scheme the user refering in the last message  = {chat_history}
              """).format(chat_history = chat)
    convo.send_message(prompt)
    print(convo.last.text.split(','))
    return convo.last.text.split(',')

def get_elgibilty_ques(context, model)