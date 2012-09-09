# -*- coding: utf8 -*-

import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class list_item:
    def __init__(self):
        pass
        
    def process_item(self, data):
        post_data = QLabel()
        
        if data["in_reply_to_screen_name"]:
            nickname = data["nickname"] + " " + u"\u2794" + " " + data["in_reply_to_screen_name"]
        else:
            nickname = data["nickname"]
        
        post_data.setText(QString.fromUtf8("<b>{0}</b> <span style='font-size:8pt;'>{2}</span><p style='padding:0;'>{1}</p>".format(nickname, data["text"], data["date"])))
        post_data.setWordWrap(True)
        post_data.setAlignment(Qt.AlignTop)
        post_data.setOpenExternalLinks(True)
        post_height = post_data.sizeHint().height()
        #print post_data.width(), post_height
        post_data.setMinimumWidth(300)
        post_data.setMaximumWidth(6000)
        post_data.setMaximumHeight(post_height)
        post_data.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        post_data_layout = QVBoxLayout()
        post_data_layout.addWidget(post_data)
        post_data_layout.setContentsMargins(3, 0, 0, 0)
        post_data_layout.setAlignment(Qt.AlignTop)
        
        # Poster avatar and post actions
        avatar_data = QLabel()
        extension = data["avatar"].split(".")[-1:][0]
        avatar = os.path.expanduser("~/.local/share/qtdenter/avatars/") + "%s.%s" % (data["nickname"], extension)
        avatar_data.setText("<img src='{0}' height=48 width=48 />".format(avatar))
        avatar_data.setMinimumSize(0, 0)
        avatar_data.setMaximumSize(48, 48)
        avatar_data.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.MinimumExpanding)
        
        like_button = QPushButton()
        if data["in_favorites"]:
            like_button.setText("X")
            like_button.setToolTip("De-Favoritize")
        else:
            like_button.setText(u"\u2665")
            like_button.setToolTip("Favoritize")
        #like_button.setFlat(True)
        like_button.setFixedSize(32, 32)
        like_button.setObjectName("like_button_" + str(data["id"]))
        
        redent_button = QPushButton()
        redent_button.setText(u"\u267a")
        #redent_button.setFlat(True)
        redent_button.setFixedSize(32, 32)
        redent_button.setObjectName("redent_button_" + str(data["id"]))
        
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(like_button)
        buttons_layout.addWidget(redent_button)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        
        buttons_widget = QWidget()
        buttons_widget.setLayout(buttons_layout)
        
        post_avatar_layout = QVBoxLayout()
        post_avatar_layout.addWidget(avatar_data)
        
        post_avatar_widget = QWidget()
        post_avatar_widget.setLayout(post_avatar_layout)
        
        post_data_widget = QWidget()
        post_data_widget.setLayout(post_data_layout)
        
        # Some underpost buttons
        dentid_button = QPushButton()
        dentid_button.setText("#" + str(data["id"]))
        dentid_button.setObjectName("dentid_button_" + str(data["id"]))
        dentid_button.setFixedHeight(20)
        dentid_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        source = QLabel()
        source.setText("<span style='font-size:8pt;'>from {0}".format(data["source"]))
        source.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.MinimumExpanding)
        source.setWordWrap(True)
        
        post_info_layout = QVBoxLayout()
        post_info_layout.addWidget(dentid_button)
        post_info_layout.addWidget(source)
        post_info_layout.addWidget(buttons_widget)
        post_info_layout.setAlignment(Qt.AlignRight)
        
        post_info_widget = QWidget()
        post_info_widget.setLayout(post_info_layout)
        post_info_widget.setFixedWidth(100)

        # Final post widget
        post_layout = QHBoxLayout()
        post_layout.addWidget(post_data_widget)
        post_layout.addWidget(post_info_widget)
        
        post_widget = QWidget()
        post_widget.setLayout(post_layout)
        
        item = QTreeWidgetItem()
        
        item.setText(2, str(data["id"]) + ":" + data["nickname"])
        if data["in_favorites"]:
            item.setText(3, "favorited")
        else:
            item.setText(3, "not")
            
        item.setText(4, data["text"])
        
        return (item, post_avatar_widget, post_widget)

##########################################################################
# Overriding QTreeWidgetItem in servers list for human numbers sorting
##########################################################################

class item(QStyledItemDelegate):
    """
    This class is used for item overriding, for human-style numbers sorting
    and HTMLs
    """
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
