function toggleCategory() {
    var fictionCategories = document.getElementById("fiction-categories");
    var nonfictionCategories = document.getElementById("nonfiction-categories");
    var toggleBtn = document.querySelector(".toggle-btn");
  
    if (fictionCategories.style.display === "none") {
      fictionCategories.style.display = "block";
      nonfictionCategories.style.display = "none";
      toggleBtn.textContent = "Ficción";
    } else {
      fictionCategories.style.display = "none";
      nonfictionCategories.style.display = "block";
      toggleBtn.textContent = "No Ficción";
    }
  }
  
  function toggleCategory2() {
    var fictionCategories = document.getElementById("fiction-categories");
    var nonfictionCategories = document.getElementById("nonfiction-categories");
    var toggleBtn = document.querySelector(".toggle-btn");
  
    if (nonfictionCategories.style.display === "none") {
      nonfictionCategories.style.display = "block";
      fictionCategories.style.display = "none";
      toggleBtn.textContent = "No Ficción";
    } else {
      nonfictionCategories.style.display = "none";
      fictionCategories.style.display = "block";
      toggleBtn.textContent = "Ficción";
    }
  }