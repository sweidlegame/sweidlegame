let pyodide;
let pyClick;
let pySecond;
let pyCPS;
let pyBuyProducer;
let pyProducerPrice;

async function main() {
    pyodide = await loadPyodide();

    let response = await fetch("game.py?v=" + Date.now());
    let code = await response.text();

    pyodide.runPython(code);

    pyClick = pyodide.globals.get("increment");
    pySecond = pyodide.globals.get("second");
    pyCPS = pyodide.globals.get("CPS");
    pyBuyProducer = pyodide.globals.get("buy_producer");
    pyProducerPrice = pyodide.globals.get("producer_price");

    // Currency button
    document.getElementById("btn").onclick = () => {
        let result = pyClick();
        updateDisplay(result);
    };

    // Producer button
    document.getElementById("prod").onclick = () => {
        let result = pyBuyProducer();
        updateDisplay(result);
    };

    function updateDisplay(currency) {
        let CPS = pyCPS();
        let price = pyProducerPrice();

        document.getElementById("btn").innerText = "Currency: " + Math.floor(currency);
        document.getElementById("CPS").innerText = "Currency Per Second: " + CPS;
        document.getElementById("prod").innerText = "Buy Producer (" + price + ")";
    }

    // Tick every second
    setInterval(() => {
        let result = pySecond();
        updateDisplay(result);
    }, 1000);
}

main();
