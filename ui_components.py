from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QFrame,
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QPixmap


class HeaderWidget(QWidget):
    """Header widget containing logo, search bar, and notification icon"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 10, 0)
        layout.setSpacing(0)

        layout.addWidget(self._createLogoContainer())
        layout.addWidget(self._createMainContainer())

        self.setLayout(layout)
        self.setStyleSheet("QWidget { background-color: white; }")

    def _createLogoContainer(self):
        """Create container for the logo"""
        container = QWidget()
        container.setFixedWidth(200)
        container.setFixedHeight(100)
        container.setStyleSheet("background-color: white;")

        layout = QHBoxLayout(container)
        layout.setContentsMargins(10, 10, 10, 10)

        logo_label = QLabel()
        logo_pixmap = QPixmap("logo.png")
        if not logo_pixmap.isNull():
            scaled_pixmap = logo_pixmap.scaled(
                200, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setFixedSize(scaled_pixmap.size())
        else:
            logo_label.setText("YourTodo")
            logo_label.setFont(QFont("Arial", 24, QFont.Bold))
            logo_label.setStyleSheet("color: #00B4D8;")

        layout.addWidget(logo_label, 0, Qt.AlignCenter)
        return container

    def _createMainContainer(self):
        """Create container for search bar and notification icon"""
        container = QWidget()
        container.setStyleSheet("background-color: white;")
        layout = QHBoxLayout(container)
        layout.setContentsMargins(10, 0, 0, 0)

        search_bar = self._createSearchBar()
        notif_btn = self._createNotificationButton()

        layout.addWidget(search_bar)
        layout.addStretch()
        layout.addWidget(notif_btn)

        return container

    def _createSearchBar(self):
        """Create search bar widget"""
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search tasks...")
        search_bar.setStyleSheet(
            """
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 15px;
                padding: 5px 15px;
                background: white;
                min-width: 300px;
                height: 30px;
            }
        """
        )
        return search_bar

    def _createNotificationButton(self):
        """Create notification button widget"""
        notif_btn = QPushButton()
        notif_btn.setIcon(QIcon("icons/notification.png"))
        notif_btn.setIconSize(QSize(24, 24))
        notif_btn.setStyleSheet(
            """
            QPushButton {
                border: none;
                background: transparent;
                padding-right: 20px;
            }
        """
        )
        return notif_btn


class SidebarButton(QPushButton):
    """Custom button for sidebar navigation"""

    def __init__(self, text, icon_path=None, parent=None):
        super().__init__(text, parent)
        self.initUI(icon_path)

    def initUI(self, icon_path):
        if icon_path:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(24, 24))

        self.setStyleSheet(
            """
            QPushButton {
                text-align: left;
                padding: 12px 20px;
                border: none;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
                margin: 4px 12px;
                color: #333;
                font-size: 15px;
                font-weight: 500;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: rgba(0, 180, 216, 0.08);
                color: #00B4D8;
            }
            QPushButton:checked {
                background-color: rgba(0, 180, 216, 0.15);
                color: #00B4D8;
                font-weight: 600;
                border-left : 5px solid rgb(30 , 90, 150);
            }
            QPushButton:checked:hover {
                background-color: rgba(0, 180, 216, 0.2);
            }
        """
        )
        self.setCheckable(True)
        self.setMinimumHeight(48)


class SidebarWidget(QWidget):
    """Sidebar widget containing navigation buttons"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 15, 0, 15)
        layout.setSpacing(8)

        # Create navigation buttons
        self.today_btn = SidebarButton("Today Task", "icons/today.png")
        self.upcoming_btn = SidebarButton("Upcoming", "icons/weekly.png")
        self.scheduled_btn = SidebarButton("Scheduled", "icons/monthly.png")
        self.history_btn = SidebarButton("History", "icons/history.png")

        # Set default selected button
        self.today_btn.setChecked(True)

        # Add buttons to layout
        for btn in [
            self.today_btn,
            self.upcoming_btn,
            self.scheduled_btn,
            self.history_btn,
        ]:
            layout.addWidget(btn)
        layout.addStretch()

        self.setLayout(layout)
        self.setStyleSheet("QWidget { background-color: #E3F8FF; border-right: none; }")
        self.setFixedWidth(200)


class TaskItemWidget(QFrame):
    """Widget representing a single task item"""

    PRIORITY_COLORS = {
        "High": "#FF4444",
        "Medium": "#FF8C00",
        "Low": "#FFD700",
        "None": "#999",
    }

    def __init__(self, task_data, parent=None):
        super().__init__(parent)
        self.task_data = task_data
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()

        # Add task components
        layout.addWidget(self._createCheckbox())
        layout.addLayout(self._createTaskInfo(), stretch=2)
        layout.addLayout(self._createTimesLayout(), stretch=1)
        layout.addWidget(self._createPriorityButton())
        layout.addWidget(self._createStatusButton())

        self.setLayout(layout)
        self.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border-radius: 10px;
                margin: 5px;
                padding: 10px;
            }
            QFrame:hover {
                background-color: #f5f5f5;
            }
        """
        )

    def _createCheckbox(self):
        """Create task completion checkbox"""
        checkbox = QPushButton()
        checkbox.setCheckable(True)
        checkbox.setFixedSize(24, 24)
        checkbox.setStyleSheet(
            """
            QPushButton {
                border: 2px solid #ccc;
                border-radius: 12px;
                background-color: white;
            }
            QPushButton:checked {
                background-color: #00B4D8;
                border-color: #00B4D8;
            }
        """
        )
        return checkbox

    def _createTaskInfo(self):
        """Create layout for task name and description"""
        info_layout = QVBoxLayout()

        name_label = QLabel(self.task_data.get("name", ""))
        name_label.setFont(QFont("Arial", 12, QFont.Bold))

        desc_label = QLabel(self.task_data.get("description", ""))
        desc_label.setStyleSheet("color: #666;")

        info_layout.addWidget(name_label)
        info_layout.addWidget(desc_label)

        return info_layout

    def _createTimesLayout(self):
        """Create layout for start and deadline times"""
        times_layout = QVBoxLayout()

        start_label = QLabel(f"StartLine: {self.task_data.get('start_time', '')}")
        deadline_label = QLabel(f"Deadline: {self.task_data.get('deadline', '')}")

        times_layout.addWidget(start_label)
        times_layout.addWidget(deadline_label)

        return times_layout

    def _createPriorityButton(self):
        """Create priority indicator button"""
        priority = self.task_data.get("priority", "None")
        btn = QPushButton(priority)
        btn.setFixedWidth(80)
        btn.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self.PRIORITY_COLORS.get(priority, "#999")};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 5px;
            }}
        """
        )
        return btn

    def _createStatusButton(self):
        """Create status indicator button"""
        status = self.task_data.get("status", "Due")
        btn = QPushButton(status)
        btn.setFixedWidth(80)
        btn.setStyleSheet(
            """
            QPushButton {
                background-color: #eee;
                border: none;
                border-radius: 10px;
                padding: 5px;
            }
        """
        )
        return btn
