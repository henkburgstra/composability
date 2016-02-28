#
#  -*- coding: utf-8 -*-

import wx
from composability.template import Template
from composability.controller import Message
from composability.transformers import TransformDate
from composability.view import View


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
        orientation = template.orientation if template.orientation else Template.ORI_VERTICAL
        self.orientation = orientation
        self.template = template
        if template.name:
            self.SetName(template.name)

    def add_container(self, parent, template):
        pass

    def create_widget(self, parent, template, with_label=True):
        label = None
        widget = None

        if with_label:
            if template.kind in [View.VK_PLACEHOLDER, View.VK_BUTTON, View.VK_LABEL]:
                label = wx.Panel(parent, wx.ID_ANY, style=wx.TRANSPARENT_WINDOW, name="placeholder-%s" % template.name)
            else:
                label = wx.StaticText(parent, wx.ID_ANY, " %s " % template.title, name="label-%s" % template.name)

        if template.kind == View.VK_PLACEHOLDER:
            widget = wx.Panel(parent, wx.ID_ANY, style=wx.TRANSPARENT_WINDOW, name=template.name)
            widget.SetBackgroundColour(parent.GetBackgroundColour())
        if template.kind == View.VK_LABEL:
            widget = wx.StaticText(parent, wx.ID_ANY, template.title, name=template.name)
        elif template.kind == View.VK_BUTTON:
            widget = wx.Button(parent, wx.ID_ANY, template.title, name=template.name)
            widget.Bind(wx.EVT_BUTTON, self.on_button, source=widget)
        elif template.kind == View.VK_DATE:
            td = TransformDate(template.value)
            widget = wx.DatePickerCtrl(parent, wx.ID_ANY, dt=wx.DateTimeFromDMY(td.d(), td.m() - 1, td.y()),
                                       name=template.name, style=wx.TAB_TRAVERSAL|wx.DP_SHOWCENTURY)
            if template.readonly:
                widget.Enable(False)
                widget.SetBackgroundColour(parent.GetBackgroundColour())
            widget.Bind(wx.EVT_DATE_CHANGED, self.on_date, source=widget)
        elif template.kind == View.VK_TEXT:
            widget = wx.TextCtrl(parent, wx.ID_ANY,
                template.value if template.value is not None else "", name=template.name)
            if template.readonly:
                widget.SetEditable(False)
                widget.SetBackgroundColour(parent.GetBackgroundColour())
            widget.Bind(wx.EVT_TEXT, self.on_text, source=widget)
        elif template.kind == View.VK_COMBO:
            widget = wx.ComboBox(parent, wx.ID_ANY, name=template.name)
            i = 0
            selected = -1
            for key, option in template.options:
                widget.Append(option, key)
                if key == template.value:
                    selected = i
                i += 1
            if selected != -1:
                widget.SetSelection(selected)
            widget.Bind(wx.EVT_COMBOBOX, self.on_combobox, source=widget)

        # if template.readonly:
        #     widget.Enable(False)
        #     widget.SetBackgroundColour(parent.GetBackgroundColour())
        return label, widget

    def add_widget(self, parent, template):
        pass

    def insert(self, sibling_name, pos, template):
        # onderstaande code werkt, maar heeft als nadeel dat het hele scherm
        # opnieuw wordt opgebouwd en de waarde van de widgets opnieuw
        # moet worden ingesteld.
        #
        # Zie BoxPanel.insert() voor nieuwe implementatie.
        parent_name = template.get_parent_name()
        if not parent_name:
            return  # TODO: foutmelding
        if parent_name == self.Name:
            parent_template = self.template
            parent_template.insert(sibling_name, pos, template)
            self.clear()
            self.set_template(parent_template)
            self.render()
        else:
            parent = wx.FindWindowByName(parent_name)
            if not parent:
                return  # TODO: foutmelding
            parent_template = getattr(parent, "template", None)
            if not parent_template:
                return  # TODO: foutmelding
            self.remove(parent_name)
            parent_template.insert(sibling_name, pos, template)
            self.add(parent_template)

    def add(self, template):
        if not template.visible:
            return
        self.Freeze()
        parent = None

        if template.parent:
            parent = wx.FindWindowByName(template.parent.name)
        if parent is None:
            parent = self  # TODO: dit is verkeerd. recursief add aanroepen met template.parent

        if template.kind == View.VK_CONTAINER:
            self.add_container(parent, template)
        else:
            self.add_widget(parent, template)

        sizer = parent.GetSizer()
        sizer.Layout()
        sizer.Fit(parent)
        self.Thaw()

    def clear(self):
        pass

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

    def on_date(self, msg):
        vw_msg = Message(Message.CHANGE)
        vw_msg.set("view", self)
        ctrl = msg.GetEventObject()
        vw_msg.set("value", ctrl.GetValue().Format("%d-%m-%Y"))
        self.controller.view_message(ctrl.GetName(), vw_msg)

    def on_text(self, msg):
        vw_msg = Message(Message.CHANGE)
        vw_msg.set("view", self)
        ctrl = msg.GetEventObject()
        vw_msg.set("value", ctrl.GetValue())
        self.controller.view_message(ctrl.GetName(), vw_msg)

    def on_combobox(self, msg):
        vw_msg = Message(Message.CHANGE)
        vw_msg.set("view", self)
        ctrl = msg.GetEventObject()
        vw_msg.set("value", ctrl.GetClientData(ctrl.GetSelection()))
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
        self.item_panel.set_orientation(self.orientation)
        if template.colcount != -1:
            self.item_panel.set_colcount(template.colcount)
        self.item_panel.set_label_position(template.label_position)
        self.item_panel.SetBackgroundColour(template.background_colour)

    def add_container(self, parent, template):
        super(BoxPanel, self).add_container(parent, template)
        if template.display == Template.DISP_INLINE:
            box = BoxPanel(parent.item_panel, name=template.name)
            parent.item_panel.add(box, colspan=2)
        elif template.display == Template.DISP_RIGHT:
            box = BoxPanel(parent.right_panel, name=template.name)
            parent.right_panel.add(box)
        else:
            box = BoxPanel(parent, name=template.name)
            parent.item_sizer.Add(box, 0, wx.BOTTOM | wx.EXPAND, 2)
        box.set_template(template)
        box.set_controller(self.controller)
        box.render()

    def add_widget(self, parent, template):
        if isinstance(parent, ItemPanel):
            panel = parent
        elif isinstance(parent, BoxPanel):
            panel = parent.item_panel
        else:
            return  #  TODO: exception

        label, widget = self.create_widget(panel, template, with_label=panel.with_label(template))
        if label:
            panel.add(label)

        if widget:
            panel.add(widget, rowspan=template.rowspan, colspan=template.colspan)

        sizer = panel.GetSizer()
        sizer.Layout()
        sizer.Fit(panel)

    def insert(self, sibling_name, pos, template):
        # nieuwe implementatie van WxView.insert()
        parent_name = template.get_parent_name()
        if not parent_name:
            return  # TODO: foutmelding
        parent_template = self.template
        parent_template.insert(sibling_name, pos, template)
        sibling = wx.FindWindowByName(sibling_name)
        if not sibling:
            return  # TODO: foutmelding
        parent = sibling.GetParent()   # TODO: dit moet een ItemPanel instantie zijn, anders foutmelding
        self.Freeze()
        parent.insert(sibling_name, pos, template)
        sizer = self.GetSizer()
        sizer.Layout()
        sizer.Fit(self)
        self.Thaw()

    def clear(self):
        self.item_panel.clear()
        self.right_panel.clear()


class ItemPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        self.SetSizer(wx.GridBagSizer())
        self.colcount = -1
        self.label_position = Template.POS_ABOVE
        self.init()

    def init(self):
        self.row = 0
        self.col = 0
        self.items = []

    def set_orientation(self, orientation):
        self.orientation = orientation
        if self.orientation == Template.ORI_VERTICAL:
            self.colcount = 2

    def set_colcount(self, colcount):
        self.colcount = colcount

    def set_label_position(self, position):
        self.label_position = position

    def with_label(self, template):
        if (template.kind == View.VK_PLACEHOLDER and self.orientation == Template.ORI_HORIZONTAL
                and self.label_position == Template.POS_LEFT):
            return False
        if self.orientation == Template.ORI_HORIZONTAL and not template.title:
            return False
        return True

    def insert(self, sibling_name, pos, template):
        parent = self.GetParent()
        label, widget = parent.create_widget(self, template, with_label=self.with_label(template))
        sizer = self.GetSizer()
        items = []

        for item in self.items:
            sizer.Detach(item)
            if sibling_name == item.Name:
                if pos == Template.POS_BEFORE:
                    if label:
                        items += [label]
                    items += [widget]
                    items += [item]
                else:
                    items += [item]
                    if label:
                        items += [label]
                    items += [widget]
            else:
                items += [item]

        self.init()

        for item in items:
            colspan = 1
            rowspan = 1
            t = parent.template.get(item.Name)
            if t:
                colspan = t.colspan
                rowspan = t.rowspan
            self.add(item, colspan=colspan, rowspan=rowspan)

        sizer.Layout()
        sizer.Fit(self)

    def add(self, item, rowspan=1, colspan=1):
        self.items += [item]
        sizer = self.GetSizer()
        sizer.Add(item, pos=(self.row, self.col), span=(rowspan, colspan), flag=wx.EXPAND | wx.ALIGN_CENTER)
        if self.orientation == Template.ORI_VERTICAL:
            # verticaal is steeds een label en een invoerveld naast elkaar
            self.col += colspan
            if self.col == self.colcount:
                self.col = 0
                self.row += rowspan
        else:
            if self.label_position == Template.POS_ABOVE:
                # steeds een label en een invoerveld boven elkaar
                self.row += rowspan
                if self.row  % 2 == 0:
                    self.row -= 2
                    self.col += colspan
                if self.col == self.colcount:
                    self.col = 0
                    self.row += 2
            else:
                # steeds een label en een invoerveld naast elkaar
                self.col += colspan
                if self.col == self.colcount:
                    self.col = 0
                    self.row += 1

    def clear(self):
        sizer = self.GetSizer()
        for item in self.items:
            sizer.Detach(item)
            item.Destroy()
        self.init()

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

    def clear(self):
        sizer = self.GetSizer()
        for item in self.items:
            sizer.Detach(item)
            item.Destroy()
        self.items = []
        sizer.Layout()
        sizer.Fit(self)

    def remove(self, item):
        if item in self.items:
            self.items.remove(item)
            sizer = self.GetSizer()
            sizer.Detach(item)
            item.Destroy()
