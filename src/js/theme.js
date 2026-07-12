try {
    const container = document.querySelector(".container");
    const btnContainer = document.createElement("div");
    btnContainer.setAttribute("id", "btn-container-theme");
    btnContainer.style.position = "absolute";
    // btnContainer.style.width = "50px";
    // btnContainer.style.height = "20px";
    // btnContainer.style.background = "red";
    btnContainer.style.cursor = "pointer";
    btnContainer.style.overflow = "visible";
    btnContainer.style.right = "10px";
    btnContainer.style.top = "0";
    btnContainer.onclick = toggleTheme;
    container.appendChild(btnContainer);
    
    const style = document.createElement("style");
    style.textContent = `
        #btn-container-theme::before { content: "☀︎"; padding: 5px 10px; font-size: 1.2rem; background-color: var(--border-color); border-radius: 3px; width: 30px; display: block; text-align: center; }
        .dark-theme #btn-container-theme::before { content: "☾"; }
    `;
    container.appendChild(style);
// ☀︎ ⏾
} catch (error) {
    
}