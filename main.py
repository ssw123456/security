import sys
from Security.securityapp import SecurityApp
if __name__ == '__main__':
    app = SecurityApp()
    sys.exit(app.exec())