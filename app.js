document.addEventListener('DOMContentLoaded', function() {
    var b = new TestPanel(document.getElementById("composability-test"), "Composability Test");
    b.setTemplate(new Template(VK.CONTAINER));
    b.render();
    b.inheritanceTest();
});