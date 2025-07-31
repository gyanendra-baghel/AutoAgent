import requests
from typing import Dict, Any
from langchain_core.tools import tool
import os
from datetime import datetime


@tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert currency from one type to another using real-time exchange rates.
    
    Args:
        amount: The amount to convert
        from_currency: Source currency code (e.g., 'USD', 'EUR', 'GBP')
        to_currency: Target currency code (e.g., 'USD', 'EUR', 'GBP')
        
    Returns:
        Formatted conversion result with exchange rate and timestamp
    """
    try:
        # Get API key from environment
        api_key = os.getenv("FREECURRENCY_API_KEY")
        if not api_key:
            return """❌ **Error**: Currency conversion API key not found. 

Please set the FREECURRENCY_API_KEY environment variable with your API key from https://freecurrencyapi.com/"""
        
        # Validate currency codes (should be 3-letter codes)
        from_currency = from_currency.upper().strip()
        to_currency = to_currency.upper().strip()
        
        if len(from_currency) != 3 or len(to_currency) != 3:
            return f"❌ **Error**: Invalid currency codes. Please use 3-letter currency codes (e.g., USD, EUR, GBP)"
        
        # Validate amount
        if amount <= 0:
            return f"❌ **Error**: Amount must be greater than 0"
        
        # Make API request to get latest exchange rates
        api_url = f"https://api.freecurrencyapi.com/v1/latest?apikey={api_key}&base_currency={from_currency}&currencies={to_currency}"
        
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Check if the API returned an error
        if 'error' in data:
            return f"❌ **Error**: {data['error'].get('message', 'Unknown API error')}"
        
        # Extract exchange rate
        if 'data' not in data or to_currency not in data['data']:
            return f"❌ **Error**: Exchange rate not found for {from_currency} to {to_currency}"
        
        exchange_rate = data['data'][to_currency]
        converted_amount = amount * exchange_rate
        
        # Format the result
        return f"""**💱 Currency Conversion Result**

**Original Amount**: {amount:,.2f} {from_currency}
**Converted Amount**: {converted_amount:,.2f} {to_currency}
**Exchange Rate**: 1 {from_currency} = {exchange_rate:.6f} {to_currency}

**Calculation**: {amount:,.2f} × {exchange_rate:.6f} = {converted_amount:,.2f}

🕐 **Rate Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (Real-time)
🔗 **Source**: [FreeCurrencyAPI](https://freecurrencyapi.com/)

*Note: Exchange rates are updated in real-time and may fluctuate throughout the day.*"""
        
    except requests.RequestException as e:
        return f"❌ **Error**: Unable to fetch exchange rates due to network error: {str(e)}"
    except KeyError as e:
        return f"❌ **Error**: Invalid response format from currency API: {str(e)}"
    except Exception as e:
        return f"❌ **Error**: Currency conversion failed: {str(e)}"


@tool
def get_supported_currencies() -> str:
    """Get a list of supported currency codes for conversion.
    
    Returns:
        List of commonly supported currency codes with their descriptions
    """
    try:
        # Get API key from environment
        api_key = os.getenv("FREECURRENCY_API_KEY")
        if not api_key:
            return """❌ **Error**: Currency conversion API key not found. 

Please set the FREECURRENCY_API_KEY environment variable with your API key from https://freecurrencyapi.com/"""
        
        # Make API request to get supported currencies
        api_url = f"https://api.freecurrencyapi.com/v1/currencies?apikey={api_key}"
        
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if 'data' not in data:
            # Fallback to common currencies if API doesn't provide the list
            common_currencies = {
                'USD': 'US Dollar',
                'EUR': 'Euro',
                'GBP': 'British Pound',
                'JPY': 'Japanese Yen',
                'AUD': 'Australian Dollar',
                'CAD': 'Canadian Dollar',
                'CHF': 'Swiss Franc',
                'CNY': 'Chinese Yuan',
                'INR': 'Indian Rupee',
                'KRW': 'South Korean Won',
                'MXN': 'Mexican Peso',
                'BRL': 'Brazilian Real',
                'RUB': 'Russian Ruble',
                'ZAR': 'South African Rand',
                'SGD': 'Singapore Dollar',
                'HKD': 'Hong Kong Dollar',
                'NOK': 'Norwegian Krone',
                'SEK': 'Swedish Krona',
                'DKK': 'Danish Krone',
                'PLN': 'Polish Zloty'
            }
            
            formatted_currencies = []
            for code, name in common_currencies.items():
                formatted_currencies.append(f"• **{code}**: {name}")
            
            return f"""**💱 Commonly Supported Currency Codes**

{chr(10).join(formatted_currencies)}

**Usage Example**: 
- `convert_currency(100, "USD", "EUR")` - Convert 100 USD to EUR
- `convert_currency(50, "GBP", "JPY")` - Convert 50 GBP to JPY

🔗 **Source**: [FreeCurrencyAPI](https://freecurrencyapi.com/)"""
        
        # Process API response
        currencies = data['data']
        formatted_currencies = []
        
        # Sort currencies by code for better readability
        sorted_currencies = sorted(currencies.items())
        
        for code, info in sorted_currencies[:30]:  # Limit to first 30 for readability
            name = info.get('name', 'Unknown')
            formatted_currencies.append(f"• **{code}**: {name}")
        
        total_count = len(currencies)
        showing_count = min(30, total_count)
        
        return f"""**💱 Supported Currency Codes** (Showing {showing_count} of {total_count})

{chr(10).join(formatted_currencies)}

**Usage Example**: 
- `convert_currency(100, "USD", "EUR")` - Convert 100 USD to EUR
- `convert_currency(50, "GBP", "JPY")` - Convert 50 GBP to JPY

🔗 **Source**: [FreeCurrencyAPI](https://freecurrencyapi.com/)

*Note: This is a partial list. The API supports {total_count} currencies in total.*"""
        
    except requests.RequestException as e:
        return f"❌ **Error**: Unable to fetch supported currencies due to network error: {str(e)}"
    except Exception as e:
        return f"❌ **Error**: Failed to get supported currencies: {str(e)}"
