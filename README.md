# 🔐 Password Generator

A secure desktop password generator with an intuitive GUI. Generate cryptographically strong passwords that meet any website's requirements.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- **🎯 Two Generation Modes**
  - **Quick Generate**: Customize length and character types (uppercase, lowercase, numbers, special characters)
  - **Smart Parser**: Paste website password requirements and automatically generate matching passwords

- **🔒 Cryptographically Secure**: Uses Python's `secrets` module for secure random generation
- **📋 One-Click Copy**: Instantly copy passwords to clipboard
- **🖥️ Native Windows Integration**: Add to Start Menu for quick access
- **⚡ Offline**: No internet required, runs entirely on your machine

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/passwordGen.git
   cd passwordGen
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

### Windows Start Menu Setup (Optional)

For quick access from Windows Start Menu:
```bash
# Run as administrator
create_shortcut.bat
```

Then search for "passgen" in your Start Menu!

## 📖 Usage

### Mode 1: Quick Generate

Perfect for creating strong passwords quickly:

1. Select **"Generate Password"** (default mode)
2. Set your desired length (8-128 characters)
3. Choose character types:
   - ✅ Uppercase (A-Z)
   - ✅ Lowercase (a-z)
   - ✅ Numbers (0-9)
   - ✅ Special characters (!@#$%^&*)
4. Click **"Generate Password"**
5. Click **"Copy to Clipboard"**

**Example output**: `K9#mP2@xL4$nQ7&B`

### Mode 2: Smart Requirements Parser

When websites have specific password requirements:

1. Select **"Custom Instructions"**
2. Copy and paste the website's requirements:
   ```
   Example: "Password must contain uppercase, lowercase, 
   numbers, and special characters. Minimum 12 characters."
   ```
3. Click **"Generate from Instructions"**
4. The app analyzes the requirements and generates a compliant password
5. Click **"Copy to Clipboard"**

**Example output**: `Secure#Pass123`

## 🏗️ Project Structure

```
passwordGen/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── run.bat                 # Windows launcher script
├── setup.bat               # Automated setup script
├── create_shortcut.bat     # Start Menu shortcut creator
└── passgen/
    ├── __init__.py
    ├── constants.py        # Configuration constants
    ├── core/
    │   ├── generator.py    # Password generation logic
    │   ├── parser.py       # Requirements parsing
    │   └── policy.py       # Password policy definitions
    └── ui/
        └── main_window.py  # GUI implementation
```

## 🛠️ Requirements

- **Python**: 3.8 or higher
- **PyQt6**: Modern GUI framework
- **pyperclip**: Clipboard integration

## 🔧 Development

### Running in Development Mode

```bash
# With debug output
run_debug.bat

# Or directly with Python
python main.py
```

### Building from Source

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests (if available)
pytest

# Run the application
python main.py
```

## 💡 Tips & Best Practices

- **Default length of 16+ characters** provides excellent security
- **Include all character types** for maximum password strength
- Use **Custom Instructions mode** when websites have strict requirements
- The app runs **completely offline** - no data is sent anywhere
- All passwords are generated using **cryptographically secure** random functions

## 🐛 Troubleshooting

### App won't open from Start Menu
```bash
# Reinstall dependencies and recreate shortcut
setup.bat
```

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Shortcut not appearing in Start Menu
```bash
# Run as administrator
Right-click create_shortcut.bat → "Run as administrator"
```

## 📝 License

Free to use and modify for personal and commercial purposes.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 🔗 Links

- **Issues**: Report bugs or request features
- **Discussions**: Ask questions or share ideas

---

**Made with 🔒 for secure password generation**
