(function () {
  var lb, stage, strip, counter, titleEl, list = [], idx = 0;

  function build() {
    lb = document.createElement("div");
    lb.className = "lb";
    lb.innerHTML =
      '<div class="lb-bar"><b class="lb-title"></b><button class="lb-close">关闭 ESC</button></div>' +
      '<div class="lb-stage"><img alt=""></div>' +
      '<div class="lb-foot"><button class="lb-btn lb-prev" aria-label="上一张">←</button>' +
      '<div class="thumbstrip"></div>' +
      '<button class="lb-btn lb-next" aria-label="下一张">→</button></div>';
    document.body.appendChild(lb);
    stage = lb.querySelector(".lb-stage img");
    strip = lb.querySelector(".thumbstrip");
    counter = lb.querySelector(".lb-bar b");
    titleEl = counter;
    lb.querySelector(".lb-close").addEventListener("click", close);
    lb.querySelector(".lb-prev").addEventListener("click", function () { go(idx - 1); });
    lb.querySelector(".lb-next").addEventListener("click", function () { go(idx + 1); });
    lb.addEventListener("click", function (e) { if (e.target === lb || e.target.className === "lb-stage") close(); });
    document.addEventListener("keydown", function (e) {
      if (!lb || !lb.classList.contains("on")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") go(idx - 1);
      if (e.key === "ArrowRight") go(idx + 1);
    });
    var sx = 0;
    lb.addEventListener("touchstart", function (e) { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener("touchend", function (e) {
      var dx = e.changedTouches[0].clientX - sx;
      if (Math.abs(dx) > 50) go(idx + (dx < 0 ? 1 : -1));
    }, { passive: true });
  }

  function render() {
    stage.src = list[idx];
    counter.textContent = (idx + 1) + " / " + list.length + (list.title ? "　" + list.title : "");
    var thumbs = strip.children;
    for (var i = 0; i < thumbs.length; i++) {
      if (i === idx) thumbs[i].setAttribute("aria-current", "true");
      else thumbs[i].removeAttribute("aria-current");
    }
    var cur = thumbs[idx];
    if (cur && cur.scrollIntoView) cur.scrollIntoView({ block: "nearest", inline: "center", behavior: "smooth" });
  }

  function go(i) {
    if (!list.length) return;
    idx = (i + list.length) % list.length;
    render();
  }

  function open(images, start, title) {
    if (!lb) build();
    list = images.slice();
    list.title = title || "";
    strip.innerHTML = "";
    images.forEach(function (src, i) {
      var t = document.createElement("img");
      t.src = src;
      t.alt = "";
      t.loading = "lazy";
      t.addEventListener("click", function () { go(i); });
      strip.appendChild(t);
    });
    idx = start || 0;
    lb.classList.add("on");
    document.body.style.overflow = "hidden";
    render();
  }

  function close() {
    lb.classList.remove("on");
    document.body.style.overflow = "";
  }

  window.Lightbox = { open: open, close: close };

  document.addEventListener("click", function (e) {
    var card = e.target.closest("[data-images]");
    if (card) {
      e.preventDefault();
      var imgs = JSON.parse(card.getAttribute("data-images"));
      open(imgs, 0, card.getAttribute("data-title") || "");
      return;
    }
    var single = e.target.closest("[data-image]");
    if (single) {
      e.preventDefault();
      open([single.getAttribute("data-image")], 0, single.getAttribute("data-title") || "");
      return;
    }
    var play = e.target.closest(".vcard .frame");
    if (play && !play.querySelector("video")) {
      var src = play.getAttribute("data-src");
      var poster = play.getAttribute("data-poster");
      var v = document.createElement("video");
      v.src = src;
      v.poster = poster || "";
      v.controls = true;
      v.autoplay = true;
      v.playsInline = true;
      v.setAttribute("playsinline", "");
      play.innerHTML = "";
      play.style.cursor = "default";
      play.appendChild(v);
    }
  });

  document.addEventListener("DOMContentLoaded", function () {
    var bar = document.querySelector(".topbar");
    if (bar && !bar.querySelector(".theme-btn")) {
      var b = document.createElement("button");
      b.className = "theme-btn";
      b.type = "button";
      b.setAttribute("aria-label", "切换明暗主题");
      b.innerHTML =
        '<svg class="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>' +
        '<svg class="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>';
      b.addEventListener("click", function () {
        var next = document.documentElement.getAttribute("data-theme") === "light" ? "dark" : "light";
        document.documentElement.setAttribute("data-theme", next);
        try { localStorage.setItem("vh-theme", next); } catch (e) {}
      });
      bar.appendChild(b);
    }
    var w = window.WORKS || {};
    document.querySelectorAll("[data-stat]").forEach(function (el) {
      var k = el.getAttribute("data-stat");
      if (w.stats && w.stats[k] != null) el.textContent = w.stats[k];
    });
  });
})();
