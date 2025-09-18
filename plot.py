import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCharts import QChart, QChartView, QSplineSeries
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import QPointF

class MyChartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QSplineSeries Example")
        self.setGeometry(100, 100, 800, 600)

        # Create a QSplineSeries
        series = QSplineSeries()
        series.append(QPointF(0, 6))
        series.append(QPointF(2, 4))
        series.append(QPointF(3, 8))
        series.append(QPointF(7, 4))
        series.append(QPointF(10, 5))

        # Create a QChart
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Simple Spline Chart")
        chart.createDefaultAxes() # Automatically creates and adds axes based on series data

        # Create a QChartView to display the chart
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing) # For smoother rendering

        self.setCentralWidget(chart_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyChartWindow()
    window.show()
    sys.exit(app.exec())