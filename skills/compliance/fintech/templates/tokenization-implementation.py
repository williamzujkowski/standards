#!/usr/bin/env python3
"""
Payment Tokenization Implementation
PCI-DSS SAQ A compliant tokenization using Stripe and Braintree

Security Features:
- No PAN ever touches your server (SAQ A compliance)
- Client-side tokenization via JavaScript SDK
- Server-side token validation and processing
- Secure key management via environment variables
- Audit logging for all payment operations
"""

import logging
import os
from datetime import datetime
from typing import Any, Dict, Optional

import braintree
import stripe

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==== Stripe Implementation ====


class StripeTokenizer:
    """
    Stripe tokenization handler
    SAQ A compliant: Card data never touches your server
    """

    def __init__(self):
        """Initialize Stripe with API key from environment"""
        stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
        if not stripe.api_key:
            raise ValueError("STRIPE_SECRET_KEY environment variable not set")

        # Verify API key works
        try:
            stripe.Account.retrieve()
            logger.info("Stripe API initialized successfully")
        except stripe.error.AuthenticationError as e:
            logger.error(f"Stripe authentication failed: {e}")
            raise

    def create_payment_intent(
        self,
        amount: int,
        currency: str = "usd",
        customer_id: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Create a PaymentIntent for Stripe.js to complete

        Args:
            amount: Payment amount in cents (e.g., 1000 = $10.00)
            currency: Three-letter ISO currency code
            customer_id: Optional existing Stripe customer ID
            metadata: Optional metadata dictionary

        Returns:
            PaymentIntent object with client_secret for frontend
        """
        try:
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                customer=customer_id,
                metadata=metadata or {},
                automatic_payment_methods={"enabled": True},
            )

            logger.info(f"PaymentIntent created: {intent.id}")
            self._audit_log("payment_intent_created", intent.id, amount)

            return {
                "client_secret": intent.client_secret,
                "payment_intent_id": intent.id,
                "amount": amount,
                "currency": currency,
            }
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {e}")
            raise

    def process_payment(self, token: str, amount: int, description: str) -> Dict[str, Any]:
        """
        Process a payment using a Stripe token

        Args:
            token: Token created by Stripe.js (tok_xxxx)
            amount: Amount in cents
            description: Payment description

        Returns:
            Charge details
        """
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token,  # Token from Stripe.js (NOT raw card data)
                description=description,
            )

            logger.info(f"Payment processed: {charge.id}")
            self._audit_log("payment_processed", charge.id, amount)

            return {
                "success": True,
                "charge_id": charge.id,
                "amount": charge.amount,
                "status": charge.status,
                "receipt_url": charge.receipt_url,
            }
        except stripe.error.CardError as e:
            # Card declined
            logger.warning(f"Card declined: {e.user_message}")
            return {"success": False, "error": e.user_message, "decline_code": e.code}
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {e}")
            return {"success": False, "error": "Payment processing failed"}

    def create_customer_with_payment_method(
        self, email: str, payment_method_id: str, metadata: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Create a customer and attach a payment method (tokenized)

        Args:
            email: Customer email
            payment_method_id: PaymentMethod ID from Stripe.js
            metadata: Optional customer metadata

        Returns:
            Customer details
        """
        try:
            customer = stripe.Customer.create(
                email=email,
                payment_method=payment_method_id,
                invoice_settings={"default_payment_method": payment_method_id},
                metadata=metadata or {},
            )

            logger.info(f"Customer created: {customer.id}")
            self._audit_log("customer_created", customer.id, 0)

            return {"customer_id": customer.id, "email": customer.email, "payment_method": payment_method_id}
        except stripe.error.StripeError as e:
            logger.error(f"Customer creation failed: {e}")
            raise

    def charge_saved_customer(self, customer_id: str, amount: int, description: str) -> Dict[str, Any]:
        """
        Charge an existing customer using saved payment method

        Args:
            customer_id: Stripe customer ID
            amount: Amount in cents
            description: Charge description

        Returns:
            Charge details
        """
        try:
            charge = stripe.Charge.create(amount=amount, currency="usd", customer=customer_id, description=description)

            logger.info(f"Recurring payment processed: {charge.id}")
            self._audit_log("recurring_payment", charge.id, amount)

            return {"success": True, "charge_id": charge.id, "amount": charge.amount}
        except stripe.error.StripeError as e:
            logger.error(f"Recurring payment failed: {e}")
            return {"success": False, "error": str(e)}

    def _audit_log(self, event_type: str, reference_id: str, amount: int):
        """
        Audit logging for compliance (PCI-DSS 10.2)

        Args:
            event_type: Type of payment event
            reference_id: Stripe object ID
            amount: Transaction amount
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "reference_id": reference_id,
            "amount": amount,
            "user": "system",  # Replace with actual user ID in production
        }

        # In production: Send to SIEM, write to audit database
        logger.info(f"AUDIT: {log_entry}")


# ==== Braintree Implementation ====


class BraintreeTokenizer:
    """
    Braintree tokenization handler (PayPal owned)
    SAQ A compliant with hosted fields
    """

    def __init__(self):
        """Initialize Braintree gateway with credentials from environment"""
        self.gateway = braintree.BraintreeGateway(
            braintree.Configuration(
                environment=braintree.Environment.Production,  # or Sandbox for testing
                merchant_id=os.environ.get("BRAINTREE_MERCHANT_ID"),
                public_key=os.environ.get("BRAINTREE_PUBLIC_KEY"),
                private_key=os.environ.get("BRAINTREE_PRIVATE_KEY"),
            )
        )

        if not all(
            [
                os.environ.get("BRAINTREE_MERCHANT_ID"),
                os.environ.get("BRAINTREE_PUBLIC_KEY"),
                os.environ.get("BRAINTREE_PRIVATE_KEY"),
            ]
        ):
            raise ValueError("Braintree credentials not set in environment")

        logger.info("Braintree gateway initialized")

    def generate_client_token(self, customer_id: Optional[str] = None) -> str:
        """
        Generate client token for Braintree.js

        Args:
            customer_id: Optional existing customer ID

        Returns:
            Client token for frontend initialization
        """
        try:
            params = {}
            if customer_id:
                params["customer_id"] = customer_id

            client_token = self.gateway.client_token.generate(params)
            logger.info("Client token generated")
            return client_token
        except Exception as e:
            logger.error(f"Token generation failed: {e}")
            raise

    def process_payment(self, nonce: str, amount: str, customer_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process payment using payment method nonce from Braintree.js

        Args:
            nonce: Payment method nonce from client
            amount: Transaction amount (e.g., "10.00")
            customer_id: Optional customer ID

        Returns:
            Transaction result
        """
        try:
            result = self.gateway.transaction.sale(
                {
                    "amount": amount,
                    "payment_method_nonce": nonce,
                    "customer_id": customer_id,
                    "options": {"submit_for_settlement": True},
                }
            )

            if result.is_success:
                transaction = result.transaction
                logger.info(f"Payment successful: {transaction.id}")
                self._audit_log("payment_processed", transaction.id, amount)

                return {
                    "success": True,
                    "transaction_id": transaction.id,
                    "amount": transaction.amount,
                    "status": transaction.status,
                }
            else:
                logger.warning(f"Payment declined: {result.message}")
                return {
                    "success": False,
                    "error": result.message,
                    "errors": [error.message for error in result.errors.deep_errors],
                }
        except Exception as e:
            logger.error(f"Braintree error: {e}")
            return {"success": False, "error": "Payment processing failed"}

    def create_customer(self, email: str, payment_method_nonce: str) -> Dict[str, Any]:
        """
        Create customer and vault payment method

        Args:
            email: Customer email
            payment_method_nonce: Payment method nonce from client

        Returns:
            Customer details
        """
        try:
            result = self.gateway.customer.create({"email": email, "payment_method_nonce": payment_method_nonce})

            if result.is_success:
                customer = result.customer
                logger.info(f"Customer created: {customer.id}")
                self._audit_log("customer_created", customer.id, "0")

                return {
                    "customer_id": customer.id,
                    "email": customer.email,
                    "payment_methods": [pm.token for pm in customer.payment_methods],
                }
            else:
                logger.error(f"Customer creation failed: {result.message}")
                raise Exception(result.message)
        except Exception as e:
            logger.error(f"Braintree error: {e}")
            raise

    def charge_saved_customer(self, customer_id: str, amount: str) -> Dict[str, Any]:
        """
        Charge existing customer using vaulted payment method

        Args:
            customer_id: Braintree customer ID
            amount: Transaction amount

        Returns:
            Transaction result
        """
        try:
            result = self.gateway.transaction.sale(
                {"amount": amount, "customer_id": customer_id, "options": {"submit_for_settlement": True}}
            )

            if result.is_success:
                transaction = result.transaction
                logger.info(f"Recurring payment successful: {transaction.id}")
                self._audit_log("recurring_payment", transaction.id, amount)

                return {"success": True, "transaction_id": transaction.id, "amount": transaction.amount}
            else:
                return {"success": False, "error": result.message}
        except Exception as e:
            logger.error(f"Braintree error: {e}")
            return {"success": False, "error": str(e)}

    def _audit_log(self, event_type: str, reference_id: str, amount: str):
        """Audit logging for compliance"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "reference_id": reference_id,
            "amount": amount,
            "user": "system",
        }
        logger.info(f"AUDIT: {log_entry}")


# ==== Usage Examples ====


def example_stripe_flow():
    """Example Stripe payment flow"""
    tokenizer = StripeTokenizer()

    # 1. Frontend creates PaymentMethod using Stripe.js
    # 2. Backend receives payment_method_id (pm_xxxx)

    # Create customer with tokenized payment method
    customer = tokenizer.create_customer_with_payment_method(
        email="customer@example.com",
        payment_method_id="pm_xxxxxxxxxxxxxx",  # From Stripe.js
        metadata={"user_id": "12345"},
    )

    # Charge the customer
    result = tokenizer.charge_saved_customer(
        customer_id=customer["customer_id"], amount=5000, description="Product purchase"  # $50.00
    )

    print(f"Payment result: {result}")


def example_braintree_flow():
    """Example Braintree payment flow"""
    tokenizer = BraintreeTokenizer()

    # 1. Generate client token for frontend
    client_token = tokenizer.generate_client_token()

    # 2. Frontend collects payment info and creates nonce
    # 3. Backend receives payment_method_nonce

    # Create customer and process payment
    customer = tokenizer.create_customer(
        email="customer@example.com", payment_method_nonce="fake-valid-nonce"  # From Braintree.js
    )

    # Charge saved customer
    result = tokenizer.charge_saved_customer(customer_id=customer["customer_id"], amount="50.00")

    print(f"Payment result: {result}")


# ==== Client-Side Integration Examples ====

CLIENT_SIDE_STRIPE = """
<!-- Stripe.js integration (client-side) -->
<script src="https://js.stripe.com/v3/"></script>
<script>
  const stripe = Stripe('pk_test_xxxxxxxxxxxxx');

  // Create PaymentIntent on backend
  const response = await fetch('/create-payment-intent', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({amount: 5000})
  });
  const {client_secret} = await response.json();

  // Confirm payment with card details (never touches your server)
  const {error, paymentIntent} = await stripe.confirmCardPayment(client_secret, {
    payment_method: {
      card: cardElement,  // Stripe Elements card input
      billing_details: {name: 'Customer Name'}
    }
  });

  if (error) {
    console.error(error.message);
  } else {
    console.log('Payment successful:', paymentIntent.id);
  }
</script>
"""

CLIENT_SIDE_BRAINTREE = """
<!-- Braintree hosted fields (client-side) -->
<script src="https://js.braintreegateway.com/web/3.88.0/js/client.min.js"></script>
<script src="https://js.braintreegateway.com/web/3.88.0/js/hosted-fields.min.js"></script>
<script>
  // Get client token from backend
  const response = await fetch('/client-token');
  const {clientToken} = await response.json();

  // Create hosted fields instance
  const clientInstance = await braintree.client.create({authorization: clientToken});
  const hostedFieldsInstance = await braintree.hostedFields.create({
    client: clientInstance,
    fields: {
      number: {selector: '#card-number'},
      cvv: {selector: '#cvv'},
      expirationDate: {selector: '#expiration-date'}
    }
  });

  // Tokenize card data (never touches your server)
  hostedFieldsInstance.tokenize(async (err, payload) => {
    if (err) {
      console.error(err);
      return;
    }

    // Send nonce to backend
    const response = await fetch('/process-payment', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        nonce: payload.nonce,
        amount: '50.00'
      })
    });

    const result = await response.json();
    console.log('Payment result:', result);
  });
</script>
"""

if __name__ == "__main__":
    print("Payment Tokenization Implementation")
    print("=" * 50)
    print("\nThis module provides PCI-DSS SAQ A compliant tokenization.")
    print("Card data NEVER touches your server.\n")
    print("Set environment variables:")
    print("  - STRIPE_SECRET_KEY")
    print("  - BRAINTREE_MERCHANT_ID")
    print("  - BRAINTREE_PUBLIC_KEY")
    print("  - BRAINTREE_PRIVATE_KEY")
