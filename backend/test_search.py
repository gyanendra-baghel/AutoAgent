#!/usr/bin/env python3
"""
Test script for the AI Agent with search capabilities
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.tools.search_tools import web_search, search_conversion_info

def test_search_tools():
    print("Testing web search tool...")
    
    # Test basic web search
    print("\n1. Testing basic web search:")
    result = web_search("Python programming", 2)
    print(result)
    
    # Test conversion info search
    print("\n2. Testing conversion info search:")
    result = search_conversion_info("meter to feet")
    print(result)
    
    print("\n✅ Search tools test completed!")

if __name__ == "__main__":
    test_search_tools()
