import openai
import pdfplumber

# Authenticate with the API
openai.api_key = "Your_Api_key"

# Load the PDF using pdfplumber
def load_pdf(filepath):
    with pdfplumber.open(filepath) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Generate a response using GPT-3
def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.7,
        max_tokens=2048,
        n=1,
        stop=None,
    )
    return response.choices[0].text.strip()

# Main loop
while True:
    file_path = input("Enter the path to the PDF file: ")
    try:
        text = load_pdf(file_path)
        while True:
            user_input = input("Ask a question: ")
            if user_input.lower() == "exit":
                break
            prompt = f"{text}\nQ: {user_input}\nA:"
            response = generate_response(prompt)
            print(response)
    except Exception as e:
        print("Error:", str(e))
