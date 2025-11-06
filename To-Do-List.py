"""
--------------------------------------------
Project: PyQt5 To-Do List Application
Author: [Your Name]
Description:
    A simple yet elegant To-Do List app built with PyQt5.
    Features include:
      • Dark theme UI
      • Daily calendar for date-based tasks
      • Live task counters (total, completed, remaining)
      • Task completion with checkboxes
      • Persistent in-memory storage (per session)

Usage:
    Run the script using:
        python main.py

Version: 1.0
License: MIT
--------------------------------------------
"""

from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QWidget, QHBoxLayout, QCheckBox, QCalendarWidget
)
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("ToDoList-project.ui", self)

        self.add_button = self.findChild(QPushButton, "add_Button")
        self.delete_button = self.findChild(QPushButton, "delete_Button")

        self.total_label = self.findChild(QLabel, "total_label")
        self.remaining_label = self.findChild(QLabel, "remaining_label")
        self.completed_label = self.findChild(QLabel, "completed_label")

        self.calendar = self.findChild(QCalendarWidget, "calendarWidget")
        self.task_line_edit = self.findChild(QLineEdit, "lineEdit")
        self.task_list = self.findChild(QListWidget, "listWidget")

        self.task_list.setStyleSheet("""
            QListWidget {
                background-color: #1e1e1e;
                border: 2px solid #444;
                border-radius: 10px;
                padding: 8px;
                font-size: 16px;
                color: white;
            }
        """)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
            }
            QLabel {
                color: white;
                font-family: "Segoe UI";
            }
            QLineEdit {
                background-color: #2c2c2c;
                border: 2px solid #555;
                border-radius: 8px;
                color: white;
                padding: 5px;
                font-size: 16px;
            }
            QPushButton {
                background-color: #0078d7;
                color: white;
                border-radius: 8px;
                font-size: 15px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #2894ff;
            }
            QCalendarWidget {
                background-color: #2e2e2e;
                border: 2px solid #555;
                border-radius: 10px;
                color: white;
            }
            QScrollBar:vertical {
                background: #2c2c2c;
                width: 10px;
            }
            QScrollBar::handle:vertical {
                background: #555;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #888;
            }
        """)

        self.time = dict()

        self.add_button.clicked.connect(self.add_task)
        self.delete_button.clicked.connect(self.delete_task)
        self.calendar.selectionChanged.connect(self.task_list_update)

        self.show()

    def add_task(self):
        current_date = str(self.calendar.selectedDate())
        text = self.task_line_edit.text().strip()
        if not text:
            return

        if current_date not in self.time:
            self.time[current_date] = []

        self.time[current_date].append({'text': text, 'done': False})
        self.task_line_edit.clear()
        self.task_list_update()

    def delete_task(self):
        current_date = str(self.calendar.selectedDate())
        self.time[current_date] = []
        self.task_list_update()

    def task_list_update(self):
        self.task_list.clear()
        current_date = str(self.calendar.selectedDate())
        tasks = self.time.get(current_date, [])

        total = len(tasks)
        completed = len([t for t in tasks if t['done']])
        remaining = total - completed

        self.total_label.setText(f"Total Tasks : {total}")
        self.completed_label.setText(f"Completed Tasks : {completed}")
        self.remaining_label.setText(f"Remaining Tasks : {remaining}")

        for i, task in enumerate(tasks):
            item_widget = QWidget()
            layout = QHBoxLayout()
            layout.setContentsMargins(8, 2, 8, 2)

            checkbox = QCheckBox()
            checkbox.setChecked(task['done'])
            label = QLabel(task['text'])
            label.setFont(QFont("Segoe UI", 12))

            if task['done']:
                label.setStyleSheet("color: #888; text-decoration: line-through;")
            else:
                label.setStyleSheet("color: white;")

            checkbox.stateChanged.connect(lambda state, d=current_date, idx=i, lbl=label: self.toggle_done(d, idx, lbl, state))

            layout.addWidget(checkbox)
            layout.addWidget(label)
            layout.addStretch()

            item_widget.setLayout(layout)
            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())

            self.task_list.addItem(item)
            self.task_list.setItemWidget(item, item_widget)

    def toggle_done(self, date, index, label, state):
        if state == Qt.Checked:
            done = True
        else:
            done = False
        self.time[date][index]['done'] = done
        label.setStyleSheet("color: #888; text-decoration: line-through;" if done else "color: white;")
        self.task_list_update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()
