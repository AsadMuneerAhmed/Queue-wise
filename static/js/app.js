
const tokenForm = document.getElementById("tokenForm");
const formMessage = document.getElementById("formMessage");
const submitButton = document.getElementById("submitButton");

function escapeHTML(value) {
    return String(value ?? "").replace(/[&<>"']/g, character => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[character]);
}

async function requestJSON(url, options = {}) {
    const response = await fetch(url, options);
    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Something went wrong.");
    }

    return data;
}

function queueItemHTML(token, isServing = false) {
    const detail = isServing
        ? (token.counter ? `At ${escapeHTML(token.counter)}` : "Being served")
        : `Position ${token.position} · About ${token.estimated_wait_minutes} min`;

    return `
        <div class="queue-item">
            <div>
                <strong>${escapeHTML(token.visitor_name)}</strong>
                <small>${escapeHTML(token.service)} · ${detail}</small>
            </div>
            <span class="queue-number">${escapeHTML(token.token_number)}</span>
        </div>
    `;
}

async function refreshQueue() {
    try {
        const data = await requestJSON("/api/queue");

        document.getElementById("waitingCount").textContent =
            data.waiting.length;
        document.getElementById("servingCount").textContent =
            data.serving.length;
        document.getElementById("counterCount").textContent =
            data.active_counters;

        document.getElementById("servingList").innerHTML =
            data.serving.length
                ? data.serving.map(token => queueItemHTML(token, true)).join("")
                : '<p class="muted">No tokens are being served right now.</p>';

        document.getElementById("waitingList").innerHTML =
            data.waiting.length
                ? data.waiting.slice(0, 6).map(token => queueItemHTML(token)).join("")
                : '<p class="muted">The queue is currently empty.</p>';

        if (window.currentQueueTokenId) {
            const current = await requestJSON(
                `/api/tokens/${window.currentQueueTokenId}`
            );
            showToken(current.token);
        }
    } catch (error) {
        console.error("Queue refresh failed:", error);
    }
}

function showToken(token) {
    document.getElementById("tokenResult").hidden = false;
    document.getElementById("resultNumber").textContent = token.token_number;

    let statusText = token.status;
    if (token.status === "Waiting") {
        statusText = "You are in the queue. Please wait for your token to be called.";
    } else if (token.status === "Serving") {
        statusText = `Your turn has arrived${token.counter ? " at " + token.counter : ""}!`;
    } else if (token.status === "Completed") {
        statusText = "Your service has been completed.";
    }

    document.getElementById("resultStatus").textContent = statusText;
    document.getElementById("resultPosition").textContent =
        token.status === "Waiting" ? token.position : "—";
    document.getElementById("resultWait").textContent =
        token.status === "Waiting"
            ? `${token.estimated_wait_minutes} min`
            : "—";
    document.getElementById("tokenLink").href = `/token/${token.id}`;
}

tokenForm.addEventListener("submit", async event => {
    event.preventDefault();

    formMessage.textContent = "";
    formMessage.className = "message";
    submitButton.disabled = true;
    submitButton.textContent = "Creating token...";

    const payload = {
        visitor_name: document.getElementById("visitorName").value.trim(),
        service: document.getElementById("service").value
    };

    try {
        const data = await requestJSON("/api/tokens", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        window.currentQueueTokenId = data.token.id;
        showToken(data.token);

        formMessage.textContent = "Your token has been created successfully.";
        formMessage.className = "message success";
        tokenForm.reset();

        await refreshQueue();
        document.getElementById("tokenResult").scrollIntoView({
            behavior: "smooth",
            block: "nearest"
        });
    } catch (error) {
        formMessage.textContent = error.message;
        formMessage.className = "message error";
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = "Get My Token →";
    }
});

refreshQueue();
setInterval(refreshQueue, 5000);