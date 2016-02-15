class Message(object):
    ADD = "ADD"
    CHANGE = "CHANGE"
    CLICK = "CLICK"
    FOCUS = "FOCUS"
    LOST_FOCUS = "LOST_FOCUS"
    SELECT = "SELECT"

    def __init__(self, kind):
        self.kind = kind
        self.data = {}

    def set(self, name, value):
        self.data[name] = value

    def get(self, name):
        return self.data.get(name)


class Controller(object):
    def __init__(self, view, binder):
        self.set_view(view)  #  root view
        self.binder = binder
        self.controllers = {}  # sub controllers

    def set_binder(self, binder):
        self.binder = binder

    def set_view(self, view):
        self.view = view
        view.set_controller(self)

    def select(self, selection):
        if self.binder is None:
            return
        self.binder.select(selection)

    def load_view(self):
        if self.view is None:
            return
        if self.binder is None:
            return
        # self.template is het root item  (i.e. patient)
        self.view.set_template(self.binder.load())
        self.view.render()

    def register_controller(self, path, controller):
        self.controllers[path] = controller

    def controller(self, view):
        return self

    def view_message(self, src, msg):
        vw = msg.get("view")
        if vw is None:
            return
        controller = self.controller(vw)
        if msg.kind == Message.CLICK:
            controller.view_clicked(src, msg)
        elif msg.kind == Message.CHANGE:
            controller.view_changed(src, msg)

    def view_changed(self, src, msg):
        self.binder.buffers.set_display(src, msg.get("value"))

    def view_focused(self, view):
        pass

    def view_clicked(self, src, msg):
        button = msg.get("button")
        if button == "RIGHT":
            self.view_right_clicked(src, msg)
        else:
            self.view_left_clicked(src, msg)

    def view_left_clicked(self, src, msg):
        pass

    def view_right_clicked(self, src, msg):
        pass
