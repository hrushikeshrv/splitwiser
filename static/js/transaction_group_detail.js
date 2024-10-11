const groupPaymentShareURL = document.querySelector('#transaction-group-share-url').value;
const currency = document.querySelector('#transaction-group-currency').value;
const paymentShareCells = document.querySelectorAll('.payment-share-cell');
// const paymentShareRow = document.querySelectorAll('.payment-share-row');

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
                        <button class="flexbox-row aife close-popup-button" style="margin-left: 0; font-size: 1rem; cursor: pointer;">
                            <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-arrow-left" width="28" height="28" viewBox="0 0 24 24" stroke-width="1.5" stroke="#ffffff" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                                <line x1="5" y1="12" x2="19" y2="12" />
                                <line x1="5" y1="12" x2="11" y2="18" />
                                <line x1="5" y1="12" x2="11" y2="6" />
                            </svg>
                            <span class="space-lr">Back</span>
                        </button>
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
                    </div>
                `;
                document.body.appendChild(popupContainer);
                popupContainer.querySelector('.close-popup-button').addEventListener('click', (e) => {
                    popupContainer.classList.add('hidden');
                })
                document.querySelector(`.payment-share-row[data-username="${cell.dataset.username}"]`).addEventListener('click', () => {
                    popupContainer.classList.remove('hidden');
                })
            }
        })
    })