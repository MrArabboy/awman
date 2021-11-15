
const openModal = (id) => {
    var modal = document.getElementById(`myModal${id}`);
    var span = document.getElementById(`closeModal${id}`);
    modal.style.display = "block";
    // When the user clicks on <span> (x), close the modal
    span.onclick = function () {
        modal.style.display = "none";
    }
    
    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}

// When the user clicks on the button, open the modal