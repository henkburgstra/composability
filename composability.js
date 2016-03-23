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
var templateProperties = ["kind", "name", "title", "value", "readonly", "visible", "attributes", "items"];
var views = {};
var deleteView = function(name) {
    delete views[name];
}

var Template = function(kind, attributes) {
    this.parent = null;
    this.kind = kind;
    this.visible = true;
    this.readonly = false;
    this.attributes = {};
    if (attributes != undefined) {
        this.loadAttributes(attributes);
    }
    this.items = [];

    this.loadAttributes = function(attributes) {
        for (var key in attributes) {
            if (attributes.hasOwnProperty(key)) {
                if (templateProperties.indexOf(key) == -1) {
                    this.attributes[key] = attributes[key];
                } else {
                    this[key] = attributes[key];
                }
            }
        }
    };

    this.loadString = function(s) {
        this.loadObject(JSON.parse(s));
    };

    this.loadObject = function(o) {
        for (var key in o) {
            if (!o.hasOwnProperty(key)) {
                continue;
            }
            if (templateProperties.indexOf(key) == -1) {
                this.attributes[key] = o[key];
            } else {
                if (key == "items") {
                    continue;
                }
                this[key] = o[key];
            }
        }
        if (o.items == undefined) {
            return
        }
        for (var i = 0; i < o.items.length; i++) {
            var item = o.items[i];
            var t = new Template();
            t.loadObject(item);
            this.items.push(t);
        }
    };
};

var View = function(parent, name) {
    this.parent = parent;
    this.name = name;
    views[name] = this;
    this.template = null;
    this.element = null;
};

View.prototype.createWidget = function(parent, template, withLabel) {
    var label = null;
    var widget = null;

    withLabel = typeof withLabel == 'undefined' ? false : withLabel;

    if (withLabel) {
        label = document.createElement('div');
        if ([VK.PLACEHOLDER, VK.BUTTON, VK.LABEL].indexOf(template.kind) != -1) {
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
        break;
    case VK.LABEL:
        widget = document.createElement('div');
        widget.id = template.name;
        widget.appendChild(document.createTextNode(template.title));
        break;
    case VK.BUTTON:
        widget = document.createElement('button');
        widget.id = template.name;
        widget.appendChild(document.createTextNode(template.title));
        break;
    case VK.DATE:
        widget = document.createElement('input');
        widget.type = 'date';
        widget.id = template.name;
        break;
    case VK.TEXT:
        widget = document.createElement('input');
        widget.type = 'text';
        widget.id = template.name;
        break;
    case VK.COMBO:
        widget = document.createElement('select');
        widget.id = template.name;
        for (var i = 0; i < template.options; i++) {
            var o = document.createElement('option');
            var v = template.options[i][0];
            var l = template.options[i][1];
            o.value = v;
            if (v == template.value) {
                // TODO: selected
            }
            o.appendChild(document.createTextNode(l));
            widget.appendChild(o);
        }
        break;
    default:
        widget = document.createElement('div');
        widget.id = template.name;
        widget.appendChild(document.createTextNode(template.title));
    }

    return [label, widget];
};


View.prototype.addContainer = function(parentView, template) {
};

View.prototype.addWidget = function(parentView, template) {
};

View.prototype.add = function(template) {
    if (!template.visible) {
        return;
    }
    var parentView = null;

    if (template.parent) {
        parentView = views[template.parent.name];
    }
    if (parent == null) {
        parentView = this;  // TODO: dit is verkeerd. recursief add aanroepen met template.parent
    }

    if (template.kind == VK.CONTAINER) {
        this.addContainer(parentView, template);
    } else {
        this.addWidget(parentView, template);
    }
};

View.prototype.inheritanceTest = function() {
    console.log('View');
}

View.prototype.createDOM = function() {
    var element = document.createElement('div');
    element.id = this.name;
    return element;
}

View.prototype.render = function() {
    this.element = this.createDOM();
    this.parent.appendChild(this.element);
    for (var i = 0; i < this.template.items.length; i++) {
        this.add(this.template.items[i]);
    }
};

View.prototype.setTemplate = function(template) {
    this.template = template;
};

/*
    BoxPanel
*/
var BoxPanel = function(parent, name) {
    this.ancestor.constructor.call(this, parent, name);
    this.itemPanel = null;
    this.rightPanel = null;
};

BoxPanel.prototype = new View(parent, name);
BoxPanel.prototype.constructor = BoxPanel;
BoxPanel.prototype.ancestor = View.prototype

BoxPanel.prototype.createDOM = function () {
    var element = this.ancestor.createDOM.call(this);
    if (this.itemPanel == null && element != null) {
        this.itemPanel = document.createElement('div');
    }
    if (this.rightPanel == null && element != null) {
        this.rightPanel = document.createElement('div');
    }
    // TODO: itemPanel en rightPanel moeten naast elkaar komen te staan.
    element.appendChild(this.itemPanel);
    element.appendChild(this.rightPanel);
    return element;
}

BoxPanel.prototype.createPanels = function() {
};

BoxPanel.prototype.addContainer = function(parentView, template) {
    this.ancestor.addContainer.call(this, parentView, template);
    if (template.display == Template.DISP_INLINE) {
        // TODO: itemPanel moet een javascript object zijn i.p.v. een dom node
        this.addWidget(parentView.itemPanel, template);
        return;
    } else if (template.display == Template.DISP_RIGHT) {
        // TODO: rightPanel moet een javascript object zijn i.p.v. een dom node
        box = new BoxPanel(parentView.rightPanel, template.name);
        parent.rightPanel.add(box);
    }
    else {
        box = new BoxPanel(parentView, template.name);
        parent.item_sizer.Add(box, 0, wx.BOTTOM | wx.EXPAND, 2);
    }
    box.setTemplate(template);
    box.render();
};

BoxPanel.prototype.addWidget = function(parentView, template) {
    // TODO: bepaal echte parent, bepaal label of niet
    var widgets = this.createWidget(parent, template, true);
    var label = widgets[0];
    var widget = widgets[1];
};
