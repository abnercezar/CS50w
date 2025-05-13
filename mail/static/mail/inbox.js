document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', () => compose_email());

    // Manipulador de envio
    document.querySelector('#compose-form').addEventListener('submit', send_email);

    // Carregar inbox por padrão
    load_mailbox('inbox');
});

function load_mailbox(mailbox = 'inbox') {
    if (!mailbox || typeof mailbox !== 'string') {

        return;
    }

    const emailsView = document.querySelector('#emails-view');
    emailsView.style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';

    // Título
    emailsView.innerHTML = '';
    const title = document.createElement('h3');
    title.textContent = mailbox.charAt(0).toUpperCase() + mailbox.slice(1);
    emailsView.appendChild(title);

    fetch(`/emails/${mailbox}`)
        .then(response => response.json())
        .then(emails => {

            emailsView.innerHTML = '';
            emailsView.appendChild(title); // Reaplica o título após limpar

            emails.forEach(singleEmail => {
                const newEmail = document.createElement('div');
                newEmail.className = 'list-group-item';
                newEmail.style.marginBottom = '10px';
                newEmail.classList.add(singleEmail.read ? 'read' : 'unread');

                const sender = document.createElement('h5');
                sender.textContent = `Sender: ${singleEmail.sender}`;
                sender.style.paddingLeft = '10px';

                const subject = document.createElement('h4');
                subject.textContent = `Subject: ${singleEmail.subject}`;
                subject.style.paddingLeft = '10px';

                const timestamp = document.createElement('p');
                timestamp.textContent = singleEmail.timestamp;
                timestamp.style.paddingLeft = '10px';

                const readBtn = document.createElement('button');
                readBtn.textContent = 'Mark as Read';
                readBtn.className = 'btn btn-primary';
                readBtn.style.marginBottom = '10px';
                readBtn.style.marginLeft = '10px';
                readBtn.addEventListener('click', (event) => {
                    event.stopPropagation(); // Impede que o clique no botão abra o e-mail
                    update_email(singleEmail.id, { read: true }, mailbox);
                });

                const archiveBtn = document.createElement('button');
                archiveBtn.textContent = singleEmail.archived ? 'Unarchive' : 'Archive';
                archiveBtn.className = `btn btn-${singleEmail.archived ? 'warning' : 'success'}`;
                archiveBtn.style.marginBottom = '10px';
                archiveBtn.style.marginLeft = '10px';
                archiveBtn.addEventListener('click', (event) => {
                    event.stopPropagation(); // Evita conflito com o clique no container
                    update_email(singleEmail.id, { archived: !singleEmail.archived }, mailbox);
                });

                newEmail.addEventListener('click', () => view_email(singleEmail.id, mailbox));

                newEmail.append(sender, subject, timestamp, readBtn, archiveBtn);
                emailsView.appendChild(newEmail);
            });
        })
        .catch(error => console.error('Error:', error));
}


// Movido para fora da load_mailbox
function send_email(event) {
    event.preventDefault();

    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({ recipients, subject, body }),
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(result => {

        load_mailbox('sent');
    })
    .catch(error => console.error('Error:', error));
}

function compose_email(email = null) {
    // Mostrar o formulário de composição e ocultar outras visualizações
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    const recipientsField = document.querySelector('#compose-recipients');
    const subjectField = document.querySelector('#compose-subject');
    const bodyField = document.querySelector('#compose-body');

    if (!email) {
        recipientsField.value = '';
        subjectField.value = '';
        bodyField.value = '';
    } else {
        recipientsField.value = email.sender
        subjectField.value = email.subject.startsWith('Re:')
            ? email.subject
            : `Re: ${email.subject}`;
        bodyField.value = `\n\nOn ${email.timestamp} ${email.sender} wrote:\n${email.body}`;
    }

    recipientsField.dispatchEvent(new Event('input'));
    subjectField.dispatchEvent(new Event('input'));
    bodyField.dispatchEvent(new Event('input'));
}

// Corrigido para aceitar email_id corretamente
function view_email(email_id, mailbox) {


    fetch(`/emails/${email_id}`)
        .then(response => response.json())
        .then(email => {
            // Construção da interface do e-mail
            document.querySelector('#emails-view').innerHTML = `
                <h3>${email.subject}</h3>
                <p><strong>From:</strong> ${email.sender}</p>
                <p><strong>To:</strong> ${email.recipients}</p>
                <p><strong>Timestamp:</strong> ${email.timestamp}</p>
                <hr>
                <p>${email.body}</p>
                <div class="button-container d-flex">
                    <button class="btn btn-primary" id="reply">Reply</button>
                    <div id="archive-container"></div>
                </div>
            `;

            // **Após o HTML ser atualizado, adicionamos o evento no botão**
            document.querySelector('#reply').addEventListener('click', () => {

                compose_email(email);
            });

            // Marcar como lido automaticamente
            if (!email.read) {
                update_email(email_id, { read: true }, mailbox);
            }

            // Se não estiver na caixa de enviados, mostrar botão Archive/Unarchive
            if (mailbox !== 'sent') {
                const archiveButton = document.createElement('button');
                archiveButton.className = `btn btn-${email.archived ? 'warning' : 'success'} ml-2`;
                archiveButton.innerText = email.archived ? 'Unarchive' : 'Archive';

                archiveButton.addEventListener('click', () => {
                    update_email(email_id, { archived: !email.archived }, mailbox);
                });

                document.querySelector('#archive-container').appendChild(archiveButton);
            }
        })
        .catch(error => console.error('Erro ao carregar o e-mail:', error));
}

// Movido para fora da load_mailbox
function update_email(email_id, update_data, mailbox = 'inbox') {
    fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify(update_data),
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => {
        if (response.ok) {
            load_mailbox(mailbox);
        }
    })
    .catch(error => console.error('Error:', error));
}
