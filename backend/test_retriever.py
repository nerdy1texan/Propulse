#!/usr/bin/env python3
"""
Test script for the Retriever Agent.
Run this to validate the agent functionality.
"""

import json
import os
import sys
from pathlib import Path

# Add the parent directory to sys.path so we can import agents
sys.path.append(str(Path(__file__).parent.parent))

from backend.agents.retriever_agent import RetrieverAgent


def test_retriever_agent():
    """Test the Retriever Agent with sample input."""
    
    # Sample RFP text for testing
    test_rfp = """
    We are looking for a software development partner to build a modern web application
    with the following requirements:
    
    - Cloud-native deployment on AWS
    - React frontend with responsive design
    - Python FastAPI backend
    - PostgreSQL database
    - RESTful API design
    - User authentication and authorization
    - Real-time notifications
    - Mobile responsive interface
    - High availability and scalability
    - Security compliance (SOC 2)
    
    The application should support 10,000 concurrent users and integrate with
    third-party payment systems. We need comprehensive documentation and
    6 months of post-launch support.
    """
    
    print("🧪 Testing Retriever Agent")
    print("=" * 50)
    
    try:
        # Initialize the agent
        print("Initializing Retriever Agent...")
        agent = RetrieverAgent()
        
        # Process the test RFP
        print("Processing test RFP...")
        input_data = {"rfp_text": test_rfp}
        
        result = agent.process(input_data)
        
        # Display results
        print(f"\n✅ Processing completed successfully!")
        print(f"Request ID: {result['request_id']}")
        print(f"Processing Time: {result['metadata']['processing_time_ms']:.2f}ms")
        print(f"Total Snippets Found: {result['results']['total_found']}")
        
        print(f"\n📋 Extracted Keywords ({len(result['query']['keywords'])}):")
        for keyword in result['query']['keywords']:
            print(f"  - {keyword}")
        
        print(f"\n📝 Extracted Requirements ({len(result['query']['requirements'])}):")
        for requirement in result['query']['requirements']:
            print(f"  - {requirement}")
        
        print(f"\n🔍 Top Relevant Snippets:")
        for i, snippet in enumerate(result['results']['snippets'][:5], 1):
            print(f"\n{i}. Source: {snippet['source_file']}")
            print(f"   Relevance: {snippet['relevance_score']:.3f}")
            print(f"   Section: {snippet['section']}")
            print(f"   Content: {snippet['content'][:200]}...")
            if snippet.get('metadata'):
                metadata = snippet['metadata']
                print(f"   Industry: {metadata.get('industry', 'N/A')}")
                print(f"   Client: {metadata.get('client', 'N/A')}")
        
        # Validate MCP schema compliance
        print(f"\n🔧 Schema Validation:")
        required_fields = ['request_id', 'query', 'results', 'metadata']
        all_present = all(field in result for field in required_fields)
        print(f"   Required fields present: {'✅' if all_present else '❌'}")
        
        query_fields = ['rfp_text', 'keywords', 'requirements']
        query_valid = all(field in result['query'] for field in query_fields)
        print(f"   Query structure valid: {'✅' if query_valid else '❌'}")
        
        results_fields = ['total_found', 'snippets']
        results_valid = all(field in result['results'] for field in results_fields)
        print(f"   Results structure valid: {'✅' if results_valid else '❌'}")
        
        metadata_fields = ['timestamp', 'processing_time_ms', 'agent_version']
        metadata_valid = all(field in result['metadata'] for field in metadata_fields)
        print(f"   Metadata structure valid: {'✅' if metadata_valid else '❌'}")
        
        print(f"\n📊 Summary:")
        print(f"   Agent Version: {result['metadata']['agent_version']}")
        print(f"   Search Method: {result['metadata']['search_method']}")
        print(f"   Timestamp: {result['metadata']['timestamp']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_edge_cases():
    """Test edge cases for the Retriever Agent."""
    print("\n🧪 Testing Edge Cases")
    print("=" * 50)
    
    agent = RetrieverAgent()
    
    # Test empty input
    print("Testing empty RFP text...")
    try:
        result = agent.process({"rfp_text": ""})
        print("❌ Should have failed with empty input")
    except ValueError:
        print("✅ Correctly handled empty input")
    
    # Test missing rfp_text key
    print("Testing missing rfp_text key...")
    try:
        result = agent.process({})
        print("❌ Should have failed with missing key")
    except ValueError:
        print("✅ Correctly handled missing key")
    
    # Test very short input
    print("Testing very short input...")
    try:
        result = agent.process({"rfp_text": "Build app"})
        print(f"✅ Handled short input, found {result['results']['total_found']} snippets")
    except Exception as e:
        print(f"❌ Failed with short input: {e}")


if __name__ == "__main__":
    print("ProPulse Retriever Agent Test Suite")
    print("=" * 60)
    
    # Check if sample RFPs exist
    sample_rfps_path = Path("shared/sample_rfps")
    if not sample_rfps_path.exists():
        print("❌ Sample RFPs directory not found!")
        print("Please ensure the shared/sample_rfps directory exists with sample files.")
        sys.exit(1)
    
    # Run main test
    success = test_retriever_agent()
    
    if success:
        # Run edge case tests
        test_edge_cases()
        print("\n🎉 All tests completed!")
    else:
        print("\n💥 Main test failed!")
        sys.exit(1) 