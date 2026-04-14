let pyodide;
let pyClick;

async function main() {
    pyodide = await loadPyodide();

    // Load your Python file
    let response = await fetch("game.py?v=" + Date.now());
    let code = await response.text();

    console.log(code);

    pyodide.runPython(code);

    // Get reference to Python function
    pyClick = pyodide.globals.get("increment");
    pySecond = pyodide.globals.get("second");

    // Hook up button
    document.getElementById("btn").onclick = () => {
        let result = pyClick();  // call Python
        document.getElementById("btn").innerText = "Currency: " + result;
    };

    // Call second() every second
setInterval(() => {
    let result = pySecond();
    document.getElementById("btn").innerText = "Currency: " + result;
}, 1000);
}

main();
