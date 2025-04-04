from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from chatbot import handle_user_query
import os

#Load environment variables from .env
load_dotenv()

#Initialize Flask app
app = Flask(__name__)

#Home route – renders the main HTML page
@app.route('/')
def home():
    return render_template("index.html")

#Chat route – receives user messages and returns AI responses
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")

    #Get the response from chatbot
    response = handle_user_query(user_message)

    return jsonify({"response": response})
#Running main function
if __name__ == '__main__':
    app.run(debug=True)
