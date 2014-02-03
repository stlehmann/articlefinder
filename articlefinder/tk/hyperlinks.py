__author__ = 'stefanlehmann'

from tkinter import *
import webbrowser


class HyperlinkManager:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.text_widget.tag_config("hyper", foreground="blue", underline=1)
        self.text_widget.tag_bind("hyper", "<Enter>", self._enter)
        self.text_widget.tag_bind("hyper", "<Leave>", self._leave)
        self.text_widget.tag_bind("hyper", "<Button-1>", self._click)
        self.links = {}

    def reset(self):
        self.links = {}

    def add(self, url):
        # add an url to the manager.  returns tags to use in
        # associated text_widget widget
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = url
        return "hyper", tag

    def _enter(self, event):
        self.text_widget.config(cursor="hand2")

    def _leave(self, event):
        self.text_widget.config(cursor="")

    def _click(self, event):
        for tag in self.text_widget.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                url = self.links[tag]
                webbrowser.open_new_tab(url)