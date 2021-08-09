## Requirements
* Python 3.7+
* Postgresql

## Challenge

### Aggregated Usage Models

Create an aggregate representation of the subscription usage metrics which will be used for more efficiently generating metrics and small reports.

We have two types of usage - data usage and voice usage. The raw usage records usage types for these exist in the `DataUsageRecord` and `VoiceUsageRecord` tables. Create an aggregate representation (using models or otherwise) that will use the data from these two tables and store aggregated metrics segmented by date.

**NOTE**: You are not required to write the query to populate the new models you create with data from the raw usage records tables. Those raw usage record tables are there for reference.

Create one or both of the APIs below:

### API - Subscriptions Exceeding Usage Price Limit

Create an API that accepts a price limit as a request parameter. Find any subscriptions that have reached the price limit on either data and/or voice (check both usage types). Return a list of the subscription id, type(s) of usage that exceeded the price limit, and by how much it's exceeded the limit.

### API - Usage Metrics By Subscription and Usage Type

Create an API that fetches data usage metrics and voice usage metrics by subscription id. This endpoint should accept a from date, to date, and usage type request parameter. Return a list of the subscription id, total price of usage for the given dates, and total usage for any subscriptions that had usage during the given from and to dates.

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

### BONUSES

1. Write a query to efficiently populate your aggregated usage models from the raw usage record tables.

**HINT**: Optimize for high volumes of raw usage records, but not long retention periods.

2. Improve and optimize the existing code where you see fit.
3. Write tests!
