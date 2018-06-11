#!/usr/bin/env python

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
import requests
import json
import yaml
import readline
import string
import re

HEADERS = {"Content-Type": "application/json"}
ACTUATOR = r"\A(\S+)\s+(\S+)\s+(\{.*\})\s+(\S+)\s+(\{.*\})(\s+.*)?\Z"
NO_ACTUATOR = r"\A(\S+)\s+(\S+)\s+(\{.*\})(\s+.*)?\Z"
TARGET_ONLY = r"\A(\S+)\s+(\S+)\Z"

class Dictionary(QWidget):

    def __init__(self, parent = None):
        super(Dictionary, self).__init__(parent)
        self.createLayout()
        self.createConnection()

    def search(self):
        word = self.lineEdit.text()
        word = str(word)
        cmd = self.parse(word)
        r = requests.post("http://localhost:9001", json=cmd, headers=HEADERS)
        with open(cmd['target']['URI'], 'r') as handle:
        #with open('/home/keiko/1.py') as handle:
            parsed = json.load(handle)
        #print parsed
        self.txt.setText(json.dumps(parsed, indent=4))

    def createLayout(self):
        self.lineEdit = QLineEdit()
        self.goButton = QPushButton("&GO")
        h1 = QHBoxLayout()
        h1.addWidget(self.lineEdit)
        h1.addWidget(self.goButton)
        
        self.txt = QTextEdit()
        self.pic = QLabel()
        self.pic.setPixmap(QPixmap('/home/keiko/logo-ncsist.jpg'))
        #self.pic.setScaledContents(True)
        #self.pic.resize(self.size())

        self.quitButton = QPushButton("&Quit")
        h2 = QHBoxLayout()
        h2.addStretch(1)
        h2.addWidget(self.quitButton)

        layout = QVBoxLayout()
        layout.addLayout(h1)
        layout.addWidget(self.pic)
        layout.addWidget(self.txt)
        layout.addLayout(h2)

        self.setLayout(layout)

    def createConnection(self):
        self.lineEdit.returnPressed.connect(self.search)
        self.lineEdit.returnPressed.connect(self.lineEdit.selectAll)
        self.goButton.clicked.connect(self.search)
        self.goButton.clicked.connect(self.lineEdit.selectAll)
        self.quitButton.clicked.connect(self.close)
    def parse(self, cmd):
        """
        Debug OpenC2 CLI parser
        """
        actuator_match = re.match(ACTUATOR, cmd)
        non_actuator_match = re.match(NO_ACTUATOR, cmd)
        target_only_match = re.match(TARGET_ONLY, cmd)

        action = None
        target_type = None
        target = {}
        actuator_type = None
        actuator = {}
        modifier = {}

        if actuator_match:
            groups = actuator_match.groups("")

            action = string.lower(groups[0])
            target_type = groups[1]
            target = yaml.load(groups[2])

            actuator_type = groups[3]
            actuator = yaml.load(groups[4])
        
            modifier = yaml.load("{{{}}}".format(groups[5]))
        elif non_actuator_match:
            groups = non_actuator_match.groups("")

            action = string.lower(groups[0])
            target_type = groups[1]
            target = yaml.load(groups[2])

            modifier = yaml.load("{{{}}}".format(groups[3]))
        elif target_only_match:
            groups = target_only_match.groups("")

            action = string.lower(groups[0])
            target_type = groups[1]
        else:
            raise SyntaxError("Invalid OpenC2 command")


        target['type'] = target_type

        if actuator_match:
            actuator['type'] = actuator_type

        return {'action': action, 'target': target, 'actuator': actuator,
            'modifier': modifier}



app = QApplication(sys.argv)

dictionary = Dictionary()
dictionary.show()

app.exec_()
