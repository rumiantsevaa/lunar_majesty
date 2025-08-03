const cards = [
  {
    title: "Moon today",
    content: "Aug 3, 2025\n\ud83c\udf19 Phase: Waxing Gibbous\nNew Moon: \u2014\nFirst Quarter: Aug 1, 2025",
    image: "img/moon.avif"
  },
  {
    title: "Moon Phase Dream Dictionary", 
    content: "The dreams of these lunar days, as a rule, show how harmoniously we move in the material and spiritual world.\nThe images that you are clearly expressed quite clearly your position at the moment. If the dream is good and you act in a positive role, then your development is in the right direction. If you act as you are causing troubles, or you yourself cause them, then in life somewhere you act incorrectly, or your spiritual world is in desolation.\nGood dreams of these lunar days Fortunately. They can carry useful information, be common, and, as a rule, are executed.\nSometimes they say that the dream that you had to go that night may come true in 3 days.\nSometimes at this time you may not see dreams, then life gives you the opportunity to just relax, since the day itself is not the lightest and very energy.",
    image: "img/Boho-Moon.avif"
  },
  {
    title: "Daily inspiration",
    content: "No matter how much you\u2019ve accomplished before, live and act today as if you\u2019re starting fresh. The great work you\u2019ve already done doesn\u2019t give you an excuse to take anything for granted.\n\nSure, you have skills, experiences, and connections that are priceless. Yet their value will quickly deteriorate if you fail to maintain and create new value with them.\n\nNo achievement gives you permission to hold off on achieving anything further. Indeed, every achievement obligates you to bring even more goodness to life.\n\nIt\u2019s easy to get arrogant about what you\u2019ve accomplished. But it\u2019s a whole lot more useful, to yourself and others, when you can be humbled by the good things you\u2019ve done.\n\nCertainly achievement provides you lots of advantages. Employ those advantages to tackle even greater challenges, not to hide from your potential.\n\nYou\u2019ve done some great things, and that\u2019s wonderful. Now is your chance to start fresh, and do much more.\n\n\u2014 \u2014 Ralph Marston",
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
    
    if (imageElement && cards[currentIndex].image) {
      imageElement.src = cards[currentIndex].image;
      imageElement.alt = cards[currentIndex].title;
      imageElement.classList.remove('hidden');
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