let cards = [];
let currentIndex = 0;

const cardConfig = {
  "Moon today": {
    image: "img/moon.avif",
    dataPath: ["moon_today", "moon_today"],
    formatter: (data) => {
      return `${data.current_time}\n🌙 Phase: ${data.moon_phase_tonight}\nNew Moon: ${data.new_moon}\nFirst Quarter: ${data.first_quarter}`;
    }
  },
  "Moon Phase Dream Dictionary": {
    image: "img/Boho-Moon.avif", 
    dataPath: ["moon_dream", "moon_dream"],
    formatter: (data) => {
      return data.dream_interpretation_translated || "Loading dream interpretation...";
    }
  },
  "Daily inspiration": {
    image: "img/Aesthetic-hands.avif",
    dataPath: ["inspiration", "inspiration"],
    formatter: (data) => {
      return `${data.content}\n\n${data.author}`;
    }
  }
};

async function loadMoonData() {
  try {
    console.log("🌙 Loading moon data...");
    
    const response = await fetch('artifacts/moon_data_processed.json');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log("✅ Moon data loaded successfully");
    
    cards = Object.entries(cardConfig).map(([title, config]) => {
      let cardData = data;
      for (const key of config.dataPath) {
        cardData = cardData[key];
      }
      
      return {
        title: title,
        content: config.formatter(cardData),
        image: config.image
      };
    });
    
    updateCard();
    
  } catch (error) {
    console.error("❌ Error loading moon data:", error);
    
    cards = [
      {
        title: "Moon today",
        content: "Unable to load current moon data. Please try refreshing the page.",
        image: "img/moon.avif"
      },
      {
        title: "Moon Phase Dream Dictionary", 
        content: "Unable to load dream interpretation. Please try refreshing the page.",
        image: "img/Boho-Moon.avif"
      },
      {
        title: "Daily inspiration",
        content: "Unable to load daily inspiration. Please try refreshing the page.",
        image: "img/Aesthetic-hands.avif"
      }
    ];
    updateCard();
  }
}

function updateCard() {
  const titleElement = document.getElementById("card-title");
  const contentElement = document.getElementById("card-content");
  const imageElement = document.getElementById("card-image");
  
  if (titleElement && contentElement && cards.length > 0 && cards[currentIndex]) {
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
  if (cards.length > 0) {
    currentIndex = (currentIndex + 1) % cards.length;
    updateCard();
  }
}

function prevCard() {
  if (cards.length > 0) {
    currentIndex = (currentIndex - 1 + cards.length) % cards.length;
    updateCard();
  }
}

document.addEventListener('DOMContentLoaded', function() {
  loadMoonData();
  
  document.addEventListener('keydown', function(event) {
    if (event.key === 'ArrowLeft') {
      prevCard();
    } else if (event.key === 'ArrowRight') {
      nextCard();
    }
  });
});
