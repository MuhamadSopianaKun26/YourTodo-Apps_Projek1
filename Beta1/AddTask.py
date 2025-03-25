from PyQt5 import QtWidgets, QtCore, QtGui
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
    QMenu,
)

from PyQt5.QtCore import QTime, QDate, Qt
from PyQt5.QtGui import QFont, QPixmap
import os
import sys



# Tambahkan path proyek ke Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.append(project_root)



class DateTimeDialog(QDialog):
    def __init__(self, parent=None, title="Select Date and Time", is_start_time=False, deadline=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.is_start_time = is_start_time
        self.deadline = deadline
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Calendar widget
        self.calendar = QCalendarWidget()
        self.calendar.setMinimumDate(QDate.currentDate())
        layout.addWidget(QLabel("Select Date:"))
        layout.addWidget(self.calendar)

        # Time widget
        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime.currentTime())
        layout.addWidget(QLabel("Select Time:"))
        layout.addWidget(self.time_edit)

        # Button container untuk tombol-tombol
        button_container = QHBoxLayout()
        
        # Reset button
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_selection)
        self.reset_button.setStyleSheet("""
            QPushButton {
                padding: 5px 10px;
                text-align: center;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #f44336;
                color: white;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        
        # Dialog buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)
        
        # Tambahkan tombol ke container
        button_container.addWidget(self.reset_button)
        button_container.addWidget(button_box)
        
        layout.addLayout(button_container)
        self.setLayout(layout)

    def reset_selection(self):
        """Reset pilihan tanggal dan waktu ke nilai default dan tutup dialog."""
        self.reject()

    def validate_and_accept(self):
        selected_date = self.calendar.selectedDate()
        selected_time = self.time_edit.time()
        selected_datetime = f"{selected_date.toString('yyyy-MM-dd')} {selected_time.toString('HH:mm')}"

        if self.is_start_time and self.deadline:
            # Jika ini adalah dialog start time dan deadline sudah dipilih
            deadline_date = QDate.fromString(self.deadline.split(" ")[0], "yyyy-MM-dd")
            deadline_time = QTime.fromString(self.deadline.split(" ")[1], "HH:mm")

            if selected_date > deadline_date or (selected_date == deadline_date and selected_time >= deadline_time):
                QMessageBox.warning(
                    self,
                    "Validation Error",
                    "Start time cannot be later than or equal to deadline!"
                )
                return

        elif not self.is_start_time and self.deadline:
            # Jika ini adalah dialog deadline dan start time sudah dipilih
            start_date = QDate.fromString(self.deadline.split(" ")[0], "yyyy-MM-dd")
            start_time = QTime.fromString(self.deadline.split(" ")[1], "HH:mm")

            if selected_date < start_date or (selected_date == start_date and selected_time <= start_time):
                QMessageBox.warning(
                    self,
                    "Validation Error",
                    "Deadline cannot be earlier than or equal to start time!"
                )
                return

        self.accept()

    def get_datetime(self):
        selected_date = self.calendar.selectedDate()
        selected_time = self.time_edit.time()
        return f"{selected_date.toString('yyyy-MM-dd')} {selected_time.toString('HH:mm')}"


## main program ##
class AddTaskWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setGeometry(QtCore.QRect(110, 190, 841, 221))
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setObjectName("AddTodo")

        # Task Name Input
        self.TaskName = QtWidgets.QLineEdit(self)
        self.TaskName.setGeometry(QtCore.QRect(20, 20, 791, 21))
        self.TaskName.setObjectName("TaskName")
        self.TaskName.setPlaceholderText("Task Name")
        self.TaskName.textChanged.connect(self.validate_input)

        # Task Description Input
        self.DescTask = QtWidgets.QTextEdit(self)
        self.DescTask.setGeometry(QtCore.QRect(20, 50, 791, 61))
        self.DescTask.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        self.DescTask.setObjectName("DescTask")
        self.DescTask.setPlaceholderText("Description")

        # Line Separator
        self.line_3 = QtWidgets.QFrame(self)
        self.line_3.setGeometry(QtCore.QRect(20, 160, 801, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")

        # Container untuk tombol-tombol utama
        self.button_container = QtWidgets.QWidget(self)
        self.button_container.setGeometry(QtCore.QRect(20, 130, 801, 28))
        self.button_container.setObjectName("button_container")
        
        # Layout horizontal untuk tombol-tombol utama
        self.button_layout = QtWidgets.QHBoxLayout(self.button_container)
        self.button_layout.setSpacing(10)
        self.button_layout.setContentsMargins(0, 0, 0, 0)

        # Buttons (Start Time, Deadline, Priority, Reminder)
        icon_path = "../images/"
        self.StartTime = self.create_button("StartTime", "Calender_icon.png", "Start time")
        self.Deadline = self.create_button("Deadline", "Calender_icon.png", "Deadline")
        self.Priority = self.create_button("Priority", "Flag_icon.png", "Priority")
        self.Reminder = self.create_button("Reminder", "Reminder_icon.png", "Reminder")

        # Tambahkan tombol ke layout utama
        self.button_layout.addWidget(self.StartTime)
        self.button_layout.addWidget(self.Deadline)
        self.button_layout.addWidget(self.Priority)
        self.button_layout.addWidget(self.Reminder)
        self.button_layout.addStretch()

        # Container untuk tombol Schedule
        self.schedule_container = QtWidgets.QWidget(self)
        self.schedule_container.setGeometry(QtCore.QRect(20, 180, 801, 28))
        self.schedule_container.setObjectName("schedule_container")
        
        # Layout horizontal untuk tombol Schedule dan tombol aksi
        self.schedule_layout = QtWidgets.QHBoxLayout(self.schedule_container)
        self.schedule_layout.setSpacing(10)
        self.schedule_layout.setContentsMargins(0, 0, 0, 0)

        # Button Schedule dengan ukuran tetap
        self.Repeated = self.create_button("Repeated", "Repeated_icon.png", "Add as Schedule")
        self.Repeated.setFixedWidth(200)
        self.schedule_layout.addWidget(self.Repeated)
        
        # Tambahkan stretch untuk spacing
        self.schedule_layout.addStretch()
        
        # Buttons (Add & Cancel) dengan style yang baru
        self.Cancel = self.create_action_button("Cancel", "Cancel")
        self.AddTask = self.create_action_button("Add Task", "AddTask")
        self.AddTask.setEnabled(False)
        
        # Tambahkan tombol aksi ke layout
        self.schedule_layout.addWidget(self.Cancel)
        self.schedule_layout.addWidget(self.AddTask)

        # Connect action buttons
        self.Cancel.clicked.connect(self.cancel_toggle)
        self.AddTask.clicked.connect(self.show_task_dialog)
        self.StartTime.clicked.connect(lambda: self.show_datetime_dialog(self.StartTime))
        self.Deadline.clicked.connect(lambda: self.show_datetime_dialog(self.Deadline))
        
        # Create dropdown menus
        self.priority_dropdown = self.create_dropdown_menu(self.Priority, ["None", "Low", "Medium", "High"])
        self.reminder_dropdown = self.create_dropdown_menu(self.Reminder, ["None", "5 minutes before", "15 minutes before", "30 minutes before", "1 hour before"])
        self.repeated_dropdown = self.create_dropdown_menu(self.Repeated, ["None", "Daily", "Weekly", "Monthly"])

        # Connect dropdown buttons
        self.Priority.clicked.connect(lambda: self.toggle_dropdown(self.priority_dropdown, self.Priority))
        self.Reminder.clicked.connect(lambda: self.toggle_dropdown(self.reminder_dropdown, self.Reminder))
        self.Repeated.clicked.connect(lambda: self.toggle_dropdown(self.repeated_dropdown, self.Repeated))




    def create_button(self, name, icon_file, text):
        """Helper untuk membuat QPushButton dengan ikon dan ukuran yang dinamis."""
        button = QtWidgets.QPushButton(text)
        button.setObjectName(name)
        button.setMinimumWidth(100)
        button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        
        # Set ikon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("images", icon_file)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        button.setIcon(icon)
        
        # Set style untuk padding dan alignment
        button.setStyleSheet(f"""
            QPushButton {{
                padding: 5px 10px;
                text-align: left;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }}
            QPushButton:hover {{
                background-color: #f0f0f0;
            }}
        """)
        
        return button

    def create_action_button(self, name, object_name):
        """Helper untuk membuat tombol aksi (Add Task & Cancel)."""
        button = QtWidgets.QPushButton(name)
        button.setObjectName(object_name)
        button.setFixedWidth(93)
        button.setFixedHeight(28)
        
        # Set style khusus untuk tombol aksi
        button.setStyleSheet(f"""
            QPushButton {{
                padding: 5px 10px;
                text-align: center;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }}
            QPushButton:hover {{
                background-color: #f0f0f0;
            }}
            QPushButton#AddTask {{
                background-color: #2196F3;
                color: white;
                border: none;
            }}
            QPushButton#AddTask:hover {{
                background-color: #1976D2;
            }}
            QPushButton#AddTask:disabled {{
                background-color: #BDBDBD;
            }}
            QPushButton#Cancel {{
                background-color: #f44336;
                color: white;
                border: none;
            }}
            QPushButton#Cancel:hover {{
                background-color: #da190b;
            }}
        """)
        
        return button

    def create_dropdown_menu(self, button, items):
        """Helper untuk membuat menu dropdown."""
        menu = QMenu(self)
        
        # Khusus untuk dropdown priority
        if button == self.Priority:
            # Dictionary untuk mengaitkan prioritas dengan ikon
            priority_icons = {
                "None": "Flag_icon.png",  # Kembali ke ikon default
                "High": "HighPriority_icon.png",
                "Medium": "MediumPriority_icon.png",
                "Low": "LowPriority_icon.png"
            }
            
            for item in items:
                action = menu.addAction(item)
                # Set ikon untuk setiap item
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(os.path.join("images", priority_icons[item])), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                action.setIcon(icon)
                action.triggered.connect(lambda checked, text=item: self.handle_dropdown_selection(button, text))
        else:
            # Untuk dropdown lainnya (reminder dan repeated)
            for item in items:
                action = menu.addAction(item)
                action.triggered.connect(lambda checked, text=item: self.handle_dropdown_selection(button, text))
        
        return menu

    def toggle_dropdown(self, menu, button):
        """Toggle visibility of dropdown menu."""
        # Hide all other dropdowns first
        self.hide_all_dropdowns()
        
        # Show the clicked dropdown
        pos = button.mapToGlobal(button.rect().bottomLeft())
        menu.exec_(pos)

    def hide_all_dropdowns(self):
        """Hide all dropdown menus."""
        self.priority_dropdown.hide()
        self.reminder_dropdown.hide()
        self.repeated_dropdown.hide()

    def handle_dropdown_selection(self, button, text):
        """Handle pemilihan item dari dropdown menu."""
        if button == self.Priority:
            # Dictionary untuk mengaitkan prioritas dengan ikon
            priority_icons = {
                "None": "Flag_icon.png",  # Kembali ke ikon default
                "High": "HighPriority_icon.png",
                "Medium": "MediumPriority_icon.png",
                "Low": "LowPriority_icon.png"
            }
            
            # Set teks button
            button.setText(text)
            
            # Set ikon sesuai prioritas yang dipilih
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join("images", priority_icons[text])), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            button.setIcon(icon)
            button.setIconSize(QtCore.QSize(24, 24))
            
        elif button == self.Reminder:
            button.setText(text)
        elif button == self.Repeated:
            button.setText(text)

    def validate_input(self):
        """Validasi input untuk mengaktifkan/menonaktifkan tombol Add Task."""
        self.AddTask.setEnabled(bool(self.TaskName.text().strip()))

    def show_task_dialog(self):
        """Menambahkan task baru ke dalam scrollArea dan menyimpannya ke database."""
        # Validasi input
        if not self.TaskName.text().strip():
            QMessageBox.warning(self, "Validation Error", "Task name cannot be empty!")
            return
            
        # Validasi waktu jika diisi
        if self.StartTime.text() != "Start time" and self.Deadline.text() != "Deadline":
            start_date = QDate.fromString(self.StartTime.text().split(" ")[0], "yyyy-MM-dd")
            start_time = QTime.fromString(self.StartTime.text().split(" ")[1], "HH:mm")
            deadline_date = QDate.fromString(self.Deadline.text().split(" ")[0], "yyyy-MM-dd")
            deadline_time = QTime.fromString(self.Deadline.text().split(" ")[1], "HH:mm")
            
            if start_date > deadline_date or (start_date == deadline_date and start_time >= deadline_time):
                QMessageBox.warning(self, "Validation Error", "Deadline must be later than start time!")
                return
            
        # Buat data task dengan nilai default untuk field yang tidak diisi
        task_data = {
            "name": self.TaskName.text(),
            "description": self.DescTask.toPlainText() if self.DescTask.toPlainText().strip() else "",
            "start_time": self.StartTime.text() if self.StartTime.text() != "Start time" else "None",
            "deadline": self.Deadline.text() if self.Deadline.text() != "Deadline" else "None",
            "priority": self.Priority.text() if self.Priority.text() != "Priority" else "None",
            "reminder": self.Reminder.text() if self.Reminder.text() != "Reminder" else "None",
            "repeated": self.Repeated.text() if self.Repeated.text() != "Add as Schedule" else "None",
            "status": "due"
        }
        
        try:
            # Simpan task ke database
            db_manager = DatabaseManager()
            saved_task = db_manager.save_task(task_data)
            
            # Dapatkan referensi ke TodayPageScreen
            today_page = self.parent().parent()
            
            # Pastikan showTodo widget ada dan todaypage ada
            if hasattr(today_page, 'ui') and hasattr(today_page.ui, 'showTodo'):
                # Clear existing tasks
                today_page.ui.showTodo.clear_tasks()
                
                # Load tasks dari database
                today_page.ui.showTodo.load_tasks()
                
                # Update jumlah task
                today_page.update_task_count()
                
                # Force update scroll area
                if hasattr(today_page.ui, 'scrollArea'):
                    today_page.ui.scrollArea.update()
                    today_page.ui.scrollArea.viewport().update()
            
            # Clear input dan sembunyikan widget
            self.clear_inputs()
            self.hide()
            
            # Tampilkan pesan sukses
            QMessageBox.information(self, "Success", "Task added successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save task: {str(e)}")

    def clear_inputs(self):
        """Hapus isi input."""
        self.TaskName.clear()
        self.DescTask.clear()
        self.StartTime.setText("Start time")
        self.Deadline.setText("Deadline")
        self.Priority.setText("Priority")
        self.Reminder.setText("Reminder")
        self.Repeated.setText("Add as Schedule")
        self.AddTask.setEnabled(False)
        self.hide_all_dropdowns()

    def cancel_toggle(self):
        """Toggle visibility of the widget dan clear inputs."""
        self.clear_inputs()
        self.hide()

    def show_datetime_dialog(self, button):
        """Menampilkan dialog untuk memilih tanggal dan waktu."""
        title = "Select Start Time" if button == self.StartTime else "Select Deadline"
        is_start_time = button == self.StartTime
        
        # Dapatkan nilai deadline atau start time yang sudah dipilih
        reference_time = None
        if is_start_time and self.Deadline.text() != "Deadline":
            reference_time = self.Deadline.text()
        elif not is_start_time and self.StartTime.text() != "Start time":
            reference_time = self.StartTime.text()

        dialog = DateTimeDialog(self, title, is_start_time, reference_time)
        if dialog.exec_():
            selected_datetime = dialog.get_datetime()
            button.setText(selected_datetime)

            # Validasi ulang tombol yang lain
            if is_start_time and self.Deadline.text() != "Deadline":
                self.validate_deadline()
            elif not is_start_time and self.StartTime.text() != "Start time":
                self.validate_start_time()
        else:
            # Jika dialog ditutup tanpa OK atau Reset ditekan, reset nilai tombol ke default
            if is_start_time:
                self.StartTime.setText("Start time")
            else:
                self.Deadline.setText("Deadline")

    def validate_start_time(self):
        """Validasi start time terhadap deadline yang sudah dipilih."""
        if self.StartTime.text() != "Start time" and self.Deadline.text() != "Deadline":
            start_date = QDate.fromString(self.StartTime.text().split(" ")[0], "yyyy-MM-dd")
            start_time = QTime.fromString(self.StartTime.text().split(" ")[1], "HH:mm")
            deadline_date = QDate.fromString(self.Deadline.text().split(" ")[0], "yyyy-MM-dd")
            deadline_time = QTime.fromString(self.Deadline.text().split(" ")[1], "HH:mm")

            if start_date > deadline_date or (start_date == deadline_date and start_time >= deadline_time):
                QMessageBox.warning(
                    self,
                    "Validation Error",
                    "Start time cannot be later than or equal to deadline!"
                )
                self.StartTime.setText("Start time")

    def validate_deadline(self):
        """Validasi deadline terhadap start time yang sudah dipilih."""
        if self.StartTime.text() != "Start time" and self.Deadline.text() != "Deadline":
            start_date = QDate.fromString(self.StartTime.text().split(" ")[0], "yyyy-MM-dd")
            start_time = QTime.fromString(self.StartTime.text().split(" ")[1], "HH:mm")
            deadline_date = QDate.fromString(self.Deadline.text().split(" ")[0], "yyyy-MM-dd")
            deadline_time = QTime.fromString(self.Deadline.text().split(" ")[1], "HH:mm")

            if deadline_date < start_date or (deadline_date == start_date and deadline_time <= start_time):
                QMessageBox.warning(
                    self,
                    "Validation Error",
                    "Deadline cannot be earlier than or equal to start time!"
                )
                self.Deadline.setText("Deadline")
