from PyQt5.QtWidgets import (
    QWidget,
    QDialog,
    QVBoxLayout,
    QPushButton,
    QTableWidget,
    QLabel,
    QComboBox,
    QLineEdit,
    QMessageBox,
    QAbstractItemView,
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QMovie
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure
import matplotlib.ticker as ticker
import mplcursors
from datetime import datetime
import matplotlib

matplotlib.use("Qt5Agg")


class HistoryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Task Completion History")
        self.setGeometry(100, 100, 800, 600)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()

        # Time span selection
        self.time_span_combo = QComboBox(self)
        self.time_span_combo.addItems(
            ["Last 7 Days", "Last 30 Days", "Last 90 Days", "Custom"]
        )
        layout.addWidget(self.time_span_combo)

        # Custom days input
        self.custom_days_input = QLineEdit(self)
        self.custom_days_input.setPlaceholderText("Enter custom days")
        self.custom_days_input.setVisible(False)
        layout.addWidget(self.custom_days_input)

        self.time_span_combo.currentTextChanged.connect(self.toggle_custom_input)

        # Matplotlib setup
        self._setup_matplotlib(layout)

        # Update button
        update_btn = QPushButton("Update Graph", self)
        update_btn.clicked.connect(self.update_graph)
        layout.addWidget(update_btn)

        self.setLayout(layout)

    def _setup_matplotlib(self, layout):
        self.figure = Figure(figsize=(8, 5), tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

    def toggle_custom_input(self):
        self.custom_days_input.setVisible(
            self.time_span_combo.currentText() == "Custom"
        )

    def update_graph(self):
        try:
            days = self._get_time_span()
            dates, counts = self._get_completion_data(days)
            self._plot_data(dates, counts)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generating graph: {str(e)}")

    def _get_time_span(self):
        if self.time_span_combo.currentText() == "Custom":
            return int(self.custom_days_input.text())
        return {"Last 7 Days": 7, "Last 30 Days": 30, "Last 90 Days": 90}[
            self.time_span_combo.currentText()
        ]

    def _get_completion_data(self, days):
        end_date = QDate.currentDate()
        start_date = end_date.addDays(-days + 1)

        # Generate date range
        current_date = start_date
        date_strings = []
        while current_date <= end_date:
            date_strings.append(current_date.toString("yyyy-MM-dd"))
            current_date = current_date.addDays(1)

        completion_counts = {date: 0 for date in date_strings}

        try:
            with open("history.txt", "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split(" | ")
                    if len(parts) == 6:
                        status = parts[5]
                        if "done" in status:
                            completion_date_str = status.split("Completed on ")[1]
                            completion_date = QDate.fromString(
                                completion_date_str, "yyyy-MM-dd"
                            )
                            if start_date <= completion_date <= end_date:
                                date_str = completion_date.toString("yyyy-MM-dd")
                                completion_counts[date_str] += 1
        except FileNotFoundError:
            QMessageBox.warning(self, "No Data", "No completion history found")
            return [], []

        return date_strings, [completion_counts[d] for d in date_strings]

    def _plot_data(self, dates, counts):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Format x-axis labels
        x_labels = [
            (
                datetime.strptime(d, "%Y-%m-%d").strftime("%a\n%m-%d")
                if len(dates) <= 7
                else datetime.strptime(d, "%Y-%m-%d").strftime("%Y-%m-%d")
            )
            for d in dates
        ]
        x_indices = range(len(dates))

        # Create bars
        bars = ax.bar(
            x_indices,
            counts,
            width=0.8,
            color="#FF69B4",
            edgecolor="black",
            linewidth=1,
        )

        # Configure axis
        ax.set_xticks(x_indices)
        ax.set_xticklabels(x_labels, rotation=45, ha="right")
        ax.set_ylabel("Completed Tasks")
        ax.set_title(f"Task Completion History: {self.time_span_combo.currentText()}")
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax.grid(True, axis="y")

        # Set y-axis limits
        y_max = max(counts) if counts else 1
        ax.set_ylim(0, y_max + 0.5)

        # Add value labels
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    height,
                    f"{height}",
                    ha="center",
                    va="bottom",
                )

        # Add interactive hover
        cursor = mplcursors.cursor(bars, hover=True)
        cursor.connect(
            "add",
            lambda sel: sel.annotation.set_text(
                f"Date: {dates[sel.index]}\nTasks Completed: {counts[sel.index]}"
            ),
        )

        self.canvas.draw()


class HistoryTodo(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()
        self.loadTasks()

    def initUI(self):
        self.setWindowTitle("History Todo")
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

        # Add show graph button
        self.showGraphButton = QPushButton("Show Graph Representation", self)
        self.showGraphButton.clicked.connect(self.showGraph)
        layout.addWidget(self.showGraphButton)

        self.dashboardButton = QPushButton("Back to Dashboard", self)
        self.dashboardButton.clicked.connect(self.showDashboard)
        layout.addWidget(self.dashboardButton)

        self.refreshButton = QPushButton("Refresh", self)
        self.refreshButton.clicked.connect(self.loadTasks)
        layout.addWidget(self.refreshButton)

        self.setLayout(layout)

    def loadTasks(self):
        from read import TodoReader

        TodoReader.load_tasks_to_table(self.taskTable, "history.txt")

    def showGraph(self):
        history_dialog = HistoryDialog(self)
        history_dialog.exec_()

    def showDashboard(self):
        self.close()
        self.main_window.show()
