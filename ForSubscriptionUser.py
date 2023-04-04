import openai
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextBoxHorizontal
import io

# Authenticate with the API
openai.api_key = "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"

# Preprocess the PDF and extract relevant information
def preprocess_pdf(filepath):
    headings = []
    key_phrases = []
    with open(filepath, 'rb') as pdf_file:
        for page_number, page_layout in enumerate(pdfminer.high_level.extract_pages(pdf_file)):
            for element in page_layout:
                if isinstance(element, LTTextBoxHorizontal):
                    if element.get_text().endswith(":"):
                        key_phrase = element.get_text().strip()[:-1]
                        key_phrases.append((page_number, key_phrase))
                    elif element.get_text().isupper() and len(element.get_text()) > 3:
                        heading = element.get_text().strip()
                        headings.append((page_number, heading))
    return headings, key_phrases

# Generate a response using GPT-3
def generate_response(prompt):
    segments = [prompt[i:i+2048] for i in range(0, len(prompt), 2048)]
    response = ""
    for segment in segments:
        segment_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=segment,
            temperature=0.7,
            max_tokens=2049,
            n=1,
            stop=None,
        )
        response += segment_response.choices[0].text.strip()
    return response

# Main loop
while True:
    file_path = input("Enter the path to the PDF file: ")
    try:
        headings, key_phrases = preprocess_pdf(file_path)
        with open(file_path, "rb") as pdf_file:
            for page_number, page_text in enumerate(extract_text(pdf_file)):
                segments = [page_text[i:i+2048] for i in range(0, len(page_text), 2048)]
                for segment in segments:
                    relevant_headings = [heading[1] for heading in headings if heading[0] == page_number]
                    relevant_key_phrases = [phrase[1] for phrase in key_phrases if phrase[0] == page_number]
                    relevant_text = "\n".join([segment] + relevant_headings + relevant_key_phrases)
                    while True:
                        user_input = input("Ask a question: ")
                        if user_input.lower() == "exit":
                            break
                        prompt = f"{relevant_text}\nQ: {user_input}\nA:"
                        response = generate_response(prompt)
                        print(response)
    except Exception as e:
        print("Error:", str(e))
