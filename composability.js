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
};

View.prototype.add = function(template) {
};

View.prototype.inheritanceTest = function() {
    console.log('View');
}

View.prototype.render = function() {
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

var TestPanel = function(parent, name) {
}

TestPanel.prototype = new BoxPanel(parent, name);
TestPanel.prototype.constructor = TestPanel;
TestPanel.prototype.ancestor = BoxPanel.prototype
TestPanel.prototype.inheritanceTest = function() {
    this.ancestor.inheritanceTest();
    console.log('TestPanel');
}
