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
    QTableWidgetItem,
)
from PyQt5.QtCore import QTime, QDate, Qt
from PyQt5.QtGui import QFont, QPixmap


class BaseDialog(QDialog):
    def __init__(self, parent=None, title=""):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)


class ImageDialog(BaseDialog):
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
    def __init__(self, parent=None, task_data=None):
        super().__init__(parent, "Task Details")
        self.task_data = task_data or {}
        self._setup_ui()

    def _setup_ui(self):
        # Task name
        self._add_task_name()

        # Task description
        self._add_task_description()

        # Start time
        self._add_start_time()

        # Deadline
        self._add_deadline()

        # Priority
        self._add_priority()

        # Save button
        self.saveButton = QPushButton("Save", self)
        self.saveButton.clicked.connect(self.validateAndAccept)
        self.layout.addWidget(self.saveButton)

    def _add_task_name(self):
        self.taskName = QLineEdit(self)
        self.taskName.setPlaceholderText("Task Name")
        if "name" in self.task_data:
            self.taskName.setText(self.task_data["name"])
        self.layout.addWidget(QLabel("Task Name:"))
        self.layout.addWidget(self.taskName)

    def _add_task_description(self):
        self.taskDescription = QTextEdit(self)
        self.taskDescription.setPlaceholderText("Task Description")
        if "description" in self.task_data:
            self.taskDescription.setText(self.task_data["description"])
        self.layout.addWidget(QLabel("Task Description:"))
        self.layout.addWidget(self.taskDescription)

    def _add_start_time(self):
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
            if self.task_data["priority"] == "Low":
                self.priorityLow.setChecked(True)
            elif self.task_data["priority"] == "Medium":
                self.priorityMedium.setChecked(True)
            elif self.task_data["priority"] == "High":
                self.priorityHigh.setChecked(True)

    def validateAndAccept(self):
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
        if (
            not self.taskName.text().strip()
            or not self.taskDescription.toPlainText().strip()
            or not start_date.isValid()
            or not deadline_date.isValid()
            or not (
                self.priorityLow.isChecked()
                or self.priorityMedium.isChecked()
                or self.priorityHigh.isChecked()
            )
        ):
            QMessageBox.warning(self, "Validation Error", "All fields must be filled!")
            return False
        return True

    def _validate_dates(self, start_date, start_time, deadline_date, deadline_time):
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
    @staticmethod
    def add_task(table_widget, save_callback):
        # Show image dialog first
        imageDialog = ImageDialog(table_widget.parent())
        if imageDialog.exec_():  # If user clicks OK
            # Continue to task input dialog
            dialog = TaskDialog(table_widget.parent())
            if dialog.exec_():
                task_data = dialog.getTaskData()
                row = table_widget.rowCount()
                table_widget.insertRow(row)
                for col, key in enumerate(
                    [
                        "name",
                        "description",
                        "start_time",
                        "deadline",
                        "priority",
                        "status",
                    ]
                ):
                    item = QTableWidgetItem(task_data[key])
                    table_widget.setItem(row, col, item)
                save_callback()
