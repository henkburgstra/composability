var VK = {
    "PLACEHOLDER": "PLACEHOLDER",
    "CONTAINER": "CONTAINER",
    "LABEL": "LABEL",
    "HYPERLINK": "HYPERLINK",
    "TEXT": "TEXT",
    "DATE": "DATE",
    "BUTTON": "BUTTON",
    "COMBO": "COMBO"
}

var Template = function(kind) {
    this.kind = kind;
    this.items = [];
};

var View = function(parent, name) {
    this.parent = parent;
    this.name = name;
    this.template = null;
    this.element = null;
};

View.prototype.createWidget = function(parent, template, withLabel) {
    var label = null;
    var widget = null;

    withLabel = typeof withLabel == 'undefined' ? false : withLabel;

    if withLabel {
        label = document.createElement('div');
        if [VK.PLACEHOLDER, VK.BUTTON, VK.LABEL].indexOf(template.kind) != -1 {
            label.id = "placeholder-" + template.name;
        } else {
            label.id = "label-" + template.name;
            label.appendChild(document.createTextNode(template.title));
        }
    }

    switch (template.kind) {
    case VK.PLACEHOLDER:
        widget = document.createElement('div');
        widget.id = template.name;
        widget.style.backgroundColor = parent.style.backgroundColor;
    case VK.LABEL:
        widget = document.createElement('div');
        widget.id = template.name;
        widget.appendChild(document.createTextNode(template.title));
    default:
        widget = document.createElement('div');
        widget.id = template.name;
        widget.appendChild(document.createTextNode(template.title));
    }

    elif template.kind == View.VK_BUTTON:
        widget = wx.Button(parent, wx.ID_ANY, template.title, name=template.name)
        widget.Bind(wx.EVT_BUTTON, self.on_button, source=widget)
    elif template.kind == View.VK_DATE:
        td = TransformDate(template.value)
        widget = masked.TextCtrl(parent, wx.ID_ANY, td.display(), name=template.name, mask="##-##-####")
        widget.SetFont(self.GetFont())
        if template.readonly:
            widget.SetEditable(False)
            widget.SetBackgroundColour(parent.GetBackgroundColour())
        widget.Bind(wx.EVT_TEXT, self.on_text, source=widget)
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

    return [label, widget];
};


View.prototype.addContainer = function(parent, template) {
};

View.prototype.addWidget = function(parent, template) {
};

View.prototype.add = function(template) {
    if not template.visible {
        return;
    }
    self.Freeze()
    parent = None

    if template.parent:
        parent = document.getElementById(template.parent.name);
    if parent is None:
        parent = this.element;  // TODO: dit is verkeerd. recursief add aanroepen met template.parent

    if template.kind == VK.CONTAINER {
        this.addContainer(parent, template);
    } else {
        this.addWidget(parent, template);
    }
};

View.prototype.inheritanceTest = function() {
    console.log('View');
}

View.prototype.render = function() {
    this.element = document.createElement('div');
    this.element.id = this.name;
    this.parent.appendChild(this.element);
    for (var i = 0; i < this.template.items.length; i++) {
        this.add(this.template.items[i]);
    }
};

View.prototype.setTemplate = function(template) {
    this.template = template;
};

var BoxPanel = function(parent, name) {
};

BoxPanel.prototype = new View(parent, name);
BoxPanel.prototype.constructor = BoxPanel;
BoxPanel.prototype.ancestor = View.prototype
BoxPanel.prototype.inheritanceTest = function() {
    this.ancestor.inheritanceTest();
    console.log('BoxPanel');
}

View.prototype.addContainer = function(parent, template) {
};

View.prototype.addWidget = function(parent, template) {
};

var TestPanel = function(parent, name) {
}

TestPanel.prototype = new BoxPanel(parent, name);
TestPanel.prototype.constructor = TestPanel;
TestPanel.prototype.ancestor = BoxPanel.prototype
TestPanel.prototype.inheritanceTest = function() {
    this.ancestor.inheritanceTest();
    console.log('TestPanel');
}
