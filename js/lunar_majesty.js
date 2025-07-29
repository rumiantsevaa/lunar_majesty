const cards = [
  {
    title: "Moon today",
    content: "Loading"
  },
  {
    title: "Moon Phase Dream Dictionary",
    content: "Loading"
  },
  {
    title: "Daily inspiration",
    content: "Loading"
  }
];

let currentIndex = 0;

function updateCard() {
  document.getElementById("card-title").textContent = cards[currentIndex].title;
  document.getElementById("card-content").textContent = cards[currentIndex].content;
}

function nextCard() {
  currentIndex = (currentIndex + 1) % cards.length;
  updateCard();
}

function prevCard() {
  currentIndex = (currentIndex - 1 + cards.length) % cards.length;
  updateCard();
}
