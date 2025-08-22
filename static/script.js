
document.addEventListener('DOMContentLoaded', () => {
    const strategySelect = document.getElementById('strategy-select');
    const strategyDescription = document.getElementById('strategy-description');
    const strategyForm = document.getElementById('strategy-form');
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultsContainer = document.getElementById('results-container');
    const resultsContent = document.getElementById('results-content');
    const loadingSpinner = document.getElementById('loading-spinner');

    const providerSelect = document.getElementById('provider-select');

    let strategiesData = {};

    // Fetch strategies from the backend
    fetch('/api/strategies')
        .then(response => response.json())
        .then(data => {
            strategiesData = data.strategy_library;
            populateStrategySelect(strategiesData);
            // Trigger change event to load the first strategy
            if (strategiesData.length > 0) {
                strategySelect.dispatchEvent(new Event('change'));
            }
        });

    function populateStrategySelect(strategies) {
        strategySelect.innerHTML = '';
        strategies.forEach(strategy => {
            const option = document.createElement('option');
            option.value = strategy.name; // Use name as value
            option.textContent = strategy.name;
            strategySelect.appendChild(option);
        });
    }

    strategySelect.addEventListener('change', () => {
        const selectedStrategyName = strategySelect.value;
        const selectedStrategy = strategiesData.find(s => s.name === selectedStrategyName);
        if (selectedStrategy) {
            updateStrategyForm(selectedStrategy);
        }
    });

    function updateStrategyForm(strategy) {
        strategyForm.innerHTML = '';
        strategyDescription.textContent = strategy.intent; // Use intent for description

        for (const paramName in strategy.inputs) {
            const paramType = strategy.inputs[paramName];
            const formGroup = document.createElement('div');
            formGroup.className = 'form-group';

            const label = document.createElement('label');
            label.setAttribute('for', paramName);
            label.textContent = paramName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()); // Capitalize and replace underscores

            const input = document.createElement('input');
            input.type = paramType === 'integer' || paramType === 'float' ? 'number' : 'text';
            if (paramType === 'float') {
                input.step = 'any';
            }
            input.id = paramName;
            input.name = paramName;
            input.className = 'form-control';
            input.placeholder = `Enter ${paramName}`;
            
            formGroup.appendChild(label);
            formGroup.appendChild(input);
            strategyForm.appendChild(formGroup);
        }
    }

    analyzeBtn.addEventListener('click', () => {
        const selectedStrategyId = strategySelect.value;
        const formElements = strategyForm.elements;
        const params = {};

        for (let i = 0; i < formElements.length; i++) {
            const element = formElements[i];
            params[element.name] = element.value;
        }

        // Show spinner and hide results
        loadingSpinner.style.display = 'block';
        resultsContainer.style.display = 'none';

        const selectedProvider = providerSelect.value;

        fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ strategy: selectedStrategyId, params: params, provider: selectedProvider })
        })
        .then(response => response.json())
        .then(data => {
            // Hide spinner and show results
            loadingSpinner.style.display = 'none';
            displayResults(data);
        })
        .catch(error => {
            loadingSpinner.style.display = 'none';
            resultsContent.innerHTML = `<div class="alert alert-danger">An error occurred: ${error}</div>`;
            resultsContainer.style.display = 'block';
        });
    });

    function displayResults(data) {
        resultsContent.innerHTML = `
            <h5>Strategy: ${data.strategy}</h5>
            <p><strong>Data Provider:</strong> ${data.provider}</p>
            <p><strong>Recommendation:</strong> <span class="badge badge-success">${data.recommendation}</span></p>
            <p><strong>Justification:</strong> ${data.justification}</p>
            <h6>Parameters Used:</h6>
            <pre>${JSON.stringify(data.parameters, null, 2)}</pre>
            <h6>Returned Data:</h6>
            <pre>${JSON.stringify(data.data, null, 2)}</pre>
        `;
        resultsContainer.style.display = 'block';
    }
});
