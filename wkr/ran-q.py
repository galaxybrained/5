import requests

def generate_random_question():
    response = requests.get("https://opentdb.com/api.php?amount=1&category=16")
    data = response.json()
    question = data["results"][0]["question"]
    return question

if __name__ == "__main__":
    random_question = generate_random_question()
    print(random_question)

