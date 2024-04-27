import numpy as np

import torch
from transformers import BertTokenizer, BertForSequenceClassification


def classificate(path: str, answers: list[str]) -> int:
    """Классифицирует с помощью переданного классификатора
    path: str - путь к модели
    return: int - предсказанная метка
    """
    tokenizer = BertTokenizer.from_pretrained(path)
    model = BertForSequenceClassification.from_pretrained(path)
    
    model.to('cpu')
    
    text = ' '.join(answers)
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()
    
    return predicted_class

def classificate_relevant(answers: list[str]) -> int:
    """Классифицирует по информативности
    answers: list[str] - ответы студента на вопросы
    return: int - метка класса по релевантности
    """
    model_path = "models/relevant"
    return classificate(model_path, answers)


def classificate_positive(answers: list[str]) -> int:
    """Классифицирует по сантименту
    answers: list[str] - ответы студента на вопросы
    return: int - метка класса по сантименту
    """
    modal_path = "models/positive"
    return classificate(modal_path, answers)


def classificate_object(answers: list[str]) -> int:
    """Классифицирует по объекту отзыва
    answers: list[str] - ответы студента на вопросы
    return: int - метка класса по объекту отзыва
    """
    model_path = "models/object"
    return classificate(model_path, answers)


if __name__ == "__main__":
    answers = ["Это худший преподаватель, которого я видел", "Пусть он никогда не говориь", "Ужасный преподаватель", "Он просто не умеет говорить и ничего не знает"]
    print("Relevant: ", classificate_relevant(answers))
    print("Positive: ", classificate_positive(answers))
    print("Object: ", classificate_object(answers))
