cowtapult
=========
Enterprise class infrastructure for reliably sending data from Python to Salesforce or Salesforce to Python.


Overview
========
The Salesforce API provides complete access to all data via either SOAP or REST calls.  With an API wrapper library, making calls to the API is fairly easy.  However, as integrations grow, the need for more sophisticated handling of Salesforce integration become more apparent:
* API calls should be done asynchronously to avoid performance bottlenecks
* API calls need to handle temporary errors such as an API downtime or network downtime
* API calls need to handle permanent errors with way to manually edit and retrigger
* API calls should be batched where possible
* A process is needed for matching against existing objects on non-unique fields such as first name, last name, and postal code

Many frameworks and projects could benefit from well thought out solutions to these common use cases for an enterprise class Salesforce integration.  While built on Python with integrations to Python frameworks, this package could handle these Salesforce use cases for any language via HTTP POST submission of tasks.

This package is based around Celery, a mature, highly flexible task queue for Python with a large user base and active development community.  Celery provides support for multiple backends for the broker and result data, asynchronous scheduling of tasks, flexible distribution of tasks, and highly configurable multiple-task workflows.


Quick-Start
===========
At this point, there is a doctest which shows how to insert/update individual records or multiple records using a Celery chain.  You'll need an amqp server and a Salesforce sandbox.

1. Setup your amqp server.  RabbitMQ's base install should work with the celeryconfig.py file included with the package.  If you want to use a different broker/result store, modify celeryconfig.py per the Celery docs.  In the future, this will be handled in a more eligant way.

2. Configure Salesforce Authentication.  Edit the salesforce.cfg file and plug in your info.

3. Run the doctests
`cd cowtapult 
python runtests.py`

After running the tests, you should have 3 Contacts, 3 Opportunities, and 3 OpportunityContactRoles relating them together.

These tests have only been run against a Non-profit Starter Pack based Salesforce instance.  I have no idea if they work against a standard Salesforce sandbox.


Cowta-WHAT?
===========
http://www.amazon.com/Monty-Python-Cow-Catapult-Deluxe/dp/B0006JGW9S/ref=cm_rdp_product
