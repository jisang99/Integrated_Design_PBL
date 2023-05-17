// 진행상황 바
const buttons = document.querySelectorAll(".selectButton");

buttons.forEach((button) => {
  button.addEventListener("click", () => {
    buttons.forEach((btn) => {
      btn.classList.remove("selected");
    });
    button.classList.add("selected");
  });
});

// 다음으로 넘어가도록
let nextButton = document.querySelector(".nextButton");

nextButton.addEventListener("click", function () {
  window.location.href = "../2페이지/filter2.html";
});


// 이전으로 넘어가도록
let preButton = document.querySelector(".preButton");

preButton.addEventListener("click", function () {
  window.location.href = "";
});