import requests
from typing import List, Dict, Any
from langchain_core.tools import tool
import os
from datetime import datetime


@tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Search the web for information and return results with references.
    
    Args:
        query: The search query string
        num_results: Number of search results to return (default: 3, max: 5)
        
    Returns:
        Formatted search results with titles, snippets, and URLs
    """
    try:
        # Limit num_results to prevent too many results
        num_results = min(max(num_results, 1), 5)
        
        # For unit conversion queries, provide immediate conversion factors
        if "unit conversion" in query.lower() and any(unit in query.lower() for unit in ["millimeter", "centimeter", "meter", "inch", "foot", "yard"]):
            # Common conversion factors
            conversions = {
                "millimeter to centimeter": "1 centimeter = 10 millimeters, so to convert millimeters to centimeters, divide by 10",
                "centimeter to millimeter": "1 centimeter = 10 millimeters, so to convert centimeters to millimeters, multiply by 10",
                "meter to centimeter": "1 meter = 100 centimeters, so to convert meters to centimeters, multiply by 100",
                "centimeter to meter": "1 meter = 100 centimeters, so to convert centimeters to meters, divide by 100",
                "meter to millimeter": "1 meter = 1000 millimeters, so to convert meters to millimeters, multiply by 1000",
                "millimeter to meter": "1 meter = 1000 millimeters, so to convert millimeters to meters, divide by 1000",
                "inch to centimeter": "1 inch = 2.54 centimeters, so to convert inches to centimeters, multiply by 2.54",
                "centimeter to inch": "1 inch = 2.54 centimeters, so to convert centimeters to inches, divide by 2.54",
                "foot to meter": "1 foot = 0.3048 meters, so to convert feet to meters, multiply by 0.3048",
                "meter to foot": "1 foot = 0.3048 meters, so to convert meters to feet, divide by 0.3048"
            }
            
            for conv_key, conv_info in conversions.items():
                if all(word in query.lower() for word in conv_key.split()):
                    return f"""**1. Unit Conversion: {conv_key.title()}**
{conv_info}
🔗 Source: [Metric System Reference](https://en.wikipedia.org/wiki/Metric_system)

**Formula**: Use the conversion factor above to multiply or divide as indicated."""
        
        # Use DuckDuckGo's instant answer API as a fallback search
        encoded_query = quote_plus(query)
        ddg_url = f"https://api.duckduckgo.com/?q={encoded_query}&format=json&no_html=1&skip_disambig=1"
        
        response = requests.get(ddg_url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        results = []
        
        # Process instant answer if available
        if data.get('Abstract'):
            results.append({
                'title': data.get('Heading', 'DuckDuckGo Instant Answer'),
                'snippet': data.get('Abstract', ''),
                'url': data.get('AbstractURL', 'https://duckduckgo.com'),
                'source': data.get('AbstractSource', 'DuckDuckGo')
            })
        
        # Process related topics
        for topic in data.get('RelatedTopics', [])[:num_results-len(results)]:
            if isinstance(topic, dict) and topic.get('Text'):
                results.append({
                    'title': topic.get('Text', '').split(' - ')[0] if ' - ' in topic.get('Text', '') else 'Related Topic',
                    'snippet': topic.get('Text', ''),
                    'url': topic.get('FirstURL', 'https://duckduckgo.com'),
                    'source': 'DuckDuckGo'
                })
        
        # If no results from instant answer, create a fallback response
        if not results:
            results.append({
                'title': f'Search Results for: {query}',
                'snippet': f'Search performed for "{query}". For detailed results, please visit a search engine directly.',
                'url': f'https://duckduckgo.com/?q={encoded_query}',
                'source': 'DuckDuckGo'
            })
        
        # Format results for display
        formatted_results = []
        for i, result in enumerate(results[:num_results], 1):
            formatted_result = f"""**{i}. {result['title']}**
{result['snippet']}
🔗 Source: [{result['source']}]({result['url']})
"""
            formatted_results.append(formatted_result)
        
        return "\n".join(formatted_results)
        
    except requests.RequestException as e:
        return f"Search temporarily unavailable due to network error: {str(e)}"
    except Exception as e:
        return f"Search error: {str(e)}"


@tool 
def search_conversion_info(query: str) -> str:
    """Search for specific conversion information, formulas, or unit definitions.
    
    Args:
        query: Conversion-related search query
        
    Returns:
        Search results focused on conversion information with references
    """
    # Built-in conversion database for common units
    conversion_database = {
        "millimeter to centimeter": {
            "factor": 0.1,
            "description": "1 centimeter = 10 millimeters, so to convert millimeters to centimeters, divide by 10 (or multiply by 0.1)",
            "formula": "centimeters = millimeters ÷ 10",
            "source": "International System of Units (SI)"
        },
        "centimeter to millimeter": {
            "factor": 10,
            "description": "1 centimeter = 10 millimeters, so to convert centimeters to millimeters, multiply by 10",
            "formula": "millimeters = centimeters × 10",
            "source": "International System of Units (SI)"
        },
        "meter to centimeter": {
            "factor": 100,
            "description": "1 meter = 100 centimeters, so to convert meters to centimeters, multiply by 100",
            "formula": "centimeters = meters × 100",
            "source": "International System of Units (SI)"
        },
        "centimeter to meter": {
            "factor": 0.01,
            "description": "1 meter = 100 centimeters, so to convert centimeters to meters, divide by 100 (or multiply by 0.01)",
            "formula": "meters = centimeters ÷ 100",
            "source": "International System of Units (SI)"
        },
        "millimeter to meter": {
            "factor": 0.001,
            "description": "1 meter = 1000 millimeters, so to convert millimeters to meters, divide by 1000 (or multiply by 0.001)",
            "formula": "meters = millimeters ÷ 1000",
            "source": "International System of Units (SI)"
        },
        "meter to millimeter": {
            "factor": 1000,
            "description": "1 meter = 1000 millimeters, so to convert meters to millimeters, multiply by 1000",
            "formula": "millimeters = meters × 1000",
            "source": "International System of Units (SI)"
        },
        "inch to centimeter": {
            "factor": 2.54,
            "description": "1 inch = 2.54 centimeters, so to convert inches to centimeters, multiply by 2.54",
            "formula": "centimeters = inches × 2.54",
            "source": "International System of Units (SI)"
        },
        "centimeter to inch": {
            "factor": 0.393701,
            "description": "1 inch = 2.54 centimeters, so to convert centimeters to inches, divide by 2.54",
            "formula": "inches = centimeters ÷ 2.54",
            "source": "International System of Units (SI)"
        }
    }
    
    # Normalize the query to find matching conversion
    query_lower = query.lower().strip()
    
    # Try to find a matching conversion
    for conversion_key, conversion_data in conversion_database.items():
        # Check if the query contains the conversion pattern
        units = conversion_key.split(" to ")
        if len(units) == 2:
            from_unit, to_unit = units[0], units[1]
            if (from_unit in query_lower and to_unit in query_lower) or conversion_key in query_lower:
                return f"""**Unit Conversion: {conversion_key.title()}**

{conversion_data['description']}

**Formula**: {conversion_data['formula']}
**Conversion Factor**: {conversion_data['factor']}

🔗 Source: [{conversion_data['source']}](https://en.wikipedia.org/wiki/International_System_of_Units)

**Example**: To convert X {from_unit}s to {to_unit}s, calculate: X × {conversion_data['factor']} = result in {to_unit}s"""
    
    # If no direct match found, try partial matching
    for conversion_key, conversion_data in conversion_database.items():
        units = conversion_key.split(" to ")
        if len(units) == 2:
            from_unit, to_unit = units[0], units[1]
            # Check for partial matches
            if any(unit in query_lower for unit in [from_unit, to_unit]):
                return f"""**Unit Conversion: {conversion_key.title()}**

{conversion_data['description']}

**Formula**: {conversion_data['formula']}
**Conversion Factor**: {conversion_data['factor']}

🔗 Source: [{conversion_data['source']}](https://en.wikipedia.org/wiki/International_System_of_Units)"""
    
    # Fallback response
    return f"""**Conversion Information for: {query}**

I searched for conversion information related to "{query}". For detailed conversion factors and formulas, please refer to standard measurement references.

🔗 Source: [Unit Conversion Reference](https://en.wikipedia.org/wiki/Conversion_of_units)

**Note**: Use standard metric or imperial conversion tables for accurate conversion factors."""


@tool
def calculator(expression: str) -> str:
    """Perform mathematical calculations and return the result.
    
    Args:
        expression: Mathematical expression to evaluate (supports +, -, *, /, **, (), sqrt, sin, cos, tan, log, etc.)
        
    Returns:
        Formatted calculation result with the expression and answer
    """
    try:
        # Clean and validate the expression
        expression = expression.strip()
        
        # Replace common mathematical functions and constants
        replacements = {
            'sqrt': 'math.sqrt',
            'sin': 'math.sin',
            'cos': 'math.cos',
            'tan': 'math.tan',
            'log': 'math.log',
            'ln': 'math.log',
            'log10': 'math.log10',
            'exp': 'math.exp',
            'pi': 'math.pi',
            'e': 'math.e',
            'abs': 'abs',
            'round': 'round',
            'ceil': 'math.ceil',
            'floor': 'math.floor',
            '^': '**'  # Replace ^ with ** for exponentiation
        }
        
        # Apply replacements
        safe_expression = expression
        for old, new in replacements.items():
            # Use word boundaries to avoid partial replacements
            pattern = r'\b' + re.escape(old) + r'\b'
            safe_expression = re.sub(pattern, new, safe_expression)
        
        # Remove any potentially dangerous characters/functions
        dangerous_patterns = [
            r'import\s+',
            r'exec\s*\(',
            r'eval\s*\(',
            r'__',
            r'open\s*\(',
            r'file\s*\(',
            r'input\s*\(',
            r'raw_input\s*\('
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, safe_expression, re.IGNORECASE):
                return f"❌ **Error**: Invalid expression - contains prohibited operations"
        
        # Validate that expression only contains allowed characters
        allowed_chars = set('0123456789+-*/().abcdefghijklmnopqrstuvwxyz_')
        if not all(c.lower() in allowed_chars or c.isspace() for c in safe_expression):
            return f"❌ **Error**: Expression contains invalid characters"
        
        # Evaluate the expression
        result = eval(safe_expression, {"__builtins__": {}}, {"math": math})
        
        # Format the result nicely
        if isinstance(result, float):
            if result.is_integer():
                result = int(result)
            else:
                # Round to 10 decimal places to avoid floating point precision issues
                result = round(result, 10)
        
        return f"""**🧮 Calculator Result**

**Expression**: `{expression}`
**Result**: `{result}`

**Calculation**: {expression} = {result}"""
        
    except ZeroDivisionError:
        return f"❌ **Error**: Division by zero in expression: `{expression}`"
    except ValueError as e:
        return f"❌ **Error**: Invalid value in expression `{expression}`: {str(e)}"
    except SyntaxError:
        return f"❌ **Error**: Invalid syntax in expression: `{expression}`"
    except Exception as e:
        return f"❌ **Error**: Could not evaluate expression `{expression}`: {str(e)}"


@tool
def advanced_calculator(expression: str, description: str = "") -> str:
    """Perform advanced mathematical calculations with step-by-step explanation.
    
    Args:
        expression: Complex mathematical expression
        description: Optional description of what the calculation represents
        
    Returns:
        Detailed calculation result with explanation
    """
    try:
        # First get the basic calculation result
        basic_result = calculator(expression)
        
        if basic_result.startswith("❌"):
            return basic_result
        
        # Extract the result value for additional analysis
        result_match = re.search(r'Result.*?`([^`]+)`', basic_result)
        if result_match:
            result_value = result_match.group(1)
            
            additional_info = []
            
            # Try to parse the result as a number for additional insights
            try:
                num_result = float(result_value)
                
                # Add number properties
                if num_result == int(num_result):
                    additional_info.append(f"• Integer value: {int(num_result)}")
                
                if num_result > 0:
                    additional_info.append(f"• Square root: ≈ {math.sqrt(num_result):.6f}")
                    
                if num_result != 0:
                    additional_info.append(f"• Reciprocal: {1/num_result:.6f}")
                
                # Scientific notation for large/small numbers
                if abs(num_result) >= 1000 or (0 < abs(num_result) < 0.001):
                    additional_info.append(f"• Scientific notation: {num_result:.3e}")
                    
            except (ValueError, OverflowError):
                pass
            
            # Add description if provided
            if description:
                description_text = f"\n**Context**: {description}\n"
            else:
                description_text = ""
            
            if additional_info:
                additional_text = "\n**Additional Information**:\n" + "\n".join(additional_info)
            else:
                additional_text = ""
            
            return f"""{basic_result}{description_text}{additional_text}"""
        
        return basic_result
        
    except Exception as e:
        return f"❌ **Error**: Advanced calculation failed: {str(e)}"
