document.addEventListener('DOMContentLoaded', function() {
    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);

    // By default, load the inbox
    load_mailbox('inbox');

    // Send email when form is submitted
    document.querySelector('#compose-form').onsubmit = send_email;
});

function compose_email() {
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#email-view').style.display = 'none';

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'none';

    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    // Fetch emails for the mailbox
    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
        // Print emails
        console.log(emails);

        // Display emails
        emails.forEach(email => {
            const element = document.createElement('div');
            element.className = 'email';
            element.innerHTML = `
                <div>
                    <strong>${email.sender}</strong>
                    <span>${email.subject}</span>
                    <span>${email.timestamp}</span>
                </div>
            `;
            element.addEventListener('click', () => view_email(email.id));
            if (email.read) {
                element.style.backgroundColor = 'gray';
            } else {
                element.style.backgroundColor = 'white';
            }
            document.querySelector('#emails-view').append(element);
        });
    });
}

function send_email(event) {
    event.preventDefault();

    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    fetch('/emails/send', {
        method: 'POST',
        body: JSON.stringify({
            recipients: recipients,
            subject: subject,
            body: body
        })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        // Load sent mailbox
        load_mailbox('sent');
    });
}

function view_email(email_id) {
    // Show the email view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';

    // Fetch the email
    fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
        // Print email
        console.log(email);

        // Display email details
        document.querySelector('#email-view').innerHTML = `
            <div>
                <strong>From:</strong> ${email.sender}
            </div>
            <div>
                <strong>To:</strong> ${email.recipients.join(', ')}
            </div>
            <div>
                <strong>Subject:</strong> ${email.subject}
            </div>
            <div>
                <strong>Timestamp:</strong> ${email.timestamp}
            </div>
            <hr>
            <div>
                ${email.body}
            </div>
            <hr>
        `;

        // Add archive/unarchive button
        const archiveButton = document.createElement('button');
        archiveButton.innerHTML = email.archived ? 'Unarchive' : 'Archive';
        archiveButton.addEventListener('click', () => {
            fetch(`/emails/${email_id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    archived: !email.archived
                })
            })
            .then(() => load_mailbox('inbox'));
        });
        document.querySelector('#email-view').append(archiveButton);

        // Add reply button
        const replyButton = document.createElement('button');
        replyButton.innerHTML = 'Reply';
        replyButton.addEventListener('click', () => {
            compose_email();
            document.querySelector('#compose-recipients').value = email.sender;
            document.querySelector('#compose-subject').value = email.subject.startsWith('Re:') ? email.subject : `Re: ${email.subject}`;
            document.querySelector('#compose-body').value = `On ${email.timestamp}, ${email.sender} wrote:\n${email.body}\n`;
        });
        document.querySelector('#email-view').append(replyButton);

        // Mark email as read
        if (!email.read) {
            fetch(`/emails/${email_id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    read: true
                })
            });
        }
    });
}
