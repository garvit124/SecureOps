// Form validation
document.addEventListener("DOMContentLoaded", function () {
  // Auto-dismiss alerts after 5 seconds
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach((alert) => {
    setTimeout(() => {
      alert.style.opacity = "0";
      setTimeout(() => alert.remove(), 300);
    }, 5000);
  });

  // Search functionality for tables
  const searchInputs = document.querySelectorAll(".search-input");
  searchInputs.forEach((input) => {
    input.addEventListener("input", function () {
      const searchTerm = this.value.toLowerCase();
      const table = this.closest(".card").querySelector("table tbody");
      const rows = table.querySelectorAll("tr");

      rows.forEach((row) => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchTerm) ? "" : "none";
      });
    });
  });

  // Confirm before checkout/delete actions
  const confirmButtons = document.querySelectorAll("[data-confirm]");
  confirmButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      const message = this.getAttribute("data-confirm");
      if (!confirm(message)) {
        e.preventDefault();
      }
    });
  });

  // Real-time clock
  function updateClock() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    const dateString = now.toLocaleDateString();

    const clockElements = document.querySelectorAll(".live-clock");
    clockElements.forEach((el) => {
      el.textContent = `${dateString} ${timeString}`;
    });
  }

  if (document.querySelector(".live-clock")) {
    updateClock();
    setInterval(updateClock, 1000);
  }

  // Form validation
  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    form.addEventListener("submit", function (e) {
      const requiredFields = form.querySelectorAll("[required]");
      let isValid = true;

      requiredFields.forEach((field) => {
        if (!field.value.trim()) {
          isValid = false;
          field.style.borderColor = "var(--danger-color)";
        } else {
          field.style.borderColor = "var(--border-color)";
        }
      });

      if (!isValid) {
        e.preventDefault();
        alert("Please fill in all required fields");
      }
    });
  });

  // Contact number validation
  const contactInputs = document.querySelectorAll('input[name="contact"]');
  contactInputs.forEach((input) => {
    input.addEventListener("input", function () {
      this.value = this.value.replace(/[^0-9+]/g, "");
    });
  });

  // Print functionality
  const printButtons = document.querySelectorAll(".btn-print");
  printButtons.forEach((button) => {
    button.addEventListener("click", function () {
      window.print();
    });
  });

  // Export to CSV functionality
  const exportButtons = document.querySelectorAll(".btn-export");
  exportButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const table = this.closest(".card").querySelector("table");
      if (table) {
        exportTableToCSV(table, "export.csv");
      }
    });
  });
});

// Export table to CSV
function exportTableToCSV(table, filename) {
  const rows = table.querySelectorAll("tr");
  const csv = [];

  rows.forEach((row) => {
    const cols = row.querySelectorAll("td, th");
    const rowData = [];
    cols.forEach((col) => {
      rowData.push('"' + col.textContent.trim() + '"');
    });
    csv.push(rowData.join(","));
  });

  const csvContent = csv.join("\n");
  const blob = new Blob([csvContent], { type: "text/csv" });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  window.URL.revokeObjectURL(url);
}

// Filter functionality
function filterTable(selectElement, columnIndex) {
  const table = selectElement.closest(".card").querySelector("table tbody");
  const rows = table.querySelectorAll("tr");
  const filterValue = selectElement.value.toLowerCase();

  rows.forEach((row) => {
    const cell = row.querySelectorAll("td")[columnIndex];
    if (!filterValue || cell.textContent.toLowerCase().includes(filterValue)) {
      row.style.display = "";
    } else {
      row.style.display = "none";
    }
  });
}

// Refresh data
function refreshData() {
  location.reload();
}

// Toggle mobile menu
function toggleMenu() {
  const menu = document.querySelector(".navbar-menu");
  menu.classList.toggle("active");
}
