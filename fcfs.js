function runFCFS() {
    // Get input values
    const inputRequests = document.getElementById('requests').value;
    const headPosition = parseInt(document.getElementById('head').value);
  
    // Validate input
    if (!inputRequests || isNaN(headPosition)) {
      alert("Please enter valid inputs.");
      return;
    }
  
    // Convert input to array of integers
    const requests = inputRequests.split(',').map(num => parseInt(num.trim()));
    
    if (requests.some(isNaN)) {
      alert("Invalid request input. Please enter numbers only.");
      return;
    }
  
    // Perform FCFS Calculation
    let totalHeadMovement = 0;
    let currentPosition = headPosition;
    const movementPath = [currentPosition]; // Track head movements for visualization
  
    requests.forEach(request => {
      totalHeadMovement += Math.abs(request - currentPosition);
      currentPosition = request;
      movementPath.push(currentPosition);
    });
  
    // Display result
    document.getElementById('result').innerText = `Total Head Movement: ${totalHeadMovement} Cylinders`;
  
    // Visualize using Chart.js
    plotChart(movementPath);
  }
  
  // Chart.js Visualization
  function plotChart(path) {
    const ctx = document.getElementById('fcfsChart').getContext('2d');
    if (window.myChart) window.myChart.destroy(); // Destroy previous chart if it exists
  
    const positions = Array.from({ length: path.length }, (_, i) => i); // X-axis for sequence
  
    window.myChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: positions, // X-axis represents sequence
        datasets: [{
          label: 'Disk Head Movement (FCFS)',
          data: path, // Y-axis represents cylinder positions
          borderColor: 'blue',
          borderWidth: 2,
          fill: false,
          tension: 0, // Sharp turns for zigzag effect
          pointRadius: 5,
          pointBackgroundColor: 'red'
        }]
      },
      options: {
        indexAxis: 'y', // Flips axes to make it vertical
        scales: {
          x: {
            title: { display: true, text: "Cylinder Position" }
          },
          y: {
            title: { display: true, text: "Sequence of Operations" },
            reverse: false // Ensures downward movement
          }
        }
      }
    });
  }
  