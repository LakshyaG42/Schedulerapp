
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
            // You may choose to send this event data to background.js or another script
            // chrome.runtime.sendMessage({ type: 'add_event', event });
        } else {
            alert('Please fill in all fields.');
        }
    });

    // Load Google Sign-In API
    gapi.load('auth2', function () {
        gapi.auth2.init({
            client_id: '19769659267-tfiqfr1hpu9l1jm4600i6nbimncelgr0.apps.googleusercontent.com',
        }).then(function (auth2) {
            auth2.attachClickHandler(submitEventsButton, {}, handleAuthorization, handleAuthResult);
        });
    });

    function handleAuthorization() {
        gapi.auth2.getAuthInstance().signIn();
    }

    function handleAuthResult(authResult) {
        if (authResult && !authResult.error) {
            // Authorization was successful. Now create the events.
            createGoogleCalendarEvents();
        } else {
            // Authorization failed. Handle the error.
            alert('Authorization failed. Please try again.');
        }
    }

    function createGoogleCalendarEvents() {
        gapi.client.load('calendar', 'v3', function () {
            eventList.forEach(function (event) {
                const request = gapi.client.calendar.events.insert({
                    'calendarId': 'primary',  // 'primary' refers to the user's primary calendar
                    'resource': {
                        'summary': event.title,
                        'description': 'Priority: ' + event.priority,
                        'start': {
                            'dateTime': new Date(event.deadline).toISOString(),
                            'timeZone': 'UTC',
                        },
                        'end': {
                            'dateTime': new Date(event.deadline).toISOString(),
                            'timeZone': 'UTC',
                        },
                    }
                });

                request.execute(function (event) {
                    // Handle the response after creating the event
                    console.log('Event created: ' + event.summary);
                });
            });

            // Clear the events list after submitting to Google Calendar
            clearEvents();
            displayEvents();
            alert('Events submitted to Google Calendar.');
        });
    }

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
    }
});

document.getElementById('submit-events').addEventListener('click', function () {
    // Assuming you have an appropriate way to gather eventData for this button click
    const eventData = { /* ... */ };

    fetch('http://localhost:8000/add_event', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(eventData),
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
