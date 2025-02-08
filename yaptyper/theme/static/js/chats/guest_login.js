const  setGuestUsername = () => {
    const guestNameInput = document.getElementById("guest_name");
    const usernameInput = document.getElementById("username");
        if (guestNameInput.value) {
            usernameInput.value = guestNameInput.value + " (guest)";
        }
}
