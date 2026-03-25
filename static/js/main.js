const sendBtn = document.getElementById("send-btn");
const userInput = document.getElementById("user-input");
const chatWindow = document.getElementById("chat-window");

function appendMessage(text, sender) {
    const div = document.createElement("div");
    div.classList.add("message", sender === "user" ? "human-message" : "ai-message");
    div.innerHTML = sender === "user"
        ? `<strong>👤 You:</strong> ${text}`
        : `<strong>🤖 AI:</strong> ${text}`;
    chatWindow.appendChild(div);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

sendBtn.addEventListener("click", sendMessage);

userInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter") sendMessage();
})

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage(message, "user");
    userInput.value = "";

    const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
    });

    // 1. Create a blank AI bubble on the screen
    const div = document.createElement("div");
    div.classList.add("message", "ai-message");
    div.innerHTML = `<strong>🤖 AI:</strong> `;
    chatWindow.appendChild(div);

    // 2. Open the "pipe" to read the incoming streaming response
    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    // 3. Loop repeatedly to catch every chunk (word) as it arrives
    while (true) {
        const { done, value } = await reader.read();

        if (done) break; // AI is finished!

        // Decode the binary text chunk and append it directly
        const chunk = decoder.decode(value);
        div.innerHTML += chunk;

        // Auto-scroll to the bottom as it types
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
}