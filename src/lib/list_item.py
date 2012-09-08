# -*- coding: utf8 -*-

import os
from PyQt4.QtCore import QSize
from PyQt4.QtGui import QTreeWidgetItem, QStyledItemDelegate, QStyleOptionViewItemV4, QTextDocument, QStyle, QAbstractTextDocumentLayout

##########################################################################
# Overriding QTreeWidgetItem in servers list for human numbers sorting
##########################################################################

class item(QStyledItemDelegate):
    def __init__(self, parent=None):
        QTreeWidgetItem.__init__(self, parent)
     
    def __lt__(self, otherItem):
        column = self.treeWidget().sortColumn()
        
        print otherItem
     
        return self.text(column) < otherItem.text(column)
            
    def paint(self, painter, option, index):
        options = QStyleOptionViewItemV4(option)
        self.initStyleOption(options,index)

        style = QApplication.style() if options.widget is None else options.widget.style()

        doc = QTextDocument()
        doc.setHtml(options.text)

        options.text = ""
        style.drawControl(QStyle.CE_ItemViewItem, options, painter);

        ctx = QAbstractTextDocumentLayout.PaintContext()

        textRect = style.subElementRect(QStyle.SE_ItemViewItemText, options)
        painter.save()
        painter.translate(textRect.topLeft())
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        doc.documentLayout().draw(painter, ctx)

        painter.restore()

    def sizeHint(self, option, index):
        options = QStyleOptionViewItemV4(option)
        self.initStyleOption(options,index)

        doc = QTextDocument()
        doc.setHtml(options.text)
        doc.setTextWidth(options.rect.width())
        return QSize(doc.idealWidth(), doc.size().height())
