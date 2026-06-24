(function() {
    var html = document.documentElement;
    
    // 1. Initial theme set (PaperMod logic replacement to bypass CSP inline block)
    if (localStorage.getItem("pref-theme") === "dark") {
        html.dataset.theme = 'dark';
    } else if (localStorage.getItem("pref-theme") === "light") {
        html.dataset.theme = 'light';
    } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        html.dataset.theme = 'dark';
    } else {
        html.dataset.theme = 'light';
    }

    // 2. SPA Bridge (.dark class sync)
    if (html.dataset.theme === 'dark') html.classList.add('dark');
    new MutationObserver(function() {
        html.classList.toggle('dark', html.dataset.theme === 'dark');
    }).observe(html, {attributes: true, attributeFilter: ['data-theme']});
})();
