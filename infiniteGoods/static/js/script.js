$(document).ready(function() {
    setTimeout(function(){
        $('#message').fadeOut('slow');
    }, 5000);
});

document.addEventListener('DOMContentLoaded', function() {
    // Retrieve order total from data attribute
    var grandTotal = parseFloat(document.getElementById('data-container').dataset.orderTotal);

    // Configure PayPal Smart Buttons
    paypal.Buttons({
        createOrder: function(data, actions) {
            return actions.order.create({
                purchase_units: [{
                    amount: {
                        value: grandTotal
                    }
                }]
            });
        },
        onApprove: function(data, actions) {
            return actions.order.capture().then(function(details) {
                console.log(details);
                alert('Transaction completed by ' + details.payer.name);
                // Call your server to save transaction details
            });
        }
    }).render('#paypal-button-container');
});

