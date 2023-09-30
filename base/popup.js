document.addEventListener('DOMContentLoaded', function () {
    const eventList = [];

    const eventForm = document.getElementById('event-form');
    const eventTitleInput = document.getElementById('event-title');
    const eventDeadlineInput = document.getElementById('event-deadline');
    const eventPriorityInput = document.getElementById('event-priority');
    const addEventButton = document.getElementById('add-event');
    const submitEventsButton = document.getElementById('submit-events');
    const eventListDiv = document.getElementById('event-list');

    addEventButton.addEventListener('click', function () {
        const eventTitle = eventTitleInput.value;
        const eventDeadline = eventDeadlineInput.value;
        const eventPriority = eventPriorityInput.value;

        if (eventTitle && eventDeadline && eventPriority) {
            const event = {
                title: eventTitle,
                deadline: eventDeadline,
                priority: eventPriority,
            };

            eventList.push(event);
            clearForm();
            displayEvents();
            chrome.runtime.sendMessage({ type: 'add_event', event });
        } else {
            alert('Please fill in all fields.');
        }
    });

    submitEventsButton.addEventListener('click', function () {
        // Here, you can add code to submit events to Google Calendar API
        // For now, we'll just display a message
        alert('Events submitted to Google Calendar.');
        clearEvents();
        displayEvents();
    });

    function clearForm() {
        eventTitleInput.value = '';
        eventDeadlineInput.value = '';
        eventPriorityInput.value = 'high';
    }

    function displayEvents() {
        eventListDiv.innerHTML = '';
        if (eventList.length === 0) {
            eventListDiv.innerHTML = '<p>No events added yet.</p>';
        } else {
            const ul = document.createElement('ul');
            eventList.forEach(function (event, index) {
                const li = document.createElement('li');
                li.innerHTML = `
                    <strong>${event.title}</strong><br>
                    Deadline: ${event.deadline}<br>
                    Priority: ${event.priority}
                `;
                ul.appendChild(li);
            });
            eventListDiv.appendChild(ul);
        }
    }
    
    function clearEvents() {
        eventList.length = 0;
        displayEvents();
    }
});
document.getElementById('submit-events').addEventListener('click', function () {
    fetch('http://localhost:8000/add_event', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(eventData), // Replace with your event data
    })
    .then(response => {
        if (response.ok) {
            alert('Events submitted successfully!');
        } else {
            alert('Error submitting events.');
        }
    })
    .catch(error => {
        alert('Error: ' + error.message);
    });
});