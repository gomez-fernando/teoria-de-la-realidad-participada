(() => {
  const updated = document.getElementById("updated");
  if (updated) {
    const now = new Date();
    const month = now.toLocaleString("es-ES", { month: "long" });
    const formatted = `${month} ${now.getFullYear()}`;
    updated.textContent = formatted.charAt(0).toUpperCase() + formatted.slice(1);
  }

  const cards = Array.from(document.querySelectorAll(".card"));
  if (cards.length) {
    cards.forEach((card, index) => {
      card.style.animationDelay = `${index * 0.12 + 0.15}s`;
      card.classList.add("reveal");
    });
  }
})();


  const cta = document.querySelector('a.cta[href="#contenidos"]');
  const target = document.getElementById('contenidos');
  if (cta && target) {
    const easeInOut = (t) => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2);
    cta.addEventListener('click', (event) => {
      event.preventDefault();
      const start = window.scrollY;
      const end = target.getBoundingClientRect().top + window.scrollY - 12;
      const duration = 900;
      let startTime = null;

      const step = (timestamp) => {
        if (!startTime) startTime = timestamp;
        const elapsed = timestamp - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = easeInOut(progress);
        window.scrollTo(0, start + (end - start) * eased);
        if (progress < 1) {
          window.requestAnimationFrame(step);
        }
      };

      window.requestAnimationFrame(step);
    }, { passive: false });
  }
