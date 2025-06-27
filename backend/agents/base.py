"""
Base Agent class for ProPulse system.
Provides common functionality for all agents.
"""

import json
import logging
import os
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import google.generativeai as genai
from pydantic import BaseModel


class AgentConfig(BaseModel):
    """Configuration for agents."""
    name: str
    version: str
    log_level: str = "INFO"
    max_tokens: int = 8192
    temperature: float = 0.7


class BaseAgent(ABC):
    """Base class for all ProPulse agents."""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.logger = self._setup_logger()
        self.gemini_client = self._setup_gemini()
        
    def _setup_logger(self) -> logging.Logger:
        """Set up logging for the agent."""
        logger = logging.getLogger(f"propulse.{self.config.name}")
        logger.setLevel(getattr(logging, self.config.log_level))
        
        # Create logs directory if it doesn't exist
        log_dir = Path("backend/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # File handler for this agent
        file_handler = logging.FileHandler(
            log_dir / f"{self.config.name}.log"
        )
        file_handler.setLevel(getattr(logging, self.config.log_level))
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _setup_gemini(self) -> genai.GenerativeModel:
        """Set up Gemini client."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        genai.configure(api_key=api_key)
        
        # Use Gemini 2.5 model
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config={
                "temperature": self.config.temperature,
                "max_output_tokens": self.config.max_tokens,
            }
        )
        
        return model
    
    def generate_request_id(self) -> str:
        """Generate a unique request ID."""
        return str(uuid.uuid4())
    
    def log_request_response(self, request_data: Dict[str, Any], 
                           response_data: Dict[str, Any], 
                           log_file: str) -> None:
        """Log request and response to a JSONL file."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent": self.config.name,
            "version": self.config.version,
            "request": request_data,
            "response": response_data
        }
        
        log_dir = Path("backend/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_path = log_dir / log_file
        
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and return output according to agent's purpose."""
        pass
    
    def validate_schema(self, data: Dict[str, Any], schema_path: str) -> bool:
        """Validate data against JSON schema."""
        try:
            # For now, just basic validation
            # In production, use jsonschema library
            return isinstance(data, dict)
        except Exception as e:
            self.logger.error(f"Schema validation failed: {e}")
            return False 