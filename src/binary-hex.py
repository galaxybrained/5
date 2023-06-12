import time

def decimal_to_binary(decimal):
    binary_value = bin(decimal & 0xFFFFFFFF).lstrip("0b")
    return binary_value

def decimal_to_hex(decimal):
    hex_value = hex(decimal & 0xFFFFFFFF).lstrip("0x").rstrip("L")
    return hex_value.upper()

def sentence_to_binary(sentence):
    binary_value = ' '.join(decimal_to_binary(ord(char)) for char in sentence)
    return binary_value

def sentence_to_hex(sentence):
    hex_value = ' '.join(decimal_to_hex(ord(char)) for char in sentence)
    return hex_value

def main():
    while True:
        print("=== Conversion Menu ===")
        print("1. Decimal to Binary")
        print("2. Decimal to Hexadecimal")
        print("3. Sentence to Binary")
        print("4. Sentence to Hexadecimal")
        print("5. Exit")

        option = input("Enter your choice (1-5): ")

        if option == "1":
            decimal = int(input("Enter a decimal number: "))
            binary_value = decimal_to_binary(decimal)
            print(f"Decimal {decimal} in Binary: {binary_value}")
        elif option == "2":
            decimal = int(input("Enter a decimal number: "))
            hex_value = decimal_to_hex(decimal)
            print(f"Decimal {decimal} in Hexadecimal: 0x{hex_value}")
        elif option == "3":
            sentence = input("Enter a sentence: ")
            binary_value = sentence_to_binary(sentence)
            print(f"Sentence '{sentence}' in Binary: {binary_value}")
        elif option == "4":
            sentence = input("Enter a sentence: ")
            hex_value = sentence_to_hex(sentence)
            print(f"Sentence '{sentence}' in Hexadecimal: 0x{hex_value}")
        elif option == "5":
            print("Exiting the program...")
            break
        else:
            print("Invalid option selected. Please try again.")
        print()
        time.sleep(1)

if __name__ == "__main__":
    main()
