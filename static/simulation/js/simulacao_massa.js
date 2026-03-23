const ctx = document.getElementById('massChart').getContext('2d')
    let massChart = new Chart(ctx, {
      type: 'line', // Tipo de gráfico (linha para espectrometria de massa)
      data: {
        labels: [], // Rótulos para o eixo X (massas)
        datasets: [
          {
            label: 'Intensidade',
            data: [], // Dados para o eixo Y (intensidades)
            borderColor: '#7B904B',
            backgroundColor: 'rgba(123, 144, 75, 0.5)',
            fill: true,
            tension: 0.1
          }
        ]
      },
      options: {
        scales: {
          x: {
            title: {
              display: true,
              text: 'Massa/Carga'
            }
          },
          y: {
            title: {
              display: true,
              text: 'Intensidade'
            },
            beginAtZero: true
          }
        }
      }
    })
    
    function updateChart() {
      const massas = []
      const intensidades = []
    
      const rows = document.getElementById('data-table').getElementsByTagName('tbody')[0].rows
      Array.from(rows).forEach((row) => {
        const mass = row.cells[0].getElementsByTagName('input')[0].value
        const intensity = row.cells[1].getElementsByTagName('input')[0].value
        if (mass && intensity) {
          massas.push(mass)
          intensidades.push(intensity)
        }
      })
    
      massChart.data.labels = massas
      massChart.data.datasets[0].data = intensidades
      massChart.update()
    }

function addRow() {
    const table = document.getElementById('data-table').getElementsByTagName('tbody')[0];

    // Desabilita todos os inputs das linhas existentes antes de adicionar uma nova linha
    Array.from(table.rows).forEach(row => {
        Array.from(row.cells).forEach(cell => {
            const inputs = cell.getElementsByTagName('input');
            for (let input of inputs) {
                input.disabled = true;
                input.classList.add('input-field'); // Garante que a classe CSS seja aplicada aos inputs existentes
            }
        });
    });

    // Adiciona uma nova linha
    const newRow = document.createElement('tr');

    let cell1 = document.createElement('td');
    let cell2 = document.createElement('td');
    let cell3 = document.createElement('td');

    // Adiciona os inputs com as classes corretas
    const inputMass = document.createElement('input');
    inputMass.type = 'number';
    inputMass.name = 'mass';
    inputMass.className = 'input-field'; // Aplica a classe CSS

    const inputIntensity = document.createElement('input');
    inputIntensity.type = 'number';
    inputIntensity.name = 'intensity';
    inputIntensity.className = 'input-field'; // Aplica a classe CSS

    // Adiciona os elementos de ação (botões)
    cell1.appendChild(inputMass);
    cell2.appendChild(inputIntensity);
    cell3.innerHTML = `
        <button onclick="removeRow(this)" class="btn-icon"><i class="fas fa-times"></i></button>
        <button onclick="editRow(this)" class="btn-icon"><i class="fas fa-pencil-alt"></i></button>`;

    newRow.appendChild(cell1);
    newRow.appendChild(cell2);
    newRow.appendChild(cell3);

    table.appendChild(newRow);
    // Atualiza o gráfico
    updateChart()

}

function removeRow(btn) {
    var row = btn.parentNode.parentNode;
    row.parentNode.removeChild(row);
    // Atualiza o gráfico
    updateChart()

}

function editRow(btn) {
    const row = btn.parentNode.parentNode;
    const cells = row.getElementsByTagName('input');
    
    for (let i = 0; i < cells.length; i++) {
        cells[i].disabled = !cells[i].disabled; // Alterna entre habilitado e desabilitado
    }
    
    // Atualiza o gráfico
    updateChart();
}


function goBack() {
    window.history.back(); // Simplesmente volta para a página anterior
}

function goNext() {
    const rows = document.getElementById('data-table').getElementsByTagName('tbody')[0].rows;
    const massas = [];
    const intensidades = [];

    let allFieldsFilled = true;  // Flag para verificar se todos os campos estão preenchidos

    Array.from(rows).forEach(row => {
        const massInput = row.cells[0].getElementsByTagName('input')[0].value.trim();
        const intensityInput = row.cells[1].getElementsByTagName('input')[0].value.trim();

        // Verifica se algum campo está vazio
        if (massInput === "" || intensityInput === "") {
            allFieldsFilled = false;  // Encontra um campo vazio e atualiza a flag
        } else {
            massas.push(massInput);  // Adiciona o valor de massa/carga à lista se não estiver vazio
            intensidades.push(intensityInput);  // Adiciona o valor de intensidade à lista se não estiver vazio
        }
    });
            // Atualiza o gráfico
            updateChart()

    // Se todos os campos estiverem preenchidos, procede para submeter o formulário
    if (allFieldsFilled) {
        document.getElementById('mass-form').submit();  // Submete o formulário
    } else {
        alert('Por favor, preencha todos os campos antes de prosseguir.');
    }
}
