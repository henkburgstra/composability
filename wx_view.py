#
#  -*- coding: utf-8 -*-

import wx
from view import Message, Template

class ItemPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        self.SetSizer(wx.GridBagSizer())
        self.row = 0
        self.col = 0
        self.items = []

    def set_orientation(self, orientation):
        self.orientation = orientation

    def add(self, item, rowspan=1, colspan=1):
        self.items += [item]
        sizer = self.GetSizer()
        sizer.Add(item, pos=(self.row, self.col), span=(rowspan, colspan))
        if self.orientation == Template.ORI_VERTICAL:
            # verticaal is steeds een label en een invoerveld naast elkaar
            self.col += colspan
            if self.col == 2:
                self.col = 0
                self.row += 1
        else:
            # horizontaal is steeds een label en een invoerveld boven elkaar
            self.row += rowspan
            if self.row == 2:
                self.row = 0
                self.col += 1

    def remove(self, item):
        if item in self.items:
            self.items.remove(item)
            sizer = self.GetSizer()
            sizer.Detach(item)
            item.Destroy()
            sizer.Layout()
            sizer.Fit(self)


class SubBoxPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        self.SetSizer(wx.BoxSizer(wx.VERTICAL))
        self.items = []

    def add(self, box):
        self.items += [box]
        sizer = self.GetSizer()
        sizer.Add(box, 0, wx.ALL | wx.EXPAND, 2)

    def remove(self, item):
        if item in self.items:
            self.items.remove(item)
            sizer = self.GetSizer()
            sizer.Detach(item)
            item.Destroy()
            sizer.Layout()
            sizer.Fit(self)


class WxView(wx.Panel):
    """
    WxView implements the View interface.
    """
    def __init__(self, parent, **kwargs):
        wx.Panel.__init__(self, parent, wx.ID_ANY, **kwargs)
        self.template = None
        self.controller = None

    def set_controller(self, controller):
        self.controller = controller

    def get_value(self, name):
        widget = wx.FindWindowByName(name)
        if widget is None:
            return
        if isinstance(widget, wx.TextCtrl):
            return widget.GetValue()

    def set_value(self, name, value):
        widget = wx.FindWindowByName(name)
        if widget is None:
            return
        if isinstance(widget, wx.TextCtrl):
            widget.SetValue(value)

    def set_template(self, template):
        self.template = template

    def add_container(self, parent, template):
        pass

    def add_item(self, parent, template):
        pass

    def add(self, template):
        if not template.visible:
            return
        parent = None
        if template.parent:
            parent = wx.FindWindowByName(template.parent.name)
        if parent is None:
            parent = self  # TODO: dit is verkeerd. recursief add aanroepen met template.parent
        if template.kind == Template.VK_CONTAINER:
            self.add_container(parent, template)

        else:
            self.add_item(parent, template)

        sizer = parent.GetSizer()
        sizer.Layout()
        sizer.Fit(parent)

    def remove(self, name):
        widget = wx.FindWindowByName(name)
        if widget is None:
            return
        parent = widget.GetParent()
        parent.remove(widget)
        sizer = self.GetSizer()
        sizer.Layout()
        sizer.Fit(self)

    def render(self):
        for child_view in self.template.items:
            self.add(child_view)

    def on_button(self, msg):
        vw_msg = Message(Message.CLICK)
        vw_msg.set("view", self)
        ctrl = msg.GetEventObject()
        self.controller.view_message(ctrl.GetName(), vw_msg)

    def on_text(self, msg):
        vw_msg = Message(Message.CHANGE)
        vw_msg.set("view", self)
        ctrl = msg.GetEventObject()
        vw_msg.set("value", ctrl.GetValue())
        self.controller.view_message(ctrl.GetName(), vw_msg)


class BoxPanel(WxView):
    """
    BoxPanel presenteert elementen als blokken.
    Elke entry opent een grid van één rij en twee kolommen.

    Layout van subentries:
    - inline
    - onder de parent
    - rechts van de parent

    Een grid en kolommen hebben geen intrinsieke breedte. Een kolom
    zonder elementen neemt geen ruimte in. Ruimte tussen blokken
    moet worden geregeld met padding.
    """
    def __init__(self, parent, **kwargs):
        WxView.__init__(self, parent, **kwargs)
        sizer = wx.GridBagSizer()
        self.SetSizer(sizer)
        self.orientation = Template.ORI_VERTICAL
        self.item_sizer = wx.BoxSizer(wx.VERTICAL)
        self.item_panel = ItemPanel(self)
        self.item_panel.SetBackgroundColour(self.GetParent().GetBackgroundColour())
        self.item_sizer.Add(self.item_panel, 0, wx.ALL | wx.EXPAND, 2)
        self.right_panel = SubBoxPanel(self)
        sizer.Add(self.item_sizer, pos=(0, 0))
        sizer.Add(self.right_panel, pos=(0, 1))

    def set_template(self, template):
        super(BoxPanel, self).set_template(template)
        orientation = template.orientation if template.orientation else Template.ORI_VERTICAL
        self.orientation = orientation
        self.item_panel.set_orientation(orientation)
        self.item_panel.SetBackgroundColour(template.background_colour)

    def add_container(self, parent, template):
        super(BoxPanel, self).add_container(parent, template)
        if template.display == Template.DISP_INLINE:
            box = BoxPanel(parent.item_panel, name=template.name)
            box.set_template(template)
            box.set_controller(self.controller)
            parent.item_panel.add(box, colspan=2)
        elif template.display == Template.DISP_RIGHT:
            box = BoxPanel(parent.right_panel, name=template.name)
            box.set_template(template)
            box.set_controller(self.controller)
            parent.right_panel.add(box)
        else:
            box = BoxPanel(parent, name=template.name)
            box.set_template(template)
            box.set_controller(self.controller)
            parent.item_sizer.Add(box, 0, wx.BOTTOM | wx.EXPAND, 2)
        box.render()

    def add_item(self, parent, template):
        if isinstance(parent, ItemPanel):
            panel = parent
        elif isinstance(parent, BoxPanel):
            panel = parent.item_panel
        else:
            return  #  TODO: exception
        wx_view = None
        label = wx.StaticText(panel, wx.ID_ANY, template.title, name=template.name)
        if template.kind == Template.VK_LABEL:
            panel.add(label, colspan=2)
        elif template.kind == Template.VK_BUTTON:
            wx_view = wx.Button(panel, wx.ID_ANY, template.title, name=template.name)
            wx_view.Bind(wx.EVT_BUTTON, self.on_button, source=wx_view)
            panel.add(wx_view)
        else:
            panel.add(label)
            label.SetName("label-%s" % template.name)
            if template.kind == Template.VK_TEXT:
                wx_view = wx.TextCtrl(panel, wx.ID_ANY,
                    template.value if template.value is not None else "", name=template.name)
                wx_view.Bind(wx.EVT_TEXT, self.on_text, source=wx_view)
            if wx_view is not None:
                panel.add(wx_view)

