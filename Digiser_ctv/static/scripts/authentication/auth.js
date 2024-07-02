function validateNumberInput(event) {
  // Chỉ nhận số
  const key = event.key;
  if (
    !/^\d$/.test(key) &&
    key !== "Backspace" &&
    key !== "ArrowLeft" &&
    key !== "ArrowRight" &&
    key !== "Delete"
  ) {
    event.preventDefault();
  }
}
