from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QScrollArea,
    QMessageBox,
    QStackedWidget,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys

from create import TodoCreator
from ui_components import HeaderWidget, SidebarWidget, TaskItemWidget


class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.loadTasks()

    def initUI(self):
        """Initialize the main user interface"""
        self.setWindowTitle("YourTodo")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #F0FBFF;")

        # Set up main layout structure
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Add header and content area
        self.header = HeaderWidget()
        main_layout.addWidget(self.header)
        main_layout.addLayout(self._setupContentArea())

        self.setLayout(main_layout)

    def _setupContentArea(self):
        """Set up the main content area with sidebar and stacked widget"""
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Add sidebar
        self.sidebar = SidebarWidget()
        content_layout.addWidget(self.sidebar)

        # Set up stacked widget for different sections
        self.stacked_widget = QStackedWidget()
        self._setupStackedWidgets()
        content_layout.addWidget(self.stacked_widget, stretch=1)

        # Connect sidebar buttons
        self._connectSidebarButtons()

        return content_layout

    def _setupStackedWidgets(self):
        """Set up all section widgets in the stacked widget"""
        # Create widgets for each section
        self.today_widget = QWidget()
        self.weekly_widget = QWidget()
        self.monthly_widget = QWidget()
        self.history_widget = QWidget()

        # Set up each widget's content
        self.setupTodayWidget()
        self.setupSimpleWidget(self.weekly_widget, "Weekly Task")
        self.setupSimpleWidget(self.monthly_widget, "Monthly Task")
        self.setupSimpleWidget(self.history_widget, "History")

        # Add all widgets to the stacked widget
        for widget in [
            self.today_widget,
            self.weekly_widget,
            self.monthly_widget,
            self.history_widget,
        ]:
            self.stacked_widget.addWidget(widget)

    def _connectSidebarButtons(self):
        """Connect sidebar buttons to their respective sections"""
        button_sections = {
            self.sidebar.today_btn: "today",
            self.sidebar.weekly_btn: "weekly",
            self.sidebar.monthly_btn: "monthly",
            self.sidebar.history_btn: "history",
        }

        for button, section in button_sections.items():
            button.clicked.connect(lambda checked, s=section: self.showSection(s))

        # Set up button group for exclusive selection
        self.sidebar_buttons = list(button_sections.keys())
        for button in self.sidebar_buttons:
            button.clicked.connect(
                lambda checked, btn=button: self.updateSidebarButtons(btn)
            )

    def setupTodayWidget(self):
        """Set up the Today section with task list and controls"""
        layout = QVBoxLayout(self.today_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # Add header with task count
        layout.addLayout(self._setupTodayHeader())

        # Add scrollable task list
        layout.addWidget(self._setupTaskList())

    def _setupTodayHeader(self):
        """Create the header for Today section with count and add button"""
        header = QHBoxLayout()

        # Add "Today" label
        today_label = QLabel("Today")
        today_label.setFont(QFont("Arial", 24, QFont.Bold))
        header.addWidget(today_label)

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

        # Add task button
        add_btn = QPushButton("Add")
        add_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #00B4D8;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 8px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0096B7;
            }
        """
        )
        add_btn.clicked.connect(self.addTask)
        header.addWidget(add_btn)

        return header

    def _setupTaskList(self):
        """Create scrollable task list area"""
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

    def setupSimpleWidget(self, widget, text):
        """Set up a simple widget with centered text"""
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        header_label = QLabel(text)
        header_label.setFont(QFont("Arial", 24, QFont.Bold))
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("color: #333;")

        layout.addWidget(header_label)
        layout.addStretch()

    def loadTasks(self):
        """Load tasks from file and update UI"""
        # Clear existing tasks
        for i in reversed(range(self.task_list_layout.count())):
            self.task_list_layout.itemAt(i).widget().setParent(None)

        try:
            with open("tasks.txt", "r", encoding="utf-8") as file:
                for line in file:
                    data = line.strip().split(" | ")
                    if len(data) == 6:
                        task_data = {
                            "name": data[0],
                            "description": data[1],
                            "start_time": data[2],
                            "deadline": data[3],
                            "priority": data[4],
                            "status": data[5],
                        }
                        task_widget = TaskItemWidget(task_data)
                        self.task_list_layout.addWidget(task_widget)
        except FileNotFoundError:
            open("tasks.txt", "w").close()

        self.updateTaskCount()

    def addTask(self):
        """Open dialog to add a new task"""
        TodoCreator.add_task(self, self.saveNewTask)

    def saveNewTask(self, task_data):
        """Save new task to file and update UI"""
        try:
            # Save to file
            with open("tasks.txt", "a", encoding="utf-8") as file:
                data = [
                    task_data["name"],
                    task_data["description"],
                    task_data["start_time"],
                    task_data["deadline"],
                    task_data["priority"],
                    task_data["status"],
                ]
                file.write(" | ".join(data) + "\n")

            # Update UI
            task_widget = TaskItemWidget(task_data)
            self.task_list_layout.addWidget(task_widget)
            self.updateTaskCount()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving task: {e}")

    def showSection(self, section):
        """Switch to the specified section in the stacked widget"""
        section_widgets = {
            "today": self.today_widget,
            "weekly": self.weekly_widget,
            "monthly": self.monthly_widget,
            "history": self.history_widget,
        }
        if section in section_widgets:
            self.stacked_widget.setCurrentWidget(section_widgets[section])

    def updateSidebarButtons(self, clicked_button):
        """Update sidebar button states"""
        for button in self.sidebar_buttons:
            button.setChecked(button == clicked_button)

    def saveTasks(self):
        """Save all tasks to file"""
        try:
            with open("tasks.txt", "w", encoding="utf-8") as file:
                for i in range(self.task_list_layout.count()):
                    widget = self.task_list_layout.itemAt(i).widget()
                    if isinstance(widget, TaskItemWidget):
                        task_data = widget.task_data
                        data = [
                            task_data["name"],
                            task_data["description"],
                            task_data["start_time"],
                            task_data["deadline"],
                            task_data["priority"],
                            task_data["status"],
                        ]
                        file.write(" | ".join(data) + "\n")
            self.loadTasks()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving tasks: {e}")

    def updateTaskCount(self):
        """Update the task count display"""
        self.task_count_label.setText(str(self.task_list_layout.count()))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec_())
