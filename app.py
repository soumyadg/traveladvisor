from flask import Flask, render_template, request, redirect, url_for
import os
from langchain.llms import OpenAI
from langchain.prompts import (
    ChatPromptTemplate, PromptTemplate, SystemMessagePromptTemplate,
    AIMessagePromptTemplate, HumanMessagePromptTemplate
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.chat_models import ChatOpenAI

# Set your OpenAI API key here
OPENAI_API_KEY = 'key'
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Initializing OpenAI with API key
llm = OpenAI(openai_api_key=OPENAI_API_KEY)

# Chat prompt templates
system_template = "You are an AI assistant that is a {travel_planner} for people who has a {certain_budget}."
system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
human_template = "{destination}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
chat = ChatOpenAI(openai_api_key=OPENAI_API_KEY)


def travelgpt_placetovisit(certain_budget, destination, days):
    system_template = "You are an AI travel planning assistant that generates plan for people in {destination} who has a budget of {certain_budget} for {days} days."
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = "{travel_help_request}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    request = chat_prompt.format_prompt(certain_budget=certain_budget,
                                        destination=destination,
                                        days=days,
                                        travel_help_request="Please give me a travel itinerary").to_messages()

    result = chat(request)
    return result.content


@app.route('/')
def welcome():
    return render_template('index2.html')


@app.route('/success/<string:res>')
def success(res):
    result = f"Here is your itinerary: {res}"
    return render_template('results2.html', result=result)


@app.route('/submit', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        destination = str(request.form['destination'])
        amount = float(request.form['amount'])
        number = float(request.form['number_of_days'])
        res = travelgpt_placetovisit(amount, destination, number)
        return redirect(url_for('success', res=res))
    return redirect(url_for('welcome'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
