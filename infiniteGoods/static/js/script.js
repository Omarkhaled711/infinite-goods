$(document).ready(function () {
    setTimeout(function () {
        $('#message').fadeOut('slow');
    }, 5000);
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
document.addEventListener('DOMContentLoaded', function () {
    // Retrieve order total from data attribute
    var dataContainer = document.getElementById('data-container');
    var paypalButtonContainer = document.getElementById('paypal-button-container');

    if (!dataContainer || !paypalButtonContainer) {
        return;
    }

    var grandTotal = parseFloat(dataContainer.dataset.orderTotal);
    var paymentUrl = dataContainer.getAttribute('pay-url');
    var orderID = dataContainer.getAttribute('order-id');
    var redirect_url = dataContainer.getAttribute('redirect-url')
    var payment_method = 'PayPal';
    const csrftoken = getCookie('csrftoken');

    // Configure PayPal Smart Buttons
    paypal.Buttons({
        createOrder: function (data, actions) {
            return actions.order.create({
                purchase_units: [{
                    amount: {
                        value: grandTotal
                    }
                }]
            });
        },
        onApprove: function (data, actions) {
            return actions.order.capture().then(function (details) {
                console.log(details);
                sendData();
                function sendData() {
                    fetch(paymentUrl, {
                        method: "POST",
                        headers: {
                            "Content-type": "application/json",
                            "X-CSRFToken": csrftoken,
                        },
                        body: JSON.stringify({
                            orderID: orderID,
                            transicID: details.id,
                            payment_method: payment_method,
                            status: details.status,
                        }),
                    })
                        .then(response => response.json())
                        .then(data => {
                            window.location.href = redirect_url + '?order_number=' + data.order_number + '&payment_id=' + data.payment_id;
                        });
                }
                // Call your server to save transaction details
            });
        }
    }).render('#paypal-button-container');
});

