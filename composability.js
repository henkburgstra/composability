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
var templateProperties = ["kind", "name", "title", "value", "readonly", "visible"];

var Template = function(kind, attributes) {
    this.parent = null;
    this.kind = kind;
    this.attributes = {};
    if (attributes != undefined) {
        for (var key in attributes) {
            if (attributes.hasOwnProperty(key)) {
                if (templateProperties.indexOf(key) == -1) {
                    this[key] = attributes[key];
                } else {
                    this.attributes[key] = attributes[key];
                }
            }
        }
    }
    this.items = [];

    this.loadString = function(s) {
        this.loadObject(JSON.parse(s));
    };

    this.loadObject = function(o) {
        for (var i = 0; i < templateProperties.length; i++) {
            var name = templateProperties[i];
            var v = o[name];
            if (v != undefined) {
                this[name] = v;
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
    case VK.LABEL:
        widget = document.createElement('div');
        widget.id = template.name;
        widget.appendChild(document.createTextNode(template.title));
    case VK.BUTTON:
        widget = document.createElement('button');
        widget.id = template.name;
        widget.appendChild(document.createTextNode(template.title));
    case VK.DATE:
        widget = document.createElement('input');
        widget.type = 'date';
        widget.id = template.name;
    case VK.TEXT:
        widget = document.createElement('input');
        widget.type = 'text';
        widget.id = template.name;
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
    default:
        widget = document.createElement('div');
        widget.id = template.name;
        widget.appendChild(document.createTextNode(template.title));
    }

    return [label, widget];
};


View.prototype.addContainer = function(parent, template) {
};

View.prototype.addWidget = function(parent, template) {
};

View.prototype.add = function(template) {
    if (!template.visible) {
        return;
    }
    parent = null;

    if (template.parent) {
        parent = document.getElementById(template.parent.name);
    }
    if (parent == null) {
        parent = this.element;  // TODO: dit is verkeerd. recursief add aanroepen met template.parent
    }

    if (template.kind == VK.CONTAINER) {
        this.addContainer(parent, template);
    } else {
        this.addWidget(parent, template);
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
    return element;
}

BoxPanel.prototype.createPanels = function() {
};

BoxPanel.prototype.addContainer = function(parent, template) {
};

BoxPanel.prototype.addWidget = function(parent, template) {
};
