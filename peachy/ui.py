import peachy

class UICanvas(object):
    def __init__(self):
        self.widgets = []
        self._focused_widget = None

    @property
    def focused_widget(self):
        return self._focused_widget

    @focused_widget.setter
    def focused_widget(self, widget):
        if self._focused_widget != None:
            self._focused_widget.focused = False
        self._focused_widget = widget

    def add(self, widget):
        widget.parent = self
        if self.focused_widget == None:
            self.focused_widget = widget
        self.widgets.append(widget)

    def remove(self, widget):
        widget.parent = None
        if self.focused_widget == widget:
            self.focused_widget = None
        self.widgets.remove(widget)

    def render(self):
        for widget in self.widgets:
            if widget.visible:
                widget.render()
                widget.render_children()

    def resize(self):
        for widget in self.widgets:
            widget.resize()

    def poll_widgets(self):
        """
        Cycle through widgets and fire Widget.clicked(). Attempt to change focus
        to the last Widget that was clicked.
        Note: Widget.clicked() is only fired for the Widget with the highest
        z-order at Mouse.location
        """
        mx, my = peachy.utils.Mouse.location
        for i in range(len(self.widgets)-1, -1, -1):
            if self.__poll_widget(self.widgets[i], mx, my):
                break

    def __poll_widget(self, widget, mx, my):
        # Recurse through children and check if any have been clicked. If so,
        # then return true
        for child in widget.children:
            if self.__poll_widget(child, mx, my):
                widget.child_clicked()
                if not child.focused and widget.focusable:
                    self.focused_widget = self
                return True

        # Check if this widget has been clicked
        if widget.x <= mx <= widget.x + widget.width and \
           widget.y <= my <= widget.y + widget.height:
            widget.clicked(mx, my)
            if widget.focusable:
                self.focused_widget = widget
            return True

    def update(self):
        if peachy.utils.Mouse.pressed('left'):
            self.poll_widgets()

        for widget in self.widgets:
            if widget.active:
                widget.update()
                widget.update_children()


class Widget(object):
    def __init__(self, x, y, width=0, height=0, label=''):
        self.label = ''

        self.x = x
        self.y = y
        self.width = 0
        self.height = 0

        self.active = True
        self.visible = True
        self._focus = False

        self.parent = None
        self.children = []

        self.focusable = True

    @property
    def focused(self):
        return self._focus

    @focused.setter
    def focused(self, value):
        if self.focusable:
            self._focus = value
            if value == True and self.parent != None:
                self.parent.focused = True
        else:
            raise AttributeError("This Widget cannot be focused.")

    def add(self, widget):
        """ Add a child to this widget """
        widget.parent = self
        self.children.append(widget)

    def clicked(self, x, y):
        return

    def child_clicked(self):
        return

    def normalize(self, x, y):
        return (x - self.x, y - self.y)

    def render(self):
        return

    def render_children(self):
        for child in self.children:
            child.render()

    def resize(self):
        for widget in self.children:
            widget.resize()

    def update(self):
        return

    def update_children(self):
        for child in self.children:
            child.update()