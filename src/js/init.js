const root = document.documentElement;

// Check for explicit saved user preference
const getUserTheme = () => {
    const savedTheme = localStorage.getItem('user-theme');
    return savedTheme || "";
};

// Get system theme
const getSystemTheme = () => {
  const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  return systemPrefersDark ? 'dark' : 'light';
};

// Apply theme to the DOM
const applyTheme = (theme) => {
    root.classList.remove('light-theme', 'dark-theme');
    if (theme) {
        root.classList.add(`${theme}-theme`);
    }
};

// 3. Handle manual theme toggle trigger
const toggleTheme = () => {
    const currentTheme = getUserTheme() || getSystemTheme();
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    localStorage.setItem('user-theme', newTheme);
    applyTheme(newTheme);
};

// Watch for OS theme changes to respond dynamically if user hasn't overridden it
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    if (!getUserTheme()) {
        applyTheme(getSystemTheme());
    }
});

// Initialize on page load
applyTheme(getUserTheme() || getSystemTheme());
