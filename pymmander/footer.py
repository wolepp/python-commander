import urwid

RIGHT_ARROW = ">>"
LEFT_ARROW = "<<"
SHOW_HIDDEN_FILES = "show"
HIDE_HIDDEN_FILES = "hide"

class Footer(urwid.WidgetWrap):
    def __init__(self):
        self.arrow = RIGHT_ARROW
        self.show_hidden = SHOW_HIDDEN_FILES
        init_text = Footer._footer_text(self.arrow, self.show_hidden)
        self.text = urwid.Text(init_text)
        self.prompt = urwid.Edit("Prompt: ")
        super(Footer, self).__init__(self.text)

    @staticmethod
    def _footer_text(arrow, hidden):
        return f"F2 Copy {arrow} | " + \
            f"F3 Move {arrow} | " + \
             "F4 Mkdir | " + \
             "F5 Rename | " + \
             "F6 Remove | " + \
            f"F7 {hidden} hidden files | " + \
             "F8/q Quit"

    def show_prompt(self, prompt_text):
        self.prompt.set_caption(prompt_text)
        self.prompt.set_edit_text("")
        self._w = self.prompt

    def get_edit_text(self):
        return self.prompt.get_edit_text()

    def show_text(self):
        self._w = self.text

    def update_text(self, active_pane, show_hidden):
        if active_pane == 0:
            self.arrow = RIGHT_ARROW
        else:
            self.arrow = LEFT_ARROW
        if show_hidden:
            self.show_hidden = HIDE_HIDDEN_FILES    
        else:
            self.show_hidden = SHOW_HIDDEN_FILES
        text = Footer._footer_text(self.arrow, self.show_hidden)
        self.text.set_text(text)
        self.show_text()
            
    def keypress(self, size, key):
        if key == 'enter':
            return key

        if key == 'esc':
            return key

        key = self._w.keypress(size, key)

        return key