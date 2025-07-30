const cards = [
  {
    title: "Moon today",
    content: "Loading current moon phase and celestial information..."
  },
  {
    title: "Moon Phase Dream Dictionary", 
    content: "Loading dream interpretations based on lunar cycles..."
  },
  {
    title: "Daily inspiration",
    content: "Loading cosmic wisdom and daily inspiration..."
  }
];

let currentIndex = 0;

function updateCard() {
  const titleElement = document.getElementById("card-title");
  const contentElement = document.getElementById("card-content");
  
  if (titleElement && contentElement && cards[currentIndex]) {
    titleElement.textContent = cards[currentIndex].title;
    
    // Поддерживаем HTML разметку в контенте (переносы строк)
    contentElement.innerHTML = cards[currentIndex].content.replace(/\n/g, '<br>');
    
    // Добавляем плавный эффект при смене карточки
    const card = document.getElementById("carousel-card");
    card.style.opacity = '0.7';
    setTimeout(() => {
      card.style.opacity = '1';
    }, 200);
  }
}

function nextCard() {
  currentIndex = (currentIndex + 1) % cards.length;
  updateCard();
}

function prevCard() {
  currentIndex = (currentIndex - 1 + cards.length) % cards.length;
  updateCard();
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
  updateCard();
  
  // Поддержка клавиатуры
  document.addEventListener('keydown', function(event) {
    if (event.key === 'ArrowLeft') {
      prevCard();
    } else if (event.key === 'ArrowRight') {
      nextCard();
    }
  });
  
  // Индикатор активной карточки (опционально)
  updateCardIndicator();
});

function updateCardIndicator() {
  // Можно добавить визуальные индикаторы для карточек
  console.log(`Active card: ${currentIndex + 1}/${cards.length}`);
}
