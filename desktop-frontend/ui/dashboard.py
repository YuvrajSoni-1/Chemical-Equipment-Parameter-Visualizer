from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QComboBox, QMessageBox, QTabWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from utils.api import upload_dataset, get_history, get_analysis, download_report

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Top Config Bar
        self.top_bar = QHBoxLayout()
        
        self.btn_upload = QPushButton("Upload CSV")
        self.btn_upload.clicked.connect(self.upload_csv)
        self.top_bar.addWidget(self.btn_upload)
        
        self.dataset_selector = QComboBox()
        self.dataset_selector.currentIndexChanged.connect(self.load_analysis)
        self.top_bar.addWidget(self.dataset_selector)
        
        self.btn_refresh = QPushButton("Refresh List")
        self.btn_refresh.clicked.connect(self.load_history)
        self.top_bar.addWidget(self.btn_refresh)

        self.btn_report = QPushButton("Download Report")
        self.btn_report.clicked.connect(self.download_pdf)
        self.top_bar.addWidget(self.btn_report)
        
        self.layout.addLayout(self.top_bar)
        
        # Stats Area
        self.stats_label = QLabel("Select a dataset to view statistics.")
        self.stats_label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 10px;")
        self.layout.addWidget(self.stats_label)

        # Charts Area (Tabs for Bar and Pie)
        self.tabs = QTabWidget()
        self.bar_tab = QWidget()
        self.pie_tab = QWidget()
        
        self.bar_layout = QVBoxLayout()
        self.bar_tab.setLayout(self.bar_layout)
        
        self.pie_layout = QVBoxLayout()
        self.pie_tab.setLayout(self.pie_layout)
        
        self.tabs.addTab(self.bar_tab, "Flow & Pressure")
        self.tabs.addTab(self.pie_tab, "Equipment Type Distribution")
        
        self.layout.addWidget(self.tabs)
        
        # Init Charts
        self.figure_bar = plt.figure()
        self.canvas_bar = FigureCanvas(self.figure_bar)
        self.bar_layout.addWidget(self.canvas_bar)
        
        self.figure_pie = plt.figure()
        self.canvas_pie = FigureCanvas(self.figure_pie)
        self.pie_layout.addWidget(self.canvas_pie)

        self.load_history()

    def upload_csv(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if path:
            res = upload_dataset(path)
            if res.status_code == 201:
                QMessageBox.information(self, "Success", "File Uploaded!")
                self.load_history()
            else:
                QMessageBox.critical(self, "Error", f"Upload Failed: {res.text}")

    def load_history(self):
        self.dataset_selector.blockSignals(True)
        self.dataset_selector.clear()
        data = get_history()
        for item in data:
            self.dataset_selector.addItem(f"{item['filename']} ({item['upload_date']})", item['id'])
        self.dataset_selector.blockSignals(False)
        
        if self.dataset_selector.count() > 0:
            self.load_analysis()

    def load_analysis(self):
        dataset_id = self.dataset_selector.currentData()
        if not dataset_id:
            return
            
        data = get_analysis(dataset_id)
        if not data:
            return
            
        # Update Stats
        stats = data['stats']
        self.stats_label.setText(
            f"Count: {stats['total_count']} | "
            f"Avg Flow: {stats['avg_flowrate']:.2f} | "
            f"Avg Pressure: {stats['avg_pressure']:.2f} | "
            f"Avg Temp: {stats['avg_temperature']:.2f}"
        )
        
        # Update Bar Chart (First 10 items)
        self.figure_bar.clear()
        ax = self.figure_bar.add_subplot(111)
        raw = data['raw_data'][:10]
        names = [x['equipment_name'] for x in raw]
        flows = [x['flowrate'] for x in raw]
        pressures = [x['pressure'] for x in raw]
        
        import numpy as np
        x = np.arange(len(names))
        width = 0.35
        
        ax.bar(x - width/2, flows, width, label='Flowrate')
        ax.bar(x + width/2, pressures, width, label='Pressure')
        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=45, ha='right')
        ax.legend()
        ax.set_title("Flowrate & Pressure (Top 10)")
        self.canvas_bar.draw()
        
        # Update Pie Chart
        self.figure_pie.clear()
        ax_pie = self.figure_pie.add_subplot(111)
        dist = data['type_distribution']
        labels = [x['equipment_type'] for x in dist]
        counts = [x['count'] for x in dist]
        ax_pie.pie(counts, labels=labels, autopct='%1.1f%%')
        ax_pie.set_title("Equipment Type Distribution")
        self.canvas_pie.draw()

    def download_pdf(self):
        dataset_id = self.dataset_selector.currentData()
        if not dataset_id: return
        
        path, _ = QFileDialog.getSaveFileName(self, "Save Report", "report.pdf", "PDF Files (*.pdf)")
        if path:
            if download_report(dataset_id, path):
                QMessageBox.information(self, "Success", "Report Saved!")
            else:
                QMessageBox.critical(self, "Error", "Failed to download report.")
