const cards = [
  {
    title: "Moon today",
    content: "Jul 30, 2025\n\ud83c\udf19 Phase: Waxing Crescent\nNew Moon: Jul 24, 2025\nFirst Quarter: Aug 1, 2025",
    image: "img/moon.avif"
  },
  {
    title: "Moon Phase Dream Dictionary", 
    content: "Dreams on this day can bring useful information, there are even prophetic information. Can come true, but not  \nsoon.\nIn these dreams there may be tips that will help interpret the meaning of your life. As a rule \nThese tips are clear, and clearly show your situation, your tasks, goals. Particular attention  \nTurn to the words that will be uttered in a dream. It is through words that day that the subconscious mind communicates with us. Words heard in a dream, preferably recorded, and during the seventh lunar  \nFor a day to observe what you hear from others, you can visit the insight from what you heard. On this day, in a dream you can get a revelation through words from the Higher Forces, you may come to the highest image, everything that you hear from them will certainly be a direct indication of the action.\nIf in a dream you see a combat rooster, be attentive to life situations.\nIf you have a bad dream, then tell the running water about its content, then everything bad will leave, \nAnd the good will come close.",
    image: "img/Boho-Moon.avif"
  },
  {
    title: "Daily inspiration",
    content: "You can make a difference in the way this day unfolds. You can make a difference for how tomorrow turns out.\n\nYou can make a difference for yourself. You can make a difference in the lives of others.\n\nEverything you choose to engage in brings consequences. You have the opportunity to make those consequences the best they can be.\n\nYou have the ability to make a positive difference in the space that\u2019s right in front of you. You\u2019re also able to have a positive impact on certain situations far away in time and location.\n\nWhat you do matters, in all sorts of ways. So be sure to put your love, your best considerations, and your highest truth into it.\n\nYou can make a difference, and you do make a difference all the time. Keep up the great work, and continue being a positive force in your world.\n\n\u2014 \u2014 Ralph Marston",
    image: "img/Aesthetic-hands.avif"
  }
];

let currentIndex = 0;

function updateCard() {
  const titleElement = document.getElementById("card-title");
  const contentElement = document.getElementById("card-content");
  const imageElement = document.getElementById("card-image");
  
  if (titleElement && contentElement && cards[currentIndex]) {
    titleElement.textContent = cards[currentIndex].title;
    contentElement.innerHTML = cards[currentIndex].content.replace(/\n/g, '<br>');
    
    // Обновляем картинку
    if (imageElement && cards[currentIndex].image) {
      imageElement.src = cards[currentIndex].image;
      imageElement.alt = cards[currentIndex].title;
      imageElement.classList.remove('hidden');
      // Скрываем картинку при ошибке загрузки
      imageElement.onerror = function() {
        this.classList.add('hidden');
      };
    }
    
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

document.addEventListener('DOMContentLoaded', function() {
  updateCard();
  
  document.addEventListener('keydown', function(event) {
    if (event.key === 'ArrowLeft') {
      prevCard();
    } else if (event.key === 'ArrowRight') {
      nextCard();
    }
  });
});