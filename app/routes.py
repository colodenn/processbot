import os

from flask import render_template, request, jsonify, send_file
from app import app
from app.models import Process, Node

import app.utils.dialogflowHelper as dialogflowHelper
import app.utils.intentFunctions.triggerIntentFunction as triggerIntentFunction
import app.utils.intentFunctions.triggerButtonFunction as triggerButtonFunction

from app.utils import threadingBpmn
from app.utils import bpmnReader

import json

PROCESS_NAME_ENTITY_TYPE_ID = os.environ.get("PROCESS_NAME_ENTITY_TYPE_ID")
TASK_NAME_ENTITY_TYPE_ID = os.environ.get("TASK_NAME_ENTITY_TYPE_ID")

# bpmnResourcesFolder = con.basedir + "/app/static/resources"
# def checkBpmnFiles(bpmnResourcesFolder):
#     # alle aktuellen Prozessnamen aus der Datenbank laden
#     processesList = []
#     for process in Process.query.all():
#         processesList.append((process.processName, process.importDate))
    
#     for process in processesList:
#         if (process[1] == None):
#             print(process[0] + " importDate: none")
#         else:
#             print(process[0] + " importDate: " + process[1])

#     for filename in os.listdir(bpmnResourcesFolder):
#         if filename.endswith(".bpmn"):
#             print((os.path.join(bpmnResourcesFolder, filename)))
#         else:
#             continue

    # for root, dirnames, filenames in os.walk(path):
    #     for filename in filenames:
    #         process, fileType = filename.split(".")
    #         if (fileType == "bpmn"):
    #             path = os.path.join(root, filename)
    #             print((os.stat(path)[-2]))

# Standard Route zum Anzeigen der Index.html

@app.route("/")
def index():
    # threadingBpmn.ThreadingBpmn()
    return render_template("index.html")

#TODO:  sich klassen angucken; => mit getMethoden aus threadingBPMN eine Prozessliste bekommen mit den Prozessen die sich geändert haben 
@app.route("/get_status_bpmnDir")
def get_status_bpmnDir():
    return jsonify(threadingBpmn.processGlobal)
    # return jsonify([])


#TODO: datenbank mit geänderten Prozessen refreshen => aus frontend Prozess bekommen der aktualisiert werden soll
# @app.route("/update_database", methods=["POST"])
# def update_database():
#     return

@app.route("/get_image/<process>.html")
def get_image(process):
    # TODO: Welcome Messages anzeigen!
    return send_file('./static/resources/svg/'+process+'.svg', mimetype='image/svg+xml')

# Route um Dialogflow zu initialisieren
@app.route("/init")
def initDialogflow():

    for process in Process.query.all():
        processName = process.processName
        # print(processName)
        dialogflowHelper.create_entity(PROCESS_NAME_ENTITY_TYPE_ID, processName, [])

    for task in Node.query.filter_by(type="task"):
        taskName = task.name
        print(taskName)
        dialogflowHelper.create_entity(TASK_NAME_ENTITY_TYPE_ID, taskName, [])

    return render_template("index.html")

# Route um eine Nachricht des Nutzers an Dialogflow zu schicken und dann die Bearbeitung für den Intent zu starten
@app.route('/send_userText', methods=["POST"])
def send_userText():
    userText = request.form["userText"]
    dialogflowResponse = dialogflowHelper.detect_intent_texts(userText)
    responseObject = triggerIntentFunction.run(dialogflowResponse)

    return responseObject

# Route um einen gedrückten Button zu verarbeiten
@app.route('/send_button', methods=["POST"])
def send_button():
    pressedButtonValue = request.form["pressedButtonValue"]
    currentProcess = request.form["currentProcess"]
    previousProcessStep = request.form["previousProcessStep"]
    currentProcessStep = request.form["currentProcessStep"]
    
    responseObject = triggerButtonFunction.run(pressedButtonValue, currentProcess, currentProcessStep, previousProcessStep)

    return responseObject

@app.route("/test")
def test():
    bpmnReader.readBpmn()
    return jsonify("Success")