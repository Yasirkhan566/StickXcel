// Function to implement auto type text effect
// Function to implement auto type text effect
function autoType(element, lines, delayBetweenLines, charDelay) {
  let currentLineIndex = 0;
  let currentCharIndex = 0;

  function typeLine() {
    const currentLine = lines[currentLineIndex];
    element.innerHTML = currentLine.substr(0, currentCharIndex);
    currentCharIndex++;

    if (currentCharIndex > currentLine.length) {
      setTimeout(() => {
        eraseLine();
      }, delayBetweenLines);
    } else {
      setTimeout(typeLine, charDelay);
    }
  }

  function eraseLine() {
    const currentLine = lines[currentLineIndex];
    element.innerHTML = currentLine.substr(0, currentCharIndex);
    currentCharIndex--;

    if (currentCharIndex < 0) {
      currentLineIndex = (currentLineIndex + 1) % lines.length;
      setTimeout(typeLine, charDelay);
    } else {
      setTimeout(eraseLine, charDelay);
    }
  }

  typeLine();
}

// Function to implement image slider
function imageSlider() {
  const images = document.querySelectorAll(".image-slider img");
  let index = 0;

  function showImage(indexToShow) {
    images.forEach((img, i) => {
      if (i === indexToShow) {
        img.classList.add("active");
      } else {
        img.classList.remove("active");
      }
    });
  }

  setInterval(() => {
    showImage(index);
    index = (index + 1) % images.length;
  }, 4000);
}

function logosSlider() {
  const logosContainer = document.querySelector(".logos-container");
  const logos = logosContainer.querySelectorAll("img");
  const numVisibleLogos = 4; // Number of logos visible at a time
  const animationDuration = 20000; // Duration of animation in milliseconds

  const totalLogoWidth = 100 + 50; // Width of each logo + margin (adjust as needed)

  let currentIndex = 0;

  function updateLogosPosition() {
    const offset = -(currentIndex * totalLogoWidth);
    logosContainer.style.transform = `translateX(${offset}px)`;
  }

  function slideLogos() {
    currentIndex = (currentIndex + 1) % (logos.length / 2); // Divide by 2 since we have duplicate logos
    updateLogosPosition();
  }

  setInterval(slideLogos, animationDuration / numVisibleLogos);
  updateLogosPosition();
}

// Call the logosSlider function when the DOM content is loaded
document.addEventListener("DOMContentLoaded", logosSlider);


function addHoverEffect() {
  const serviceImages = document.querySelectorAll(".service-img");
  serviceImages.forEach((img) => {
    img.addEventListener("mouseover", () => {
      img.style.transform = "scale(1.1)";
    });
    img.addEventListener("mouseout", () => {
      img.style.transform = "scale(1)";
    });
  });
}

// Function to display client reviews


// Event listener for Join Us button
const joinButton = document.querySelector(".join-btn");
joinButton.addEventListener("click", () => {
  // Replace with your join us functionality (e.g., open a modal, redirect to a page, etc.)
  alert("Join Us button clicked!");
});

// JavaScript to toggle the menu icon and navigation links
document.addEventListener("DOMContentLoaded", function () {
  const menuIcon = document.querySelector(".menu-icon");
  const navLinks = document.querySelector(".nav-links");

  menuIcon.addEventListener("click", function () {
    navLinks.classList.toggle("show");
  });
});








// Call the functions when the DOM content is loaded
document.addEventListener("DOMContentLoaded", () => {
  // Auto type effect for the h2 element
  const autoTypeElement = document.querySelector(".auto-text h2");
  const lines = [
    "Welcome to StitchXcel..",
    "The Best Online tailor services..",
    "Pick your favourite tailor..",
    "24/7 available for services..",
    // Add more lines as needed
  ];
  const delayBetweenLines = 1000; // Delay between lines in milliseconds
  const charDelay = 60; // Delay between characters in milliseconds
 
  autoType(autoTypeElement, lines, delayBetweenLines, charDelay);


  // Start the image slider
  imageSlider();

  // // Start the logos slider
  logosSlider();

  // Add hover effect to service images

  // Display client reviews

});


