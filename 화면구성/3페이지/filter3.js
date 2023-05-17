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
  window.location.href = "../4페이지/filter4.html";
});

let preButton = document.querySelector(".preButton");

preButton.addEventListener("click", function () {
  window.location.href = "../2페이지/filter2.html";
});
