from flask import Blueprint, request, jsonify, session, render_template
from src.context import chatbot_manager
import markdown

chatbot = Blueprint('chatbot', __name__)

@chatbot.route('/chat', methods=['POST'])
def chat_handler():
    data = request.json
    user_message = data.get('message', '')
    
    chatbot = chatbot_manager.ChatBotManager()
    response = markdown.markdown(chatbot.process_query(user_message), extensions=['md_in_html'])
    
    return jsonify({
        'response': response
    })

@chatbot.route('/reset', methods=['POST'])
def reset_context():
    session.pop('conversation', None)
    return jsonify({'status': 'context reset'})

@chatbot.route('/', methods=['GET'])
def index():
    return render_template('index.html')