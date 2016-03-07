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
    if not template.visible {
        return;
    }
    parent = null;

    if (template.parent) {
        parent = document.getElementById(template.parent.name);
    }
    if parent == null {
        parent = this.element;  // TODO: dit is verkeerd. recursief add aanroepen met template.parent
    }

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

/*
    BoxPanel
*/
var BoxPanel = function(parent, name) {
    this.itemPanel = null;
    this.rightPanel = null;
};

BoxPanel.prototype = new View(parent, name);
BoxPanel.prototype.constructor = BoxPanel;
BoxPanel.prototype.ancestor = View.prototype
BoxPanel.prototype.inheritanceTest = function() {
    this.ancestor.inheritanceTest();
    console.log('BoxPanel');
}

BoxPanel.prototype.createPanels = function() {
    if (this.itemPanel == null && this.element != null) {
        this.itemPanel = document.createElement('div');
    }
    if (this.rightPanel == null && this.element != null) {
        this.rightPanel = document.createElement('div');
    }
};

BoxPanel.prototype.addContainer = function(parent, template) {
    this.createPanels();
};

BoxPanel.prototype.addWidget = function(parent, template) {
    this.createPanels();
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
