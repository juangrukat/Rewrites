# This Python file uses the following encoding: utf-8
import os
import json
from openai import OpenAI
from typing import Dict, Any, Optional, Tuple, List

class OpenAIAPI:
    def __init__(self, api_key=None, model=None):
        """Initialize the OpenAI API handler"""
        self.api_key = api_key
        self.client = None
        if api_key:
            self.client = OpenAI(api_key=api_key)
        self.model = model if model else "gpt-4"
        
    def set_model(self, model):
        """Set the OpenAI model to use"""
        self.model = model
    
    def set_api_key(self, api_key):
        """Set the OpenAI API key"""
        self.api_key = api_key
        if api_key:
            self.client = OpenAI(api_key=api_key)
    
    def analyze_rewrite(self, excerpt: str, rewrite: str, prompt_template: str) -> Tuple[bool, str]:
        """Send the excerpt and rewrite to OpenAI for analysis"""
        if not self.api_key or not self.client:
            return False, "API key not set. Please set your OpenAI API key in Settings."
        
        # Replace placeholders in the prompt template
        prompt = prompt_template.replace("{excerpt}", excerpt).replace("{rewrite}", rewrite)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert writing coach analyzing rewrites of text excerpts."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            analysis = response.choices[0].message.content
            return True, analysis
                
        except Exception as e:
            return False, f"Error communicating with OpenAI API: {str(e)}"
    
    def get_default_prompt_templates(self) -> Dict[str, str]:
        """Return a dictionary of default prompt templates"""
        return {
            "Basic Analysis": "Please analyze my rewrite of the following excerpt:\n\nOriginal: {excerpt}\n\nRewrite: {rewrite}\n\nProvide feedback on clarity, conciseness, and how well I've maintained the original meaning.",
            "Detailed Critique": "I've rewritten the following excerpt:\n\nOriginal: {excerpt}\n\nRewrite: {rewrite}\n\nPlease provide a detailed critique focusing on:\n1. How well I've maintained the original meaning\n2. Improvements in clarity and conciseness\n3. Grammar and style\n4. Suggestions for further improvement",
            "Academic Style": "I've rewritten this excerpt for an academic paper:\n\nOriginal: {excerpt}\n\nRewrite: {rewrite}\n\nPlease analyze how well I've adapted this to academic writing standards, focusing on formality, precision, and appropriate tone."
        }
    
    def fetch_available_models(self) -> Tuple[bool, List[str]]:
        """Fetch available models from OpenAI API"""
        if not self.api_key or not self.client:
            return False, ["API key not set. Please set your OpenAI API key in Settings."]
        
        try:
            models = self.client.models.list()
            model_ids = [model.id for model in models]
            # Filter for chat models only
            chat_models = [model for model in model_ids if 'gpt' in model.lower()]
            return True, chat_models
        except Exception as e:
            return False, [f"Error fetching models from OpenAI API: {str(e)}"]