const buttons = document.querySelectorAll(".selectButton");

buttons.forEach((button) => {
  button.addEventListener("click", () => {
    buttons.forEach((btn) => {
      btn.classList.remove("selected");
    });
    button.classList.add("selected");
  });
});


let nextButton = document.querySelector(".nextButton");

nextButton.addEventListener("click", function () {
  window.location.href = "../9페이지/recommend.html";
});


let preButton = document.querySelector(".preButton");

preButton.addEventListener("click", function () {
  window.location.href = "../7페이지/filter7.html";
});