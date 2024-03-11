document.addEventListener('DOMContentLoaded', () => {
    const descriptionTextarea = document.getElementById('description');
    descriptionTextarea.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault(); // Prevent the default Enter behavior.
            document.querySelector('input[type="submit"][name="submit"]').click(); // Simulate clicking the Generate button.
        }
    });
});
document.addEventListener('DOMContentLoaded', (event) => {
    const conversation = document.querySelector('.conversation');
    conversation.scrollTop = conversation.scrollHeight;
});