Schedule Activity Access
------------------------
Odoo Version : Odoo 13.0 Enterprise

Installation 
-------------
Install the Application => Apps -> Schedule Activity Access

Configuration
-------------
* No configuration required

Version - 13.0.1.0.0
--------------------
* The schedule activity will be visible to the one who has access to the 
document.
* The created user of the activity can't make any changes ones the activity 
is created.
* The user to whom the activity is assigned can make changes in the assign 
activity.
* A 'REJECT BY CUSTOMER' button is added in the Sale Order/Quotation and it's 
visible in 'Quotation' and 'Quotation Sent' state.
* On click of the 'REJECTED BY CUSTOMER' button the Sale Order/Quotation will 
be moved to 'REJECTED BY CUSTOMER' state.
* A filter name 'Rejected Quotations' is added to filter quotations. 
* A group by of 'State' is added to filter Quotation/Sale Order by states

Version - 13.0.1.0.1
--------------------
* Added 'sale_discount_total' in manifest as 'sale_discount_total' module has 
override the state field of 'sale.order' and it is used in Schedule Activity 
Access

Version - 13.0.1.0.2
--------------------
* Changed the schedule activity edit access in calender view of employee.
