let pyodide;

// Placeholders for Python functions. We will 'capture' these from game.py later.
let pyClick, pySecond, pyCPS;
let pyBuyProducer, pyGetPrice, pyGetOwned, pyGetProduction;
let pyIsDrainActive, pyStopDrain;
let pyGetDrainMultiplier;


// The core setup function. Runs once when the page loads. 
async function main() {
    // Initialize Pyodide (Downloading the Python runtime)
    pyodide = await loadPyodide();

    // Fetch game.py and execute it inside Pyodide
    // Date.now() is added to the URL to prevent the browser from using an old cached version
    let response = await fetch("game.py?v=" + Date.now());
    let code = await response.text();
    pyodide.runPython(code);

    // Map Python functions to JS variables for easy calling
    pyClick = pyodide.globals.get("increment");
    pySecond = pyodide.globals.get("second");
    pyCPS = pyodide.globals.get("CPS");
    pyBuyProducer = pyodide.globals.get("buy_producer");
    pyGetPrice = pyodide.globals.get("get_price");
    pyGetOwned = pyodide.globals.get("get_owned");
    pyGetProduction = pyodide.globals.get("get_production");

    pyIsDrainActive = pyodide.globals.get("is_drain_active");
    pyStopDrain = pyodide.globals.get("stop_drain");
    pyGetDrainMultiplier = pyodide.globals.get("get_drain_multiplier");

    // --- EVENT LISTENERS ---

    // Manual click on the main currency button
    document.getElementById("btn").onclick = () => {
        let result = pyClick(); // Calls Python 'increment()'
        updateDisplay(result);
    };

    // Clicking the "Fix Drain" button
    document.getElementById("drainBtn").onclick = () => {
        let result = pyStopDrain(); // Calls Python 'stop_drain()'
        updateDisplay(result);
    };

    // Set up click events for all 5 producer buttons
    for (let i = 0; i < 5; i++) {
        let btn = document.getElementById("prod" + i);
        btn.onclick = () => {
            let result = pyBuyProducer(i); // Pass the index to Python
            updateDisplay(result);
        };
    }

    
    // Updates the text and visibility of all UI elements based on current game state.    
    function updateDisplay(currency) {
        let cps = pyCPS();                // Get base CPS from Python
        let drainActive = pyIsDrainActive(); // Check if drain is happening
        let multiplier = pyGetDrainMultiplier(); // Get current multiplier

        // Update the main currency counter (rounded down for clean UI)
        document.getElementById("btn").innerText =
            "Currency: " + Math.floor(currency);

        // Update CPS display and show if a drain is reducing income
        if (drainActive) {
            let effective = cps * multiplier; // Calculate final income
            document.getElementById("CPS").innerText =
                `Currency Per Second: ${cps} → ${Math.floor(effective)} (drained)`;
        } else {
            document.getElementById("CPS").innerText =
                "Currency Per Second: " + cps;
        }

        // Show "Fix Drain" button only when the drain is actually active
        let drainBtn = document.getElementById("drainBtn");
        drainBtn.style.display = drainActive ? "inline-block" : "none";

        // Update Producer Buttons
        for (let i = 0; i < 5; i++) {
            let price = pyGetPrice(i);
            let owned = pyGetOwned(i);
            let producing = pyGetProduction(i);
            let btn = document.getElementById("prod" + i);

            let total = producing * owned;

            // Unlock Logic: Show a producer if it's the first one, 
            // or if the player owns at least one of the previous producer.
            if (i === 0 || pyGetOwned(i - 1) > 0) {
                btn.style.display = "block";
            }

            // Update button text to show price and current stats
            if (owned === 0) {
                btn.innerText = `Buy Producer ${i + 1} (${price})`;
            } else {
                btn.innerText =
                    `Upgrade Producer ${i + 1} (${price}) | Owned: ${owned} | Producing: ${producing} each, ${total} total`;
            }
        }
    }

    // --- GAME LOOP ---
    // Every 1000ms (1 second), call the Python 'second' function and refresh UI
    setInterval(() => {
        let result = pySecond();
        updateDisplay(result);
    }, 1000);
}

// Start the application
main();
