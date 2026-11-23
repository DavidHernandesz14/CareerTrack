
let allApplications = [];
let editingApplicationId = null;

const form = document.getElementById("application-form");
const submitButton = form.querySelector('button[type="submit"]');
const formHeading = form.parentElement.querySelector("h2");

// Create the Cancel Edit button
const cancelButton = document.createElement("button");
cancelButton.type = "button";
cancelButton.textContent = "Cancel Edit";
cancelButton.style.backgroundColor = "#64748b";
cancelButton.style.display = "none";
form.appendChild(cancelButton);


// -------------------------
// LOAD APPLICATIONS
// -------------------------

async function loadApplications() {
  const container = document.getElementById("applications-container");

  try {
    const response = await fetch("/applications");

    if (!response.ok) {
      throw new Error("Failed to load applications");
    }

    allApplications = await response.json();

    updateStatistics();
    updateChart();
    displayApplications();

  } catch (error) {
    console.error(error);
    container.textContent = "Unable to load applications.";
  }
}


// -------------------------
// STATISTICS
// -------------------------

function updateStatistics() {
  document.getElementById("total-count").textContent =
    allApplications.length;

  document.getElementById("applied-count").textContent =
    allApplications.filter(app => app.status === "Applied").length;

  document.getElementById("interview-count").textContent =
    allApplications.filter(app => app.status === "Interview").length;

  document.getElementById("offer-count").textContent =
    allApplications.filter(app => app.status === "Offer").length;
}


// -------------------------
// STATUS CHART
// -------------------------

function updateChart() {
  const chart = document.getElementById("status-chart");
  chart.innerHTML = "";

  const statuses = [
    "Saved",
    "Applied",
    "Interview",
    "Offer",
    "Rejected"
  ];

  const total = allApplications.length;

  statuses.forEach(status => {
    const count = allApplications.filter(
      app => app.status === status
    ).length;

    const percentage = total > 0
      ? (count / total) * 100
      : 0;

    const row = document.createElement("div");
    row.className = "chart-row";

    const label = document.createElement("span");
    label.className = "chart-label";
    label.textContent = status;

    const track = document.createElement("div");
    track.className = "chart-track";

    const bar = document.createElement("div");
    bar.className = "chart-bar";
    bar.style.width = `${percentage}%`;

    track.appendChild(bar);

    const value = document.createElement("span");
    value.className = "chart-value";
    value.textContent = count;

    row.append(label, track, value);
    chart.appendChild(row);
  });
}


// -------------------------
// SORT APPLICATIONS
// -------------------------

function sortApplications(applications) {
  const sortBy = document.getElementById("sort-select").value;

  const sorted = [...applications];

  const compareDate = (a, b, newestFirst) => {
    // Applications without dates appear last
    if (!a.date_applied && !b.date_applied) {
      return a.id - b.id;
    }

    if (!a.date_applied) return 1;
    if (!b.date_applied) return -1;

    const comparison = a.date_applied.localeCompare(b.date_applied);

    return newestFirst ? -comparison : comparison;
  };

  switch (sortBy) {
    case "newest":
      sorted.sort((a, b) => b.id - a.id);
      break;

    case "oldest":
      sorted.sort((a, b) => a.id - b.id);
      break;

    case "company-asc":
      sorted.sort((a, b) =>
        a.company.localeCompare(b.company)
      );
      break;

    case "company-desc":
      sorted.sort((a, b) =>
        b.company.localeCompare(a.company)
      );
      break;

    case "status":
      sorted.sort((a, b) =>
        a.status.localeCompare(b.status)
      );
      break;

    case "date-newest":
      sorted.sort((a, b) => compareDate(a, b, true));
      break;

    case "date-oldest":
      sorted.sort((a, b) => compareDate(a, b, false));
      break;
  }

  return sorted;
}


// -------------------------
// DISPLAY APPLICATIONS
// -------------------------

function displayApplications() {
  const container = document.getElementById("applications-container");

  const searchTerm = document
    .getElementById("search-input")
    .value.toLowerCase().trim();

  const selectedStatus =
    document.getElementById("status-filter").value;

  container.innerHTML = "";

  if (allApplications.length === 0) {
    container.textContent = "No applications found.";
    return;
  }

  const filtered = allApplications.filter(application => {
    const matchesSearch =
      application.company.toLowerCase().includes(searchTerm) ||
      application.position.toLowerCase().includes(searchTerm);

    const matchesStatus =
      selectedStatus === "All" ||
      application.status === selectedStatus;

    return matchesSearch && matchesStatus;
  });

  if (filtered.length === 0) {
    container.textContent = "No matching applications found.";
    return;
  }

  const sortedApplications = sortApplications(filtered);

  sortedApplications.forEach(application => {
    const card = document.createElement("div");
    card.className = "application-card";

    const title = document.createElement("h3");
    title.textContent = application.company;

    const position = document.createElement("p");
    position.textContent = `Position: ${application.position}`;

    const status = document.createElement("p");
    status.textContent = `Status: ${application.status}`;

    const date = document.createElement("p");
    date.textContent =
      `Date Applied: ${application.date_applied || "Not specified"}`;

    const notes = document.createElement("p");
    notes.textContent =
      `Notes: ${application.notes || "No notes"}`;

    // EDIT BUTTON
    const editButton = document.createElement("button");
    editButton.textContent = "Edit";
    editButton.className = "edit-button";

    editButton.addEventListener("click", () => {
      startEditing(application);
    });

    // DELETE BUTTON
    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";
    deleteButton.className = "delete-button";

    deleteButton.addEventListener("click", async () => {
      const confirmed = confirm(
        `Are you sure you want to delete ${application.company}?`
      );

      if (!confirmed) return;

      try {
        const response = await fetch(
          `/applications/${application.id}`,
          { method: "DELETE" }
        );

        if (!response.ok) {
          throw new Error("Failed to delete application");
        }

        if (editingApplicationId === application.id) {
          resetForm();
        }

        await loadApplications();

      } catch (error) {
        console.error(error);
        alert("Unable to delete application.");
      }
    });

    card.append(
      title,
      position,
      status,
      date,
      notes,
      editButton,
      deleteButton
    );

    container.appendChild(card);
  });
}


// -------------------------
// START EDITING
// -------------------------

function startEditing(application) {
  editingApplicationId = application.id;

  document.getElementById("company").value =
    application.company;

  document.getElementById("position").value =
    application.position;

  document.getElementById("status").value =
    application.status;

  document.getElementById("date_applied").value =
    application.date_applied || "";

  document.getElementById("notes").value =
    application.notes || "";

  formHeading.textContent = "Edit Application";
  submitButton.textContent = "Save Changes";
  cancelButton.style.display = "block";

  form.scrollIntoView({
    behavior: "smooth",
    block: "start"
  });
}


// -------------------------
// RESET FORM
// -------------------------

function resetForm() {
  editingApplicationId = null;

  form.reset();

  formHeading.textContent = "Add New Application";
  submitButton.textContent = "Add Application";
  cancelButton.style.display = "none";
}

cancelButton.addEventListener("click", resetForm);


// -------------------------
// ADD OR UPDATE APPLICATION
// -------------------------

form.addEventListener("submit", async function(event) {
  event.preventDefault();

  const application = {
    company: document.getElementById("company").value.trim(),
    position: document.getElementById("position").value.trim(),
    status: document.getElementById("status").value,
    date_applied:
      document.getElementById("date_applied").value || null,
    notes:
      document.getElementById("notes").value.trim() || null
  };

  if (!application.company || !application.position) {
    alert("Company and position are required.");
    return;
  }

  const isEditing = editingApplicationId !== null;

  const url = isEditing
    ? `/applications/${editingApplicationId}`
    : "/applications";

  const method = isEditing ? "PUT" : "POST";

  try {
    const response = await fetch(url, {
      method,
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(application)
    });

    if (!response.ok) {
      throw new Error("Failed to save application");
    }

    resetForm();
    await loadApplications();

    alert(
      isEditing
        ? "Application updated successfully!"
        : "Application added successfully!"
    );

  } catch (error) {
    console.error(error);
    alert("Unable to save application.");
  }
});


// -------------------------
// SEARCH, FILTER AND SORT
// -------------------------

document.getElementById("search-input")
  .addEventListener("input", displayApplications);

document.getElementById("status-filter")
  .addEventListener("change", displayApplications);

document.getElementById("sort-select")
  .addEventListener("change", displayApplications);


// -------------------------
// INITIAL PAGE LOAD
// -------------------------

loadApplications();
