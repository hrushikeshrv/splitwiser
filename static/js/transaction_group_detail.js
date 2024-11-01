const groupPaymentShareURL = document.querySelector('#transaction-group-share-url').value;
const currency = document.querySelector('#transaction-group-currency').value;
const paymentShareCells = document.querySelectorAll('.payment-share-cell');

fetch(groupPaymentShareURL)
    .then(response => response.json())
    .then(response => {
        console.log(response);
        paymentShareCells.forEach(cell => {
            const data = response[cell.dataset.username];
            if (data) {
                const amount = (parseInt(data.amount_paid) - parseInt(data.amount_owed)) / 100;
                cell.textContent = `${amount < 0 ? '-' : '+'}${currency}${Math.abs(amount)}`;
                if (amount < 0) cell.style.color = 'var(--error-dark-1)';
                else cell.style.color = 'var(--success-dark-3)';

                const popupContainer = document.createElement('div');
                popupContainer.classList.add('floating-popup-container', 'hidden', 'payment-share-summary-popup');
                popupContainer.dataset.username = cell.dataset.username;
                popupContainer.innerHTML = `
                    <div class="floating-popup flexbox-column pad-20">
                        <strong style="font-size: 1.2rem;">Transaction Summary for ${cell.dataset.username}</strong>
                        <div class="table-container mt-20">
                            <table style="border-color: transparent;">
                                <tbody>
                                    <tr>
                                        <td>Total transactions</td>
                                        <td>${data.n_transactions}</td>
                                    </tr>
                                    <tr>
                                        <td>Spent</td>
                                        <td>${currency}${data.amount_paid / 100}</td>
                                    </tr>
                                    <tr>
                                        <td>Actually owed</td>
                                        <td>${currency}${data.amount_owed / 100}</td>
                                    </tr>
                                    <tr style="border-top: 2px dashed var(--muted-font);">
                                        <td>${amount > 0 ? 'Will get back' : 'Will pay the group'}</td>
                                        <td style="background-color: ${amount > 0 ? 'var(--success-light-3)' : 'var(--error-light-3)'}">${currency}${Math.abs(data.amount_paid - data.amount_owed) / 100}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                `;
                document.body.appendChild(popupContainer);
                popupContainer.addEventListener('click', (e) => {
                    if (e.target !== popupContainer) return;
                    popupContainer.classList.add('hidden');
                })
                document.querySelector(`.payment-share-row[data-username="${cell.dataset.username}"]`).addEventListener('click', () => {
                    popupContainer.classList.remove('hidden');
                })
            }
        })
    })

const copyInviteCodeButton = document.querySelector('#copy-invite-code');
const copyInviteLinkButton = document.querySelector('#copy-invite-link');

copyInviteCodeButton.addEventListener('click', () => {
    navigator.clipboard.writeText(copyInviteCodeButton.dataset.code).then(() => {
        document.querySelector('#copy-success-message').classList.remove('hidden');
    })
});

copyInviteLinkButton.addEventListener('click', () => {
    navigator.clipboard.writeText(copyInviteLinkButton.dataset.link).then(() => {
        document.querySelector('#copy-success-message').classList.remove('hidden');
    })
})
