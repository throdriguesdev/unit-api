const API_URL = "http://localhost:8000"; // Altere para o URL real da sua API

// Função para carregar ativos
async function loadAssets() {
  try {
    const response = await fetch(`${API_URL}/assets`);
    const data = await response.json();
    const table = document.getElementById("assetsList");
    table.innerHTML = ""; // Limpa a tabela

    data.forEach(asset => {
      const row = `
                <tr>
                    <td>${asset.name}</td>
                    <td>${asset.description}</td>
                    <td>${asset.category}</td>
                    <td>${asset.status}</td>
                </tr>
            `;
      table.innerHTML += row;
    });
  } catch (error) {
    console.error("Error loading assets:", error);
  }
}

// Função para adicionar um ativo
async function addAsset(event) {
  event.preventDefault(); // Impede o reload da página
  const name = document.getElementById("name").value;
  const description = document.getElementById("description").value;
  const category = document.getElementById("category").value;
  const status = document.getElementById("status").value;

  try {
    const response = await fetch(`${API_URL}/assets`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, description, category, status }),
    });

    if (response.ok) {
      alert("Asset added successfully!");
      document.getElementById("assetForm").reset(); // Limpa o formulário
      loadAssets(); // Atualiza a lista
    } else {
      alert("Failed to add asset!");
    }
  } catch (error) {
    console.error("Error adding asset:", error);
  }
}

// Adiciona evento ao formulário
document.getElementById("assetForm").addEventListener("submit", addAsset);

// Carrega ativos ao abrir a página
loadAssets();
