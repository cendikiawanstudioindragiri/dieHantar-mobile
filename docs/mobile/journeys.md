# User Journeys — dieHantar

This document maps the primary user journeys. Each journey should be captured as a sequence diagram or flow chart; below are textual flows and suggested diagram nodes for implementation.

## 1) Registration & Onboarding
- Passenger: Sign up -> Email/Phone verification -> Basic profile -> Add payment method (optional) -> Welcome tour
- Driver: Sign up -> Document upload (ID, SIM, vehicle) -> Background check -> Activation -> Training flow -> Receive first job
- Merchant: Sign up -> Business profile -> Menu upload -> Open for orders

## 2) Booking a Ride
Nodes: Open app -> Select Transport tab -> Choose pickup (map / pin) -> Select destination -> Choose vehicle type -> Fare estimate displayed -> Confirm -> Match driver -> Track driver (ETA & route) -> Ride start -> Ride end -> Payment & Rating

## 3) Ordering Food
Nodes: Open Food tab -> Browse restaurants -> Select menu items -> Configure options -> Add to cart -> Checkout (address, tip, payment) -> Order placed -> Restaurant accepts -> Preparing -> Courier assigned -> Pickup -> Delivering -> Delivered -> Rating & feedback

## 4) Payment Flow
Nodes: Choose payment method -> If wallet: check balance -> If top-up required: top-up flow -> Process payment via gateway -> Confirm settlement status to user -> Provide receipt

## 5) Tracking & Completion
Nodes: Order active -> Real-time location updates -> ETA adjustments -> Notifications on milestones (driver nearby, arrived) -> Completion -> Rating -> Receipt

## 6) Complaints & Disputes
Nodes: Open order -> Report issue -> Select category (delivery, food quality, payment) -> Attach photo/evidence -> Submit -> Ops triage -> Refund/escalation


Diagram notes:
- For each flow, export a sequence diagram (Mermaid or draw.io) showing actors (User, App, Backend, Driver, Restaurant, Payment Gateway) and transitions.
- Make sure to include failure paths (e.g., payment failed, restaurant closed, driver cancel) and retry/cancel options.

```