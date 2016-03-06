document.addEventListener('DOMContentLoaded', function() {
    var b = new TestPanel("id", "test");
    b.setTemplate(new Template(VK.CONTAINER));
    b.render();
    b.inheritanceTest();
});