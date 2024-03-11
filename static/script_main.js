function scrollToBottom() {
    const conversation = document.querySelector('.conversation');
    if (conversation) {
      conversation.scrollTop = conversation.scrollHeight;
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    // This will scroll the conversation to the bottom on page load
    scrollToBottom();

    // This part is for the description textarea to handle the Enter key press
    const descriptionTextarea = document.getElementById('description');
    if (descriptionTextarea) {
      descriptionTextarea.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault(); // Prevent the default Enter behavior.
          document.querySelector('input[type="submit"][name="submit"]').click(); // Simulate clicking the Generate button.
        }
      });
    }
  });
