let thinkingElement = null;

function showThinking() {
  if (thinkingElement) return;

  const chatWindow = document.getElementById("chat-window");

  const html = `
    <div id="thinking-message" class="flex gap-4">
        <div class="flex-1">
            <div class="bg-gray-100 text-gray-700 rounded-3xl rounded-tl-none px-6 py-4">
                <div class="flex items-center gap-3">

                    <div class="flex gap-1">
                        <span class="w-2 h-2 rounded-full bg-emerald-500 animate-bounce"></span>
                        <span class="w-2 h-2 rounded-full bg-emerald-500 animate-bounce [animation-delay:150ms]"></span>
                        <span class="w-2 h-2 rounded-full bg-emerald-500 animate-bounce [animation-delay:300ms]"></span>
                    </div>

                    <span class="text-sm text-gray-600">
                        کولیب در حال فکر کردنه...
                    </span>

                </div>
            </div>
        </div>

        <div class="w-9 h-9 bg-emerald-100 text-emerald-600 rounded-2xl flex items-center justify-center shrink-0 mt-1">
            <i class="fas fa-robot text-xl"></i>
        </div>
    </div>
  `;

  chatWindow.insertAdjacentHTML("beforeend", html);

  thinkingElement = chatWindow.lastElementChild;

  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function hideThinking() {
    if (thinkingElement) {
        thinkingElement.remove();
        thinkingElement = null;
    }
}

marked.setOptions({
  gfm: true,
  breaks: true,
});

function formatAIResponse(rawMarkdown, element) {
  try {
    const mathBlocks = [];
    let placeholderCounter = 0;

    let processedText = rawMarkdown.replace(
      /\$\$([\s\S]+?)\$\$/g,
      (match, equation) => {
        const placeholder = `AIKATEBLOCKSLOT${placeholderCounter}`;
        mathBlocks.push({ placeholder, equation, isBlock: true });
        placeholderCounter++;
        return placeholder;
      },
    );

    processedText = processedText.replace(
      /\\\[([\s\S]+?)\\\]/g,
      (match, equation) => {
        const placeholder = `AIKATEBLOCKSLOT${placeholderCounter}`;
        mathBlocks.push({ placeholder, equation, isBlock: true });
        placeholderCounter++;
        return placeholder;
      },
    );

    processedText = processedText.replace(
      /\\begin\{([a-zA-Z\*]+)\}([\s\S]+?)\\end\{\1\}/g,
      (match) => {
        const placeholder = `AIKATEBLOCKSLOT${placeholderCounter}`;
        mathBlocks.push({ placeholder, equation: match, isBlock: true });
        placeholderCounter++;
        return placeholder;
      },
    );

    processedText = processedText.replace(
      /\$([^\$\n]+?)\$/g,
      (match, equation) => {
        const placeholder = `AIKATEINLINESLOT${placeholderCounter}`;
        mathBlocks.push({ placeholder, equation, isBlock: false });
        placeholderCounter++;
        return placeholder;
      },
    );

    processedText = processedText.replace(
      /\\\(([\s\S]+?)\\\)/g,
      (match, equation) => {
        const placeholder = `AIKATEINLINESLOT${placeholderCounter}`;
        mathBlocks.push({ placeholder, equation, isBlock: false });
        placeholderCounter++;
        return placeholder;
      },
    );

    let html = marked.parse(processedText);

    mathBlocks.forEach(({ placeholder, equation, isBlock }) => {
      const regex = new RegExp(placeholder, "g");
      try {
        const renderedMath = katex.renderToString(equation.trim(), {
          displayMode: isBlock,
          throwOnError: false,
          trust: true,
        });
        html = html.replace(regex, renderedMath);
      } catch (mathErr) {
        html = html.replace(regex, equation);
      }
    });
    element.innerHTML = html;
  } catch (err) {
    element.textContent = rawMarkdown;
  }
}

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".ai-static-message").forEach(function (el) {
    const rawContent = el.textContent || el.innerText;
    formatAIResponse(rawContent.trim(), el);
  });
});

const chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/");
let currentAIElement = null;
let currentAIContent = null;
let currentAIRawContent = "";

chatSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  const chatWindow = document.getElementById("chat-window");

  if (data.type === "user_message") {
    const userHTML = `
                <div class="flex justify-end gap-4 max-w-3xl ml-auto">
                    <div class="w-9 h-9 bg-zinc-200 text-zinc-700 rounded-2xl flex items-center justify-center shrink-0 mt-1">
                        <i class="fas fa-user text-xl"></i>
                    </div>
                    <div class="flex-1 text-right">
                        <div class="bg-emerald-600 text-white rounded-3xl rounded-tr-none px-6 py-4 leading-relaxed inline-block">
                            ${data.text}
                        </div>
                    </div>
                </div>
            `;
    chatWindow.insertAdjacentHTML("beforeend", userHTML);
    showThinking();
    chatWindow.scrollTop = chatWindow.scrollHeight;
  } else if (data.type === "chunk") {
    hideThinking();
    if (!currentAIElement) {
      const aiHTML = `
                    <div class="flex gap-4 ai-response">
                        <div class="flex-1">
                            <div class="bg-gray-100 text-gray-800 rounded-3xl rounded-tl-none px-6 py-4 leading-relaxed prose-custom">
                                <span class="ai-content"></span>
                            </div>
                        </div>
                        <div class="w-9 h-9 bg-emerald-100 text-emerald-600 rounded-2xl flex items-center justify-center shrink-0 mt-1">
                            <i class="fas fa-robot text-xl"></i>
                        </div>
                    </div>
                `;
      chatWindow.insertAdjacentHTML("beforeend", aiHTML);
      currentAIElement = chatWindow.lastElementChild;
      currentAIContent = currentAIElement.querySelector(".ai-content");
      currentAIRawContent = "";
    }

    if (currentAIContent) {
      currentAIRawContent += data.text;
      formatAIResponse(currentAIRawContent, currentAIContent);
    }
    chatWindow.scrollTop = chatWindow.scrollHeight;
  } else if (data.type === "done") {
    currentAIElement = null;
    currentAIContent = null;
    currentAIRawContent = "";
  } else if (data.type === "error") {
    hideThinking();
    Swal.fire({
        title: "یه مشکل پیش اومد 👀",
        text: data.text,
        icon: "error",
        confirmButtonText : "باشه، بعدا امتحان میکنم"
    });
  } else if (data.type == "redirect") {
    window.location.replace(`/qulib-ai/chat/${data.uuid}/?default=${data.default}`);
  }
};

function sendMessage() {
  const inputDom = document.getElementById("message-input");
  const message = inputDom.value.trim();

  if (!message || chatSocket.readyState !== WebSocket.OPEN) return;
  const chatUUID = inputDom.dataset.uuid ? inputDom.dataset.uuid : "";

  chatSocket.send(JSON.stringify({ message: message , uuid: chatUUID }));
  inputDom.value = "";
}

document
  .getElementById("message-input")
  .addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

function toggleSidebar() {
  const sidebar = document.getElementById("sidebar");
  const overlay = document.getElementById("sidebar-overlay");
  sidebar.classList.toggle("translate-x-full");
  overlay.classList.toggle("hidden");
}
