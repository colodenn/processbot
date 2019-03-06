import sys
from app.utils.intentFunctions import process_names, process_run

# Mapt alle Intents einer entsprechenden Intent-Funktion
intentDict = {
    "process_names": process_names,
    "process_run": process_run
}

# Führt die jeweiligen Intent-Funktion zum Intent aus
# Input: response (dialogflow)
# Ouput: TODO
def run(dialogflowResponse):
    intentDisplayName = dialogflowResponse.query_result.intent.display_name
    # print(name)
    if intentDisplayName in intentDict:
        # print("intent exist")
        return intentDict.get(intentDisplayName).run(dialogflowResponse)
    else:
        # print("intent not exist")
        return ""   #TODO: eigenen Typ definieren! 

