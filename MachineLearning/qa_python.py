from transformers import BertTokenizer, BertForQuestionAnswering
from langchain.text_splitter import CharacterTextSplitter,TokenTextSplitter
import torch
import fitz

def import_pdf(file_obj):
    doc = fitz.open(stream=file_obj.read(), filetype="pdf")
    return "".join(page.get_text() for page in doc)

def text_splitter(text, chunk_size=400, chunk_overlap=50):
    splitter = TokenTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_text(text)

def load_model():
    checkpoint = "bert-large-uncased-whole-word-masking-finetuned-squad"
    tokenizer = BertTokenizer.from_pretrained(checkpoint)
    model = BertForQuestionAnswering.from_pretrained(checkpoint)

    return tokenizer, model

def get_answer(question, chunks, tokenizer, model):
    best_answer = ""
    best_score = float("-inf")

    for chunk in chunks:
        inputs = tokenizer(question, chunk, return_tensors="pt", truncation=True)
        with torch.no_grad():
            output = model(**inputs)

        start_logits = output.start_logits
        end_logits = output.end_logits

        start_index = torch.argmax(start_logits)
        end_index = torch.argmax(end_logits) + 1

        score = start_logits[0][start_index] + end_logits[0][end_index - 1]

        if score > best_score and end_index > start_index and score > 5:
            best_score = score
            answer_ids = inputs["input_ids"][0][start_index:end_index]
            best_answer = tokenizer.decode(answer_ids, skip_special_tokens=True)

    return best_answer if best_answer else "No answer found."
