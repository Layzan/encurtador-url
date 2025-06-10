document.getElementById('urlForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const originalUrl = document.getElementById('originalUrl').value;
    
    if (!originalUrl) {
        alert("Por favor, insira uma URL.");
        return;
    }

    try {
        // Enviar a URL para a API FastAPI
        const response = await fetch('http://127.0.0.1:8000/shorten/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ original_url: originalUrl }),
        });

        if (!response.ok) {
            throw new Error('Erro ao encurtar a URL.');
        }

        // Receber a URL encurtada
        const data = await response.json();
        const shortUrl = data.short_url;

        // Exibir o resultado na página
        document.getElementById('result').style.display = 'block';
        document.getElementById('shortUrl').textContent = `http://127.0.0.1:8000/${shortUrl}`;
    } catch (error) {
        alert("Erro ao encurtar a URL: " + error.message);
    }
});
