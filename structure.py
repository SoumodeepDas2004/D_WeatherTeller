from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QPushButton,QLineEdit,QComboBox,QDateEdit,QTextEdit,QTableWidget,QVBoxLayout,QHBoxLayout,QMessageBox,QTableWidgetItem,QDialog
from PyQt5.QtSql import QSqlDatabase,QSqlQuery
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate,Qt
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets,QtGui
import requests,sys
import pandas as pd
import numpy as np
from weather import findweather
class weatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.heading=QLabel("Weather Forcast App")
        
        self.locationfield=QLineEdit()
        self.locationfield.setPlaceholderText("Put Location Name for live Weather data")
        self.searchbtn=QPushButton("SHOW WEATHER")
        
        self.dataoutputfield=QTextEdit()
        
        
        self.plotbtn=QPushButton("Plot")
        #connectivity
        
        self.searchbtn.clicked.connect(self.getdata)
        
        self.plotbtn.clicked.connect(self.plotdata)
        
        
        #color 
        self.heading.setStyleSheet("color: yellow; font-weight:bold;")
        
        
        #self.plotbtn.setAlignment(Qt.AlignCenter)
        self.heading.setAlignment(Qt.AlignCenter)
        
        self.mLayout=QVBoxLayout()
        self.r1=QHBoxLayout()
        self.r2=QHBoxLayout()
        self.r3=QHBoxLayout()
        self.r4=QHBoxLayout()
        
        self.r1.addWidget(self.heading)
        
        self.r2.addWidget(self.locationfield)
        self.r2.addWidget(self.searchbtn)
        
        self.r3.addWidget(self.dataoutputfield)
        
        self.r4.addWidget(self.plotbtn)
        
        self.mLayout.addLayout(self.r1)
        self.mLayout.addLayout(self.r2)
        self.mLayout.addLayout(self.r3)
        self.mLayout.addLayout(self.r4)
        self.setLayout(self.mLayout)
    
    def getdata(self):
        self.location=self.locationfield.text()
        self.weather=findweather(self.location)
        self.dataoutputfield.setText(str(self.weather.T))
        
        return self.weather
    
    def plotdata(self):
        self.weather = self.getdata()
        if self.weather.empty:
            print("No data to plot.")
            return

        desired_keys = {"tempmax", "tempmin", "humidity", "pressure", "visibility"}
        plotdata = [key for key in desired_keys if key in ["tempmax", "tempmin"]]

        df = self.weather

        # Bar plot for tempmax and tempmin
        if plotdata:  # Check if there are temp values to plot
            x = np.arange(1)  # the label locations
            width = 0.35  # the width of the bars

            fig, ax = plt.subplots()
            rects1 = ax.bar(x - width/2, df["tempmax"][0], width, label="Temp Max")
            rects2 = ax.bar(x + width/2, df["tempmin"][0], width, label="Temp Min")

            # Add some text for labels, title and custom x-axis tick labels, etc.
            ax.set_ylabel('Temperature (°C)')
            ax.set_title(f'Temp Max & Min for {self.location}')
            ax.set_xticks(x)
            ax.set_xticklabels([self.location])  # Set location as x-axis label
            ax.legend()

            def autolabel(rects):
                """Attach a text label above each bar in *rects*, displaying its height."""
                for rect in rects:
                    height = rect.get_height()
                    ax.annotate('{}'.format(height),
                                xy=(rect.get_x() + rect.get_width() / 2, height),
                                xytext=(0, 3),  # 3 points vertical offset
                                textcoords="offset points",
                                ha='center', va='bottom')

            autolabel(rects1)
            autolabel(rects2)

            fig.tight_layout()

        # Rest of the code for plotting other parameters (remains unchanged)
        other_keys = [key for key in desired_keys if key not in ["tempmax", "tempmin"]]

        if other_keys:
            num_plots = len(other_keys)
            fig, axes = plt.subplots(2, (num_plots + 1) // 2, figsize=(10, 8))
            axes = axes.flatten()

            for i, key in enumerate(other_keys):
                axes[i].bar(self.location, df[key][0], label=key)
                axes[i].set_title(key.capitalize())
                axes[i].set_ylabel("Value")

            # Remove extra subplots
            if num_plots < len(axes):
                for j in range(num_plots, len(axes)):
                    fig.delaxes(axes[j])
            fig.suptitle(f'Humidity,Pressure,Visibility for {self.location}')
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show()
        
        
        
        
    

if __name__ == "__main__":
    
    app=QApplication(sys.argv)
    widget=QtWidgets.QStackedWidget()
    Ewindow = weatherApp()
    Ewindow.resize(674,400)
    Ewindow.setWindowTitle("Weather Tracker")
    #Ewindow.setWindowIcon(QIcon("expens.png"))
    
    widget.addWidget(Ewindow)
    
    widget.resize(674,400)
    widget.setWindowTitle("Weather Tracker")
    #widget.setWindowIcon(QIcon("expens.png"))
    
    widget.setStyleSheet("""
    QStackedWidget
    {
        background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(138, 0, 108, 1), stop:1 rgba(0, 48, 255, 0.96));
        color: black;
        font: 20px;
        font-style: italic;
    }
    """)
    widget.show()
    app.exec_()
        
        