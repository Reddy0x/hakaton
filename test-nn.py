from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 200)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(50, 50, 400, 80))
        self.pushButton.setStyleSheet("background-color:white;\n"
                                      "color: black;\n"
                                      "border-style: outset;\n"
                                      "border-width:2px;\n"
                                      "border-color:black;\n"
                                      "font:bold 30px;\n")
        self.pushButton.setObjectName("pushButton")
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Выберите папку с фото"))
        self.pushButton.clicked.connect(self.pushButton_handler)

    def pushButton_handler(self):
        self.open_dialog_box()

    def open_dialog_box(self):
        import cv2
        import numpy as np
        import os
        filename = QFileDialog.getExistingDirectory()
        track = filename

        def vectors(x, y, x1, y1):
            return ((x - x1) ** 2 + (y - y1) ** 2) ** 0.5

        color_yellow = (0, 255, 255)

        region = "chunskiy";
        part = "part4"
        img = cv2.imread(str(track) + "/before.jpg", 1)  # читаем изображение до
        img2 = cv2.imread(str(track) + "/after.jpg", 1)  # читаем изображение после

        cv2.imshow("1", img)  # выводим первое изображение
        cv2.imwrite(str(track) + "/new.jpg", img2)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # переводом первое изображение в оттенки серого
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)  # переводом второе изображение в оттенки серого
        ret, thresh = cv2.threshold(gray, 85, 255,
                                    cv2.THRESH_BINARY)  # переводим первое изображение в бинарный код  (0 до 90 - черный; 90 до 255 - белый)
        ret2, thresh2 = cv2.threshold(gray2, 85, 255,
                                      cv2.THRESH_BINARY)  # переводим второе изображение в бинарный код  (0 до 90 - черный; 90 до 255 - белый)

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)  # находим все конторы в первом изображение, составляем иерархию по их параметрам
        contours2, hierarchy2 = cv2.findContours(thresh2, cv2.RETR_EXTERNAL,
                                                 cv2.CHAIN_APPROX_SIMPLE)  # находим все конторы в изображение, составляем иерархию по их параметрам

        for cnt in contours:

            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            area = int(rect[1][0] * rect[1][1])
            if (area > 70) and (area < 1500000) and rect[1][0] < 10000 and rect[1][1] < 10000 and rect[1][0] > 0 and \
                    rect[1][1] > 0:
                cv2.drawContours(img, [box], 0, (0, 255, 0), 2)
                cv2.drawContours(img2, [box], 0, (10, 10, 10), -1)

        img3 = cv2.imread(str(track) + "/new.jpg", 1)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        ret2, thresh2 = cv2.threshold(gray2, 90, 255, cv2.THRESH_BINARY)
        contours2, hierarchy2 = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt2 in contours2:  # перебирает все контуры по очереди

            rect2 = cv2.minAreaRect(cnt2)  # создаем переменную для работы с площадью контура
            box2 = cv2.boxPoints(rect2)  # записываем координаты опорных точек
            box2 = np.int0(box2)  # преобразуем координаты опорных точек в формат Int
            area2 = int(rect2[1][0] * rect2[1][1])  # устанавливаем фактическую площадь контура
            x, y, w, h = cv2.boundingRect(cnt2)  # устанавливаем переменные для рассчета отношения
            aspect_ratio = float(w) / h  # создаем переменную для отношения и рассчитываем его
            if (area2 > 75) and (area2 < 1500000) and rect2[1][0] < 10000 and rect2[1][1] < 10000 and rect2[1][
                0] > 0 and \
                    rect2[1][1] > 0:

                if vectors(box2[0][0], box2[0][1], box2[1][0], box2[1][1]) >= vectors(box2[1][0], box2[1][1],
                                                                                      box2[2][0], box2[2][1]):
                    if vectors(box2[0][0], box2[0][1], box2[1][0], box2[1][1]) / vectors(box2[1][0], box2[1][1],
                                                                                         box2[2][0], box2[2][1]) <= 6.3:
                        cv2.line(img3, (box2[0][0], box2[0][1]), (box2[1][0], box2[1][1]), (0, 255, 0), 1)
                        cv2.line(img3, (box2[1][0], box2[1][1]), (box2[2][0], box2[2][1]), (0, 255, 0), 1)
                        if area2 > 1000:
                            cv2.drawContours(img3, [box2], 0, (0, 0, 255), 1)
                        elif area2 > 500 and area2 <= 1000:
                            cv2.drawContours(img3, [box2], 0, (0, 100, 255), 1)
                        else:
                            cv2.drawContours(img3, [box2], 0, (0, 200, 255), 1)


                else:
                    if vectors(box2[1][0], box2[1][1], box2[2][0], box2[2][1]) / vectors(box2[0][0], box2[0][1],
                                                                                         box2[1][0], box2[1][1]) <= 6.3:
                        cv2.line(img3, (box2[0][0], box2[0][1]), (box2[1][0], box2[1][1]), (0, 255, 0), 1)
                        cv2.line(img3, (box2[1][0], box2[1][1]), (box2[2][0], box2[2][1]), (0, 255, 0), 1)

                        if area2 > 1000:
                            cv2.drawContours(img3, [box2], 0, (0, 0, 255), 1)
                        elif area2 > 500 and area2 <= 1000:
                            cv2.drawContours(img3, [box2], 0, (0, 100, 255), 1)
                        else:
                            cv2.drawContours(img3, [box2], 0, (0, 200, 255), 1)

        cv2.imshow("new", img3)
        k = cv2.waitKey(0)  # создаем переменную для выхода
        if k == 27:  # вывод через ESCAPE
            cv2.destroyAllWindows()  # закрытие окон
        file_path = (str(track) + "/new.jpg")
        os.remove(file_path)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
