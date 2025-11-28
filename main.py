from gui import DataProcessingGUI

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

if __name__ == "__main__":
    app = DataProcessingGUI()
    app.run()