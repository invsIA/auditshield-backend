fetch("https://auditshield-backend.onrender.com/")
  .then(response => response.json())
  .then(data => {
    document.body.innerHTML += `<h1>${data.message}</h1>`;
  });
