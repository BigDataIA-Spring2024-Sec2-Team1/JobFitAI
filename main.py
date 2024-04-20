from pydparser import ResumeParser
from pydparser import utils
from constants import RESUME_SECTIONS_GRAD
import re

def extract_entity_sections_grad(text):
    '''
    Helper function to extract all the raw text from sections of
    resume specifically for graduates and undergraduates

    :param text: Raw text of resume
    :return: dictionary of entities
    '''
    text_split = [i.strip() for i in text.split('\n')]
    # sections_in_resume = [i for i in text_split if i.lower() in sections]
    entities = {}
    key = False
    for phrase in text_split:
        if len(phrase) == 1:
            p_key = phrase
        else:
            p_key = set(phrase.lower().split()) & set(RESUME_SECTIONS_GRAD)
        try:
            p_key = list(p_key)[0]
        except IndexError:
            pass
        if p_key in RESUME_SECTIONS_GRAD:
            if p_key not in entities:
                entities[p_key] = []
            key = p_key
        elif key and phrase.strip():
            entities[key].append(phrase)
    return entities


def cleanExperienceSection(text, date=False, output_format="array"):
    pattern = r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sept(?:ember)?|Sep(?:tember)|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d+\b(?:\s*(?:–|-|–|–)\s*\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Sept(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d+)?'
    if date:
        text_with_dates = []
        for i in text:
            _text = i.replace('•', '').strip()
            if(_text.strip() == ""):
                continue
            _text = utils.remove_non_readable_chars(_text)
            text_with_dates.append(_text)
        if output_format == "array":
            return text_with_dates
        elif output_format == "str":
            return " ".join(text_with_dates)
        else:
            return text_with_dates
    else:
        text_without_dates = []
        for i in text:
            _text = re.sub(pattern, '', i).replace('•', '')
            if(_text.strip() == ""):
                continue
            _text = utils.remove_non_readable_chars(_text)
            text_without_dates.append(_text.strip())
        if output_format == "array":
            return text_without_dates
        elif output_format == "str":
            return " ".join(text_without_dates)
        else:
            return text_without_dates

# file_path = 'data/resumes/pdf/Anupama_resume.pdf'
file_path = 'data/resumes/docx/Vivek.BSA.docx'
# data = ResumeParser(file_path).get_extracted_data()
# print(data)

# if not len(data.get("experience")):
text = utils.extract_text(file_path, f".{file_path.split('/')[-1].split('.')[-1]}")
print(text)
#     cc= extract_entity_sections_grad(text)
#     print("Text without year", cleanExperienceSection(cc.get("experience"), False, "str"))
