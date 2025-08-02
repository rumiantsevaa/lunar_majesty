const cards = [
  {
    title: "Moon today",
    content: "Aug 2, 2025\n\ud83c\udf19 Phase: First Quarter\nNew Moon: \u2014\nFirst Quarter: Aug 1, 2025",
    image: "img/moon.avif"
  },
  {
    title: "Moon Phase Dream Dictionary", 
    content: "The tenth lunar day, as you know, are associated with the family and family, and sleep also reflects this principle. Therefore, in a dream, you can see relatives or spouse (spouse), children, and even ancestors of the whole kind, including spiritual ones. If in a dream you have strong kinds, or the guardian spirit-guard, be careful to what you say, or what is happening, since through this you can come to any understanding, discovery, you may have some kind of support of the genus or will be transmitted by the family, if you are ready. Dreams on these lunar days can be quite light, bright and fabulous, but they, as a rule, do not matter. An alarming dreams must be understood and either let them go with them, or work with them so that they do not overtake you in life. If you want to use the moment and work with your family or birth, before you go to bed, tune in to it, and as soon as you wake up, write everything down.",
    image: "img/Boho-Moon.avif"
  },
  {
    title: "Daily inspiration",
    content: "Give yourself something to look forward to. Give yourself something meaningful and compelling to work toward.\n\nLife can often be difficult and challenging. Make sure you have plenty of good reasons to pay the price, to push through the challenges.\n\nWhen there\u2019s a light at the end of the tunnel, every step brings you closer to that light. No matter how difficult each step may be, you can bear the difficulty because you know what\u2019s ahead.\n\nWhat do you see ahead for you, right now? Provide yourself with a brilliant, desirable light that becomes more reachable with every action.\n\nEquip yourself with a way to stay in touch with your purpose. Envision the specific details of a situation that you truly desire to inhabit.\n\nIdentify what will get you going and keep you going, and firmly insert it into your idea of the future. With something compelling to look forward to, you\u2019re certain to move forward.\n\n\u2014 \u2014 Ralph Marston",
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