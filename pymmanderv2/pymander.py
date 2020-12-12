import urwid
from pane import Pane
from footer import Footer
from pathlib import Path
from filemanager import FileManager
import actions

class PyMander(urwid.Frame):
    def __init__(self):
        self.active_pane = 0
        self.show_hidden = False
        self.fm = FileManager()
        self.panes = urwid.AttrMap(urwid.Columns([Pane(self.show_hidden), Pane(self.show_hidden)], 2), 'columns')
        super(PyMander, self).__init__(self.panes, footer=Footer(), header=urwid.Text(""))
        self._w = urwid.AttrMap(self, 'pymander')

    def set_active_pane(self, pane_number: int):
        self.active_pane = pane_number

    def update_footer(self):
        self.footer.update_text(self.active_pane, self.show_hidden)

    def switch_hidden(self):
        self.show_hidden = not self.show_hidden
        self.update_footer()

    def get_pane(self, number):
        return self.panes.original_widget.contents[number][0]
    
    def get_active_pane(self):
        return self.get_pane(self.active_pane)

    def get_inactive_pane(self):
        return self.get_pane(abs(self.active_pane - 1))

    def get_focus_filepath(self):
        return self.get_active_pane().get_focus_filepath()

    def get_active_curdir(self):
        return self.get_active_pane().curdir

    def get_destination_path(self):
        return self.get_inactive_pane().curdir

    def is_back_button_focused(self):
        return self.get_active_pane().is_back_button_focused()

    def headertext(self, text):
        self.header.set_text(text)

    def update_panes(self, preserve_focus=False):
        self.get_inactive_pane().update_content(preserve_focus=preserve_focus)
        self.get_active_pane().update_content(preserve_focus=preserve_focus)

    def ask_for(self, prompt):
        self.footer.show_prompt(prompt)
        self.set_focus('footer')

    def set_response(self):
        self.action.set_response(self.footer.get_edit_text().strip())
    
    def close_prompt(self):
        self.footer.show_text()
        self.set_focus('body')
        self.update_panes(preserve_focus=True)

    def keypress(self, size, key):
        if key in ('up', 'down'):
            self.headertext("")

        if key == 'left':
            self.set_active_pane(0)
            self.update_footer()
            self.headertext("")

        elif key == 'right':
            self.set_active_pane(1)
            self.update_footer()
            self.headertext("")

        elif key == 'f2': # copy
            if not self.is_back_button_focused():
                src = self.get_focus_filepath()
                dest = self.get_destination_path().joinpath(src.name)
                self.fm.copy(src, dest)
                self.update_panes(preserve_focus=True)
                self.headertext("Copied")

        elif key == 'f3': # move
            if not self.is_back_button_focused():
                src = self.get_focus_filepath()
                dest = self.get_destination_path().joinpath(src.name)
                self.fm.move(src, dest)
                self.update_panes(preserve_focus=True)
                self.headertext("Moved")

        elif key == 'f4': # mkdir
            path = self.get_active_curdir()
            self.action = actions.Mkdir(self.fm, path)
            self.ask_for("Directory name: ")
        
        elif key == 'f5': # rename
            if not self.is_back_button_focused():
                file_to_rename = self.get_focus_filepath()
                self.action = actions.Rename(self.fm, file_to_rename)
                self.ask_for(f"Renaming {file_to_rename}: ")

        elif key == 'f6': # remove
            if not self.is_back_button_focused():
                to_remove = self.get_focus_filepath()
                self.action = actions.Rm(self.fm, to_remove)
                self.ask_for(f"Remove {to_remove}? (y/yes/tak): ")

        elif key == 'f7': # switch hidden files
            self.switch_hidden()
            self.update_footer()
            self.update_panes(preserve_focus=True)

        key = super(PyMander, self).keypress(size, key)
        if key == 'enter':
            if self.get_focus() == 'footer':
                self.set_response()
                try:
                    self.action.run()
                    self.headertext(self.action.success_text)
                except:
                    self.headertext(self.action.exception_text)
                self.close_prompt()
                self.update_panes(preserve_focus=True)
            else:
                return key

        elif key == 'esc':
            if self.get_focus() == 'footer':
                self.close_prompt()

        elif key in ('f8', 'q'):
            raise urwid.ExitMainLoop()

        return key
