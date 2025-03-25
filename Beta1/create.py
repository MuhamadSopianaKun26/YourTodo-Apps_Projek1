from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QCalendarWidget,
    QRadioButton,
    QHBoxLayout,
    QLabel,
    QTimeEdit,
    QMessageBox,
    QDialogButtonBox,
)
from PyQt5.QtCore import QTime, QDate, Qt
from PyQt5.QtGui import QFont, QPixmap


class BaseDialog(QDialog):
    """Base dialog class with common initialization"""

    def __init__(self, parent=None, title=""):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)


class ImageDialog(BaseDialog):
    """Dialog displaying an image with a message"""

    def __init__(self, parent=None):
        super().__init__(parent, "Bayar Dulu Bos!!")
        self._setup_ui()

    def _setup_ui(self):
        # Text label
        self.textLabel = QLabel("Bayar dulu bos!!", self)
        self.textLabel.setFont(QFont("Arial", 16, QFont.Bold))
        self.textLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.textLabel)

        # Image label
        self.imageLabel = QLabel(self)
        pixmap = QPixmap("img.png")
        if pixmap.isNull():
            self.imageLabel.setText("Gambar tidak ditemukan!")
        else:
            self.imageLabel.setPixmap(pixmap)
        self.layout.addWidget(self.imageLabel)

        # OK button
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok, self)
        self.buttonBox.accepted.connect(self.accept)
        self.layout.addWidget(self.buttonBox)


class TaskDialog(BaseDialog):
    """Dialog for creating or editing a task"""

    def __init__(self, parent=None, task_data=None):
        super().__init__(parent, "Task Details")
        self.task_data = task_data or {}
        self._setup_ui()

    def _setup_ui(self):
        """Set up the task dialog UI components"""
        self._add_task_name()
        self._add_task_description()
        self._add_start_time()
        self._add_deadline()
        self._add_priority()
        self._add_save_button()

    def _add_task_name(self):
        """Add task name input field"""
        self.taskName = QLineEdit(self)
        self.taskName.setPlaceholderText("Task Name")
        if "name" in self.task_data:
            self.taskName.setText(self.task_data["name"])
        self.layout.addWidget(QLabel("Task Name:"))
        self.layout.addWidget(self.taskName)

    def _add_task_description(self):
        """Add task description input field"""
        self.taskDescription = QTextEdit(self)
        self.taskDescription.setPlaceholderText("Task Description")
        if "description" in self.task_data:
            self.taskDescription.setText(self.task_data["description"])
        self.layout.addWidget(QLabel("Task Description:"))
        self.layout.addWidget(self.taskDescription)

    def _add_start_time(self):
        """Add start date and time input fields"""
        self.layout.addWidget(QLabel("Starting Date:"))
        self.startCalendar = QCalendarWidget(self)
        if "start_time" in self.task_data:
            date_part = self.task_data["start_time"].split(" ")[0]
            self.startCalendar.setSelectedDate(
                QDate.fromString(date_part, "yyyy-MM-dd")
            )
        self.layout.addWidget(self.startCalendar)

        self.layout.addWidget(QLabel("Starting Time:"))
        self.startTime = QTimeEdit(self)
        if "start_time" in self.task_data:
            time_part = self.task_data["start_time"].split(" ")[1]
            self.startTime.setTime(QTime.fromString(time_part, "HH:mm"))
        self.layout.addWidget(self.startTime)

    def _add_deadline(self):
        """Add deadline date and time input fields"""
        self.layout.addWidget(QLabel("Deadline Date:"))
        self.calendar = QCalendarWidget(self)
        if "deadline" in self.task_data:
            date_part = self.task_data["deadline"].split(" ")[0]
            self.calendar.setSelectedDate(QDate.fromString(date_part, "yyyy-MM-dd"))
        self.layout.addWidget(self.calendar)

        self.layout.addWidget(QLabel("Deadline Time:"))
        self.deadlineTime = QTimeEdit(self)
        if "deadline" in self.task_data:
            time_part = self.task_data["deadline"].split(" ")[1]
            self.deadlineTime.setTime(QTime.fromString(time_part, "HH:mm"))
        self.layout.addWidget(self.deadlineTime)

    def _add_priority(self):
        """Add priority selection radio buttons"""
        priorityLayout = QHBoxLayout()
        self.priorityLow = QRadioButton("Low")
        self.priorityMedium = QRadioButton("Medium")
        self.priorityHigh = QRadioButton("High")
        priorityLayout.addWidget(self.priorityLow)
        priorityLayout.addWidget(self.priorityMedium)
        priorityLayout.addWidget(self.priorityHigh)
        self.layout.addWidget(QLabel("Task Priority:"))
        self.layout.addLayout(priorityLayout)

        if "priority" in self.task_data:
            priority_map = {
                "Low": self.priorityLow,
                "Medium": self.priorityMedium,
                "High": self.priorityHigh,
            }
            if self.task_data["priority"] in priority_map:
                priority_map[self.task_data["priority"]].setChecked(True)

    def _add_save_button(self):
        """Add save button with validation"""
        self.saveButton = QPushButton("Save", self)
        self.saveButton.clicked.connect(self.validateAndAccept)
        self.layout.addWidget(self.saveButton)

    def validateAndAccept(self):
        """Validate form inputs before accepting"""
        start_date = self.startCalendar.selectedDate()
        start_time = self.startTime.time()
        deadline_date = self.calendar.selectedDate()
        deadline_time = self.deadlineTime.time()

        if not self._validate_fields(start_date, deadline_date):
            return
        if not self._validate_dates(
            start_date, start_time, deadline_date, deadline_time
        ):
            return

        self.accept()

    def _validate_fields(self, start_date, deadline_date):
        """Validate that all required fields are filled"""
        if not (
            self.taskName.text().strip()
            and self.taskDescription.toPlainText().strip()
            and start_date.isValid()
            and deadline_date.isValid()
            and (
                self.priorityLow.isChecked()
                or self.priorityMedium.isChecked()
                or self.priorityHigh.isChecked()
            )
        ):
            QMessageBox.warning(self, "Validation Error", "All fields must be filled!")
            return False
        return True

    def _validate_dates(self, start_date, start_time, deadline_date, deadline_time):
        """Validate that dates are logically correct"""
        if start_date == deadline_date and start_time == deadline_time:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Starting time and deadline time cannot be the same!",
            )
            return False
        if start_date > deadline_date or (
            start_date == deadline_date and start_time >= deadline_time
        ):
            QMessageBox.warning(
                self, "Validation Error", "Deadline must be later than starting time!"
            )
            return False
        return True

    def getTaskData(self):
        """Get the task data from the form"""
        priority = (
            "Low"
            if self.priorityLow.isChecked()
            else "Medium" if self.priorityMedium.isChecked() else "High"
        )
        return {
            "name": self.taskName.text(),
            "description": self.taskDescription.toPlainText(),
            "start_time": f"{self.startCalendar.selectedDate().toString('yyyy-MM-dd')} {self.startTime.time().toString('HH:mm')}",
            "deadline": f"{self.calendar.selectedDate().toString('yyyy-MM-dd')} {self.deadlineTime.time().toString('HH:mm')}",
            "priority": priority,
            "status": "due",
        }


class TodoCreator:
    """Static class for handling task creation"""

    @staticmethod
    def add_task(parent_widget, save_callback):
        """Show image dialog and then task dialog for creating a new task"""
        # Show image dialog first
        imageDialog = ImageDialog(parent_widget)
        if imageDialog.exec_():
            # Continue to task input dialog
            dialog = TaskDialog(parent_widget)
            if dialog.exec_():
                task_data = dialog.getTaskData()
                save_callback(task_data)
