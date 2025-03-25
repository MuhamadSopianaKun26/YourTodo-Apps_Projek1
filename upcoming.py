from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from ui_components import HeaderWidget, SidebarWidget, TaskItemWidget

class UpcomingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        #adding header and task count
        main_layout.addLayout(self._setupUpcomingHeader())

        #adding task list
        main_layout.addWidget(self._setupTaskList())


    def _setupUpcomingHeader(self):
        header = QHBoxLayout()

        upcoming_label = QLabel("Upcoming")
        upcoming_label.setFont(QFont("Arial", 24, QFont.Bold))
        header.addWidget(upcoming_label)

        # Add task count label
        self.task_count_label = QLabel("0")
        self.task_count_label.setStyleSheet(
            """
            background-color: #E3F8FF;
            color: #00B4D8;
            padding: 5px 15px;
            border-radius: 15px;
            font-size: 18px;
            font-weight: bold;
        """
        )
        header.addWidget(self.task_count_label)
        header.addStretch()

        return header
    
    def _setupTaskList(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            "QScrollArea { border: none; background-color: transparent; }"
        )

        self.task_list_widget = QWidget()
        self.task_list_layout = QVBoxLayout(self.task_list_widget)
        self.task_list_layout.setAlignment(Qt.AlignTop)
        scroll.setWidget(self.task_list_widget)

        return scroll
        

        
       