const cards = [
  {
    title: "Moon today",
    content: "Jul 31, 2025\n\ud83c\udf19 Phase: Waxing Crescent\nNew Moon: Jul 24, 2025\nFirst Quarter: Aug 1, 2025",
    image: "img/moon.avif"
  },
  {
    title: "Moon Phase Dream Dictionary", 
    content: "Dreams on these lunar days indicate your capabilities that you have not implemented, but which is still worth realizing. In addition, you can see an indication of the problems from which you turned away in the past and forgot about them, but they need to be solved. You can see those tasks for which you have strength, do not turn away from them, try to attach these forces to solve the tasks and not spend energy in vain. In addition, the images of dreams at this time show you to change and transformation, if you dream of closed spaces, obstacles, dead ends and the like, then you have not changed yet. If, on the contrary, open spaces, fields, mountains, sea, beautiful rooms, bright, clean, then you go, in the right direction and make efforts to transformation. The main task of dreams on this day is to show your purpose. Sometimes dreams are intricate, and it is difficult to understand what is the meaning of your life task. Sometimes they clearly describe the whole picture. If you want your destiny to clarify through a dream, set a goal the day before.  Having woken up, analyze everything that you dreamed, and keep in mind that life does not always set us great tasks, maybe this is from your point of view and a small task, but its fulfillment will be of great importance for you.",
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