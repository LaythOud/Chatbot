from flask import session
from src.services.query import Query
from src.logger import Logger
import json
import src.models as models

log = Logger.get_logger()

class ChatBotManager:
    def __init__(self):
        self.context_window = 3

    def process_query(self, user_input):
        """
        Classifies the query, fetches relevant data, and updates context.
        """
        conversation = session.get('conversation', [])
        
        pre_conversation = self._build_prompt(user_input, conversation)

        log.debug(f"conversation: {pre_conversation}")

        response = self._parse_llm_response(Query.classify_query(user_input, pre_conversation.copy()))
        log.info(f"User query classified as: {response}")

        candidates = self._handle_query(response)
        log.info(f"Candidates that match user query: {candidates}")

        response = Query.response_to_query(user_input, pre_conversation.copy(), candidates)
        log.info(f"Responded to user query as: {response}")

        self._update_context(conversation, user_input, response)

        return response
    
    def _build_prompt(self, user_input, conversation_history):
        base_prompt = []
        for msg in conversation_history[-self.context_window:]:
            base_prompt.append({"role": "user", "content": msg['user']})
            base_prompt.append({"role": "assistant", "content": msg['bot']})

        base_prompt.append({"role": "user", "content": user_input})
        return base_prompt
    
    def _parse_llm_response(self, response):
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"category": "OTHER", "details": {}}

    def _handle_query(self, category_data):
        category = category_data.get("category", "OTHER")
        details = category_data.get("details", {})

        query_map = {
            "FIND_SKILLS": lambda: models.Candidate.find_by_field(models.Candidate.skills, details.get("keywords", [])),
            "FIND_EXPERIENCE": lambda: models.Candidate.find_by_field(models.Candidate.work_experience, details.get("keywords", [])),
            "FIND_EDUCATION": lambda: models.Candidate.find_by_field(models.Candidate.education_history, details.get("keywords", [])),
            "FIND_CERTIFICATIONS": lambda: models.Candidate.find_by_field(models.Candidate.certifications, details.get("keywords", [])),
            "FIND_PROJECTS": lambda: models.Candidate.find_by_field(models.Candidate.projects, details.get("keywords", [])),
            "MATCH_JOB_REQUIREMENTS": lambda: models.Candidate.match_job_requirements(details),
            "OTHER": lambda: "I couldn't classify this query."
        }

        return query_map.get(category, lambda: "Invalid query category.")()


    def _update_context(self, conversation, user_input, response):
        """
        Updates conversation context in the session.
        """
        conversation.append({'user': user_input, 'bot': response})
        session['conversation'] = conversation[-self.context_window:]