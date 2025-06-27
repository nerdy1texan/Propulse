"""
Retriever Agent for ProPulse system.
Searches through historical proposals and RFPs to find relevant content.
"""

import json
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .base import BaseAgent, AgentConfig


class RetrieverAgent(BaseAgent):
    """Agent responsible for retrieving relevant content from historical proposals."""
    
    def __init__(self):
        config = AgentConfig(
            name="retriever_agent",
            version="1.0.0",
            log_level="INFO"
        )
        super().__init__(config)
        self.sample_rfps_path = Path("shared/sample_rfps")
        
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process RFP text and return relevant snippets from sample RFPs.
        
        Args:
            input_data: Dictionary containing 'rfp_text' key
            
        Returns:
            Dictionary following MCP schema for retriever output
        """
        start_time = time.time()
        request_id = self.generate_request_id()
        
        try:
            rfp_text = input_data.get("rfp_text", "")
            if not rfp_text:
                raise ValueError("rfp_text is required in input_data")
            
            self.logger.info(f"Processing retrieval request {request_id}")
            
            # Extract keywords and requirements using Gemini
            keywords, requirements = self._extract_keywords_and_requirements(rfp_text)
            
            # Search through sample RFPs
            snippets = self._search_sample_rfps(rfp_text, keywords, requirements)
            
            # Build response according to MCP schema
            processing_time = (time.time() - start_time) * 1000
            
            response = {
                "request_id": request_id,
                "query": {
                    "rfp_text": rfp_text,
                    "keywords": keywords,
                    "requirements": requirements
                },
                "results": {
                    "total_found": len(snippets),
                    "snippets": snippets
                },
                "metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "processing_time_ms": processing_time,
                    "agent_version": self.config.version,
                    "search_method": "hybrid"
                }
            }
            
            # Log request and response
            self.log_request_response(
                request_data=input_data,
                response_data=response,
                log_file="retriever_logs.jsonl"
            )
            
            self.logger.info(f"Retrieval completed for {request_id}. Found {len(snippets)} relevant snippets")
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing retrieval request {request_id}: {e}")
            error_response = {
                "request_id": request_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.log_request_response(
                request_data=input_data,
                response_data=error_response,
                log_file="retriever_logs.jsonl"
            )
            
            raise
    
    def _extract_keywords_and_requirements(self, rfp_text: str) -> Tuple[List[str], List[str]]:
        """Extract keywords and requirements from RFP text using Gemini."""
        try:
            prompt = f"""
            Analyze the following RFP text and extract:
            1. Key technical keywords (technologies, frameworks, platforms)
            2. Main functional requirements
            
            RFP Text: {rfp_text}
            
            Please respond in JSON format:
            {{
                "keywords": ["keyword1", "keyword2", ...],
                "requirements": ["requirement1", "requirement2", ...]
            }}
            """
            
            response = self.gemini_client.generate_content(prompt)
            
            # Parse the JSON response
            try:
                parsed = json.loads(response.text)
                keywords = parsed.get("keywords", [])
                requirements = parsed.get("requirements", [])
                
                # Fallback to regex extraction if JSON parsing fails
                if not keywords and not requirements:
                    keywords, requirements = self._fallback_extraction(rfp_text)
                
                return keywords[:10], requirements[:10]  # Limit to top 10 each
                
            except json.JSONDecodeError:
                self.logger.warning("Failed to parse Gemini response as JSON, using fallback extraction")
                return self._fallback_extraction(rfp_text)
                
        except Exception as e:
            self.logger.warning(f"Error with Gemini extraction: {e}, using fallback")
            return self._fallback_extraction(rfp_text)
    
    def _fallback_extraction(self, rfp_text: str) -> Tuple[List[str], List[str]]:
        """Fallback keyword and requirement extraction using regex patterns."""
        # Common technical keywords
        tech_keywords = [
            "API", "cloud", "database", "security", "authentication", "integration",
            "mobile", "web", "microservices", "AWS", "Azure", "React", "Python",
            "Java", "JavaScript", "SQL", "REST", "GraphQL", "Docker", "Kubernetes"
        ]
        
        # Extract keywords that appear in the text
        keywords = []
        text_lower = rfp_text.lower()
        for keyword in tech_keywords:
            if keyword.lower() in text_lower:
                keywords.append(keyword)
        
        # Extract requirements (sentences containing requirement indicators)
        requirement_patterns = [
            r"must\s+\w+",
            r"should\s+\w+",
            r"require[ds]?\s+\w+",
            r"need[s]?\s+to\s+\w+"
        ]
        
        requirements = []
        for pattern in requirement_patterns:
            matches = re.findall(pattern, rfp_text, re.IGNORECASE)
            requirements.extend(matches[:3])  # Limit matches per pattern
        
        return keywords[:10], requirements[:5]
    
    def _search_sample_rfps(self, rfp_text: str, keywords: List[str], 
                           requirements: List[str]) -> List[Dict[str, Any]]:
        """Search through sample RFPs and return relevant snippets."""
        snippets = []
        
        # Load all sample RFP files
        rfp_files = self._load_sample_rfps()
        
        for file_path, rfp_data in rfp_files:
            # Calculate relevance score
            relevance_score = self._calculate_relevance(
                rfp_text, keywords, requirements, rfp_data
            )
            
            if relevance_score > 0.1:  # Threshold for relevance
                # Extract relevant content snippets
                content_snippets = self._extract_content_snippets(
                    rfp_data, keywords, requirements
                )
                
                for content, section in content_snippets:
                    snippet = {
                        "source_file": str(file_path.relative_to(Path("."))),
                        "relevance_score": relevance_score,
                        "content": content,
                        "section": section,
                        "metadata": rfp_data.get("metadata", {})
                    }
                    snippets.append(snippet)
        
        # Sort by relevance score (descending) and limit results
        snippets.sort(key=lambda x: x["relevance_score"], reverse=True)
        return snippets[:20]  # Return top 20 snippets
    
    def _load_sample_rfps(self) -> List[Tuple[Path, Dict[str, Any]]]:
        """Load all sample RFP files."""
        rfp_files = []
        
        if not self.sample_rfps_path.exists():
            self.logger.warning(f"Sample RFPs directory not found: {self.sample_rfps_path}")
            return rfp_files
        
        for file_path in self.sample_rfps_path.rglob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    rfp_data = json.load(f)
                    rfp_files.append((file_path, rfp_data))
            except Exception as e:
                self.logger.warning(f"Failed to load {file_path}: {e}")
        
        self.logger.info(f"Loaded {len(rfp_files)} sample RFP files")
        return rfp_files
    
    def _calculate_relevance(self, rfp_text: str, keywords: List[str], 
                           requirements: List[str], rfp_data: Dict[str, Any]) -> float:
        """Calculate relevance score between input RFP and sample RFP."""
        score = 0.0
        rfp_text_lower = rfp_text.lower()
        
        # Convert RFP data to searchable text
        searchable_text = self._rfp_to_text(rfp_data).lower()
        
        # Keyword matching (40% of score)
        keyword_matches = 0
        for keyword in keywords:
            if keyword.lower() in searchable_text:
                keyword_matches += 1
        
        if keywords:
            score += 0.4 * (keyword_matches / len(keywords))
        
        # Industry matching (30% of score)
        rfp_industry = rfp_data.get("metadata", {}).get("industry", "")
        if rfp_industry:
            # Simple industry detection in input text
            if rfp_industry.lower() in rfp_text_lower:
                score += 0.3
        
        # Proposal type matching (20% of score)
        proposal_type = rfp_data.get("metadata", {}).get("proposal_type", "")
        if proposal_type:
            # Check for similar proposal types
            type_keywords = proposal_type.replace("_", " ").split()
            type_matches = sum(1 for word in type_keywords if word.lower() in rfp_text_lower)
            if type_keywords:
                score += 0.2 * (type_matches / len(type_keywords))
        
        # Requirement similarity (10% of score)
        if requirements:
            req_text = " ".join(requirements).lower()
            common_words = set(req_text.split()) & set(searchable_text.split())
            if req_text.split():
                score += 0.1 * (len(common_words) / len(set(req_text.split())))
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _rfp_to_text(self, rfp_data: Dict[str, Any]) -> str:
        """Convert RFP data structure to searchable text."""
        text_parts = []
        
        # Add metadata text
        metadata = rfp_data.get("metadata", {})
        for key, value in metadata.items():
            if isinstance(value, str):
                text_parts.append(value)
        
        # Add sections text
        sections = rfp_data.get("sections", {})
        for section_name, section_content in sections.items():
            if isinstance(section_content, str):
                text_parts.append(section_content)
            elif isinstance(section_content, dict):
                # Handle nested structures like requirements
                for key, value in section_content.items():
                    if isinstance(value, list):
                        text_parts.extend([str(item) for item in value])
                    else:
                        text_parts.append(str(value))
            elif isinstance(section_content, list):
                text_parts.extend([str(item) for item in section_content])
        
        return " ".join(text_parts)
    
    def _extract_content_snippets(self, rfp_data: Dict[str, Any], 
                                keywords: List[str], requirements: List[str]) -> List[Tuple[str, str]]:
        """Extract relevant content snippets from RFP data."""
        snippets = []
        
        sections = rfp_data.get("sections", {})
        for section_name, section_content in sections.items():
            if isinstance(section_content, str):
                # Check if section contains relevant keywords
                if any(keyword.lower() in section_content.lower() for keyword in keywords):
                    snippets.append((section_content[:500], section_name))
            
            elif isinstance(section_content, dict):
                for subsection, content in section_content.items():
                    if isinstance(content, list):
                        # Join list items and check for relevance
                        content_text = ". ".join([str(item) for item in content])
                        if any(keyword.lower() in content_text.lower() for keyword in keywords):
                            snippets.append((content_text[:500], f"{section_name}.{subsection}"))
            
            elif isinstance(section_content, list):
                content_text = ". ".join([str(item) for item in section_content])
                if any(keyword.lower() in content_text.lower() for keyword in keywords):
                    snippets.append((content_text[:500], section_name))
        
        return snippets[:5]  # Limit to 5 snippets per RFP 