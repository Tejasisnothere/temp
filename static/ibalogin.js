const selectedOrder = [];

document.querySelectorAll('#imageGrid img').forEach(img => {
    img.addEventListener('click', () => {
        const id = img.getAttribute('data-id');
        if (!selectedOrder.includes(id)) {
            selectedOrder.push(id);
            img.classList.add('selected');
        }
    });
});

function submitSelection() {
    document.getElementById('output').textContent =
        "Selected Order: " + selectedOrder.join(", ");

    // You can also send this to a server via AJAX here
    console.log("Selection sent:", selectedOrder);
}
