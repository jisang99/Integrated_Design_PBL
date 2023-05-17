const slider = document.querySelector(".slider");
const slides = document.querySelectorAll(".slide");

let touchStartX = 0;
let touchEndX = 0;

slider.addEventListener("touchstart", handleTouchStart);
slider.addEventListener("touchend", handleTouchEnd);

function handleTouchStart(event) {
  touchStartX = event.touches[0].clientX;
}

function handleTouchEnd(event) {
  touchEndX = event.changedTouches[0].clientX;
  handleSwipe();
}

function handleSwipe() {
  const swipeDistance = touchEndX - touchStartX;
  const minSwipeDistance = 50; // 최소 스와이프 거리

  if (swipeDistance > minSwipeDistance) {
    moveSlide("prev");
  } else if (swipeDistance < -minSwipeDistance) {
    moveSlide("next");
  }
}

function moveSlide(direction) {
  let slideIndex = 0;
  for (let i = 0; i < slides.length; i++) {
    if (slides[i].classList.contains("active")) {
      slideIndex = i;
      slides[i].classList.remove("active");
    }
  }

  if (direction === "prev") {
    slideIndex--;
    if (slideIndex < 0) {
      slideIndex = slides.length - 1;
    }
  } else if (direction === "next") {
    slideIndex++;
    if (slideIndex === slides.length) {
      slideIndex = 0;
    }
  }

  slides[slideIndex].classList.add("active");
  const translateValue = `translateX(-${slideIndex * 100}%)`;
  slider.style.transform = translateValue;
}
