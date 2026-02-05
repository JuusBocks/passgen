"""Entry point when running as python -m passgen or via the passgen console script."""
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
            # Log in project root / logs (one level up from passgen package)
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            logs_dir = os.path.join(base_dir, "logs")
            os.makedirs(logs_dir, exist_ok=True)
            log_path = os.path.join(logs_dir, "passgen_error.log")
            with open(log_path, "a", encoding="utf-8") as f:
                f.write("=== Unhandled exception ===\n")
                traceback.print_exc(file=f)
                f.write("\n")
        except Exception:
            pass
        # Don't use QMessageBox here: Qt can crash (e.g. on macOS 26) if no app is running
        err_log = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "logs", "passgen_error.log"
        )
        print(f"passgen error: {exc}", file=sys.stderr)
        print(f"Details written to: {err_log}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
