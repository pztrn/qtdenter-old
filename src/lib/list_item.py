# -*- coding: utf8 -*-

import os
from PyQt4.QtCore import QString, QSize, Qt, QRect
from PyQt4.QtGui import QTreeWidgetItem, QPushButton, QLabel, QSizePolicy, QVBoxLayout, QHBoxLayout, QWidget, QSpacerItem, QStyledItemDelegate

class list_item:
    """
    List Item class. Forming QTreeWidgetItem items, some QWidgets and sending
    it back to main thread.
    
    Item Structure:
    
    =======================================================================================================
    | Avatar       | Nickname (with arror and  | Buttons: redent, | Dent ID,  | Favoritized   | server   |
    | (QLabel)     | nickname a person to whom | context,         | nickname, | state, redent | name,     |
    | (optionally  | replying), dent text.     | source.          | conv id,  | state         | dent type |
    | dent destroy |                           |                  | read state| (hidden)      | (hidden)  |
    | btn)         |                           |                  | (hidden)  |               |           |
    =======================================================================================================
    """
    def __init__(self):
        pass
        
    def process_item(self, data, last_dent_id, username, server, dent_type):
        if data["in_reply_to_screen_name"]:
            nickname = data["nickname"] + " " + u"\u2794" + " " + data["in_reply_to_screen_name"]
            if data["in_reply_to_screen_name"] == username:
                dent_type = "mentions"

            context_button = QPushButton()
            context_button.setFixedHeight(20)
            context_button.setText("Context")
            context_button.setObjectName("context_button_" + str(data["conversation_id"]))
            context_button.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
            context_button.hide()

        else:
            nickname = data["nickname"]
            
        read_state = "not"
        if int(data["id"]) < int(last_dent_id) or int(data["id"]) == int(last_dent_id):
            read_state = "read"
            
        post_data_info = QLabel()
        
        post_data = QLabel()
        post_data.setText(QString.fromUtf8("<b>{0}</b> <span style='font-size:8pt;'>{2}</span><p style='padding:0;'>{1}</p>".format(nickname, data["text"], data["date"])))
        post_data.setWordWrap(True)
        post_data.setAlignment(Qt.AlignTop)
        post_data.setOpenExternalLinks(True)
        post_height = post_data.sizeHint().height()
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
        
        #reply_button = QPushButton()
        #reply_button.setText("Reply")
        
        destroy_button = QPushButton()
        destroy_button.setText("Delete")
        destroy_button.setFixedHeight(20)
        #destroy_button.setFlat(True)
        destroy_button.setObjectName("destroy_button_" + str(data["id"]))
        destroy_button.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        
        spacer = QSpacerItem(0, 1, QSizePolicy.Fixed, QSizePolicy.Expanding)
        
        post_avatar_layout = QVBoxLayout()
        post_avatar_layout.addWidget(avatar_data)
        #post_avatar_layout.addWidget(reply_button)
        post_avatar_layout.addWidget(destroy_button)
        post_avatar_layout.addItem(spacer)
        
        post_avatar_widget = QWidget()
        post_avatar_widget.setLayout(post_avatar_layout)
        
        # Like button
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
        
        spacer2 = QSpacerItem(0, 1, QSizePolicy.Fixed, QSizePolicy.Expanding)
        
        post_info_layout = QVBoxLayout()
        post_info_layout.addWidget(dentid_button)
        post_info_layout.addWidget(source)
        post_info_layout.addWidget(buttons_widget)
        if data["in_reply_to_screen_name"]:
            post_info_layout.addWidget(context_button)
        post_info_layout.addItem(spacer2)
        post_info_layout.setAlignment(Qt.AlignTop)
        post_info_layout.setContentsMargins(9, 0, 9, 0)
        
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
        
        item.setText(2, str(data["id"]) + ":" + data["nickname"] + ":" + str(data["conversation_id"]) + ":" + read_state)
        if data["in_favorites"]:
            item.setText(3, "favorited")
        else:
            item.setText(3, "not")
            
        item.setText(4, data["text"])
        item.setText(5, server + ":" + dent_type)
        
        return (item, post_avatar_widget, post_widget)
