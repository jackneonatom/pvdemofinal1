async function fetchData() {
    try {const response = await fetch('http://pv-demo.local:8000/stuff', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        const data = await response.json();
        console.log(data); // Log the data to verify its structure
        document.getElementById('bcurrent').innerHTML = `Battery Current: <span class="currentnumber1">${data.Battery_Current || 'N/A'} </span>A`;
    



    } catch (error) {
        console.error('Error:', error);
    }
}