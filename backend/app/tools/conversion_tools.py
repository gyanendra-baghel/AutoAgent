from enum import StrEnum
from langchain_core.tools import tool
from app.core.config import KM_TO_MILES, KG_TO_LBS
from app.tools.currency_tools import convert_currency, get_supported_currencies


class WeightUnit(StrEnum):
    KG = "kg"
    LBS = "lbs"


class DistanceUnit(StrEnum):
    KM = "km"
    MILES = "miles"


class TemperatureUnit(StrEnum):
    CELSIUS = "celsius"
    FAHRENHEIT = "fahrenheit"


@tool
def convert_distance(value: float, from_unit: DistanceUnit, to_unit: DistanceUnit) -> float:
    """Convert distance between kilometers and miles.
    
    Args:
        value: The numeric value to convert
        from_unit: The source unit (km or miles)
        to_unit: The target unit (km or miles)
        
    Returns:
        The converted distance value
    """
    if from_unit == DistanceUnit.KM and to_unit == DistanceUnit.MILES:
        return value * KM_TO_MILES
    elif from_unit == DistanceUnit.MILES and to_unit == DistanceUnit.KM:
        return value / KM_TO_MILES
    else:
        raise ValueError(f"Unsupported distance conversion from {from_unit} to {to_unit}")


@tool
def convert_weight(value: float, from_unit: WeightUnit, to_unit: WeightUnit) -> float:
    """Convert weight between kilograms and pounds.
    
    Args:
        value: The numeric value to convert
        from_unit: The source unit (kg or lbs)
        to_unit: The target unit (kg or lbs)
        
    Returns:
        The converted weight value
    """
    if from_unit == WeightUnit.KG and to_unit == WeightUnit.LBS:
        return value * KG_TO_LBS
    elif from_unit == WeightUnit.LBS and to_unit == WeightUnit.KG:
        return value / KG_TO_LBS
    else:
        raise ValueError(f"Unsupported weight conversion from {from_unit} to {to_unit}")


@tool
def convert_temperature(value: float, from_unit: TemperatureUnit, to_unit: TemperatureUnit) -> float:
    """Convert temperature between Celsius and Fahrenheit.
    
    Args:
        value: The numeric value to convert
        from_unit: The source unit (celsius or fahrenheit)
        to_unit: The target unit (celsius or fahrenheit)
        
    Returns:
        The converted temperature value
    """
    if from_unit == TemperatureUnit.CELSIUS and to_unit == TemperatureUnit.FAHRENHEIT:
        return (value * 9/5) + 32
    elif from_unit == TemperatureUnit.FAHRENHEIT and to_unit == TemperatureUnit.CELSIUS:
        return (value - 32) * 5/9
    else:
        raise ValueError(f"Unsupported temperature conversion from {from_unit} to {to_unit}")


# Available tools list
available_tools = [
    convert_distance,
    convert_weight,
    convert_temperature,
    convert_currency,
    get_supported_currencies
]
