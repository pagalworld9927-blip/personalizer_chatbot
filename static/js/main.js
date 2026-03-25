const sendBtn = document.getElementById("send-btn");
const userInput = document.getElementById("user-input");
const chatWindow = document.getElementById("chat-window");
const newChatBtn = document.getElementById("new-chat-btn");
const historyList = document.getElementById("History-list");

// 1. Generate a new thread ID (like "chat-1711200000") or load the last one
let currentThreadId = "chat-" + Date.now();

// Array to store our history of chats
let chatHistory = JSON.parse(localStorage.getItem("chatHistory")) || [];

// ----------------------------------------------------------------------------------
// UI FUNCTIONS
// ----------------------------------------------------------------------------------

function appendMessage(text, sender) {
    const div = document.createElement("div");
    div.classList.add("message", sender === "user" ? "human-message" : "ai-message");
    div.innerHTML = sender === "user"
        ? `<strong>👤 You:</strong> ${text}`
        : `<strong>🤖 AI:</strong> ${text}`;
    chatWindow.appendChild(div);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function renderHistorySidebar() {
    // Clear the current list
    historyList.innerHTML = "";

    // Loop backward so newest is at the top
    for (let i = chatHistory.length - 1; i >= 0; i--) {
        const thread = chatHistory[i];

        const btn = document.createElement("button");
        btn.classList.add("thread-btn");
        // Show the ID, or you can get fancy and show the first message later!
        btn.innerHTML = `Chat: ${new Date(parseInt(thread.split("-")[1])).toLocaleTimeString()}`;

        // When clicking a history button, switch back to that thread!
        btn.addEventListener("click", async () => {
            currentThreadId = thread;
            chatWindow.innerHTML = "";
            appendMessage(`<i>Loading conversation...</i>`, "ai"); // Temporary loading text

            // Ask Python for the old messages!
            const response = await fetch("/history", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ thread_id: thread })
            });

            const data = await response.json();

            chatWindow.innerHTML = ""; // Clear the temporary loading "Loading..." text

            // Loop through the history and automatically print every message on the screen!
            if (data.messages && data.messages.length > 0) {
                data.messages.forEach(msg => {
                    appendMessage(msg.content, msg.sender);
                });
            } else {
                appendMessage(`<i>Ready to continue chat!</i>`, "ai");
            }
        });

        historyList.appendChild(btn);
    }
}

// ----------------------------------------------------------------------------------
// EVENT LISTENERS
// ----------------------------------------------------------------------------------

sendBtn.addEventListener("click", sendMessage);

userInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter") sendMessage();
});

newChatBtn.addEventListener("click", () => {
    // 1. Generate a brand new ID
    currentThreadId = "chat-" + Date.now();

    // 2. Erase all the messages currently on the screen
    chatWindow.innerHTML = "";

    // 3. Let the user know
    appendMessage(`<i>Started a new conversation!</i>`, "ai");
});

// ----------------------------------------------------------------------------------
// MAIN CHAT FUNCTION
// ----------------------------------------------------------------------------------

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage(message, "user");
    userInput.value = "";

    // If this is the FIRST message of a new thread, save it to history!
    if (!chatHistory.includes(currentThreadId)) {
        chatHistory.push(currentThreadId);
        localStorage.setItem("chatHistory", JSON.stringify(chatHistory));
        renderHistorySidebar(); // Update the visual list
    }

    const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        // We now send the thread_id to Python!
        body: JSON.stringify({
            message: message,
            thread_id: currentThreadId
        })
    });

    // Create a blank AI bubble on the screen
    const div = document.createElement("div");
    div.classList.add("message", "ai-message");
    div.innerHTML = `<strong>🤖 AI:</strong> `;
    chatWindow.appendChild(div);

    // Open the pipe and read the stream
    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        div.innerHTML += chunk;
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
}

// Render the history sidebar immediately when the page loads!
renderHistorySidebar();