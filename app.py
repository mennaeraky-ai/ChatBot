#!/usr/bin/env python
# coding: utf-8

# In[5]:


from flask import Flask, request, jsonify
import openai
from langdetect import detect, LangDetectException
import requests
import re
import os
from elasticsearch import Elasticsearch

app = Flask(__name__)



# Now, you can access the variables using os.getenv
openai.api_key = "sk-kse_WDeU_zcD0YMgYmq_wMbtMzXJOX_9w1oFXxUBNWT3BlbkFJUtJdInsqGH1-mOeiojNVcrT-GdTxiQLeo1YXxGEZsA"
es = Elasticsearch(["https://elasticsearch-staging-9a4cd8.es.eu-west-1.aws.found.io/"], basic_auth=('elastic', 'EK4PdqRuUkPOYv9orqTFIBmR'), request_timeout=30)

# Helper functions
def get_embedding(text):
    try:
        response = openai.Embedding.create(input=[text], model="text-embedding-ada-002")
        return response['data'][0]['embedding']
    except openai.error.InvalidRequestError as e:
        print(f"Error fetching embedding: {e}")
        return []

def get_answers(user_query):
    # Convert the question into an embedding
    vector_of_input_keyword = get_embedding(user_query)

    # Search Elasticsearch for matching context
    search_body = {
        "knn": {
            "field": "embedding",
            "query_vector": vector_of_input_keyword,
            "k": 10,
            "num_candidates": 100
        },
        "_source": ["response_template", "category", "subcategory"]
    }

    query_response = es.search(index="chatbot_docs_vd", body=search_body)
    if query_response['hits']['total']['value'] > 0:
        top_hit = query_response['hits']['hits'][0]
        context = top_hit['_source'].get('response_template', 'No template found.')
    else:
        return "No relevant responses found."

    # Prompt for chatbot response
    prompt = f"""
    You are a customer supp ort assistant. The customer has an issue, and you are helping them resolve it based on the provided context.

    Context: {context}

    User's Question: {user_query}

    Answer (respond helpfully, be conversational, and rephrase if needed):
    """
    
    response_gen = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Return the chatbot's answer
    return response_gen['choices'][0]['message']['content']

def get_number_steps():
    api_url = f"https://mp1d9b0b258901d47314.free.beeceptor.com/"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        status_data = response.json()
        return status_data.get("step_number")
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return "No steps available"

def get_rider_phone_number():
    api_url = f"https://mpe7a207647688952ee6.free.beeceptor.com/"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        status_data = response.json()
        return status_data.get("phone_number")
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return "No phone number available"

def get_rider_name():
    api_url = f"https://mp22b824ecdec83dfae4.free.beeceptor.com/"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        status_data = response.json()
        return status_data.get("rider_name")
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return "John Doe"

def get_promo_code_info():
    try:
        response = requests.get("https://mp637a7e4fb82f799087.free.beeceptor.com/")
        response.raise_for_status()
        promo_data = response.json()
        return promo_data.get("promo_code")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching promo code info: {e}")
        return "WELCOME50"

def get_order_status_from_api():
    api_url = f"https://9g2e6.wiremockapi.cloud/order/{order_id}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        status_data = response.json()
        return status_data.get("status")
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return "Unknown status"
def get_promise_time():
    api_url = f"https://mp3c3c1bc28d9ad7d4c6.free.beeceptor.com/"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        status_data = response.json()
        return status_data.get("promise_time")
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return "Unknown status"
# Mapping placeholders to functions
placeholder_functions = {
    "rider_name": get_rider_name,
    "promo_code": get_promo_code_info,
    "order_status": get_order_status_from_api,
    "step_number": get_number_steps,
    "phone_number": get_rider_phone_number,
    "promise_time": get_promise_time
}
order_id = 456

def replace_placeholders(text):
    matches = re.findall(r'\[(.*?)\]', text)
    for match in matches:
        if match in placeholder_functions:
            replacement_value = placeholder_functions[match]()
            text = text.replace(f"[{match}]", str(replacement_value))
    return text


# Flask route to handle the chat
@app.route('/chat', methods=['POST'])
def chat():
    # Get user message from the JSON body of the POST request
    user_message = request.json.get('user_message')

    response = get_answers(user_message)
    processed_response = replace_placeholders(response)
    return jsonify({"response": processed_response})
# Run the app
if __name__ == '__main__':
    app.run(debug=True)


# In[ ]:





# In[ ]:





# In[ ]:


 

