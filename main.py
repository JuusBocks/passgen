import sys
import os
import traceback


def main():
    try:
        from PyQt6.QtWidgets import QApplication
        from passgen.ui.main_window import PasswordGeneratorApp

        app = QApplication(sys.argv)
        window = PasswordGeneratorApp()
        window.show()
        sys.exit(app.exec())
    except Exception as exc:
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            logs_dir = os.path.join(base_dir, "logs")
            os.makedirs(logs_dir, exist_ok=True)
            log_path = os.path.join(logs_dir, "passgen_error.log")
            with open(log_path, "a", encoding="utf-8") as f:
                f.write("=== Unhandled exception ===\n")
                traceback.print_exc(file=f)
                f.write("\n")
        except Exception:
            pass
        try:
            # Attempt to show a message box if Qt is available
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(None, "passgen - Error", f"An error occurred starting the app.\n\nDetails were written to logs\\passgen_error.log.\n\n{exc}")
        except Exception:
            pass
        raise


if __name__ == '__main__':
    main()


