$(document).ready(function() {
    // Shift nav in mobile when clicking the menu.
    $(document).on('click', "[data-toggle='wy-nav-top']", function() {
        $("div.documentwrapper").toggleClass("noview");
        $("div.sphinxsidebar").toggleClass("noview");
        $("body").toggleClass("bgnav");
    });
}($));
