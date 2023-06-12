from translate import Translator

def translate_text(text, source_lang, target_lang):
    translator = Translator(from_lang=source_lang, to_lang=target_lang)
    translation = translator.translate(text)
    return translation

def main():
    source_lang = "en"  # Source language (e.g., English)

    # Get input text from user
    text = input("Enter the text to translate: ")

    # Get target language from user
    target_lang = input("Enter the target language: ")

    # Perform translation
    translation = translate_text(text, source_lang, target_lang)

    # Print the translated text
    print("Translation:", translation)

# Run the main function
if __name__ == "__main__":
    main()
