// assets/js/theme-footer.js
document.addEventListener("DOMContentLoaded", function() {
    // Smart Sticky Header
    let lastScrollY = window.scrollY;
    const header = document.querySelector('.header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 100) {
                if (window.scrollY > lastScrollY) {
                    header.classList.add('nav-hidden');
                } else {
                    header.classList.remove('nav-hidden');
                }
            } else {
                header.classList.remove('nav-hidden');
            }
            lastScrollY = window.scrollY;
        }, { passive: true });
    }

    let menu = document.getElementById('menu');
    if (menu) {
        const scrollPosition = localStorage.getItem("menu-scroll-position");
        if (scrollPosition) {
            menu.scrollLeft = parseInt(scrollPosition, 10);
        }
        menu.onscroll = function () {
            localStorage.setItem("menu-scroll-position", menu.scrollLeft);
        }
    }

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener("click", function (e) {
            e.preventDefault();
            var id = this.getAttribute("href").substr(1);
            if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
                document.querySelector(`[id='${decodeURIComponent(id)}']`).scrollIntoView({
                    behavior: "smooth"
                });
            } else {
                document.querySelector(`[id='${decodeURIComponent(id)}']`).scrollIntoView();
            }
            if (id === "top") {
                history.replaceState(null, null, " ");
            } else {
                history.pushState(null, null, `#${id}`);
            }
        });
    });

    var toplink = document.getElementById("top-link");
    if (toplink) {
        window.onscroll = function () {
            const scrollThreshold = window.innerHeight;
            if (document.body.scrollTop > scrollThreshold || document.documentElement.scrollTop > scrollThreshold) {
                toplink.classList.remove("hidden");
            } else {
                toplink.classList.add("hidden");
            }
        };
    }

    const themeToggle = document.getElementById("theme-toggle");
    if (themeToggle) {
        themeToggle.addEventListener("click", () => {
            const html = document.querySelector("html");
            if (html.dataset.theme === "dark") {
                html.dataset.theme = 'light';
                localStorage.setItem("pref-theme", 'light');
                updateGiscusTheme('light');
            } else {
                html.dataset.theme = 'dark';
                localStorage.setItem("pref-theme", 'dark');
                updateGiscusTheme('dark');
            }
        });
    }

    function updateGiscusTheme(theme) {
        const iframe = document.querySelector('iframe.giscus-frame');
        if (!iframe) return;
        iframe.contentWindow.postMessage(
            { giscus: { setConfig: { theme: theme === 'dark' ? 'transparent_dark' : 'light' } } },
            'https://giscus.app'
        );
    }

    document.querySelectorAll('pre > code').forEach((codeblock) => {
        const container = codeblock.parentNode.parentNode;
        const copybutton = document.createElement('button');
        copybutton.classList.add('copy-code');
        copybutton.innerHTML = 'copy';

        function copyingDone() {
            copybutton.innerHTML = 'copied!';
            setTimeout(() => { copybutton.innerHTML = 'copy'; }, 2000);
        }

        copybutton.addEventListener('click', (cb) => {
            if ('clipboard' in navigator) {
                navigator.clipboard.writeText(codeblock.textContent);
                copyingDone();
                return;
            }
            const range = document.createRange();
            range.selectNodeContents(codeblock);
            const selection = window.getSelection();
            selection.removeAllRanges();
            selection.addRange(range);
            try {
                document.execCommand('copy');
                copyingDone();
            } catch (e) { };
            selection.removeRange(range);
        });

        if (container.classList.contains("highlight")) {
            container.appendChild(copybutton);
        } else if (container.parentNode.firstChild == container) {
        } else if (codeblock.parentNode.parentNode.parentNode.parentNode.parentNode.nodeName == "TABLE") {
            codeblock.parentNode.parentNode.parentNode.parentNode.parentNode.appendChild(copybutton);
        } else {
            codeblock.parentNode.appendChild(copybutton);
        }
    });

    // --- Instant Page Prefetching (P0) ---
    const prefetchTimers = new Map();
    const prefetchedUrls = new Set();

    function prefetchLink(url) {
        if (prefetchedUrls.has(url)) return;
        prefetchedUrls.add(url);
        const link = document.createElement("link");
        link.rel = "prefetch";
        link.href = url;
        document.head.appendChild(link);
    }

    document.addEventListener("mouseover", function(e) {
        const anchor = e.target.closest("a");
        if (!anchor || !anchor.href) return;

        const url = new URL(anchor.href, window.location.origin);
        if (url.origin !== window.location.origin) return;
        if (url.hash && url.pathname === window.location.pathname) return;
        if (url.pathname.match(/\.(xml|zip|pdf|docx|png|jpg|jpeg|gif|svg|mp4|webm)$/i)) return;

        const targetUrl = url.pathname + url.search;
        if (prefetchedUrls.has(targetUrl)) return;

        const timer = setTimeout(() => {
            prefetchLink(targetUrl);
            prefetchTimers.delete(anchor);
        }, 80);
        prefetchTimers.set(anchor, timer);
    }, { passive: true });

    document.addEventListener("mouseout", function(e) {
        const anchor = e.target.closest("a");
        if (!anchor) return;
        if (prefetchTimers.has(anchor)) {
            clearTimeout(prefetchTimers.get(anchor));
            prefetchTimers.delete(anchor);
        }
    }, { passive: true });

    document.addEventListener("touchstart", function(e) {
        const anchor = e.target.closest("a");
        if (!anchor || !anchor.href) return;
        const url = new URL(anchor.href, window.location.origin);
        if (url.origin !== window.location.origin) return;
        if (url.hash && url.pathname === window.location.pathname) return;
        if (url.pathname.match(/\.(xml|zip|pdf|docx|png|jpg|jpeg|gif|svg|mp4|webm)$/i)) return;

        const targetUrl = url.pathname + url.search;
        prefetchLink(targetUrl);
    }, { passive: true });

    // Register Service Worker for PWA
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/sw.js')
                .then(reg => console.log('Service Worker registered successfully:', reg.scope))
                .catch(err => console.error('Service Worker registration failed:', err));
        });
    }
});
