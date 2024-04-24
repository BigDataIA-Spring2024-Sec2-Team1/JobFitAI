import requests
import json
import en_core_web_sm
from spacy.matcher import PhraseMatcher
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor
from util import getAccessToken

nlp = en_core_web_sm.load()
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

def extractKeywordFromSkillNer(text):
    try:
        annotations = skill_extractor.annotate(text)
        return {
            "status": 200,
            "annotations": annotations
        }
    except Exception as e:
        print("Error in parsing text at skillNerParser.parseText", e)
        status = 501
        return {
            "status": status,
            "error": e
        }


def extractKeywordFromLightSkillAPI(text, token):
    try:
        headers = {'Authorization': f'Bearer {token["access_token"]}', 'Content-Type': "application/json"}
        url = "https://emsiservices.com/skills/versions/latest/extract"

        payload = {
            "text": text,
            "confidenceThreshold": 0.5
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        
        res = json.loads(response.text)

        if "message" in res and res["message"] == "Token expired": raise Exception("TOKEN_EXPIRED")

        skills = [] 
        for i in res['data']:
            skills.append(i["skill"]["name"])
        return skills
    except Exception as e:
        print("error -> ", e.args)
        print("error more details -> ", e)
        if e.args[0] == "TOKEN_EXPIRED":
            token = json.loads(getAccessToken())
