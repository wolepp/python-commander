import urwid


class Footer(urwid.Overlay):

    def __init__(self):
        bottom_w = urwid.Filler(urwid.Text(self._footer_text(">>", "hide")))
        top_w = urwid.Filler(urwid.Edit("Caption: "))
        super(Footer, self).__init__(top_w, bottom_w, 
            align='left', width=('relative', 100),
            valign='top', height=2)

    def update_footer_text(self, arrow, hidden_files):
        self.top_w.set_text(self._footer_text(arrow))

    def _footer_text(self, arrow, hidden_files):
        return f"!F2 Copy {arrow} | " + \
            f"!F3 Move {arrow} | " + \
             "!F4 Mkdir | " + \
             "!F5 Rename | " + \
             "!F6 Remove | " + \
            f"!F7 {hidden_files} hidden files | " + \
             "F8/q Quit"

    def get_edit_text(self):
        return self.top_w.original_widget.get_edit_text()

    def keypress(self, size, key):
        # obsługa enter przenieść do pymandera - działanie zależne od focusu
        if key == 'enter':
            return key
        self.top_w.keypress(size, key)
        if not key in ("q", 'Q'):
            return key