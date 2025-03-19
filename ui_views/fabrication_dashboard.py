from PyQt6 import QtWidgets,QtGui,QtCore
from ui.py.fabrication_dashboard_dialog import Ui_MainWindow  # Import the generated UI class
from PyQt6.QtGui import QColor,QPainter,QPixmap,QPageLayout
from PyQt6.QtWidgets import QGraphicsDropShadowEffect,QHeaderView,QTableWidgetItem,QComboBox,QMessageBox,QVBoxLayout,QLineEdit,QFileDialog
from PyQt6.QtCore import Qt,QRegularExpression,QSize
import PyQt6,textwrap
from PyQt6.QtPrintSupport import QPrinter
import re,mysql.connector,random,os,sys,mplcursors
from .db_pool import DatabasePool
from mysql.connector import pooling
from .delete_system import DeleteSystem
from PyQt6.QtGui import QIntValidator,QRegularExpressionValidator,QPageSize

# import plotly.express as px   
# from PyQt6.QtWebEngineWidgets import QWebEngineView
from .line_production import MplCanvas
from .report import MplCanvasReports
import squarify,mplcursors
from matplotlib.widgets import Cursor
from .idle_hours import MplCanvasIdle
import matplotlib.pyplot as plt

import numpy as np
def convert_to_hours_return_float(val):
        v=float(val)
        # if val>60:
        #     v=round((val/60),2)
        hours=int(v)
        mins=round((v-hours)*60)
        a=f"{hours}.{mins}"
        print("a = ",a)
        return float(a)
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        self.setupUi(self)  # Set up the UI
        self.setWindowTitle("Fabrication Tool")
        self.data_inp_btn.clicked.connect(self.switch_to_dataInputPage)
        self.home_btn.clicked.connect(self.switch_to_homePage)
        self.line_production_btn.clicked.connect(self.switch_to_lineProductionPage)
        self.result_btn.clicked.connect(self.switch_to_resultsPage)
        self.data_inp_btn.setChecked(True)
        self.stackedWidget.setCurrentIndex(0)
        self.machining_table.horizontalHeader().setVisible(True)
        self.apply_shadow([self.widget_7,self.widget_8])
        # self.apply_shadow([self.company_logo])
        self.add_placeholder_machining_table()
        self.set_section_size_table(50)
        self.stretch_table_columns()
        # self.create_db_pool()
        self.time_taken_by_machine={}
        self.set_combo_to_table_cell()
        self.get_combo()
        self.data_for_calculation()
        self.isDataFilled=False
        self.btn_calculate.clicked.connect(self.cal_machining_assemb_handling_install)
        self.btn_clear.clicked.connect(lambda:self.clear_data(self.machining_table,self.assembly_table,self.handling_table,self.installation_table))
        self.btn_save.clicked.connect(lambda:self.save_system_data(1))
        self.load_saved_systems()
        self.populate_type_combo()
        self.load_saved_type()
        self.fab_res_le.setDisabled(True)
        self.saved_system_combo.currentIndexChanged.connect(lambda:self.load_system_data(1))
        self.remove_sys_btn.clicked.connect(self.show_dialog)
        self.basic_btn.clicked.connect(self.load_b_charts)
        # self.basic_btn.clicked.connect(self.change_app_color)
        self.basic_cnc_btn.clicked.connect(self.load_bc_charts)
        # self.basic_cnc_btn.clicked.connect(self.print_me)
        self.basic_punch_btn.clicked.connect(self.load_bp_charts)
        self.basic_punch_cnc_btn.clicked.connect(self.load_bpc_charts)
        self.basic_btn_lp.clicked.connect(self.load_b_charts)
        self.basic_cnc_lp.clicked.connect(self.load_bc_charts)
        self.basic_punch_lp.clicked.connect(self.load_bp_charts)
        self.basic_punch_rs.clicked.connect(self.load_bp_charts)
        self.basic_btn_rs.clicked.connect(self.load_b_charts)
        self.basic_cnc_rs.clicked.connect(self.load_bc_charts)
        self.basic_punch_cnc_rs.clicked.connect(self.load_bpc_charts)
        self.basic_punch_cnc_lp.clicked.connect(self.load_bpc_charts)
        self.type_combo.currentIndexChanged.connect(self.render_corresponding_image)
        self.type_combo_inp.currentIndexChanged.connect(self.render_corresponding_image_2)
        self.size_le_inp.setPlaceholderText("width x height in mm")
        self.recommendation_btn.clicked.connect(self.switch_to_recommendation_page)
        self.current_type_image()
        self.set_line_edits_to_cells()
        self.print_results_btn.clicked.connect(self.save_as_image)
        self.print_lp_btn.clicked.connect(self.save_as_image_lp)
        # self.machining_table.cellClicked.connect(lambda row,col:(self.remove_placeholder(row,col),self.restore_placeholder(row,col)))
        # self.machining_table.cellClicked.connect(self.restore_placeholder)
        self.min_units=0
        self.fab_res_le.setReadOnly(False)
        self.fab_res_le.setEnabled(True)
        regex=QRegularExpression(r"^(100|[1-9]?[0-9])$")
        validator=QRegularExpressionValidator(regex,self.fab_res_le)
        validator_2=QRegularExpressionValidator(regex,self.assmb_res_le)
        self.fab_res_le.setValidator(validator)
        self.assmb_res_le.setValidator(validator_2)
        self.read_only_row()
        self.set_default_machine_count()

        # self.apply_shadow()
        # You can now access UI elements defined in the .ui file
        # For example, if you have a button with the objectName 'myButton':
        # self.myButton.clicked.connect(self.handle_button_click)
    # def save_as_image(self):
    #     printer = QPrinter(QPrinter.PrinterMode.HighResolution)
    #     printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
    #     printer.setPageOrientation(QtGui.QPageLayout.Orientation.Landscape)
    #     printer.setPageSize(QPrinter.PaperSize.A4)

    #     # File Dialog for saving PDF
    #     file_dialog = QFileDialog(self)
    #     options = QFileDialog.Option(0)  # PyQt6 Fix
    #     file_name, _ = file_dialog.getSaveFileName(self, "Save as PDF", "", "PDF Files (*.pdf)", options=options)

    #     if file_name:
    #         printer.setOutputFileName(file_name)
    #         painter = QPainter(printer)
    #         rect = painter.viewport()

    #         # 🔹 Fix `size.scale()` for PyQt6
    #         size = self.canvas.sizeHint()
    #         size = size.scaled(rect.size(), Qt.AspectRatioMode.KeepAspectRatio)  # PyQt6 Syntax

    #         # 🔹 Fix `size.toSize()`
    #         painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
    #         painter.setWindow(self.canvas.rect().toRect())  # Convert QRectF → QRect

    #         # 🔹 Render the canvas correctly
    #         self.canvas.render(painter)
    #         painter.end()

    #         print(f"✅ PDF successfully saved: {file_name}")
    # def save_as_image(self):
    #     printer = QPrinter(QPrinter.PrinterMode.HighResolution)
    #     printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
    #     printer.setPageOrientation(QtGui.QPageLayout.Orientation.Landscape)  # ✅ Fixed
    #     printer.setPageSize(QtGui.QPageSize(QtGui.QPageSize.PageSizeId.A4))  # ✅ Fully correct now

    #     # File Dialog for saving PDF
    #     file_dialog = QFileDialog(self)
    #     file_name, _ = file_dialog.getSaveFileName(self, "Save as PDF", "", "PDF Files (*.pdf)")

    #     if file_name:
    #         printer.setOutputFileName(file_name)
    #         painter = QPainter(printer)
    #         rect = painter.viewport()

    #         # ✅ Corrected scaling for PyQt6
    #         size = self.canvas2.sizeHint()
    #         size = size.scaled(rect.size(), Qt.AspectRatioMode.KeepAspectRatio)

    #         scale_factor = 0.8  # Adjust this to control the final size
    #         width = int(rect.width() * scale_factor)
    #         height = int(rect.height() * scale_factor)

    #         painter.setViewport(rect.x(), rect.y(), width, height)
    #         painter.setWindow(self.canvas.rect())  # ✅ No need for `.toRect()` in PyQt6

    #         # ✅ Render the canvas
    #         self.canvas2.render(painter)
    #         painter.end()

    #     print(f"✅ PDF successfully saved: {file_name}")

    def save_as_image(self):
        """
        Save the matplotlib figure canvas2 as a PDF when the Print button is clicked.
        """
        # Open a file save dialog to choose the PDF file location
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save as PDF",
            "",  # Default directory (current directory)
            "PDF files (*.pdf)"  # File filter for PDF
        )

        # Proceed only if the user selects a file path
        if file_path:
            try:
                # Save the figure to the selected file path as a PDF
                self.canvas2.fig.savefig(file_path, format='pdf')
                # Optional: Notify the user of success
                QMessageBox.information(self, "Success", "PDF saved successfully!")
            except Exception as e:
                # Handle potential errors (e.g., permission issues)
                QMessageBox.critical(self, "Error", f"{e}")


    def change_app_color(self):
        self.widget.setStyleSheet("QWidget{\n"
"\n"
"background-color:#444;\n"
"\n"
"\n"
"}\n"
"QPushButton{\n"
"\n"
"border:none;\n"
"color:#fff;\n"
"padding:14px;\n"
"padding-top:30px;\n"
"padding-bottom:30px;\n"
"background:none;\n"
"}\n"
"QPushButton:checked{\n"
"\n"
"\n"
"border-bottom:4px solid #fff;\n"
"\n"
"\n"
"}\n"
"QLabel{\n"
"background:none;\n"
"\n"
"}\n"
"")
        
        self.widget_3.setStyleSheet("QComboBox{\n"
"border:1px solid #ccc;\n"
"padding:4px;\n"
"border-radius: 2px;\n"
"\n"
"\n"
"}\n"
"QComboBox:focus{\n"
"\n"
" border: 1px solid #444;\n"
"            background-color: #fff;\n"
"\n"
"}\n"
"QLineEdit{\n"
"color: #666;\n"
"font-size: 14px;\n"
"padding: 4px;\n"
"border: 1px solid #ccc;\n"
"border-radius: 2px;\n"
"\n"
"}\n"
"QLineEdit:focus {\n"
"            border: 1px solid #444;\n"
"            background-color: #fff;\n"
"        }\n"
"\n"
"QPushButton{\n"
"\n"
"border:none;\n"
"background-color:#444;\n"
"color:#fff;\n"
"border-radius:2px;\n"
"padding:6px;\n"
"\n"
"\n"
"}\n"
"QPushButton:hover{\n"
"background-color:#fff;\n"
"border:1px solid #444;\n"
"color:#444;\n"
"\n"
"\n"
"\n"
"}\n"
"QPushButton:checked{\n"
"background-color:#fff;\n"
"border:1px solid #444;\n"
"color:#444;\n"
"\n"
"}")
        
        self.home_parent_wid.setStyleSheet("background-color: #575757;")
        self.result_widget_btns_2.setStyleSheet("QWidget{\n"
"\n"
"\n"
"background-color:#444;\n"
"\n"
"}\n"
"\n"
"QPushButton{\n"
"border:none;\n"
"padding-right:8px;\n"
"padding-top:6px;\n"
"padding-bottom:6px;\n"
"padding-left:8px;\n"
"border-top-left-radius:6px;\n"
"border-bottom-left-radius:6px;\n"
"color:#fff;\n"
"background-color:none;\n"
"\n"
"}\n"
"\n"
"QPushButton:checked{\n"
"background-color:#575757;\n"
"color:#fff;\n"
"\n"
"\n"
"\n"
"}")
        self.widget_9.setStyleSheet("QSpinBox{\n"
"border:1px solid #444;\n"
"padding:4px;\n"
"border-radius: 2px;\n"
"\n"
"\n"
"}\n"
"QSpinBox:focus{\n"
"\n"
" border: 1px solid #444;\n"
"            background-color: #fff;\n"
"\n"
"}\n"
"\n"
"QWidget{\n"
"border:1px solid #444;\n"
"\n"
"}")
        self.widget_5.setStyleSheet("QWidget{\n"
"\n"
"\n"
"}\n"
"QLabel{\n"
"border:none;\n"
"background-color:#444;\n"
"color:#fff;\n"
"border-radius:2px;\n"
"\n"
"min-width:80px;\n"
"min-height:20px;\n"
"padding:6px;\n"
"\n"
"}\n"
"QComboBox{\n"
"border-radius:0px;\n"
"border:1px solid #444;\n"
"min-height:20px;\n"
"}\n"
"QLineEdit{\n"
"border:1px solid #444;\n"
"min-height:22px;\n"
"\n"
"}")
        self.widget_7.setStyleSheet("QWidget{\n"
"\n"
"background: qlineargradient(spread:repeat, x1:0, y1:0, x2:1, y2:1, \n"
"                    stop:0 #444, stop:1 #575757);\n"
"\n"
"\n"
"\n"
"\n"
"border-radius:4px;\n"
"padding-bottom:6px;\n"
"padding-top:6px;\n"
"\n"
"\n"
"\n"
"}\n"
"\n"
"QLabel{\n"
"background:none;\n"
"color:#fff;\n"
"\n"
"}")

    def set_default_machine_count(self):
        self.spinBox.setValue(1)
        self.spinBox_2.setValue(1)
        self.spinBox_3.setValue(1)
        self.spinBox_4.setValue(1)
        self.spinBox_5.setValue(1)
        self.spinBox_6.setValue(1)
        self.spinBox_7.setValue(1)
        self.spinBox_8.setValue(1)
        self.spinBox_9.setValue(1)
    def save_as_image_lp(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save as PDF",
            "",  # Default directory (current directory)
            "PDF files (*.pdf)"  # File filter for PDF
        )

        # Proceed only if the user selects a file path
        if file_path:
            try:
                # Save the figure to the selected file path as a PDF
                self.canvas.fig.savefig(file_path, format='pdf')
                # Optional: Notify the user of success
                QMessageBox.information(self, "Success", "PDF saved successfully!")
            except Exception as e:
                # Handle potential errors (e.g., permission issues)
                QMessageBox.critical(self, "Error", f"{e}")

    def set_line_edits_to_cells(self):
        self.set_line_edit_to_cell(self.assembly_table,2,1)
        self.set_line_edit_to_cell(self.assembly_table,3,1)
        self.set_line_edit_to_cell(self.assembly_table,0,1)
        self.set_line_edit_to_cell(self.assembly_table,1,1)
        self.set_line_edit_to_cell_2(self.assembly_table,4,1)
        self.set_line_edit_to_cell(self.handling_table,0,1)
        self.set_line_edit_to_cell(self.handling_table,1,1)
        self.set_line_edit_to_cell(self.installation_table,0,1)
        self.set_line_edit_to_cell(self.installation_table,1,1)

    def append_mins(self):
        for line_edit in [self.assembly_table.cellWidget(2,1),self.assembly_table.cellWidget(3,1),self.handling_table.cellWidget(0,1),self.handling_table.cellWidget(1,1),self.installation_table.cellWidget(0,1),self.installation_table.cellWidget(1,1),self.assembly_table.cellWidget(0,1),self.assembly_table.cellWidget(1,1)]:
            text=line_edit.text().strip()
            if text and not text.endswith("mins"):
                line_edit.setText(f"{text} mins")
    def append_hours(self):
        for line_edit in [self.assembly_table.cellWidget(4,1)]:
            text=line_edit.text().strip()
            if text and not text.endswith("hrs"):
                line_edit.setText(f"{text} hrs")


    def add_placeholder_machining_table(self):
        # item = QTableWidgetItem("In mm")
        # item.setForeground(QColor("gray"))
        # self.machining_table.setItem(3,13,item)
        line_edit = QtWidgets.QLineEdit()
        line_edit.setPlaceholderText("In mm")  # Set Placeholder
        self.machining_table.setCellWidget(3, 13, line_edit)

        

    def remove_placeholder(self,row,col):
        item=self.machining_table.item(row,col)
        if item and item.text()=='In mm':
            item.setText("")
            item.setForeground(QColor("black"))
            
    def restore_placeholder(self,row,col):
        if row!=3 and col!=13:
            item=self.machining_table.item(3,13)
            if item and item.text().strip()=="":
                self.add_placeholder_machining_table()
        
        
    # def create_db_pool(self):
    #     db_config={
    #         # "host":"192.168.29.14",
    #         # "user":"local_app_user",
    #         # "password":"schueco&321",
    #         # "database":"fab"
    #         "host":"10.95.136.128",
    #         "user":"fabricationuser",
    #         "password":"schueco&321",
    #         "database":"fabrication"

    #     }
    #     self.db_pool=pooling.MySQLConnectionPool(pool_name="mypool", pool_size=15, **db_config)

    def show_dialog(self):
        items=[self.saved_system_combo.itemText(i) for i in range(self.saved_system_combo.count())]
        dialog=DeleteSystem(items)
        dialog.form_data_submitted.connect(self.remove_system)
        dialog.exec()
    # def get_db_connection(self):
    #     return self.db_pool.get_connection()
    
    def populate_type_combo(self):
        self.type_combo_inp.clear()
        self.type_combo_inp.addItems(["2A","2B","2C","2D","3E"])
        self.type_combo.clear()
        self.type_combo.addItems(["2A","2B","2C","2D","3E"])
    
    def load_saved_type(self):
        # conn=self.get_db_connection()
        db_instance = DatabasePool()  
        conn = db_instance.get_db_connection()
        cursor=conn.cursor()
        try:
            cursor.execute("select type from saved_systems where user_id =%s ",(1,))
            types={typ[0] for typ in cursor.fetchall() if typ[0].strip()}
            existing_types={self.type_combo.itemText(i) for i in range(self.type_combo.count())}
            new_types=types-existing_types
            
            self.type_combo_inp.addItems(new_types)
            self.type_combo.addItems(new_types)
        except mysql.connector.Error as err:
            conn.rollback()
            QMessageBox.warning(self,"Error",f"{err}")

    def update_type_combo(self):
        inp_type=self.type_combo_inp.currentText().strip()
        existing_items={self.type_combo_inp.itemText(i) for i in range(self.type_combo_inp.count())}
        if inp_type not in existing_items:
            self.type_combo_inp.addItem(inp_type)
        if inp_type not in existing_items:
            self.type_combo.addItem(inp_type)

    def remove_type(self):
        # conn=self.get_db_connection()
        db_instance = DatabasePool()  

        conn = db_instance.get_db_connection()
        cursor=conn.cursor()
        try:
            cursor.execute("select type from saved_systems where user_id =%s ",(1,))
            types={typ[0] for typ in cursor.fetchall() if typ[0].strip()}
            existing_types={"2A","2B","2C","2D","3E"}
            new_types=types-existing_types
            print("The new types are ",new_types)
            self.type_combo.clear()
            self.type_combo_inp.clear()
            self.type_combo_inp.addItems(existing_types)
            self.type_combo.addItems(existing_types)
            self.type_combo_inp.addItems(new_types)
            self.type_combo.addItems(new_types)
        except mysql.connector.Error as err:
            conn.rollback()
            QMessageBox.warning(self,"Error",f"{err}")

    def resource_path(self,relative_path):
        if getattr(sys, '_MEIPASS', False):
                base_path = sys._MEIPASS
                # print(f"Running in bundled mode. Base path: {base_path}")
        else:
                current_dir=os.path.dirname(os.path.abspath(__file__))
                # base_path = os.path.abspath(os.path.join(current_dir, "..",".."))
                project_root = os.path.abspath(os.path.join(current_dir, ".."))
                base_path = os.path.join(project_root)
                
                # print(f"Running in source mode. Base pat: {base_path}")
        full_path = os.path.join(base_path, relative_path)
        # print(f"Resolved path for {relative_path}: {full_path}")
        return full_path
    
    def render_corresponding_image_2(self):
        current_text = self.type_combo_inp.currentText().strip()
        image_extensions = [".png", ".jpg", ".jpeg"]
        for ext in image_extensions:
            image_path = self.resource_path(f"assets/icons/{current_text}{ext}")
            if os.path.exists(image_path):  # Check if file exists
                self.label_23.setPixmap(QtGui.QPixmap(image_path))
                return  # Exit after first match
        self.label_23.clear()

    def render_corresponding_image(self):
        current_text = self.type_combo.currentText().strip()
        image_extensions = [".png", ".jpg", ".jpeg"]
        for ext in image_extensions:
            image_path = self.resource_path(f"assets/icons/{current_text}{ext}")
            if os.path.exists(image_path):  # Check if file exists
                self.label_23.setPixmap(QtGui.QPixmap(image_path))
                return  # Exit after first match
        self.label_23.clear()

    def current_type_image(self):
        current_text = self.type_combo.currentText().strip()
        image_extensions = [".png", ".jpg", ".jpeg"]
        for ext in image_extensions:
            image_path = self.resource_path(f"assets/icons/{current_text}{ext}")
            if os.path.exists(image_path):  # Check if file exists
                self.label_23.setPixmap(QtGui.QPixmap(image_path))
                return  # Exit after first match
        self.label_23.clear()
    # def current_type_image(self):
    #     current_text = self.type_combo.currentText().strip()
    #     image_extensions = [".png", ".jpg", ".jpeg"]
    #     for ext in image_extensions:
    #         image_path = self.resource_path(f"assets/icons/{current_text}{ext}")
    #         if os.path.exists(image_path):  # Check if file exists
    #             pixmap=QtGui.QPixmap(image_path)
    #             scaled_pixmap=pixmap.scaled(self.label_23.width(),self.label_23.height(),Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
    #             self.label_23.setPixmap(scaled_pixmap)
    #             return  # Exit after first match
    #     self.label_23.clear()

    def remove_system(self,obj,system):
        # conn=self.get_db_connection()
        db_instance = DatabasePool()  
        conn = db_instance.get_db_connection()
        cursor=conn.cursor()
        try:
            conn.start_transaction()
            cursor.execute("SELECT COUNT(*) FROM saved_systems WHERE system_name = %s", (system,))
            system_exists=cursor.fetchone()[0]
            print("The system is ",system_exists)
            if system_exists==0:
                QMessageBox.warning(self,"Warning","System does not exist.")
                return
            cursor.execute("Delete from saved_systems where system_name=%s",(system,))
            conn.commit()
            index=self.saved_system_combo.findText(system)
            index2=self.system_combo.findText(system)
            index3=self.system_combo_inp.findText(system)

            if index!=-1:
                self.saved_system_combo.removeItem(index)
            
            if index2!=-1:
                self.system_combo.removeItem(index2)

            if index3!=-1:
                self.system_combo_inp.removeItem(index3)
            self.remove_type()
            QMessageBox.information(self,"Success","System has been removed successfully.")
            obj.close()
            # self.load_saved_systems()


        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self,"Error",f"Failed to remove system: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    
    def load_system_data(self,user_id):
        # conn=self.get_db_connection()
        db_instance = DatabasePool()  
        conn = db_instance.get_db_connection()
        cursor=conn.cursor()
        system_name=self.saved_system_combo.currentText()
        cursor.execute("SELECT id,system_name,size,type, machining_time, installation_time, assembly_time, handling_time, total_time FROM saved_systems WHERE user_id=%s AND system_name=%s", 
                   (user_id, system_name))
        system_data=cursor.fetchone()
        if not system_data:
            QMessageBox.warning(self,"Error","System not found")
            return
        system_id=system_data[0]
        self.machining_time_le.setText(system_data[4])
        self.assembly_time_le.setText(system_data[6])
        self.handling_time_le.setText(system_data[7])
        self.installation_time_le.setText(system_data[5])
        self.total_time_le.setText(system_data[8])
        self.size_le_inp.setText(system_data[2])
        self.size_le.setText(system_data[2])
        self.type_combo_inp.setCurrentText(system_data[3])
        self.type_combo.setCurrentText(system_data[3])
        self.system_combo_inp.setCurrentText(system_data[1])
        self.system_combo.setCurrentText(system_data[1])
        #load machining table data
        cursor.execute("SELECT row_num, col1, col2, col3, col4,col5,col6,col7,col8,col9,col10,col11,col12,col13 FROM machining_data WHERE user_id=%s AND system_id=%s", 
               (user_id, system_id))
        for row_data in cursor.fetchall():
            row,col1, col2, col3, col4,col5,col6,col7,col8,col9,col10,col11,col12,col13=row_data
            col_values=[col1, col2, col3, col4,col5,col6,col7,col8,col9,col10,col11,col12,col13]
            for col_offset, value in enumerate(col_values,start=1):
                col=col_offset
                cell_widget=self.machining_table.cellWidget(row,col)
                if cell_widget and isinstance(cell_widget,QComboBox):
                    index=cell_widget.findText(value)
                    if index>=0:
                        cell_widget.setCurrentIndex(index)
                else:
                    if not self.machining_table.item(row,col):
                        self.machining_table.setItem(row,col,QTableWidgetItem())
                    if col==13:
                        line_edit = QtWidgets.QLineEdit()
                        line_edit.setPlaceholderText("In mm")  # Set Placeholder
                        self.machining_table.setCellWidget(row, col, line_edit)
                        self.machining_table.cellWidget(row,col).setText(value)
                    else:
                        self.machining_table.item(row,col).setText(value)

                        

        #load assembly table data
        
        cursor.execute("SELECT row_num, col1 FROM assembly_data WHERE user_id=%s AND system_id=%s", 
               (user_id, system_id))
        for row_data in cursor.fetchall():
            row,col1=row_data
            col_values=[col1]
            for col_offset, value in enumerate(col_values,start=1):
                col=col_offset
                cell_widget=self.assembly_table.cellWidget(row,col)
                if cell_widget and isinstance(cell_widget,QComboBox):
                    index=cell_widget.findText(value)
                    if index>=0:
                        cell_widget.setCurrentIndex(index)
                elif cell_widget and isinstance(cell_widget,QLineEdit):
                    cell_widget.setText(value)
                else:
                    if not self.assembly_table.item(row,col):
                        self.assembly_table.setItem(row,col,QTableWidgetItem())
                    self.assembly_table.item(row,col).setText(value)

        #load handling data
        



        cursor.execute("SELECT row_num, col1 FROM handling_data WHERE user_id=%s AND system_id=%s", 
               (user_id, system_id))
        for row_data in cursor.fetchall():
            row,col1=row_data
            col_values=[col1]
            for col_offset, value in enumerate(col_values,start=1):
                col=col_offset
                cell_widget=self.handling_table.cellWidget(row,col)
                if cell_widget and isinstance(cell_widget,QComboBox):
                    index=cell_widget.findText(value)
                    if index>=0:
                        cell_widget.setCurrentIndex(index)
                elif cell_widget and isinstance(cell_widget,QLineEdit):
                    cell_widget.setText(value)
                else:
                    if not self.handling_table.item(row,col):
                        self.handling_table.setItem(row,col,QTableWidgetItem())
                    self.handling_table.item(row,col).setText(value)
        #load installation data
        



        cursor.execute("SELECT row_num, col1 FROM installation_data WHERE user_id=%s AND system_id=%s", 
               (user_id, system_id))
        for row_data in cursor.fetchall():
            row,col1=row_data
            col_values=[col1]
            for col_offset, value in enumerate(col_values,start=1):
                col=col_offset
                cell_widget=self.installation_table.cellWidget(row,col)
                if cell_widget and isinstance(cell_widget,QComboBox):
                    index=cell_widget.findText(value)
                    if index>=0:
                        cell_widget.setCurrentIndex(index)
                elif cell_widget and isinstance(cell_widget,QLineEdit):
                    cell_widget.setText(value)
                else:
                    if not self.installation_table.item(row,col):
                        self.installation_table.setItem(row,col,QTableWidgetItem())
                    self.installation_table.item(row,col).setText(value)
        


        conn.close()
        self.cal_machining_assemb_handling_install()
        
    def set_line_edit_to_cell(self,table,row,col,val=""):
        line_edit=QLineEdit()
        line_edit.setStyleSheet("QLineEdit{font-size:12px;color:black;}")
        line_edit.setPlaceholderText("mins")
        table.setCellWidget(row,col,line_edit)
        table.cellWidget(row,col).setText(val)
    def set_line_edit_to_cell_2(self,table,row,col,val=""):
        line_edit=QLineEdit()
        line_edit.setStyleSheet("QLineEdit{font-size:12px;color:black;}")
        line_edit.setPlaceholderText("hrs")
        table.setCellWidget(row,col,line_edit)
        table.cellWidget(row,col).setText(val)
        
        

    def load_saved_systems(self):
        # conn=self.get_db_connection()
        db_instance = DatabasePool()  
        conn = db_instance.get_db_connection()
        cursor=conn.cursor()
        try:
            cursor.execute("select system_name from saved_systems where user_id =%s ",(1,))
            systems=[sys[0] for sys in cursor.fetchall()]
            self.saved_system_combo.clear()
            self.saved_system_combo.addItem("--Saved Systems--")
            self.saved_system_combo.setCurrentIndex(0)
            self.saved_system_combo.model().item(0).setEnabled(False)
            self.system_combo.clear()
            self.system_combo.addItems(systems)
            self.system_combo_inp.clear()
            self.system_combo_inp.addItems(systems)


            self.saved_system_combo.addItems(systems)
        except mysql.connector.Error as err:
            conn.rollback()
            QMessageBox.warning(self,"Error",f"{err}")


    def save_system_data(self,user_id):
        flag=False
        # conn=self.get_db_connection()
        db_instance = DatabasePool()  
        conn = db_instance.get_db_connection()
        cursor=conn.cursor()
        try:
            conn.start_transaction()
            system_name=self.system_combo_inp.currentText().strip()
            print("the system name is ",system_name)
            type=self.type_combo_inp.currentText()
            size=self.size_le_inp.text().strip()
            machining_time = self.machining_time_le.text()
            installation_time = self.installation_time_le.text()
            assembly_time = self.assembly_time_le.text()
            handling_time = self.handling_time_le.text()
            total_time = self.total_time_le.text()  
            if not system_name:
                QMessageBox.warning(self,"No System Name","Please enter system name!")  
                return
            cursor.execute("select count(*) from saved_systems where system_name=%s",(system_name,))
            count=cursor.fetchone()[0]


            def update_system(system_name,user_id,type,size,machining_time,installation_time,assembly_time,handling_time,total_time,cursor):
                 # Step 1: Get the existing system_id
                 cursor.execute("SELECT id FROM saved_systems WHERE system_name = %s AND user_id = %s", (system_name, user_id))
                 result = cursor.fetchone()
                 if result:
                     system_id=result[0]#Extract system id
                     #step 2: update the saved system table
                     cursor.execute("""
            UPDATE saved_systems 
            SET type = %s, size = %s, machining_time = %s, installation_time = %s, 
                assembly_time = %s, handling_time = %s, total_time = %s
            WHERE system_name = %s AND user_id = %s
        """, (type, size, machining_time, installation_time, assembly_time, handling_time, total_time, system_name, user_id))
                    #  Step 3: Delete old machining, assembly, handling, and installation data for this system
                     cursor.execute("DELETE FROM machining_data WHERE system_id = %s", (system_id,))
                     cursor.execute("DELETE FROM assembly_data WHERE system_id = %s", (system_id,))
                     cursor.execute("DELETE FROM handling_data WHERE system_id = %s", (system_id,))
                     cursor.execute("DELETE FROM installation_data WHERE system_id = %s", (system_id,))



            if count>0:
                result=QMessageBox.question(self,"System Exists",f"The system '{system_name}' already exists.Do you want to replace it?",QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
                if result==QMessageBox.StandardButton.Yes:

                    update_system(system_name,user_id,type,size,machining_time,installation_time,assembly_time,handling_time,total_time,cursor)
                    flag=True
                    
                else:
                    return
                

                

            
        #     cursor.execute("""
        #     INSERT INTO saved_systems (user_id, system_name,type,size, machining_time, installation_time, assembly_time, handling_time, total_time)
        #     VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)
        # """, (user_id, system_name,type,size, machining_time, installation_time, assembly_time, handling_time, total_time))
            if not flag:
                cursor.execute("""
            INSERT INTO saved_systems (user_id, system_name,type,size, machining_time, installation_time, assembly_time, handling_time, total_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)
        """, (user_id, system_name,type,size, machining_time, installation_time, assembly_time, handling_time, total_time))


            cursor.execute("SELECT id FROM saved_systems WHERE system_name = %s AND user_id = %s", (system_name, user_id))
            res=cursor.fetchone()
            if res:
                system_id=res[0]

            
            #save machining table data
            for row in range(self.machining_table.rowCount()):
                if row==2:
                    continue
                row_data=[]
                for col in range(1,14):
                    item=self.machining_table.item(row,col)
                    cell_widget=self.machining_table.cellWidget(row,col)
                    if cell_widget and isinstance(cell_widget,QComboBox):
                        row_data.append(cell_widget.currentText())
                    elif cell_widget and isinstance(cell_widget,QLineEdit):
                        row_data.append(cell_widget.text())


                    elif item:
                        row_data.append(item.text())
                    else:
                        row_data.append("")
                cursor.execute(
        "INSERT INTO machining_data (user_id, system_id, row_num, col1, col2, col3, col4,col5,col6,col7,col8,col9,col10,col11,col12,col13) VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s,%s,%s)", 
        (user_id, system_id, row, *row_data)
    )
                
            #save assembly table data
            for row in range(self.assembly_table.rowCount()):
                row_data_2=[]
                for col in range(1,2):
                    item=self.assembly_table.item(row,col)
                    cell_widget=self.assembly_table.cellWidget(row,col)
                    if cell_widget and isinstance(cell_widget,QComboBox):
                        row_data_2.append(cell_widget.currentText())
                    elif cell_widget and isinstance(cell_widget,QLineEdit):
                        row_data_2.append(cell_widget.text())
                    elif item:
                        row_data_2.append(item.text())
                    else:
                        row_data_2.append("")
                cursor.execute("INSERT INTO assembly_data (user_id, system_id, row_num, col1) VALUES (%s, %s, %s, %s)", 
        (user_id, system_id, row, *row_data_2))
                #save handling data
            for row in range(self.handling_table.rowCount()):
                row_data_2=[]
                for col in range(1,2):
                    item=self.handling_table.item(row,col)
                    cell_widget=self.handling_table.cellWidget(row,col)
                    if cell_widget and isinstance(cell_widget,QComboBox):
                        row_data_2.append(cell_widget.currentText())
                    elif cell_widget and isinstance(cell_widget,QLineEdit):
                        row_data_2.append(cell_widget.text())
                    elif item:
                        row_data_2.append(item.text())
                    else:
                        row_data_2.append("")
                cursor.execute("INSERT INTO handling_data (user_id, system_id, row_num, col1) VALUES (%s, %s, %s, %s)", 
        (user_id, system_id, row, *row_data_2))
                #save installation data
            for row in range(self.installation_table.rowCount()):
                row_data_2=[]
                for col in range(1,2):
                    item=self.installation_table.item(row,col)
                    cell_widget=self.installation_table.cellWidget(row,col)
                    if cell_widget and isinstance(cell_widget,QComboBox):
                        row_data_2.append(cell_widget.currentText())
                    elif cell_widget and isinstance(cell_widget,QLineEdit):
                        row_data_2.append(cell_widget.text())
                    elif item:
                        row_data_2.append(item.text())
                    else:
                        row_data_2.append("")
                cursor.execute("INSERT INTO installation_data (user_id, system_id, row_num, col1) VALUES (%s, %s, %s, %s)", 
        (user_id, system_id, row, *row_data_2))

            

            conn.commit()
            QMessageBox.information(self,"Success","Data saved successfully!")
            existing_system={self.saved_system_combo.itemText(i) for i in range(self.saved_system_combo.count())}
            if system_name not in existing_system:
                self.saved_system_combo.addItem(system_name)


            self.system_combo.addItem(system_name)
            self.system_combo_inp.addItem(system_name)
            self.update_type_combo()
            self.system_combo.setCurrentText(self.system_combo_inp.currentText())
            self.size_le.setText(self.size_le_inp.text())
            self.type_combo.setCurrentText(self.type_combo_inp.currentText())

            
            print("data saved succesfully")
            print(system_id)

            #save installation data\


        


            


            

        except mysql.connector.Error as err:
            conn.rollback()
            QMessageBox.critical(self,"Failed",f"{err}")
        finally:
            cursor.close()
            conn.close()
    
    # def print_to_pdf(self):
    #     # Capture the entire widget as an image
    #     pixmap = QPixmap(self.size())
    #     self.render(pixmap)

    #     # Open Save Dialog
    #     file_name, _ = QFileDialog.getSaveFileName(self, "Save as PDF", "", "PDF Files (*.pdf)")
    #     if file_name:
    #         printer = QPrinter()
    #         printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
    #         printer.setOutputFileName(file_name)

    #         # Print the image to PDF
    #         painter = QPainter(printer)
    #         painter.drawPixmap(0, 0, pixmap)
    #         painter.end()
    #         print("PDF saved successfully!")

    # def print_to_pdf(self):
    #     # 1. Capture the widget as a QPixmap
    #     pixmap = QPixmap(self.size())
    #     self.render(pixmap)

    #     # 2. Prompt user for PDF file path
    #     file_name, _ = QFileDialog.getSaveFileName(
    #         self,
    #         "Save as PDF",
    #         "",
    #         "PDF Files (*.pdf)"
    #     )
    #     if file_name:
    #         # 3. Configure the printer
    #         printer = QPrinter()
    #         printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
    #         printer.setOutputFileName(file_name)

    #         # A4 size in Landscape
    #         printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
    #         printer.setPageOrientation(QPageLayout.Orientation.Landscape)

    #         # 4. Scale the captured pixmap to fit the printable page
    #         page_rect = printer.pageRect(QPrinter.Unit.Point)
    #         page_size = QSize(int(page_rect.width()), int(page_rect.height()))

    #         scaled_pixmap = pixmap.scaled(
    #             page_rect.size(),
    #             Qt.AspectRatioMode.KeepAspectRatio,
    #             Qt.TransformationMode.SmoothTransformation
    #         )

    #         # 5. Paint the scaled pixmap onto the PDF
    #         painter = QPainter(printer)
    #         painter.drawPixmap(0, 0, scaled_pixmap)
    #         painter.end()

    #         print("PDF saved successfully!")
    # def print_to_pdf(self):
    #     # 1. Capture the widget using grab() which is more reliable
    #     pixmap = self.grab()

    #     # 2. Prompt user for PDF file path
    #     file_name, _ = QFileDialog.getSaveFileName(
    #         self,
    #         "Save as PDF",
    #         "",
    #         "PDF Files (*.pdf)"
    #     )

    #     if not file_name:
    #         return  # User canceled the dialog

    #     # 3. Configure the printer
    #     printer = QPrinter()
    #     printer.setResolution(300)
    #     # printer.setOutputFormat(QPrinter.PdfFormat)
    #     printer.setOutputFileName(file_name)

    #     # Set A4 landscape with proper margins
    #     printer.setPageSize(QPageSize(QPageSize.A4))
    #     printer.setPageOrientation(QPageLayout.Landscape)
    #     printer.setFullPage(True)  # Remove default margins

    #     # 4. Calculate scaling and positioning
    #     painter = QPainter(printer)
    #     page_rect = printer.pageRect(QPrinter.Point)
    #     pixmap_size = pixmap.size()

    #     # Calculate scale factor while maintaining aspect ratio
    #     scale = min(page_rect.width() / pixmap_size.width(),
    #                 page_rect.height() / pixmap_size.height())

    #     scaled_size = pixmap_size * scale
    #     x_offset = (page_rect.width() - scaled_size.width()) / 2
    #     y_offset = (page_rect.height() - scaled_size.height()) / 2

    #     # 5. Draw the pixmap centered on the page
    #     painter.translate(x_offset, y_offset)
    #     painter.scale(scale, scale)
    #     painter.drawPixmap(0, 0, pixmap)
    #     painter.end()

    #     print(f"PDF saved successfully to {file_name}")
    def print_to_pdf(self):
        # 1. Capture the widget using grab() which is more reliable
        pixmap = self.grab()

        # 2. Prompt user for PDF file path
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save as PDF",
            "",
            "PDF Files (*.pdf)"
        )

        if not file_name:
            return  # User canceled the dialog

        # 3. Configure the printer
        printer = QPrinter()
        printer.setResolution(1080)  # Set high resolution (300 DPI)
        printer.setOutputFileName(file_name)  # PDF format is inferred from the file extension

        # Set A4 landscape with proper margins
        # printer.setPageSize(QPageSize(QPageSize.A4))
        printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
        printer.setPageOrientation(QPageLayout.Orientation.Landscape)
        printer.setFullPage(True)  # Remove default margins

        # 4. Calculate scaling and positioning
        painter = QPainter(printer)
        # page_rect = printer.pageRect(QPrinter.Unit.Point)  # Get the page rectangle in points
        paper_rect = printer.paperRect(QPrinter.Unit.Point)  # Get the paper rectangle in points

        pixmap_size = pixmap.size()
        # width_ratio=page_rect.width()/pixmap_size.width()
        # height_ratio=page_rect.height()/pixmap_size.height()
        width_ratio = paper_rect.width() / pixmap_size.width()
        height_ratio = paper_rect.height() / pixmap_size.height()
        scale = min(width_ratio, height_ratio) 
        
        # scale=min(width_ratio,height_ratio)*1.1

        # Calculate scale factor while maintaining aspect ratio
        # scale = min(page_rect.width() / pixmap_size.width(),
        #             page_rect.height() / pixmap_size.height())

        scaled_size = QSize(int(pixmap_size.width() * scale), int(pixmap_size.height() * scale))
        x_offset = (paper_rect.width() - scaled_size.width()) / 2
        y_offset = (paper_rect.height() - scaled_size.height()) / 2

        # 5. Draw the pixmap centered on the page
        painter.translate(x_offset, y_offset)
        painter.scale(scale, scale)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        print(f"PDF saved successfully to {file_name}")

    def print_me(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setResolution(300)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName("Test.pdf")

        painter = QPainter(printer)

        # ✅ Fix: Use QPrinter.Unit.Point for correct scaling
        page_rect = printer.pageRect(QPrinter.Unit.Point)
        paper_rect = printer.paperRect(QPrinter.Unit.Point)

        # Calculate scaling properly
        xscale = page_rect.width() / self.width()
        yscale = page_rect.height() / self.height()
        scale = min(xscale, yscale)

        # ✅ Fix: Use correct centering and scaling
        painter.translate(paper_rect.center().x(), paper_rect.center().y())
        painter.scale(scale, scale)
        painter.translate(-self.width() / 2, -self.height() / 2)

        # Render the widget to the PDF
        self.render(painter)
        painter.end()

        print("PDF saved successfully!")

    
    

    def data_for_calculation(self):
        self.time_data={
            ("cutting","45°","1Hsaw"):120, 
            ("cutting","90°","1Hsaw"):120, 
            ("cutting","45°-90°","1Hsaw"):120, 

            ("cutting","45°","2Hsaw"):60, 
            ("cutting","90°","2Hsaw"):60, 
            ("cutting","45°-90°","2Hsaw"):60, 

            ("6mmx34mm","1wall","CNC"):45,
            ("6mmx34mm","1wall","Router"):115,
            # ("6mmx34mm","1wall","Punch"):5,

            ("6mmx34mm","2wall","CNC"):90,
            ("6mmx34mm","2wall","Router"):175,
            # ("6mmx34mm","2wall","Punch"):10,

            ("8mmx34mm","1wall","CNC"):45,
            ("8mmx34mm","1wall","Router"):115,
            # ("8mmx34mm","1wall","Punch"):5,

            ("8mmx34mm","2wall","CNC"):90,
            ("8mmx34mm","2wall","Router"):175,
            # ("8mmx34mm","2wall","Punch"):10,

            ("10mmx34mm","1wall","CNC"):45,
            ("10mmx34mm","1wall","Router"):115,
            # ("10mmx34mm","1wall","Punch"):5,

            ("10mmx34mm","2wall","CNC"):90,
            ("10mmx34mm","2wall","Router"):175,
            # ("10mmx34mm","2wall","Punch"):10,

            ("12mmx34mm","1wall","CNC"):45,
            ("12mmx34mm","1wall","Router"):115,
            # ("12mmx34mm","1wall","Punch"):5,

            ("12mmx34mm","2wall","CNC"):90,
            ("12mmx34mm","2wall","Router"):175,
            # ("12mmx34mm","2wall","Punch"):10,

            ("6mmx20mm","1wall","CNC"):35,
            ("6mmx20mm","1wall","Router"):70,
            # ("6mmx20mm","1wall","Punch"):5,

            ("6mmx20mm","2wall","CNC"):70,
            ("6mmx20mm","2wall","Router"):140,
            # ("6mmx20mm","2wall","Punch"):10,

            ("8mmx20mm","1wall","CNC"):45,
            ("8mmx20mm","1wall","Router"):115,
            # ("8mmx20mm","1wall","Punch"):5,

            ("8mmx20mm","2wall","CNC"):90,
            ("8mmx20mm","2wall","Router"):175,
            # ("8mmx20mm","2wall","Punch"):10,

            ("8mmx34mm","1wall","CNC"):45,
            ("8mmx34mm","1wall","Router"):115,
            # ("8mmx34mm","1wall","Punch"):5,

            ("8mmx34mm","2wall","CNC"):90,
            ("8mmx34mm","2wall","Router"):175,
            # ("8mmx34mm","2wall","Punch"):10,

            ("cornercleathole","1wall","CNC"):35,
            ("cornercleathole","1wall","DrillingM/C"):30,
            ("cornercleathole","1wall","Punch"):5,
            ("cornercleathole","1wall","Jig"):35,
            ("cornercleathole","2wall","CNC"):70,
            ("cornercleathole","2wall","DrillingM/C"):40,
            ("cornercleathole","2wall","Punch"):10,
            ("cornercleathole","2wall","Jig"):70,
            ("drillinghole","1wall","CNC"):35, #corrected from 15 to 35
            ("drillinghole","1wall","DrillingM/C"):40,
            ("drillinghole","2wall","CNC"):60,
            ("drillinghole","2wall","DrillingM/C"):70,

            ("notching","≤50mm","CNC"):60,
            ("notching","≤100mm","CNC"):70,
            ("notching","≤150mm","CNC"):90,
            ("notching","≤200mm","CNC"):120,
            ("notching","≤250mm","CNC"):180,

            ("notching","≤50mm","NotchingSaw"):60,
            ("notching","≤100mm","NotchingSaw"):60,
            ("notching","≤150mm","NotchingSaw"):120,
            ("notching","≤200mm","NotchingSaw"):120,
            ("notching","≤250mm","NotchingSaw"):150,

            ("notching","≤50mm","Punch"):10,#corrected from 5 to 10
            ("notching","≤100mm","Punch"):10,#corrected from 5 to 10
            ("notching","≤150mm","Punch"):10,#corrected from 5 to 10
            ("notching","≤200mm","Punch"):10,#corrected from 5 to 10
            ("notching","≤250mm","Punch"):10,#corrected from 5 to 10

            ("endmilling","≤50mm","CNC"):35,
            ("endmilling","≤100mm","CNC"):35,
            ("endmilling","≤150mm","CNC"):70,
            ("endmilling","≤200mm","CNC"):70,
            ("endmilling","≤250mm","CNC"):100,

            ("endmilling","≤50mm","EndMill"):1,
            ("endmilling","≤100mm","EndMill"):1,
            ("endmilling","≤150mm","EndMill"):1,
            ("endmilling","≤200mm","EndMill"):1,
            ("endmilling","≤250mm","EndMill"):1,

            ("endmilling","≤50mm","Punch"):10,#corrected from 5 to 10
            ("endmilling","≤100mm","Punch"):10,#corrected from 5 to 10
            ("endmilling","≤150mm","Punch"):10,#corrected from 5 to 10
            ("endmilling","≤200mm","Punch"):10,#corrected from 5 to 10
            ("endmilling","≤250mm","Punch"):10,#corrected from 5 to 10

            ("freehandmilling","⌀6","CNC"):1,
            ("freehandmilling","⌀8","CNC"):1,
            ("freehandmilling","⌀10","CNC"):1,
            ("freehandmilling","⌀12","CNC"):1,
            ("freehandmilling","⌀14","CNC"):1,
            ("freehandmilling","⌀16","CNC"):1,

            ("freehandmilling","⌀6","Router"):5,
            ("freehandmilling","⌀8","Router"):5,
            ("freehandmilling","⌀10","Router"):5,
            ("freehandmilling","⌀12","Router"):5,
            ("freehandmilling","⌀14","Router"):5,
            ("freehandmilling","⌀16","Router"):5,

            # ("freehandmilling","⌀6","Punch"):5,
            # ("freehandmilling","⌀8","Punch"):5,
            # ("freehandmilling","⌀10","Punch"):5,
            # ("freehandmilling","⌀12","Punch"):5,
            # ("freehandmilling","⌀14","Punch"):5,
            # ("freehandmilling","⌀16","Punch"):5,
        }
    def switch_to_dataInputPage(self):
        self.stackedWidget.setCurrentIndex(0)
    
    def switch_to_homePage(self):
        self.stackedWidget.setCurrentIndex(1)

    def switch_to_lineProductionPage(self):
        self.stackedWidget.setCurrentIndex(2)
    
    def read_only_row(self):
        for row in range(self.machining_table.rowCount()):
            for col in range(self.machining_table.columnCount()):
                item=self.machining_table.item(row,col)
                if item:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

        for row in range(self.assembly_table.rowCount()):
            for col in range(self.assembly_table.columnCount()):
                item=self.assembly_table.item(row,col)
                if item:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        for row in range(self.handling_table.rowCount()):
            for col in range(self.handling_table.columnCount()):
                item=self.handling_table.item(row,col)
                if item:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        for row in range(self.installation_table.rowCount()):
            for col in range(self.installation_table.columnCount()):
                item=self.installation_table.item(row,col)
                if item:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        


        
        
    def plot_data(self, machining_type,data=None,labels=None):
        """Plot initial or updated data"""
        
        # self.canvas.axes1.clear()
        # normed_data=squarify.normalize_sizes(data,100,100)
        # squarify.plot(sizes=normed_data,label=labels,ax=self.canvas.axes1,alpha=0.7)
        # self.canvas.axes1.set_title("Line Production")
        # self.canvas.axes1.axis("off")
        self.canvas.fig.clear()
        self.canvas.axes1 = self.canvas.fig.add_subplot(121)
    
        normed_data = squarify.normalize_sizes(data, 100, 100)
    
    # Plot the treemap
        # wrapped_labels = [textwrap.fill(label, width=10) for label in labels]
        # colors=["#cccccc","#7b838a","#7a7d7d","#333333","#a2999e"]

        squarify.plot(sizes=normed_data, label=labels, ax=self.canvas.axes1, alpha=0.7,edgecolor="white", linewidth=2)
        self.canvas.axes1.set_title(f"Line Production {machining_type} (48 Hours)")
        self.canvas.axes1.axis("off")  # Hide axes
        
        self.canvas.draw_idle()
    
    def plot_units_per_shift(self,machining_type):
        y_pos=0.5

        units_per_shift=int((self.min_units/48)*8)
        self.canvas.axes2=self.canvas.fig.add_subplot(122)
        # self.canvas.axes2.set_title(f"{machining_type} units / 8 hours")
        self.canvas.axes2.axis("off")
        self.canvas.axes2.text(0.5,y_pos,units_per_shift,ha='center', va='center',fontsize=80)
        # self.canvas.axes2.set_xlabel(f"{machining_type} units / 8 hours")
        self.canvas.axes2.text(
    0.5, 0.4,  # (x, y) position in axis coordinates
    f" Machining Units / 8 hours",
    ha='center', va='top',
    fontsize=15,
    transform=self.canvas.axes2.transAxes
)

        # self.canvas.axes2.text(0.8,y_pos,"units / 8hrs",ha='right', va='center',fontsize=10)
        self.canvas.draw_idle()
        


    def switch_to_resultsPage(self):
        self.stackedWidget.setCurrentIndex(3)
        
    
    def get_combo(self):
        combo=QtWidgets.QComboBox()
        return combo
    

    def load_b_charts(self):
        if not self.isDataFilled:
            QMessageBox.warning(self,"No data","Please fill the data and try again!")
            return
        self.basic_btn_lp.setChecked(True)
        self.basic_btn_rs.setChecked(True)
        self.basic_btn.setChecked(True)

        machine_lables,time_labels=self.get_time_by_single_machine("basic")
        time_values=[]

        for i in range(len(time_labels)):
            time_one_unit=time_labels[i]
            t=2880/time_one_unit
            time_values.append(int(t))
        print("The time values are ",time_values)
        if len(time_values)>0:
            self.min_units=min(time_values)
        treemap_labels=[]
        for i in range(len(machine_lables)):
            treemap_labels.append(f"{machine_lables[i]}\n{time_values[i]} units")
        
        layout=self.line_production_widget.layout()
        if layout is None:
            layout = QVBoxLayout(self.line_production_widget)
        if not hasattr(self,"canvas"):
            self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
            layout.addWidget(self.canvas)
        self.plot_data("Basic",data=time_values,labels=treemap_labels)
        self.plot_units_per_shift("Basic")
        self.total_machining_time()

        self.plot_units_per_week_treemap()
        self.plot_cost_per_unit("basic")
        self.plot_machine_usage("basic")
        self.plot_time_consumption("basic")
        self.plot_idle_hours("basic")
        self.total_assembly_time()
        


    def plot_idle_hours(self,type):
        units=int(self.unit_le.text())
        assembly_resources=int(self.assmb_res_le.text())
        print("the assembly time is ",self.assemb_time)
        assembly_time_for_one_rsrc=self.assemb_time*2

        # assembly_time=self.assemb_time*units
        assembly_time=(assembly_time_for_one_rsrc/assembly_resources)*units

        try:
            total_time=self.get_total_time()
            a=round((total_time["basic"]/60),2)
            b=round((total_time["basic_cnc"]/60),2)
            c=round((total_time["basic_punch"]/60),2)
            d=round((total_time["basic_punch_cnc"]/60),2)
            total_time_b=self.convert_to_hours_return_float(a)
            total_time_bc=self.convert_to_hours_return_float(b)
            total_time_bp=self.convert_to_hours_return_float(c)
            total_time_bpc=self.convert_to_hours_return_float(d)
            print("The total time is ",total_time_b,total_time_bc,total_time_bp,total_time_bpc)
        except ZeroDivisionError:
            total_time_b=0
            total_time_bc=0
            total_time_bp=0
            total_time_bpc=0
        machine_labels,machine_time=self.get_time_by_single_machine(type)
        time_taken=[]
        idle_time=[]
        for i in range(len(machine_time)):
            consumed_time=machine_time[i]*units
            v=round((consumed_time/60),2)
            tt=self.convert_to_hours_return_float(v)
            time_taken.append(tt)
            t=(2880-consumed_time)/60
            if t<0:
                idle_time.append(0)
            else:
                idle_time.append(t)

        print("The time consumed is ",time_taken)
        
        updated_idle_time=[]
        if type=='basic':
            for i in range(len(time_taken)):
                print("The total time by b ",total_time_b)
                print("The time taken by b single machine ",time_taken[i])
                updt=self.subtract_time(8.0,time_taken[i])
                if updt>=0:
                    updated_idle_time.append(updt)
                else:
                    updated_idle_time.append(0.0)
                # updated_idle_time.append(updt)
        elif type=="basic+cnc":
            for i in range(len(time_taken)):
                print("The total time by bc ",total_time_bc)
                print("The time taken by bc single machine ",time_taken[i])
                updt=self.subtract_time(8.0,time_taken[i])
                if updt>=0:
                    updated_idle_time.append(updt)
                else:
                    updated_idle_time.append(0.0)
                # updated_idle_time.append(updt)
        elif type=="basic+punch":
            for i in range(len(time_taken)):
                print("The total time by bp ",total_time_bp)
                print("The time taken by bp single machine ",time_taken[i])
                updt=self.subtract_time(8.0,time_taken[i])
                if updt>=0:
                    updated_idle_time.append(updt)
                else:
                    updated_idle_time.append(0.0)
                # updated_idle_time.append(updt)
        elif type=="basic+punch+cnc":
            for i in range(len(time_taken)):
                print("The total time by bpc ",total_time_bpc)
                print("The time taken by bpc single machine ",time_taken[i])
                updt=self.subtract_time(8.0,time_taken[i])
                
                if updt>=0:
                    updated_idle_time.append(updt)
                else:
                    updated_idle_time.append(0.0)
                # updated_idle_time.append(updt)

        print("The updated idle timie is ",updated_idle_time)

                
        try:
            max_time_1=max(time_taken)
        except ValueError:
            max_time_1=0
        
        try:
            max_time_2=max(updated_idle_time)
        except ValueError:
            max_time_2=0
        l=machine_labels+["Assembly"]
        print("The machine labels are ",machine_labels)
        indices=np.arange(len(machine_labels))
        layout=self.time_consumption_widget.layout()
        if layout is None:
            layout=QVBoxLayout(self.time_consumption_widget)
            layout.setContentsMargins(60, 0, 0, 0)
        if not hasattr(self,"canvas3"):
            self.canvas3=MplCanvasIdle(self,width=6,height=3,dpi=80)
            layout.addWidget(self.canvas3)
        self.canvas3.fig.clear()
        self.canvas3.axes1=self.canvas3.fig.add_subplot(111)
        self.canvas3.axes1.set_title("Machine idle and consumption hours(8Hrs)",weight='bold')
#         self.canvas3.axes1.set_title(
#     "■ Machine idle  ■ Consumption hours",
#     fontsize=12,
#     color='black'
# )
        # self.canvas3.axes1.plot([], [], 's', color='#b2e580', markersize=10, label="Machine idle")
        # self.canvas3.axes1.plot([], [], 's', color='#65ca00', markersize=10, label="Consumption hours")

# Add colored squares manually
        # self.canvas3.axes1.text(0.5, 1.05, "■", color='red', transform=self.canvas3.axes1.transAxes, ha='center', va='center', fontsize=12)
        # self.canvas3.axes1.text(0.7, 1.05, "■", color='blue', transform=self.canvas3.axes1.transAxes, ha='center', va='center', fontsize=12)


        # self.canvas3.axes1.axis("off")
        # self.canvas3.fig.set_figheight(8)  # Increase height as needed
        self.canvas3.fig.set_figwidth(5)
        bars1=self.canvas3.axes1.barh(indices+0.4,time_taken,height=0.4,color="#65ca00",label="Consumption Hours")
        bars2=self.canvas3.axes1.barh(machine_labels,updated_idle_time,height=0.4,color="#b2e580",label="Machine Idle")
        bars3=self.canvas3.axes1.barh(-1,assembly_time,height=0.4,color="#65ca00")
        self.canvas3.axes1.margins(y=0.1)  # Add some vertical margin
        self.canvas3.axes1.tick_params(axis='y', pad=10)

        # self.canvas3.axes1.legend(loc='lower center', bbox_to_anchor=(0.5, -0.05), ncol=2)

        for i, value in enumerate(time_taken):
            self.canvas3.axes1.text(value+0.02,i+0.4,f'{value}',ha='left')
        for i, value in enumerate(updated_idle_time):
            self.canvas3.axes1.text(value+0.02, i, f'{value}', va='center', ha='left')
        self.canvas3.axes1.text(assembly_time+0.02,-1,f'{assembly_time:.1f}',va='center',ha='left')
        self.canvas3.axes1.spines['top'].set_visible(False) #to remove the lines of the sub plot
        self.canvas3.axes1.spines['right'].set_visible(False)
        self.canvas3.axes1.spines['bottom'].set_visible(False)
        ytick_positions = list(range(len(machine_labels))) + [-1]  # Adding the position for Assembly Time
        ytick_labels = machine_labels + ["Assembly Time"]
        self.canvas3.axes1.set_yticks(ytick_positions)
        self.canvas3.axes1.set_yticklabels(ytick_labels)
        self.canvas3.axes1.legend(loc='lower left',bbox_to_anchor=(0, -0.2))
        self.canvas3.axes1.set_xticks([])
        plt.gcf().subplots_adjust(left=0.2, right=0.8, top=0.9, bottom=0.1)
        self.canvas3.draw_idle()
        self.canvas3.fig.tight_layout()

    # def subtract_time(self,hour_min1,hour_min2):
    #     hours1, mins1 = divmod(hour_min1 * 100, 100)
    #     hours2, mins2 = divmod(hour_min2 * 100, 100)
    #      # Subtract hours and minutes separately
    #     total_hours = hours1 - hours2
    #     total_minutes = mins1 - mins2
    #     if total_minutes < 0:
    #         total_hours -= 1
    #         total_minutes += 60
    #     try:
    #         result=float(f"{int(total_hours)}.{int(total_minutes):02}")
    #     except ValueError:
    #         result=0.0
    #     return result
    # def subtract_time(self, hour_min1, hour_min2):
    #     # Extract hours and minutes correctly
    #     hours1, mins1 = divmod(int(hour_min1 * 100), 100)
    #     hours2, mins2 = divmod(int(hour_min2 * 100), 100)

    #     # Perform subtraction
    #     total_hours = hours1 - hours2
    #     total_minutes = mins1 - mins2

    #     # Adjust negative minutes
    #     if total_minutes < 0:
    #         total_hours -= 1
    #         total_minutes += 60

    #     # Return as proper HH.MM format
    #     return float(f"{total_hours}.{total_minutes:02}")
    def switch_to_recommendation_page(self):
        self.stackedWidget.setCurrentIndex(4)

    def subtract_time(self, hour_min1, hour_min2):
        # Convert HH.MM format to total minutes
        total_minutes1 = int(hour_min1) * 60 + round((hour_min1 % 1) * 100)
        total_minutes2 = int(hour_min2) * 60 + round((hour_min2 % 1) * 100)

        # Subtract time in minutes
        diff_minutes = total_minutes1 - total_minutes2

        # Convert back to HH.MM format
        hours = diff_minutes // 60
        minutes = diff_minutes % 60

        # Return in correct float format
        return float(f"{hours}.{minutes:02d}")
    
    


    def plot_units_per_week_treemap(self):
        total_units=self.get_units_per_week()
        lables=[f"Basic \n{total_units[0]}",f"Basic+CNC \n{total_units[1]}",f"Basic+Punch \n{total_units[2]}",f"Basic+Punch+CNC \n{total_units[3]}"]
        layout=self.results_page_widget.layout()
        if layout is None:
            layout=QVBoxLayout(self.results_page_widget)
        if not hasattr(self,"canvas2"):
            self.canvas2=MplCanvasReports(self,width=5,height=4,dpi=100)
            layout.addWidget(self.canvas2)
        self.canvas2.fig.clear()
        self.canvas2.axes1=self.canvas2.fig.add_subplot(221)
        # self.canvas2.axes1.clear()
        normed_data = squarify.normalize_sizes(total_units, 100, 100)
        # colors=["#cccccc","#7b838a","#7a7d7d","#333333"]
        squarify.plot(sizes=normed_data,label=lables,ax=self.canvas2.axes1,alpha=0.7,edgecolor="white", linewidth=2)
        self.canvas2.axes1.set_title("Units Per Week / 48 hours (6 working days)",fontsize=14)
        self.canvas2.axes1.axis("off")
        self.canvas2.draw_idle()

    def plot_cost_per_unit(self,type):
        outer_f=self.assembly_table.cellWidget(0,1).text().strip().lower().replace(" ","")
        outer_frame_assm=self.string_to_value("min",outer_f)
        vent_f=self.assembly_table.cellWidget(1,1).text().strip().lower().replace(" ","")
        vent_frame_assm=self.string_to_value("min",vent_f)
        fitting_h=self.assembly_table.cellWidget(2,1).text().strip().lower().replace(" ","")
        fitting_hardw=self.string_to_value("min",fitting_h)
        glass_g=self.assembly_table.cellWidget(3,1).text().strip().lower().replace(" ","")
        glass_gazing=self.string_to_value("min",glass_g)
        assembly_time_for_cpu=outer_frame_assm+vent_frame_assm+fitting_hardw+glass_gazing
        material_h=self.handling_table.cellWidget(0,1).text().strip().lower().replace(" ","")
        machine_set=self.handling_table.cellWidget(1,1).text().strip().lower().replace(" ","")
        material_handling=self.string_to_value("min",material_h)
        machine_setup=self.string_to_value("min",machine_set)
        handling_time_for_cpu=material_handling
        cost=float(self.cost_le.text())
        resources=int(self.assmb_res_le.text())+int(self.fab_res_le.text())
        assembly=(assembly_time_for_cpu*2)/int(self.assmb_res_le.text())
        units=int(self.unit_le.text())
        # machining_time_b=round((float(self.b_time_for_cpu)+assembly+handling_time_for_cpu)/60*cost*resources*units,2)
        # machining_time_bc=round((float(self.bc_time_for_cpu)+assembly+handling_time_for_cpu)/60*cost*resources*units,2)
        # machining_time_bp=round((float(self.bp_time_for_cpu)+assembly+handling_time_for_cpu)/60*cost*resources*units,2)
        # machining_time_bpc=round((float(self.bpc_time_for_cpu)+assembly+handling_time_for_cpu)/60*cost*resources*units,2)
        machining_time_b = round(((float(self.b_time_for_cpu) / units + assembly + handling_time_for_cpu) / 60) * cost * resources*units, 2)
        machining_time_bc = round(((float(self.bc_time_for_cpu) / units + assembly + handling_time_for_cpu) / 60) * cost * resources*units, 2)
        machining_time_bp = round(((float(self.bp_time_for_cpu) / units + assembly + handling_time_for_cpu) / 60) * cost * resources*units, 2)
        machining_time_bpc = round(((float(self.bpc_time_for_cpu) / units + assembly + handling_time_for_cpu) / 60) * cost * resources*units, 2)
        machining_time_btt = round(((float(self.b_time_for_cpu) / units + assembly + handling_time_for_cpu) / 60) * cost * 1*1, 2)
        machining_time_bctt = round(((float(self.bc_time_for_cpu) / units + assembly + handling_time_for_cpu) / 60) * cost * 1*1, 2)
        machining_time_bptt = round(((float(self.bp_time_for_cpu) / units + assembly + handling_time_for_cpu) / 60) * cost * 1*1, 2)
        machining_time_bpctt = round(((float(self.bpc_time_for_cpu) / units + assembly + handling_time_for_cpu) / 60) * cost * 1*1, 2)

        print(f"cost per unit is {machining_time_b} {machining_time_bc} {machining_time_bp} {machining_time_bpc}")
        # print(round((float(self.b_time_for_cpu)+assembly_time_for_cpu+handling_time_for_cpu)/60))
        # print(round((float(self.bc_time_for_cpu)+assembly_time_for_cpu+handling_time_for_cpu)/60))
        # print(round((float(self.bp_time_for_cpu)+assembly_time_for_cpu+handling_time_for_cpu)/60))
        # print(round((float(self.bpc_time_for_cpu)+assembly_time_for_cpu+handling_time_for_cpu)/60))


        


        # values_bar1=[209.0,107.4,117.5,86.6]
        values_bar1=[machining_time_b,machining_time_bc,machining_time_bp,machining_time_bpc]
        tooltip_values=[machining_time_btt,machining_time_bctt,machining_time_bptt,machining_time_bpctt]

        expensive_type=max(values_bar1)

        savings_percentage=[]
        for i in range(len(values_bar1)):
            val=round((values_bar1[i]/expensive_type*100),1)
            savings_percentage.append(100-val)
        print("The savings are ",savings_percentage)
        labels_bar1=["Basic","Basic+CNC","Basic+Punch","Basic+Punch+CNC"]
        

        # self.canvas2.axes3.clear()
        self.canvas2.axes3=self.canvas2.fig.add_subplot(223)
        secax=self.canvas2.axes3.secondary_yaxis('right')
        percentages=np.array([100,75,50,25,0])
        tick_positions = np.linspace(0, max(values_bar1), num=len(percentages))
        secax.set_ticks(tick_positions)
        secax.set_yticklabels([f'{p:.1f}%' for p in percentages],fontweight='bold',fontsize=8)
        secax.set_ylabel('Savings (%)')



        self.canvas2.axes3.set_title(f"Man-Hours cost for {units} units",fontsize=14)
        bars1=self.canvas2.axes3.bar(labels_bar1,[expensive_type]*len(values_bar1),width=0.5,color='#b2e580',edgecolor='black',linewidth=0.5)
        bars2=self.canvas2.axes3.bar(labels_bar1,values_bar1,width=0.5,color="#65ca00",edgecolor='black',linewidth=0.5)
        # cursor=Cursor(self.canvas2.axes3,horizOn=True, vertOn=False,linewidth=2,color='black')
        self.canvas2.axes3.spines['top'].set_visible(False)
        # self.canvas2.axes3.tick_params(axis='y',labelweight='bold')
        yticks = self.canvas2.axes3.get_yticks()
        self.canvas2.axes3.set_yticks(yticks)
        self.canvas2.axes3.set_yticklabels([f"{tick:.0f}" for tick in yticks], fontweight='semibold',fontsize=8)
        # xticks=self.canvas2.axes3.get_xticks()
        
        self.canvas2.axes3.set_xticks(range(len(labels_bar1)))
        self.canvas2.axes3.set_xticklabels(labels_bar1,  fontsize=8,fontweight='semibold')

        self.canvas2.axes3.set_ylim(0,max(values_bar1)*1.2)
        self.canvas2.axes3.set_ylabel("Euro")
        for i,(bar1,bar2,cost_value,saving_per) in enumerate(zip(bars2,bars2,values_bar1,savings_percentage)):
            self.canvas2.axes3.text(bar1.get_x()+bar1.get_width()/2,bar1.get_height()*0.5,f'{cost_value:.1f}€',ha='center',va='center',fontsize=8,weight='semibold',color='#fff')
            if saving_per!=0.0:
                self.canvas2.axes3.text(bar2.get_x() + bar2.get_width() / 2, bar2.get_height(), f'{saving_per:.1f}%',
                                   ha='center', va='bottom',fontsize=8,weight='semibold')

        cursor1 = mplcursors.cursor(bars1, hover=True)  # Tooltips for bars1 (background)
        # cursor2 = mplcursors.cursor(bars2, hover=True)  # Tooltips for bars2 (foreground)

        @cursor1.connect("add")
        def on_add_bars1(sel):
            # Get the index of the bar being hovered from bars1
            idx = sel.index
            # Get the label and max cost for the bar
            label = tooltip_values[idx]
            costt = cost
            # Set the tooltip text for bars1
            # sel.annotation.set_text(f'{label}\nMax Cost: {cost:.1f}€')
            sel.annotation.set_text(f'{costt}€ per man-hour cost\n {label}€ per unit cost')

        # @cursor2.connect("add")
        # def on_add_bars2(sel):
        #     # Get the index of the bar being hovered from bars2
        #     idx = sel.index
        #     # Get the label, cost, and savings for the bar
        #     label = labels_bar1[idx]
        #     cost = values_bar1[idx]
        #     saving = savings_percentage[idx]
        #     # Set the tooltip text for bars2
        #     sel.annotation.set_text(f'{label}\nCost: {cost:.1f}€\nSavings: {saving:.1f}%')

        # Draw the canvas to update the plot
        self.canvas2.draw()

    
    def get_machine_time_for_pie(self,type):
        machines=list(self.time_taken_by_machine[type].keys())
        t=list(self.time_taken_by_machine[type].values())
        time=[]
        for i in range(len(t)):
            a=round(t[i]/60,2)
            time.append(a)
        return machines,time
    
    def total_assembly_time(self):
        self.assembly_units_label.setText(f"{self.unit_le.text()} units")
        assembly_resources=int(self.assmb_res_le.text())
        units=int(self.unit_le.text())
        assembly_time_for_one_rsrc=self.assemb_time*2
        assembly_time=round((assembly_time_for_one_rsrc/assembly_resources)*units,1)
        self.assembly_time_label.setText(f":{assembly_time} hours")
    
    def plot_machine_usage(self, type):
        self.canvas2.axes2 = self.canvas2.fig.add_subplot(222)
        machines, time = self.get_machine_time_for_pie(type)
        print("The machines are ",machines)
        print("The time are",time)
        # time[0]=time[0]/2

        # Add these improvements:
        explode = [0.05] * len(time)  # Separate slices slightly
        textprops = {'fontsize': 7, 'fontweight': 'normal', 'color': 'black'}
        # color=["#393d3f","#cccccc","#c6c5b9","#62929e","#546a7b"]
    
        wedges, texts, autotexts = self.canvas2.axes2.pie(
            time,
            labels=None,  # Remove labels to avoid overlap
            autopct=lambda pct: f'{pct:.1f}%' if pct > 5 else '',  # Only show percentages > 5%
            startangle=90,
            wedgeprops={"edgecolor": "black", "linewidth": 0.5},  # Thinner outline
            explode=explode,  # Add slice separation
            pctdistance=0.75,  # Move percentages inward
            textprops=textprops  # Better text styling
          
        )

        # Improve percentage text visibility
        for autotext in autotexts:
            autotext.set_fontsize(6)
            autotext.set_color('black')  # Better contrast
            autotext.set_bbox({
        'facecolor': 'white',  # Background color
        'edgecolor': 'black',  # Border color
        'boxstyle': 'round,pad=0.2',  # Rounded corners and padding
        'alpha': 0.8  # Slightly transparent background
    })

        # Add legend instead of crowded labels
        self.canvas2.axes2.legend(
            wedges,
            machines,
            title="Machines",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1),
            fontsize=7
        )
    
        # Rotate labels to fit better (optional, if you want to keep labels)
        # for text in texts:
        #     text.set_rotation(45)
        #     text.set_fontsize(6)
        if type=="basic":
            self.canvas2.axes2.set_title(f"Basic Machine Usage", fontsize=14, pad=10)
        elif type=="basic+cnc":
            self.canvas2.axes2.set_title(f"Basic+CNC Machine Usage", fontsize=14, pad=10)
        elif type=="basic+punch":
            self.canvas2.axes2.set_title(f"Basic+Punch Machine Usage", fontsize=14, pad=10)
        elif type=="basic+punch+cnc":
            self.canvas2.axes2.set_title(f"Basic+Punch+CNC Machine Usage", fontsize=14, pad=10)






        # self.canvas2.fig.tight_layout()  # Improve spacing
    

    def plot_time_consumption(self,type):
        units=int(self.unit_le.text())
        machine_labels,machine_time=self.get_machine_time_for_pie(type)
        update_time_list=[]
        for i in range(len(machine_time)):
            update_time_list.append(machine_time[i]*units)
        time_taken_by_each_machine=[]
        # time_taken_by_each_machine.append(f"Time Consumption for {units} units")
        for i in range(len(machine_labels)):
            # updated_time=f"{round(update_time_list[i],1)} mins" if update_time_list[i]<=60 else f"{round(update_time_list[i]/60,2)} hours"
            if update_time_list[i]>60:
                tt=round((update_time_list[i]/60),2)
                t=self.convert_to_hours_return_string(tt)
                updated_time=f" {t} hours"
            else:
                updated_time=f"{round(update_time_list[i],1)} mins"
            time_taken_by_each_machine.append(f"{machine_labels[i]}: {updated_time}")
        self.canvas2.axes4=self.canvas2.fig.add_subplot(224)
        header=f"Time consumption for {units} unit"
        # text_content=""
        # text_content=header+"\n"+"-"*(len(header)*2)+"\n\n"
        system_name=self.system_combo.currentText()
        type_name=self.type_combo.currentText()
        size=self.size_le.text()
        
        # text_content=header+"\n"+"-"*(len(header)*2)+f"\n\n System:{system_name}\n\n Type:{type_name}\n"+"-"*(len(header)*2)+"\n\n"
        text_content=header+"\n"+"-"*(len(header)*2)+"\n\n"
        for machine in time_taken_by_each_machine:
            print("The machine is ",machine)
            # text_content+=f"{machine}\n"
            text_content+=f"{machine:<12}\n\n"
        text_content+="-"*(len(header)*2)+f"\n\n                           System  : {system_name}\n\n"+f"                           Type       : {type_name}\n\n"+f"                            Size       :{size}"
        text_obj=self.canvas2.axes4.text(0.3,0.5,text_content.strip(),ha='left',va='center',fontsize=10,color='black',usetex=False)
        self.canvas2.axes4.axis('off')
        # text_obj.set_picker(5)
        # cursor=mplcursors.cursor(self.canvas2.axes4,hover=True)
        # @cursor.connect("add")
        # def on_add(sel):
        # # Customize the tooltip content
        #     print("Hover event triggered")
        #     sel.annotation.set_text("Hovered Text: Machine Usage Details")
        #     sel.annotation.get_bbox_patch().set(fc="white", alpha=0.9)  # Tooltip background
        #     sel.annotation.set_fontsize(9)  
        # self.canvas2.draw()
        
   
        

        

        
    def load_bc_charts(self):
        if not self.isDataFilled:
            QMessageBox.warning(self,"No data","Please fill the data and try again!")
            return
        self.basic_cnc_lp.setChecked(True)
        self.basic_cnc_rs.setChecked(True)
        self.basic_cnc_btn.setChecked(True)
        machine_lables,time_labels=self.get_time_by_single_machine("basic+cnc")
        time_values=[]

        for i in range(len(time_labels)):
            time_one_unit=time_labels[i]
            t=2880/time_one_unit
            time_values.append(int(t))
        # print("The time values are ",time_values)
        if len(time_values)>0:
            self.min_units=min(time_values)
        treemap_labels=[]
        for i in range(len(machine_lables)):
            treemap_labels.append(f"{machine_lables[i]}\n{time_values[i]} units")
        
        layout=self.line_production_widget.layout()
        if layout is None:
            layout = QVBoxLayout(self.line_production_widget)
        if not hasattr(self,"canvas"):
            self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
            layout.addWidget(self.canvas)
        self.plot_data("Basic+CNC",data=time_values,labels=treemap_labels)
        self.plot_units_per_shift("Basic+CNC")
        self.total_machining_time()
        self.plot_units_per_week_treemap()
        self.plot_cost_per_unit("basic+cnc")
        self.plot_machine_usage("basic+cnc")
        self.plot_time_consumption("basic+cnc")
        self.plot_idle_hours("basic+cnc")
        self.total_assembly_time()


    def total_machining_time(self):
        try:
            total_time=self.get_total_time()
            print("The total time issssssssss ",total_time)
            self.b_time_for_cpu=total_time["basic"]
            self.bc_time_for_cpu=total_time["basic_cnc"]
            self.bp_time_for_cpu=total_time["basic_punch"]
            self.bpc_time_for_cpu=total_time["basic_punch_cnc"]

            a=round((total_time["basic"]/60),2)
            b=round((total_time["basic_cnc"]/60),2)
            c=round((total_time["basic_punch"]/60),2)
            d=round((total_time["basic_punch_cnc"]/60),2)
            total_time_b=self.convert_to_hours_return_float(a)
            total_time_bc=self.convert_to_hours_return_float(b)
            total_time_bp=self.convert_to_hours_return_float(c)
            total_time_bpc=self.convert_to_hours_return_float(d)
        except ZeroDivisionError:
            total_time_b=0
            total_time_bc=0
            total_time_bp=0
            total_time_bpc=0
        self.total_units_label.setText(f"{self.unit_le.text()} units")

        self.basic_label_text.setText(f":{total_time_b} hours") 
        self.basic_cnc_label_text.setText(f":{total_time_bc} hours")
        self.basic_punch_label_2.setText(f":{total_time_bp} hours")
        self.basic_punch_cnc_label_2.setText(f":{total_time_bpc} hours")


    def load_bp_charts(self):
        if not self.isDataFilled:
            QMessageBox.warning(self,"No data","Please fill the data and try again!")
            return
        self.basic_punch_lp.setChecked(True)
        self.basic_punch_rs.setChecked(True)
        self.basic_punch_btn.setChecked(True)
        machine_lables,time_labels=self.get_time_by_single_machine("basic+punch")
        time_values=[]

        for i in range(len(time_labels)):
            time_one_unit=time_labels[i]
            t=2880/time_one_unit
            time_values.append(int(t))
        # print("The time values are ",time_values)
        if len(time_values)>0:
            self.min_units=min(time_values)
        treemap_labels=[]
        for i in range(len(machine_lables)):
            treemap_labels.append(f"{machine_lables[i]}\n{time_values[i]} units")
        
        layout=self.line_production_widget.layout()
        if layout is None:
            layout = QVBoxLayout(self.line_production_widget)
        if not hasattr(self,"canvas"):
            self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
            layout.addWidget(self.canvas)
        self.plot_data("Basic+Punch",data=time_values,labels=treemap_labels)
        self.plot_units_per_shift("Basic+Punch")
        self.total_machining_time()
        self.plot_units_per_week_treemap()
        self.plot_cost_per_unit("basic+punch")
        self.plot_machine_usage("basic+punch")
        self.plot_time_consumption("basic+punch")
        self.plot_idle_hours("basic+punch")
        self.total_assembly_time()

    def load_bpc_charts(self):
        if not self.isDataFilled:
            QMessageBox.warning(self,"No data","Please fill the data and try again!")
            return
        self.basic_punch_cnc_lp.setChecked(True)
        self.basic_punch_cnc_rs.setChecked(True)
        self.basic_punch_cnc_btn.setChecked(True)
        machine_lables,time_labels=self.get_time_by_single_machine("basic+punch+cnc")
        time_values=[]

        for i in range(len(time_labels)):
            time_one_unit=time_labels[i]
            t=2880/time_one_unit
            time_values.append(int(t))
        # print("The time values are ",time_values)
        if len(time_values)>0:
            self.min_units=min(time_values)
        treemap_labels=[]
        for i in range(len(machine_lables)):
            treemap_labels.append(f"{machine_lables[i]}\n{time_values[i]} units")
        
        layout=self.line_production_widget.layout()
        if layout is None:
            layout = QVBoxLayout(self.line_production_widget)
        if not hasattr(self,"canvas"):
            self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
            layout.addWidget(self.canvas)
        self.plot_data("Basic+Punch+CNC",data=time_values,labels=treemap_labels)
        self.plot_units_per_shift("Basic+Punch+CNC")
        self.total_machining_time()
        self.plot_units_per_week_treemap()
        self.plot_cost_per_unit("basic+punch+cnc")
        self.plot_machine_usage("basic+punch+cnc")
        self.plot_time_consumption("basic+punch+cnc")
        self.plot_idle_hours("basic+punch+cnc")
        self.total_assembly_time()




    def clear_data(self,machining_table,assembly_table,handling_table,installation_table):
        pyqt_path=os.path.join(os.path.dirname(PyQt6.__file__),"Qt6","plugins")
        print(pyqt_path)
        self.isDataFilled=False
        self.machining_time_le.setText("0")
        self.assembly_time_le.setText("0")
        self.handling_time_le.setText("0")
        self.installation_time_le.setText("0")
        self.total_time_le.setText("0")
        self.curing_time_le.setText("0")
        self.setup_time_le.setText("0")
        for row in range(machining_table.rowCount()):
            for col in range(machining_table.columnCount()):
                cell_widget=machining_table.cellWidget(row,col)
                if isinstance(cell_widget,QComboBox):
                    if cell_widget.count()>0:
                        cell_widget.setCurrentIndex(0)
                if row==machining_table.rowCount()-1 and col>=1:
                    item=machining_table.item(row,col)
                    if item:
                        item.setText("")
        for row in range(assembly_table.rowCount()):
            for col in range(assembly_table.columnCount()):
                cell_widget=assembly_table.cellWidget(row,col)
                if isinstance(cell_widget,QComboBox):
                    if cell_widget.count()>0:
                        cell_widget.setCurrentIndex(0)
                elif isinstance(cell_widget,QLineEdit):
                    cell_widget.setText("")
                if col>=1:
                    item=assembly_table.item(row,col)
                    if item:
                        item.setText("0 minutes")
        for row in range(handling_table.rowCount()):
            for col in range(handling_table.columnCount()):
                cell_widget=handling_table.cellWidget(row,col)
                if isinstance(cell_widget,QComboBox):
                    if cell_widget.count()>0:
                        cell_widget.setCurrentIndex(0)
                elif isinstance(cell_widget,QLineEdit):
                    cell_widget.setText("")
                if col>=1:
                    item=handling_table.item(row,col)
                    if item:
                        item.setText("0 minutes")
        for row in range(installation_table.rowCount()):
            for col in range(installation_table.columnCount()):
                cell_widget=installation_table.cellWidget(row,col)
                if isinstance(cell_widget,QComboBox):
                    if cell_widget.count()>0:
                        cell_widget.setCurrentIndex(0)
                elif isinstance(cell_widget,QLineEdit):
                    cell_widget.setText("")
                if col>=1:
                    item=installation_table.item(row,col)
                    if item:
                        item.setText("0 minutes")
        self.machining_table.cellWidget(3,13).setText("")
    




        
    def set_combo_to_table_cell(self):
        combo=self.get_combo()
        combo.addItems(["45°","90°","45°-90°"])
        self.machining_table.setCellWidget(0,1,combo)
        for i in range(9):
            combo=self.get_combo()
            combo.addItems(["1 wall","2 wall"])
            self.machining_table.setCellWidget(0,i+2,combo)
        combo=self.get_combo()
        combo.addItems(["≤ 50mm","≤ 100mm","≤ 150mm","≤ 200mm","≤ 250mm"])
        self.machining_table.setCellWidget(0,11,combo)
        combo=self.get_combo()
        combo.addItems(["≤ 50mm","≤ 100mm","≤ 150mm","≤ 200mm","≤ 250mm"])
        self.machining_table.setCellWidget(0,12,combo)
        combo=self.get_combo()
        combo.addItems(["⌀6","⌀8","⌀10","⌀12","⌀14","⌀16"])
        self.machining_table.setCellWidget(0,13,combo)
        combo=self.get_combo()
        combo.addItems(["1Hsaw","2Hsaw"])
        self.machining_table.setCellWidget(1,1,combo)
        for i in range(7):
            combo=self.get_combo()
            combo.addItems(["CNC","Router"])
            self.machining_table.setCellWidget(1,i+2,combo)
        combo=self.get_combo()
        combo.addItems(["CNC","DrillingM/C","Punch","Jig"])
        self.machining_table.setCellWidget(1,9,combo)
        combo=self.get_combo()
        combo.addItems(["CNC","DrillingM/C"])
        self.machining_table.setCellWidget(1,10,combo)
        combo=self.get_combo()
        combo.addItems(["CNC","NotchingSaw","Punch"])
        self.machining_table.setCellWidget(1,11,combo)
        combo=self.get_combo()
        combo.addItems(["CNC","EndMill","Punch"])
        self.machining_table.setCellWidget(1,12,combo)
        combo=self.get_combo()
        combo.addItems(["CNC","Router"])
        self.machining_table.setCellWidget(1,13,combo)
        item=self.get_text_item("Profile Cutting")
        self.machining_table.setItem(2, 1, item)
        item=self.get_text_item("Drainage hole /slot on profiles")
        self.machining_table.setItem(2,2,item)
        item=self.get_text_item("Vertical jamb and interlock frames etc...")
        self.machining_table.setItem(2,11,item)
        self.machining_table.setItem(2,12,self.get_text_item("Vertical jamb and interlock frames etc..."))
        self.machining_table.setItem(2,13,self.get_text_item("Retaining catch slot/ L joint 70mm milling vertical vent frames etc..."))
        # combo=self.get_combo()
        # combo.setEditable(True)
        # combo.addItem("mins")
        # combo.setCurrentIndex(0)
        # combo.model().item(0).setEnabled(False)
        # combo.addItems(["10 mins","20 mins","30 mins"])
        # self.assembly_table.setCellWidget(0,1,combo)
        # combo=self.get_combo()
        # combo.setEditable(True)
        # combo.addItem("mins")
        # combo.setCurrentIndex(0)
        # combo.model().item(0).setEnabled(False)
        # combo.addItems(["20 mins","30 mins"])
        # self.assembly_table.setCellWidget(1,1,combo)
        # combo=self.get_combo()
        # combo.setEditable(True)
        # combo.addItem("hrs")
        # combo.setCurrentIndex(0)
        # combo.model().item(0).setEnabled(False)
        # combo.addItems(["1 hour","2 hours","3 hours"])
        # self.assembly_table.setCellWidget(4,1,combo)







        



        



        

    def get_text_item(self,text):
        item=QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        return item

        

    def apply_shadow(self,wid):
        for w in wid:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(2)       # Adjust blur radius (default is 0)
            shadow.setXOffset(1)           # Horizontal offset
            shadow.setYOffset(1)           # Vertical offset
            shadow.setColor(QColor(0, 0, 0, 50))
            w.setGraphicsEffect(shadow)
    def set_section_size_table(self,height):
        self.machining_table.verticalHeader().setDefaultSectionSize(height)
        self.machining_table.setSpan(2,2,1,7)
    def stretch_table_columns(self):
        self.assembly_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.handling_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.installation_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.machining_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.machining_table.verticalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
    def cal_machining_assemb_handling_install(self):
        self.calculate_fabrication_time(0,1,3)
        self.append_mins()
        self.append_hours()
        self.calculate_assembly_time()
        self.calculate_handling_time()
        self.calculate_installation_time()
        self.total_time()
    # code to calculate fabrication time
    def calculate_fabrication_time(self,row0,row1,row3):
        self.isDataFilled=True
        
        # 0,1,2,4
        basic=["NotchingSaw","EndMill","DrillingM/C","2Hsaw","Router"]
        basic_cnc=["2Hsaw","CNC","DrillingM/C","EndMill"]
        basic_punch=["Punch","NotchingSaw","DrillingM/C","2Hsaw","Router","EndMill"]
        basic_punch_cnc=["Punch","NotchingSaw","2Hsaw","CNC","EndMill"]
        self.cal_basic_time(basic,row0,row1,row3)
        self.cal_cnc_time(basic_cnc,row0,row1,row3)
        self.cal_punch_time(basic_punch,row0,row1,row3)
        self.cal_b_p_c_time(basic_punch_cnc,row0,row1,row3)

        time_taken=0
        for i in range(1,self.machining_table.columnCount()):
            d=self.machining_table.item(row3,i)
            if i==13:
                d=self.machining_table.cellWidget(row3,i)
            
            if d is not None and d.text().isdigit():
                no_of_opr=d.text()
                operation=self.machining_table.horizontalHeaderItem(i).text().strip().lower().replace(" ","") # This line extracts operation
                operation_type=self.machining_table.cellWidget(row0,i).currentText().strip().lower().replace(" ","") # This line extracts wall from combo box
                machine=self.machining_table.cellWidget(row1,i).currentText().strip() # This line extracts machine from combo box
                time_for_single_op=self.time_data.get((operation,operation_type,machine))
                time_for_multiple_op=int(time_for_single_op)*int(no_of_opr)
                time_taken+=time_for_multiple_op
                # print("The time taken for multiple operations is ",time_for_multiple_op)
        fab_time=time_taken/60
        # self.convert_to_hours(fab_time)
        self.f=f"{fab_time:.1f}"
        
        if time_taken>60:
            print("Total seconds ",time_taken)
            time_taken=round(time_taken/60,1)
            print("Total minutes ",time_taken)
            self.machining_time_le.setText(f":{time_taken} mins")
        else:
            self.machining_time_le.setText(f":{time_taken} seconds")
        if time_taken>60:
            time_taken=round(time_taken/60,2)
            print("Total hours before conversion ",time_taken)
            total_time=self.convert_to_hours(time_taken)
            print("Total hours after conversion ",total_time)

            self.machining_time_le.setText(f":{total_time} hours")
    

    def cal_basic_time(self,type,row0,row1,row3):
        time_taken=0
        time_taken_by_machine={}
        for i in range(1,self.machining_table.columnCount()):
            # no_of_op=self.machining_table.item(row3,i)
            cell_widget = self.machining_table.cellWidget(row3, i)
            if isinstance(cell_widget,QLineEdit):
                no_of_ops=cell_widget.text().strip()
            else:
                item = self.machining_table.item(row3, i)
                no_of_ops = item.text().strip() if item else ""
            # if no_of_op is not None and no_of_op.text().isdigit():
            if no_of_ops.isdigit():
                # no_of_ops=no_of_op.text()
                operation=self.machining_table.horizontalHeaderItem(i).text().strip().lower().replace(" ","")
                operation_type=self.machining_table.cellWidget(row0,i).currentText().strip().lower().replace(" ","")
                machine_combo=self.machining_table.cellWidget(row1,i)
                if isinstance(machine_combo,QtWidgets.QComboBox):
                        for j in range(machine_combo.count()):
                            item_text=machine_combo.itemText(j).strip()
                            if item_text in type:
                                time_for_single_op=self.time_data.get((operation,operation_type,item_text))
                                time_for_multiple_op=int(time_for_single_op)*int(no_of_ops)
                                time_taken+=time_for_multiple_op
                                if item_text not in time_taken_by_machine:
                                    time_taken_by_machine[item_text]=0
                                time_taken_by_machine[item_text]+=time_for_multiple_op
        self.set_machining_time("basic",time_taken_by_machine)                    
        print("Time taken by basic in secs is ",time_taken," ",time_taken_by_machine)

    def cal_cnc_time(self,type,row0,row1,row3):
        time_taken=0
        time_taken_by_machine={}
        for i in range(1,self.machining_table.columnCount()):
            # no_of_op=self.machining_table.item(row3,i)
            cell_widget = self.machining_table.cellWidget(row3, i)
            if isinstance(cell_widget,QLineEdit):
                no_of_ops=cell_widget.text().strip()
            else:
                item = self.machining_table.item(row3, i)
                no_of_ops = item.text().strip() if item else ""
            # if no_of_op is not None and no_of_op.text().isdigit():
            if no_of_ops.isdigit():

                operation=self.machining_table.horizontalHeaderItem(i).text().strip().lower().replace(" ","")
                operation_type=self.machining_table.cellWidget(row0,i).currentText().strip().lower().replace(" ","")
                machine_combo=self.machining_table.cellWidget(row1,i)
                if isinstance(machine_combo,QtWidgets.QComboBox):
                    if operation=="cornercleathole":
                        item_text="CNC"
                        time_for_single_op=self.time_data.get((operation,operation_type,item_text))
                        time_for_multiple_op=int(time_for_single_op)*int(no_of_ops)
                        time_taken+=time_for_multiple_op
                        if item_text not in time_taken_by_machine:
                                time_taken_by_machine[item_text]=0
                        time_taken_by_machine[item_text]+=time_for_multiple_op
                    elif operation=="endmilling":
                        item_text="EndMill"
                        time_for_single_op=self.time_data.get((operation,operation_type,item_text))
                        time_for_multiple_op=int(time_for_single_op)*int(no_of_ops)
                        time_taken+=time_for_multiple_op
                        if item_text not in time_taken_by_machine:
                                time_taken_by_machine[item_text]=0
                        time_taken_by_machine[item_text]+=time_for_multiple_op
                    
                   
                    else:
                        for i in range(machine_combo.count()):
                            item_text=machine_combo.itemText(i).strip()
                            if item_text in type and item_text!="DrillingM/C" and item_text!="EndMill":
                                time_for_single_op=self.time_data.get((operation,operation_type,item_text))
                                time_for_multiple_op=int(time_for_single_op)*int(no_of_ops)
                                time_taken+=time_for_multiple_op
                                if item_text not in time_taken_by_machine:
                                    time_taken_by_machine[item_text]=0
                                time_taken_by_machine[item_text]+=time_for_multiple_op

        self.set_machining_time("basic+cnc",time_taken_by_machine)


        print("Time taken by basic+cnc in secs is ",time_taken," ",time_taken_by_machine)
        
    def cal_punch_time(self,type,row0,row1,row3):
        time_taken=0
        time_taken_by_machine={}
        def time_for_each_machine(machine):
            if machine not in time_taken_by_machine:
                time_taken_by_machine[machine]=0
            time_taken_by_machine[machine]+=time_for_multiple_op
        
        for i in range(1,self.machining_table.columnCount()):
            # no_of_op=self.machining_table.item(row3,i)
            cell_widget = self.machining_table.cellWidget(row3, i)
            if isinstance(cell_widget,QLineEdit):
                no_of_ops=cell_widget.text().strip()
            else:
                item = self.machining_table.item(row3, i)
                no_of_ops = item.text().strip() if item else ""

            # if no_of_op is not None and no_of_op.text().isdigit():
            if no_of_ops.isdigit():
                # no_of_ops=no_of_op.text()
                operation=self.machining_table.horizontalHeaderItem(i).text().strip().lower().replace(" ","")
                operation_type=self.machining_table.cellWidget(row0,i).currentText().strip().lower().replace(" ","")
                machine_combo=self.machining_table.cellWidget(row1,i)
                if isinstance(machine_combo,QtWidgets.QComboBox):
                    if operation=="notching":
                        item_text="Punch"
                        time_for_single_op=self.time_data.get((operation,operation_type,item_text))
                        time_for_multiple_op=int(time_for_single_op)*int(no_of_ops)
                        time_taken+=time_for_multiple_op
                        time_for_each_machine(item_text)
                    elif operation=="drillinghole":
                        item_text="DrillingM/C"
                        time_for_single_op=self.time_data.get((operation,operation_type,item_text))
                        time_for_multiple_op=int(time_for_single_op)*int(no_of_ops)
                        time_taken+=time_for_multiple_op
                        time_for_each_machine(item_text)
                    elif operation=="freehandmilling":
                        item_text="Router"
                        time_for_single_op=self.time_data.get((operation,operation_type,item_text))
                        time_for_multiple_op=int(time_for_single_op)*int(no_of_ops)
                        time_taken+=time_for_multiple_op
                        time_for_each_machine(item_text)
                    elif operation=="cornercleathole":
                        item_text="Punch"
                        time_for_single_op=self.time_data.get((operation,operation_type,item_text))
                        time_for_multiple_op=int(time_for_single_op)*int(no_of_ops)
                        time_taken+=time_for_multiple_op
                        time_for_each_machine(item_text)
                    elif operation=="endmilling":
                        item_text="EndMill"
                        time_for_single_op=self.time_data.get((operation,operation_type,item_text))
                        time_for_multiple_op=int(time_for_single_op)*int(no_of_ops)
                        time_taken+=time_for_multiple_op
                        time_for_each_machine(item_text)
                    else:
                        for i in range(machine_combo.count()):
                            item_text=machine_combo.itemText(i).strip()
                            if item_text in type:
                                time_for_single_op=self.time_data.get((operation,operation_type,item_text))
                                time_for_multiple_op=int(time_for_single_op)*int(no_of_ops)
                                time_taken+=time_for_multiple_op
                                time_for_each_machine(item_text)
        print("Time taken by basic punch ",time_taken_by_machine)
        self.set_machining_time("basic+punch",time_taken_by_machine)

    def cal_b_p_c_time(self,type,row0,row1,row3):
        time_taken=0
        time_taken_by_machine={}
        def time_for_each_machine(machine):
            if machine not in time_taken_by_machine:
                time_taken_by_machine[machine]=0
            time_taken_by_machine[machine]+=time_for_multiple_op
        for i in range(1,self.machining_table.columnCount()):
            # no_of_op=self.machining_table.item(row3,i)
            cell_widget = self.machining_table.cellWidget(row3, i)
            if isinstance(cell_widget,QLineEdit):
                no_of_ops=cell_widget.text().strip()
            else:
                item = self.machining_table.item(row3, i)
                no_of_ops = item.text().strip() if item else ""
            # if no_of_op is not None and no_of_op.text().isdigit():
            if no_of_ops.isdigit():
                # no_of_ops=no_of_op.text()
                operation=self.machining_table.horizontalHeaderItem(i).text().strip().lower().replace(" ","")
                operation_type=self.machining_table.cellWidget(row0,i).currentText().strip().lower().replace(" ","")
                machine_combo=self.machining_table.cellWidget(row1,i)
                if isinstance(machine_combo,QtWidgets.QComboBox):
                    if operation=="notching":
                        item_text="Punch"
                        time_for_single_op=self.time_data.get((operation,operation_type,item_text))
                        time_for_multiple_op=int(time_for_single_op)*int(no_of_ops)
                        time_taken+=time_for_multiple_op
                        time_for_each_machine(item_text)
                    elif operation=="drillinghole":
                        item_text="CNC"
                        time_for_single_op=self.time_data.get((operation,operation_type,item_text))
                        time_for_multiple_op=int(time_for_single_op)*int(no_of_ops)
                        time_taken+=time_for_multiple_op
                        time_for_each_machine(item_text)
                    elif operation=="cornercleathole":
                        item_text="Punch"
                        time_for_single_op=self.time_data.get((operation,operation_type,item_text))
                        time_for_multiple_op=int(time_for_single_op)*int(no_of_ops)
                        time_taken+=time_for_multiple_op
                        time_for_each_machine(item_text)

                    elif operation=="endmilling":
                        item_text="EndMill"
                        time_for_single_op=self.time_data.get((operation,operation_type,item_text))
                        time_for_multiple_op=int(time_for_single_op)*int(no_of_ops)
                        time_taken+=time_for_multiple_op
                        time_for_each_machine(item_text)
                    elif operation=="freehandmilling":
                        item_text="CNC"
                        time_for_single_op=self.time_data.get((operation,operation_type,item_text))
                        time_for_multiple_op=int(time_for_single_op)*int(no_of_ops)
                        time_taken+=time_for_multiple_op
                        time_for_each_machine(item_text)


                    else:
                        for i in range(machine_combo.count()):
                            item_text=machine_combo.itemText(i).strip()
                            if item_text in type:
                                time_for_single_op=self.time_data.get((operation,operation_type,item_text))
                                time_for_multiple_op=int(time_for_single_op)*int(no_of_ops)
                                time_taken+=time_for_multiple_op
                                time_for_each_machine(item_text)
        self.set_machining_time("basic+punch+cnc",time_taken_by_machine)                        
        print("The time taken by basic+punch+cnc in secs is ",time_taken," ",time_taken_by_machine)



    def set_machining_time(self,type,dic):
        if type not in self.time_taken_by_machine:
            self.time_taken_by_machine[type]={}
        self.time_taken_by_machine[type]=dic

    def get_time_by_single_machine(self,type):
        machine_labels=list(self.time_taken_by_machine[type].keys())
        machine_time=list(self.time_taken_by_machine[type].values())
        time_values=[]
        for i in range(len(machine_time)):
            time=round(machine_time[i]/60,2)
            time_values.append(time)
        print("The machine labels are  ",machine_labels)
        print("The time taken is ",time_values)
        return machine_labels,time_values
    

    def get_total_time(self):
        units=int(self.unit_le.text())
        tt={}

        values=self.time_taken_by_machine["basic"].values()
        total=round((sum(values)*units)/60,2)
        tt["basic"]=total

        values=self.time_taken_by_machine["basic+cnc"].values()
        total=round((sum(values)*units)/60,2)
        tt["basic_cnc"]=total

        values=self.time_taken_by_machine["basic+punch"].values()
        total=round((sum(values)*units)/60,2)
        tt["basic_punch"]=total

        values=self.time_taken_by_machine["basic+punch+cnc"].values()
        total=round((sum(values)*units)/60,2)
        tt["basic_punch_cnc"]=total

        return tt





        


    def calculate_assembly_time(self):
        total_time=0
        outer_f=self.assembly_table.cellWidget(0,1).text().strip().lower().replace(" ","")
        outer_frame_assm=self.string_to_value("min",outer_f)
        vent_f=self.assembly_table.cellWidget(1,1).text().strip().lower().replace(" ","")
        vent_frame_assm=self.string_to_value("min",vent_f)
        fitting_h=self.assembly_table.cellWidget(2,1).text().strip().lower().replace(" ","")
        fitting_hardw=self.string_to_value("min",fitting_h)
        glass_g=self.assembly_table.cellWidget(3,1).text().strip().lower().replace(" ","")
        glass_gazing=self.string_to_value("min",glass_g)
        curing_t=self.assembly_table.cellWidget(4,1).text().strip().lower().replace(" ","")
        curing_time=self.string_to_value("hour",curing_t)*60
        if curing_time>60:
            ct=round((curing_time/60),2)
            curring=self.convert_to_hours(ct)
            self.curing_time_le.setText(f":{curring} hours")
        else:
            self.curing_time_le.setText(f":{curing_time} mins")
        # self.curing_time_le.setText(f"{curing_time}")
        total_time=outer_frame_assm+vent_frame_assm+fitting_hardw+glass_gazing
        self.time_for_unit_cal=total_time
        self.a=f"{total_time:.1f}"
        if total_time>60:
            total_time=round((total_time/60),2)
            self.assemb_time=self.convert_to_hours_return_float(total_time)
            total_time=self.convert_to_hours(total_time)
            self.assembly_time_le.setText(f":{total_time} hours")
        else:
            self.assembly_time_le.setText(f":{total_time} mins")
            t=round((total_time/60),2)
            self.assemb_time=self.convert_to_hours_return_float(t)


    def calculate_installation_time(self):
        outer_f=self.installation_table.cellWidget(0,1).text().strip().lower().replace(" ","")
        vent_f=self.installation_table.cellWidget(1,1).text().strip().lower().replace(" ","")
        outer_frame=self.string_to_value("min",outer_f)
        vent_frame=self.string_to_value("min",vent_f)

        total_time=outer_frame+vent_frame
        tt=total_time
        if total_time>60:
            total_time=round((total_time/60),2)
            total_time=self.convert_to_hours(total_time)
            self.installation_time_le.setText(f":{total_time} hours")
        else:
            self.installation_time_le.setText(f":{total_time} mins")
        self.i=f"{tt}"

    def calculate_handling_time(self):
        material_h=self.handling_table.cellWidget(0,1).text().strip().lower().replace(" ","")
        machine_set=self.handling_table.cellWidget(1,1).text().strip().lower().replace(" ","")
        self.set_up_time_inp=machine_set
        material_handling=self.string_to_value("min",material_h)
        machine_setup=self.string_to_value("min",machine_set)
        total_time=material_handling
        if machine_setup>60:
            st=round((machine_setup/60),2)
            set_u=self.convert_to_hours(st)
            self.setup_time_le.setText(f":{set_u} hours")
        else:
            self.setup_time_le.setText(f":{machine_setup} mins")
        
        self.handling_time=total_time
        self.setup_time=machine_setup
        t=total_time
        if total_time>60:
            total_time=round((total_time/60),2)
            total_time=self.convert_to_hours(total_time)
            self.handling_time_le.setText(f":{total_time} hours")
        else:
            self.handling_time_le.setText(f":{total_time} mins")
        self.h=f"{t}"

    def total_time(self):
        machining_time=float(self.f)
        assembly_time=float(self.a)
        handling_time=float(self.h)
        total_time_mins = machining_time + assembly_time + handling_time 
        if total_time_mins>60:
            t=round(total_time_mins/60,2)
            total_time=self.convert_to_hours(t)
            txt=f":{total_time} hours"
            self.total_time_le.setText(txt)
        else:
            txt=f":{total_time_mins} mins"
            self.total_time_le.setText(txt)

    def get_units_per_week(self):
        assembly_resources=int(self.assmb_res_le.text())
        units_per_week=[]
        try:
            handling_time=self.handling_time
        except AttributeError:
            handling_time=0

        try:
            assembly_time=(self.time_for_unit_cal*2)/assembly_resources
        except AttributeError:
            assembly_time=0
        
        values=self.time_taken_by_machine["basic"].values()
        t=round(sum(values)/60,2)+handling_time+assembly_time
        total=round(t/60,2)
        units_per_week.append(int(48/total))

        values=self.time_taken_by_machine["basic+cnc"].values()
        t=round(sum(values)/60,2)+handling_time+assembly_time
        total=round(t/60,2)
        units_per_week.append(int(48/total))

        values=self.time_taken_by_machine["basic+punch"].values()
        t=round(sum(values)/60,2)+handling_time+assembly_time
        total=round(t/60,2)
        units_per_week.append(int(48/total))

        values=self.time_taken_by_machine["basic+punch+cnc"].values()
        t=round(sum(values)/60,2)+handling_time+assembly_time
        total=round(t/60,2)
        units_per_week.append(int(48/total))
        return units_per_week



        








    def convert_to_hours_return_float(self,val):
        v=float(val)
        # if val>60:
        #     v=round((val/60),2)
        hours=int(v)
        mins=round((v-hours)*60)
        a=f"{hours}.{mins}"
        print("a = ",a)
        return float(a)
    
    def convert_to_hours_return_string(self,val):
        v=float(val)
        # if val>60:
        #     v=round((val/60),2)
        hours=int(v)
        mins=round((v-hours)*60)
        a=f"{hours}.{mins}"
        print("The a is ",a)
        return a
        
    def string_to_value(self,pattern,val):
        try:
            p=self.check_pattern(pattern,val)
            l=len(p)
            value=int(p[:l])
            return value
        except ValueError:
            try:
                value=float(p[:l])
                return value
            except ValueError:
                return 0
            
    def check_pattern(self,pattern,text):
        try:
            # Remove everything except digits and dots.
            t = re.sub(r"[^0-9.]", "", text)
        
            # If there are multiple dots, keep only the first one.
            if t.count('.') > 1:
                first_dot_index = t.find('.')
                t = t[:first_dot_index+1] + t[first_dot_index+1:].replace('.', '')
        
            # If the resulting string is empty, return "0"
            return t if t else "0"
        except Exception as e:
            return "0"
    def convert_to_hours(self,val):
        # self.convert_hours(val)
        v=float(val)
        # if val>60:
        #     v=round((val/60),2)
        hours=int(v)
        mins=round((v-hours)*60)
        return f"{hours}.{mins}"
    def convert_hours(self,val):
        input_hours=float(val)
        hours = int(input_hours)
        fractional_part = input_hours - hours
        # Convert fractional part to minutes (assuming it's in hundredths)
        minutes = round(fractional_part * 100)
        # Calculate total minutes
        total_minutes = hours * 60 + minutes
        # Convert back to hours and minutes
        new_hours = total_minutes // 60
        new_minutes = total_minutes % 60
        fixed_val=round(new_hours + new_minutes / 100, 2)
        print("The converted hours is ",fixed_val)
        return f"{fixed_val}"

        



    

    