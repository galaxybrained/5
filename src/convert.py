import pint

# Initialize the UnitRegistry
ureg = pint.UnitRegistry()

# Define the available unit conversions
unit_conversions = {
    1: {
        'm': ureg.meter,
        'km': ureg.kilometer,
        'cm': ureg.centimeter,
        'ft': ureg.foot,
        'in': ureg.inch,
        'mi': ureg.mile
    },
    2: {
        'C': ureg.degC,
        'F': ureg.degF,
        'K': ureg.kelvin
    },
    3: {
        'm^2': ureg.meter**2,
        'km^2': ureg.kilometer**2,
        'cm^2': ureg.centimeter**2,
        'ft^2': ureg.foot**2,
        'in^2': ureg.inch**2,
        'mi^2': ureg.mile**2
    }
}

# Define the available temperature conversions
temp_conversions = {
    'C_to_F': lambda temp: (temp * 9/5) + 32,
    'C_to_K': lambda temp: temp + 273.15,
    'F_to_C': lambda temp: (temp - 32) * 5/9,
    'F_to_K': lambda temp: (temp + 459.67) * 5/9,
    'K_to_C': lambda temp: temp - 273.15,
    'K_to_F': lambda temp: (temp * 9/5) - 459.67
}

def convert_unit(value, from_unit, to_unit, category):
    if category not in unit_conversions:
        return "Invalid category. Available categories: " + ", ".join(str(cat) for cat in unit_conversions.keys())

    conversions = unit_conversions[category]
    if from_unit not in conversions or to_unit not in conversions:
        return f"Invalid units for category {category}. Available units: " + ", ".join(conversions.keys())

    from_quantity = value * conversions[from_unit]
    converted_value = from_quantity.to(conversions[to_unit])
    return converted_value.magnitude

def convert_temperature(value, from_unit, to_unit):
    if from_unit not in temp_conversions or to_unit not in temp_conversions:
        return "Invalid temperature units. Available units: " + ", ".join(temp_conversions.keys())

    converted_value = temp_conversions[f"{from_unit}_to_{to_unit}"](value)
    return converted_value

while True:
    # Display available categories
    print("\nAvailable categories:")
    for category, units in unit_conversions.items():
        print(f"{category}. {', '.join(units.keys())}")

    # Prompt user for category selection
    category = input("Select a category (or 'quit' to exit): ")

    if category == 'quit':
        break

    category = int(category)

    # Validate category selection
    while category not in unit_conversions:
        print("Invalid category. Please try again.")
        category = input("Select a category (or 'quit' to exit): ")

    # Display available units for the selected category
    print(f"\nAvailable units for category {category}:")
    for unit in unit_conversions[category].keys():
        print(f"- {unit}")

    # Prompt user for unit conversion
    from_unit = input("Convert from unit: ")
    to_unit = input("Convert to unit: ")

    # Validate unit conversion
    while from_unit not in unit_conversions[category] or to_unit not in unit_conversions[category]:
        print("Invalid units. Please try again.")
        from_unit = input("Convert from unit: ")
        to_unit = input("Convert to unit: ")

    # Prompt user for value to convert
    value = float(input("Enter the value to convert: "))

    # Perform unit conversion
    converted_value = convert_unit(value, from_unit, to_unit, category)
    print(f"{value} {from_unit} = {converted_value} {to_unit}")

    # Prompt user to go back to the menu or exit
    choice = input("\nEnter 'menu' to go back to the menu or 'quit' to exit: ")
    if choice == 'quit':
        break
