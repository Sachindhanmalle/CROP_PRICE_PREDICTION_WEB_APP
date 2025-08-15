document.querySelector("form").addEventListener("submit", function(e) {
    e.preventDefault();

    const crop = document.querySelector("#crop").value;
    const market = document.querySelector("#market").value;
    const date = document.querySelector("#date").value; // make sure it's YYYY-MM-DD

    fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            crop: crop,
            market: market,
            date: date
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }
        document.querySelector("#max-price").textContent = data.max_price;
        document.querySelector("#min-price").textContent = data.min_price;
    });
});
