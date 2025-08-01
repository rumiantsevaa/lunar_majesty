const cards = [
  {
    title: "Moon today",
    content: "Aug 1, 2025\n\ud83c\udf19 Phase: Waxing Crescent\nNew Moon: Jul 24, 2025\nFirst Quarter: Aug 1, 2025",
    image: "img/moon.avif"
  },
  {
    title: "Moon Phase Dream Dictionary", 
    content: "Dreams of these days can show an internal conflict hidden in the human subconscious, and in its character. They can be unpleasant and even terrible, but this only indicates the problems that are hidden in your subconscious and, as a rule, are due to your karmic tasks that need to be resolved. Power the energy of the day is difficult, then dreams may not be aim The meaning of the images that appeared on this day in a dream. Just analyze the dream, and either remove useful information, or discard and forget the dream with the words: \u2018where is the night, there and dreams. Good dreams can even come true.",
    image: "img/Boho-Moon.avif"
  },
  {
    title: "Daily inspiration",
    content: "Do what you have to do. Just go ahead and get it done.\n\nThough you\u2019re not looking forward to it, you\u2019ll get through it. Though it\u2019s not your ideal activity, it\u2019s not the end of the world.\n\nThink of how great you\u2019ll feel to have it behind you. Imagine the confidence and sense of satisfaction you\u2019ll gain by making it happen.\n\nThose positive outcomes can be a part of your life very soon. All it takes is for you to do what you have to do.\n\nLet go of the resentment, don\u2019t concern yourself about whether it\u2019s fair or not. Simply take one action after another and get it done.\n\nYou\u2019ve put it off long enough, the excuses have run out, and now you can finally be done with it. Get to work now and get it done.\n\n\u2014 \u2014 Ralph Marston",
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