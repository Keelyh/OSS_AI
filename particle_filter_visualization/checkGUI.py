import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class CheckLocation(QMainWindow):
	"""Check if the location is correct"""
	def __init__(self, pos, parent = None):
		super(CheckLocation, self).__init__(parent)
		self.xlabel = QLabel("x Coordinate:")
		self.ylabel = QLabel("y Coordinate:")
		self.orilabel = QLabel("Orientation:")
		self.CorrectButton = QPushButton("Correct!")
		self.WrongButton = QPushButton("Recaclulate")
		self.connect(self.CorrectButton, SIGNAL("clicked()"), self.correct)
		self.connect(self.WrongButton, SIGNAL("clicked()"), self.wrong)

		self.x_val = QLabel("%s" %pos[0])
		self.y_val = QLabel("%s" %pos[1])
		self.o_val = QLabel("%s" %pos[2])


		self.infoLabel = QWidget()
		infoLabelLayout = QVBoxLayout()
		self.infoLabel.setLayout(infoLabelLayout)
		infoLabelLayout.addWidget(self.xlabel)
		infoLabelLayout.addWidget(self.ylabel)
		infoLabelLayout.addWidget(self.orilabel)

		self.infoval = QWidget()
		infovalLayout = QVBoxLayout()
		self.infoval.setLayout(infovalLayout)
		infovalLayout.addWidget(self.x_val)
		infovalLayout.addWidget(self.y_val)
		infovalLayout.addWidget(self.o_val)

		self.goal01 = QRadioButton("Goal 1")
		self.goal02 = QRadioButton("Goal 2")
		self.goal03 = QRadioButton("Goal 3")
		self.goal04 = QRadioButton("Goal 4")
		self.goal05 = QRadioButton("Goal 5")


		self.GoalOptions = QWidget()
		GoalLayout = QVBoxLayout()
		self.GoalOptions.setLayout(GoalLayout)
		GoalLayout.addWidget(self.goal01)
		GoalLayout.addWidget(self.goal02)
		GoalLayout.addWidget(self.goal03)
		GoalLayout.addWidget(self.goal04)
		GoalLayout.addWidget(self.goal05)

        #fileName = QFileDialog.getOpenFileName(self, "Open File",
         #       QDir.currentPath())
        #image = QImage(fileName)
            
        #self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))
        #self.scaleFactor = 1.0
        
        #hbox = QHBoxLayout(self)
        pixmap = QPixmap("/Testing/Robot_04/Image_05.png")

        lbl = QLabel(self)
        lbl.setPixmap(pixmap)

        hbox.addWidget(lbl)
        lbl.setLayout(hbox)

        imagePath = "/Testing/Robot_04/Image_05.png"
        pic = QImage()
        pic.load(imagePath)
        pix = QPixmap(pic)

        self.lbl = QLabel(self)
        self.lbl.setPixmap(pix)


		self.inoutSplitter = QSplitter(Qt.Vertical)
		self.imageinfoSplitter = QSplitter(Qt.Horizontal)
		self.outSplitter = QSplitter(Qt.Horizontal)
		self.ButtonSplitter = QSplitter(Qt.Horizontal)
		self.mainSplitter = QSplitter(Qt.Vertical)
		self.outSplitter.addWidget(self.infoLabel)
		self.outSplitter.addWidget(self.infoval)
		self.inoutSplitter.addWidget(self.outSplitter)
		self.inoutSplitter.addWidget(self.GoalOptions)
		self.imageinfoSplitter.addWidget(self.inoutSplitter)
		#  self.imageinfoSplitter.addWidget(self.lbl)
		self.ButtonSplitter.addWidget(self.CorrectButton)
		self.ButtonSplitter.addWidget(self.WrongButton)
		self.mainSplitter.addWidget(self.inoutSplitter)
		self.mainSplitter.addWidget(self.ButtonSplitter)

		self.setCentralWidget(self.mainSplitter)

		#self.resize(800, 480)
		self.setWindowTitle("Check Location")
		self.show()       
 

	def correct(self):
		flag = True
		goal = "goal01"
		return flag, goal
		self.close()
	def wrong(self):
		flag = False
		goal = "goal04"
		return flag, goal
		self.close()

def main():
    pos = [35,35,7]
    app = QApplication(sys.argv)
    form = CheckLocation(pos)
    form.show()
    app.exec_()

main()
