# from PyQt6 import QtWidgets
# from ui_views.fabrication_dashboard import MyApp
# import os
# from PyQt6.QtGui import QFontDatabase,QFont
# import matplotlib.pyplot as plt
# plt.switch_backend("QtAgg")
# # def resource_path(relative_path):
# #     if hasattr(sys,'_MEIPASS'):
# #         return os.path.join(sys._MEIPASS,relative_path)
# #     return os.path.join(os.path.abspath("."),relative_path)
# # def load_fonts():
# #     font_path=resource_path("assets/fonts/Roboto-Medium.ttf")
# #     font_id=QFontDatabase.addApplicationFont(font_path)
# #     if font_id==-1:
# #         print("Failed to load font")
# #     else:
# #         print("fon succsw")

# def resource_path(relative_path):
#     """
#     Get the absolute path to a resource, works for both development and PyInstaller bundle.
#     """
#     if hasattr(sys, '_MEIPASS'):
#         # Running in a PyInstaller bundle
#         base_path = sys._MEIPASS
#     else:
#         # Running in a normal Python environment
#         base_path = os.path.abspath(".")
    
#     return os.path.join(base_path, relative_path)

# def load_fonts():
#     """
#     Load custom fonts into the application.
#     """
#     font_path = resource_path("assets/fonts/Roboto-Medium.ttf")
    
#     # Check if the font file exists
#     if not os.path.exists(font_path):
#         print(f"Error: Font file not found at {font_path}")
#         return
    
#     # Load the font
#     font_id = QFontDatabase.addApplicationFont(font_path)
#     if font_id == -1:
#         print("Failed to load font")
#     else:
#         # Verify the font family name
#         font_family = QFontDatabase.applicationFontFamilies(font_id)
#         if font_family:
#             print(f"Font loaded successfully: {font_family[0]}")
#         else:
#             print("Error: Font loaded, but no font family found.")
            
# def load_stylesheet(file_path):
#     """Load the QSS stylesheet from the given file path."""
#     try:
#         with open(file_path, "r") as file:
#             return file.read()
#     except Exception as e:
#         print(f"Error loading stylesheet: {e}")
#         return ""
# if __name__ == "__main__":

#     import sys
#     print("hello world")
#     if hasattr(sys,"_MEIPASS"):
#         print("PyInstaller extraction path:",sys._MEIPASS)
#         qt_plugin_path = os.path.join(sys._MEIPASS, "PyQt6", "Qt6", "plugins")
#         print(" Using extracted plugin path:", qt_plugin_path)
#     else:
#         qt_plugin_path = os.path.join(os.path.dirname(__file__), "PyQt6", "Qt6", "plugins")
#         print("⚠️ Using local plugin path:", qt_plugin_path)
#     os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugin_path

#     app = QtWidgets.QApplication(sys.argv)
#     load_fonts()
#     stylesheet_path=resource_path("assets/styles.qss")
#     stylesheet=load_stylesheet(stylesheet_path)
#     app.setStyleSheet(stylesheet)


#     window = MyApp()
#     window.show()
#     sys.exit(app.exec())

from PyQt6 import QtWidgets
from ui_views.fabrication_dashboard import MyApp
import os
import sys
from PyQt6 import QtWidgets
from PyQt6.QtGui import QFontDatabase

def resource_path(relative_path):
    """
    Get the absolute path to a resource. Works for both development and PyInstaller bundle.
    """
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS  # PyInstaller bundle
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))  # Development mode

    return os.path.join(base_path, relative_path)

def load_fonts():
    """
    Load custom fonts into the application.
    """
    font_path = resource_path("assets/fonts/Roboto-Medium.ttf")
    
    # Debugging: Print font path
    print(f"🔍 Checking font at: {font_path}")
    
    if not os.path.exists(font_path):
        print(f"❌ Error: Font file not found at {font_path}")
        return
    
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id == -1:
        print("❌ Failed to load font")
    else:
        font_family = QFontDatabase.applicationFontFamilies(font_id)
        if font_family:
            print(f"✅ Font loaded successfully: {font_family[0]}")
        else:
            print("❌ Error: Font loaded, but no font family found.")

def load_stylesheet(relative_path):
    """
    Load the QSS stylesheet from the given file path.
    """
    full_path = resource_path(relative_path)
    
    # Debugging: Print stylesheet path
    print(f"🔍 Checking stylesheet at: {full_path}")
    
    if not os.path.exists(full_path):
        print(f"❌ Stylesheet file not found: {full_path}")
        return ""
    
    try:
        with open(full_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print(f"❌ Error loading stylesheet: {e}")
        return ""

if __name__ == "__main__":
    print("👋 Hello World")
    

    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    # Check if running from PyInstaller bundle
    if hasattr(sys, "_MEIPASS"):
        print("🚀 Running as PyInstaller bundle")
        print("📁 PyInstaller extraction path:", sys._MEIPASS)
    else:
        print("⚙️ Running in development mode")

    app = QtWidgets.QApplication(sys.argv)
    
    # Load custom fonts
    load_fonts()

    # Load and apply stylesheet
    stylesheet_path = "assets/styles.qss"
    stylesheet = load_stylesheet(stylesheet_path)
    app.setStyleSheet(stylesheet)

    # Initialize the main application window
    window = MyApp()
    window.show()

    sys.exit(app.exec())
