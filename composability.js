var view = function(parent, name) {
    this.parent = parent;
    this.name = name;
    this.template = null;

    this.setTemplate = function(template) {
        this.template = template;
    };

    this.render = function() {
    }
}