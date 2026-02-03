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
