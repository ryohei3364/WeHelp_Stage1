document.addEventListener('DOMContentLoaded', function() {
  const deleteButtons = document.getElementsByClassName('messageDelete'); // Get all delete buttons

  // Convert HTMLCollection to an array and loop through each button
  Array.from(deleteButtons).forEach(button => {
    button.onclick = function(event) {
      event.preventDefault(); // Prevent the default form submission
      const message = this.closest('.message'); // Find the closest parent message div
      if (confirm('確定要刪除這則留言嗎？')) {
        // If confirmed, submit the form
        message.submit(); // Submit the form associated with this message
        message.remove(); // Remove the message div
      }
      // If canceled, do nothing (the form will not be submitted)
    };
  });
});