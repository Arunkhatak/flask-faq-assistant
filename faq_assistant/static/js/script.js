function askQuestion() {
    let query = document.getElementById("query").value;

    fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("answer").innerText = "Answer: " + data.answer;
    });
}
