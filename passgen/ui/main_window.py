import string
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QRadioButton, QButtonGroup, QMessageBox, QSpinBox, QCheckBox)
from PyQt6.QtGui import QFont
import pyperclip

from passgen.core.generator import PasswordGenerator
from passgen.core.parser import PolicyParser


class PasswordGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.policy_parser = PolicyParser()
        self.generator = PasswordGenerator()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("passgen - Password Generator")
        self.setGeometry(100, 100, 600, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        title = QLabel("Password Generator")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        mode_layout = QHBoxLayout()
        mode_label = QLabel("Mode:")
        mode_group = QButtonGroup()
        
        self.mode_custom = QRadioButton("Custom Instructions")
        self.mode_generate = QRadioButton("Generate Password")
        self.mode_generate.setChecked(True)
        
        mode_group.addButton(self.mode_custom, 1)
        mode_group.addButton(self.mode_generate, 2)
        
        self.mode_custom.toggled.connect(self.on_mode_changed)
        
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_custom)
        mode_layout.addWidget(self.mode_generate)
        mode_layout.addStretch()
        layout.addLayout(mode_layout)
        
        self.custom_label = QLabel("Paste password requirements:")
        layout.addWidget(self.custom_label)
        
        self.custom_input = QTextEdit()
        self.custom_input.setPlaceholderText("Example: Must contain uppercase, lowercase, numbers, and special characters. Min 12 characters.")
        self.custom_input.setMaximumHeight(120)
        layout.addWidget(self.custom_input)
        
        self.gen_settings_label = QLabel("Password Settings:")
        layout.addWidget(self.gen_settings_label)
        
        settings_layout = QHBoxLayout()
        length_label = QLabel("Length:")
        self.length_spinbox = QSpinBox()
        self.length_spinbox.setMinimum(8)
        self.length_spinbox.setMaximum(128)
        self.length_spinbox.setValue(16)
        
        settings_layout.addWidget(length_label)
        settings_layout.addWidget(self.length_spinbox)
        settings_layout.addStretch()
        layout.addLayout(settings_layout)
        
        checkbox_layout = QHBoxLayout()
        self.include_uppercase = QCheckBox("Uppercase (A-Z)")
        self.include_uppercase.setChecked(True)
        self.include_lowercase = QCheckBox("Lowercase (a-z)")
        self.include_lowercase.setChecked(True)
        self.include_numbers = QCheckBox("Numbers (0-9)")
        self.include_numbers.setChecked(True)
        self.include_special = QCheckBox("Special (!@#$%)")
        self.include_special.setChecked(True)
        
        checkbox_layout.addWidget(self.include_uppercase)
        checkbox_layout.addWidget(self.include_lowercase)
        checkbox_layout.addWidget(self.include_numbers)
        checkbox_layout.addWidget(self.include_special)
        layout.addLayout(checkbox_layout)
        
        self.gen_settings_label.hide()
        self.length_spinbox.hide()
        self.include_uppercase.hide()
        self.include_lowercase.hide()
        self.include_numbers.hide()
        self.include_special.hide()
        
        output_label = QLabel("Generated Password:")
        layout.addWidget(output_label)
        
        self.password_output = QLineEdit()
        self.password_output.setReadOnly(True)
        self.password_output.setMinimumHeight(40)
        password_font = QFont()
        password_font.setPointSize(12)
        password_font.setFamily("Courier New")
        self.password_output.setFont(password_font)
        layout.addWidget(self.password_output)
        
        button_layout = QHBoxLayout()
        self.generate_btn = QPushButton("Generate Password")
        self.generate_btn.setMinimumHeight(40)
        self.generate_btn.clicked.connect(self.generate_password)
        
        self.copy_btn = QPushButton("Copy to Clipboard")
        self.copy_btn.setMinimumHeight(40)
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        
        button_layout.addWidget(self.generate_btn)
        button_layout.addWidget(self.copy_btn)
        layout.addLayout(button_layout)
        
        layout.addStretch()

        # Ensure initial state matches the default selected mode
        self.on_mode_changed()
    
    def on_mode_changed(self):
        if self.mode_custom.isChecked():
            self.custom_label.show()
            self.custom_input.show()
            self.gen_settings_label.hide()
            self.length_spinbox.hide()
            self.include_uppercase.hide()
            self.include_lowercase.hide()
            self.include_numbers.hide()
            self.include_special.hide()
            self.generate_btn.setText("Generate from Instructions")
        else:
            self.custom_label.hide()
            self.custom_input.hide()
            self.gen_settings_label.show()
            self.length_spinbox.show()
            self.include_uppercase.show()
            self.include_lowercase.show()
            self.include_numbers.show()
            self.include_special.show()
            self.generate_btn.setText("Generate Password")
    
    def generate_password(self):
        try:
            if self.mode_custom.isChecked():
                instructions = self.custom_input.toPlainText().strip()
                if not instructions:
                    QMessageBox.warning(self, "Input Error", "Please paste password requirements.")
                    return
                policy = self.policy_parser.parse(instructions)
                password = self.generator.generate_from_policy(policy)
            else:
                length = self.length_spinbox.value()
                password = self.generator.generate_random(
                    length=length,
                    include_uppercase=self.include_uppercase.isChecked(),
                    include_lowercase=self.include_lowercase.isChecked(),
                    include_numbers=self.include_numbers.isChecked(),
                    include_special=self.include_special.isChecked(),
                )
            self.password_output.setText(password)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
    
    def copy_to_clipboard(self):
        password = self.password_output.text()
        if not password:
            QMessageBox.warning(self, "Empty Password", "Generate a password first.")
            return
        pyperclip.copy(password)
        QMessageBox.information(self, "Success", "Password copied to clipboard!")


