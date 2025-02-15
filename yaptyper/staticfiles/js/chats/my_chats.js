document.addEventListener("DOMContentLoaded",  () => {
    const chatroomSelect = document.getElementById("chatroom-select");
    if (chatroomSelect) {
        chatroomSelect.addEventListener("change", function () {
            const selectedValue = chatroomSelect.value;
            if (selectedValue) {
                window.location.href = selectedValue;
            }
        });
    }
});