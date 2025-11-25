document.addEventListener('DOMContentLoaded', function() {
  // profile click now handled by normal link behavior in templates

  // Simple placeholder: focus search input on click of icon
  const searchIcon = document.querySelector('.search-icon');
  const searchInput = document.querySelector('.search-input input');
  if (searchIcon && searchInput) {
    searchIcon.addEventListener('click', function() { searchInput.focus(); });
  }
});

    // ---- Эффект печатания текста ----
    const element = document.getElementById('typewriter');
    const texts = [
      'Ваши нейро планы',
      'Планируйте всё, что хотите',
      'Достигайте целей с помощью нейросети'
    ];

    let textIndex = 0;
    let charIndex = 0;
    let isDeleting = false;

    const typedSpan = document.createElement('span');
    typedSpan.className = 'typed';
    const cursorSpan = document.createElement('span');
    cursorSpan.className = 'cursor';
    cursorSpan.textContent = '|';

    element.appendChild(typedSpan);
    element.appendChild(cursorSpan);

    function updateText() {
      const current = texts[textIndex];
      typedSpan.textContent = current.substring(0, charIndex);
    }

    function type() {
      updateText();

      if (!isDeleting && charIndex < texts[textIndex].length) {
        charIndex++;
        setTimeout(type, 100);
      } else if (isDeleting && charIndex > 0) {
        charIndex--;
        setTimeout(type, 50);
      } else if (!isDeleting && charIndex === texts[textIndex].length) {
        isDeleting = true;
        setTimeout(type, 1500);
      } else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        textIndex = (textIndex + 1) % texts.length;
        setTimeout(type, 500);
      }
    }

    type();

