document.addEventListener('DOMContentLoaded',()=>{const t=document.querySelector('.menu-toggle'),m=document.querySelector('#mobile-menu');if(t&&m)t.addEventListener('click',()=>{const o=t.getAttribute('aria-expanded')==='true';t.setAttribute('aria-expanded',String(!o));m.hidden=o});const p=new URLSearchParams(location.search).get('interest'),s=document.querySelector('#interest-select');if(p&&s){const x=[...s.options].find(o=>o.value===p);if(x)s.value=p}});
document.addEventListener("DOMContentLoaded", () => {
  const slides = Array.from(document.querySelectorAll(".testimonial-slide"));
  if (slides.length > 1) {
    let current = 0;
    setInterval(() => {
      slides[current].classList.remove("active");
      current = (current + 1) % slides.length;
      slides[current].classList.add("active");
    }, 6000);
  }

  document.querySelectorAll(".accordion-toggle").forEach((button) => {
    button.addEventListener("click", () => {
      const panel = button.nextElementSibling;
      const expanded = button.getAttribute("aria-expanded") === "true";
      button.setAttribute("aria-expanded", String(!expanded));
      const marker = button.querySelector("span");
      if (marker) marker.textContent = expanded ? "+" : "−";
      if (panel) panel.hidden = expanded;
    });
  });
});
