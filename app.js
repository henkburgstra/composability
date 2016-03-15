document.addEventListener('DOMContentLoaded', function() {
    var b = new BoxPanel(document.getElementById("composability-test"), "bezoek");
    b.setTemplate(new Template(VK.CONTAINER));
    b.render();
});