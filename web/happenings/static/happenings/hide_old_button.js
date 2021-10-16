function myFunction(elemID) {
  var x = document.getElementById(elemID);
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}