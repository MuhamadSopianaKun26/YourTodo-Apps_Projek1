from PyQt5.QtWidgets import (
    QDialog, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QMessageBox, QWidget, QListWidget,
    QListWidgetItem, QInputDialog, QMenu, QAction, QCalendarWidget,
    QDateEdit, QTimeEdit, QTextEdit, QRadioButton
)
from PyQt5.QtCore import Qt, pyqtSignal, QDate, QTime
from PyQt5.QtGui import QPixmap, QFont, QIcon

import re
import bcrypt
import os

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def validEmail(email):
        formatEmail = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(formatEmail, email) is not None
    
    @staticmethod
    def validPassword(password):
        if len(password) < 8:
            return False, "Password must be at least 8 characters!"
        if not re.search(r'[A-Z]', password):  
            return False, "Password must contain uppercase letters!"
        if not re.search(r'[a-z]', password):  
            return False, "Password must contain lowercase letters!"
        if not re.search(r'[0-9]', password): 
            return False, "Password must contain numbers!"
        return True, "Password is valid"

    @staticmethod
    def hashPassword(password):
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


class ManageAuth:
    def __init__(self):
        self.users = self.loadUsers()

    def loadUsers(self):
        users = {}
        try:
            with open('data/Users.txt', 'r') as file:
                for line in file:
                    line = line.strip()
                    if ' | ' in line:
                        parts = line.split(' | ')
                        if len(parts) == 3:
                            username, email, password = parts
                            users[email] = User(username, email, password)
        except FileNotFoundError as e:
            print(f"Users.txt file not found: {e}")
        except Exception as e:
            print(f"Error loading user data: {e}")
        
        print(f"Total users loaded: {len(users)}")
        return users
    
    def saveUsers(self):
        try:
            os.makedirs('data', exist_ok=True)
            with open('data/Users.txt', 'w') as file:
                for user in self.users.values():
                    userData = f"{user.username} | {user.email} | {user.password}\n"
                    file.write(userData)
        except Exception as e:
            print(f"Error saving user data: {e}")

    def register(self, username, email, password):
        if not User.validEmail(email):
            return False, "Invalid email format!"
        valid, message = User.validPassword(password)
        if not valid:
            return False, message
        if email in self.users:
            return False, "Email already registered!"
        if username in [user.username for user in self.users.values()]:
            return False, "Username already exists!"
        
        passwordHash = User.hashPassword(password)
        self.users[email] = User(username, email, passwordHash)
        self.saveUsers()
        return True, "Account created successfully"
    
    def login(self, email, password):
        print(f"Attempting login with email: {email}")
        print(f"Registered emails: {list(self.users.keys())}")

        if email not in self.users:
            return False, "Email not found!"
        
        storeHash = self.users[email].password.encode('utf-8')
        print(f"Stored password hash: {storeHash}")

        if bcrypt.checkpw(password.encode('utf-8'), storeHash):
            return True, "Login successful"
        else:
            return False, "Incorrect password!"

class TaskDialog(QDialog):
    """Dialog for creating or editing tasks with interactive calendar"""
    
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.username = username
        self.setWindowTitle("Add New Task")
        self.setFixedSize(500, 600)
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        # Task Name
        self.task_name = QLineEdit()
        self.task_name.setPlaceholderText("Task name")
        layout.addWidget(QLabel("Task Name:"))
        layout.addWidget(self.task_name)
        
        # Task Description
        self.task_desc = QTextEdit()
        self.task_desc.setPlaceholderText("Task description")
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.task_desc)
        
        # Start Date with interactive calendar
        self.start_date = QDateEdit(calendarPopup=True)
        self.start_date.setDate(QDate.currentDate())
        self.start_date.setDisplayFormat("yyyy-MM-dd")
        layout.addWidget(QLabel("Start Date:"))
        layout.addWidget(self.start_date)
        
        # Deadline with interactive calendar
        self.deadline = QDateEdit(calendarPopup=True)
        self.deadline.setDate(QDate.currentDate().addDays(1))
        self.deadline.setDisplayFormat("yyyy-MM-dd")
        layout.addWidget(QLabel("Deadline:"))
        layout.addWidget(self.deadline)
        
        # Priority Selection
        self.priority_low = QRadioButton("Low")
        self.priority_med = QRadioButton("Medium")
        self.priority_high = QRadioButton("High")
        self.priority_med.setChecked(True)
        
        priority_layout = QHBoxLayout()
        priority_layout.addWidget(self.priority_low)
        priority_layout.addWidget(self.priority_med)
        priority_layout.addWidget(self.priority_high)
        layout.addWidget(QLabel("Priority:"))
        layout.addLayout(priority_layout)
        
        # Save Button
        save_btn = QPushButton("Save Task")
        save_btn.clicked.connect(self.validate_and_save)
        layout.addWidget(save_btn)
        
        self.setLayout(layout)
    
    def validate_and_save(self):
        name = self.task_name.text().strip()
        desc = self.task_desc.toPlainText().strip()
        start = self.start_date.date().toString("yyyy-MM-dd")
        end = self.deadline.date().toString("yyyy-MM-dd")
        
        if not name:
            QMessageBox.warning(self, "Error", "Task name cannot be empty!")
            return
            
        if QDate.fromString(start, "yyyy-MM-dd") > QDate.fromString(end, "yyyy-MM-dd"):
            QMessageBox.warning(self, "Error", "Deadline cannot be before start date!")
            return
            
        priority = "Low" if self.priority_low.isChecked() else "Medium" if self.priority_med.isChecked() else "High"
        
        task_data = {
            'username': self.username,
            'name': name,
            'description': desc,
            'start_date': start,
            'deadline': end,
            'priority': priority,
            'status': 'Pending'
        }
        
        self.accept()
        return task_data
        
    
    
class LoginDialog(QDialog):
    """
    A dialog window for user authentication that provides login functionality
    and navigation to registration.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(1100, 650)
        self.manage_auth = ManageAuth()
        self._setup_styles()
        self.initUI()

    def _setup_styles(self):
        """Configure the styling for the login dialog components."""
        self.setStyleSheet(
            """
            QDialog {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #E0F7FA,
                    stop: 1 #B2EBF2
                );
            }
            QLabel {
                color: #333;
                font-size: 18px;
            }
            QLineEdit {
                padding: 12px;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                background: white;
                font-size: 18px;
                min-width: 300px;
            }
            QPushButton#loginBtn {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-size: 18px;
                min-width: 300px;
            }
            QPushButton#loginBtn:hover {
                background-color: #1976D2;
            }
            QPushButton#registerBtn {
                background: none;
                border: none;
                color: #2196F3;
                text-decoration: underline;
                font-size: 18px;
            }
            QPushButton#registerBtn:hover {
                color: #1976D2;
            }
            QLabel#errorLabel {
                color: #F44336;
                font-size: 14px;
            }
        """
        )

    def initUI(self):
        """Initialize and setup the user interface components."""
        main_layout = QHBoxLayout()
        main_layout.addWidget(self._create_login_form())
        main_layout.addWidget(self._create_illustration())
        self.setLayout(main_layout)

    def _create_login_form(self):
        """Create and return the login form widget."""
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(50, 50, 50, 50)
        left_layout.setSpacing(15)

        title = QLabel("Login")
        title.setFont(QFont("Arial", 48, QFont.Bold))
        title.setStyleSheet("color: #333; font-size: 48px;")

        self.email = QLineEdit()
        self.email.setPlaceholderText("Enter Your Email...")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter Your Password...")
        self.password.setEchoMode(QLineEdit.Password)

        self.error_label = QLabel()
        self.error_label.setObjectName("errorLabel")
        self.error_label.setWordWrap(True)

        login_btn = QPushButton("Login")
        login_btn.setObjectName("loginBtn")
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.clicked.connect(self.login)

        left_layout.addWidget(title)
        left_layout.addSpacing(20)
        left_layout.addWidget(QLabel("Email"))
        left_layout.addWidget(self.email)
        left_layout.addWidget(QLabel("Password"))
        left_layout.addWidget(self.password)
        left_layout.addWidget(self.error_label)
        left_layout.addSpacing(10)
        left_layout.addWidget(login_btn)
        left_layout.addWidget(self._create_register_link())
        left_layout.addStretch()
        left_layout.addWidget(self._create_logo())

        left_widget.setLayout(left_layout)
        return left_widget

    def _create_register_link(self):
        """Create and return the registration link widget."""
        register_container = QWidget()
        register_layout = QHBoxLayout()

        register_label = QLabel("Don't have an account?")
        register_label.setStyleSheet("color: #666;")

        register_btn = QPushButton("Sign up")
        register_btn.setObjectName("registerBtn")
        register_btn.setCursor(Qt.PointingHandCursor)
        register_btn.clicked.connect(self.register)

        register_layout.addWidget(register_label)
        register_layout.addWidget(register_btn)
        register_layout.setAlignment(Qt.AlignLeft)
        register_container.setLayout(register_layout)
        return register_container

    def _create_logo(self):
        """Create and return the logo widget."""
        logo_label = QLabel()
        logo_pixmap = QPixmap("images/logo.png")
        if not logo_pixmap.isNull():
            logo_pixmap = logo_pixmap.scaled(
                250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            logo_label.setPixmap(logo_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
        return logo_label

    def _create_illustration(self):
        """Create and return the illustration widget."""
        right_widget = QWidget()
        right_layout = QVBoxLayout()

        illustration_label = QLabel()
        illustration_pixmap = QPixmap("images/auth_illustration.png")
        if not illustration_pixmap.isNull():
            illustration_pixmap = illustration_pixmap.scaled(
                500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            illustration_label.setPixmap(illustration_pixmap)
            illustration_label.setAlignment(Qt.AlignCenter)

        right_layout.addWidget(illustration_label)
        right_widget.setLayout(right_layout)
        return right_widget

    def login(self):
        """Handle the login process and validation."""
        email = self.email.text().strip()
        password = self.password.text()

        if not email or not password:
            self.error_label.setText("All fields must be filled!")
            return

        success, message = self.manage_auth.login(email, password)
        if success:
            QMessageBox.information(self, "Success", "Login successful!")
            self.accept()
            self.open_main_app(email)
        else:
            self.error_label.setText(message)

  
    def open_main_app(self, email):
        from main import ToDoApp
        self.main_app = ToDoApp()
        username = self.manage_auth.users[email].username
        self.main_app.set_current_user(username)
        self.main_app.show()
        self.hide()

    def register(self):
        """Open the registration dialog."""
        dialog = RegistrationDialog(self.manage_auth, self)
        if dialog.exec_() == QDialog.Accepted:
            self.email.setText(dialog.email.text())
            self.password.clear()

class TaskManager:
    def __init__(self, username):
        self.username = username
        self.tasks_file = 'data/tasks.txt'
        self.tasks = self.load_tasks()

    def load_tasks(self):
        tasks = []
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'r') as file:
                for line in file:
                    parts = line.strip().split(' | ')
                    if len(parts) == 7 and parts[6] == self.username:
                        tasks.append({
                            'name': parts[0],
                            'description': parts[1],
                            'start_date': parts[2],
                            'deadline': parts[3],
                            'priority': parts[4],
                            'status': parts[5],
                            'username': parts[6]
                        })
        return tasks

    def save_task(self, task):
        os.makedirs('data', exist_ok=True)
        with open(self.tasks_file, 'a') as file:
            task_line = f"{task['name']} | {task['description']} | {task['start_date']} | {task['deadline']} | {task['priority']} | {task['status']} | {task['username']}\n"
            file.write(task_line)
        self.tasks.append(task)

    def get_tasks(self):
        return self.tasks