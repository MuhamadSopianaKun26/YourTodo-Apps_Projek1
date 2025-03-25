from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTableWidget,
    QLabel,
    QAbstractItemView,
    QMessageBox,
)
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt
import sys

from create import TodoCreator
from read import TodoReader
from update import TodoUpdater
from delete import TodoDeleter
from history import HistoryTodo


class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.loadTasks()

    def initUI(self):
        self.setWindowTitle("To-Do List")
        self.setGeometry(100, 100, 1500, 950)

        layout = QVBoxLayout()

        # Add loading animation label
        self.loadingLabel = QLabel(self)
        self.loadingMovie = QMovie("loading.gif")
        self.loadingLabel.setMovie(self.loadingMovie)
        self.loadingLabel.setAlignment(Qt.AlignCenter)
        self.loadingLabel.setFixedSize(
            200, 200
        )  # Set fixed size for the loading animation
        self.loadingLabel.hide()
        layout.addWidget(self.loadingLabel, alignment=Qt.AlignCenter)

        self.taskTable = QTableWidget(self)
        self.taskTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.taskTable.setColumnCount(6)
        self.taskTable.setHorizontalHeaderLabels(
            ["Name", "Description", "Start Time", "Deadline", "Priority", "Status"]
        )
        # Set column width for status column
        self.taskTable.setColumnWidth(5, 300)
        layout.addWidget(self.taskTable)

        self._add_buttons(layout)
        self.setLayout(layout)

    def _add_buttons(self, layout):
        buttons = [
            ("Add Task", self.addTask),
            ("Update Task", self.updateTask),
            ("Delete Task", self.deleteTask),
            ("Clear All Tasks", self.clearTasks),
            ("Mark Task as Done", self.markTaskAsDone),
            ("Mark Task as Failed", lambda: self.markTaskAsFailed()),
            ("Move Task to History", self.moveTaskToHistory),
            ("Show History", self.showHistory),
            ("Refresh", self.loadTasks),
        ]

        for text, callback in buttons:
            button = QPushButton(text, self)
            button.clicked.connect(callback)
            layout.addWidget(button)

    def loadTasks(self):
        TodoReader.load_tasks_to_table(self.taskTable, "tasks.txt")
        TodoReader.check_past_deadline_tasks(self.taskTable, self.markTaskAsFailed)

    def addTask(self):
        TodoCreator.add_task(self.taskTable, self.saveTasks)

    def updateTask(self):
        TodoUpdater.update_task(self.taskTable, self.saveTasks)

    def deleteTask(self):
        TodoDeleter.delete_task(self.taskTable, self.saveTasks)

    def clearTasks(self):
        TodoDeleter.clear_all_tasks(self.taskTable, self.saveTasks)

    def markTaskAsDone(self):
        TodoUpdater.mark_task_as_done(self.taskTable, self.saveTasks)

    def markTaskAsFailed(self, row=None):
        TodoUpdater.mark_task_as_failed(self.taskTable, row, self.saveTasks)

    def moveTaskToHistory(self):
        TodoUpdater.move_task_to_history(self.taskTable, self.saveTasks)

    def saveTasks(self):
        try:
            with open("tasks.txt", "w", encoding="utf-8") as file:
                for row in range(self.taskTable.rowCount()):
                    data = []
                    for col in range(6):
                        item = self.taskTable.item(row, col)
                        data.append(item.text() if item else "")
                    if data:
                        file.write(" | ".join(data) + "\n")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving tasks: {e}")

    def showHistory(self):
        self.history_window = HistoryTodo(self)
        self.history_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec_())
