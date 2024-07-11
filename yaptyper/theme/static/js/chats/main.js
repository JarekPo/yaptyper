const isUserInLocalStorage = () => {
    const username = localStorage.getItem("username");
    return !!username;
}

const setUsername = (username) => {
    localStorage.setItem("username", username);
}

const getUsername = () => {
    const usernameInput = document.getElementById('username-input').value;
    setUsername(usernameInput)
    return usernameInput
}
