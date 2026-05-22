function toggleRoleFields() {
  const role = document.getElementById("role-select")?.value;
  document.querySelectorAll(".field-student").forEach((el) => {
    el.style.display = role === "student" ? "grid" : "none";
  });
  document.querySelectorAll(".field-university").forEach((el) => {
    el.style.display = ["student", "teacher", "university"].includes(role) ? "grid" : "none";
  });
}

document.getElementById("role-select")?.addEventListener("change", toggleRoleFields);
toggleRoleFields();