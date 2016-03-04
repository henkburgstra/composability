var View = function(parent, name) {
    this.parent = parent;
    this.name = name;
    this.template = null;

    this.add = function(template) {
    };
    this.render = function() {
        for (var i = 0; i < this.template.items.length; i++) {
            this.add(this.template.items[i]);
        }
    };
    this.setTemplate = function(template) {
        this.template = template;
    };

};

var BoxPanel = function(parent, name) {
    this.prototype = new View(parent, name);
    this.ancestor = View.prototype;
};