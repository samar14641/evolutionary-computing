# evolutionary-computing

Obejective functions:

* SETUPS: Minimise the number of setups. A setup occurs whenever we switch from producing one type of item to another. Do not count the first item in the production sequence as a setup. Setups can be minimised by trying to manufacture all orders of a given product together as much as possible, but this might delay high-priority orders or produce some orders out of sequence.

* LOWPRIORITY: Produce the high-priority orders as soon as possible. The quantifiable goal is to minimise the total number of low priority items (sum total of their quantities) produced before the LAST high-priority order is fulfilled. Producing all the high-priority orders first will minimise this objective to zero but at the expense of setups and other order delays. For example if three low priority orders are produced before the last high-priority order is completed and their quantities are 100, 200, and 150 widgets, the LOWPRIORITY score would be 450.

* DELAYS: Orders should be fulfilled in the order they were received to the extent possible. Use the order IDs to determine when orders are fulfilled out of sequence. The order quantities are the measure the delay. Let’s say order 10 (quantity 15) is produced before order 5 (quantity 20). Order 5 must wait while the 15 items for order 10 are produced, so add 15 delay points to the total delay. Sum across the entire production schedule. You only need to consider delays by looking at sequential pairs of orders in the production schedule. It doesn’t matter, for example, if order 9 was produced before order 10 – the delay measure for each order is only based on the 
quantity of the order immediately preceding. The optimal approach is to schedule the orders in ssequence (zero delay), but this will make other objectives worse.

To run:
```
python driver.py
```