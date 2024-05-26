const form = document.getElementById('copy-form');
const generatedCopyDiv = document.getElementById('generated-copy');

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const formData = new FormData(form);
  const propertyType = formData.get('propertyType');
  const location = formData.get('location');
  const targetAudience = formData.get('targetAudience') || '';  // Handle optional field

  const response = await fetch('/generate-copy', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      propertyType,
      location,
      targetAudience
    })
  });

  if (!response.ok) {
    generatedCopyDiv.textContent = 'Error generating copy. Please try again later.';
    return;
  }

  const data = await response.json();
  generatedCopyDiv.textContent = data.copy;
});
