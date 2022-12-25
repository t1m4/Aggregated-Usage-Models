# Wingtel interview project 

## Technical requirements

### Requirements
* Python 3.7+
* Postgresql


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

## Technical solutions
There are two way to do it.
1. First one using Django ORM. Create new aggregated table and add signals to old raw model on CRUD operations
2. Second one using PostgreSQL triggers. The same, but all logic pass to database layers.
3. Third one using PostgreSQL view. Different from previous solutions. Create virtual table on database that can be queried.

## Tools

- Django and DRF 
- Celery and Redis
- pytest
- PostgreSQL triggers, procedures, functions and views using Django ORM

## Solution using Django ORM signals
- Solution in [master](https://github.com/t1m4/Aggregated-Usage-Models/tree/v1.0-django_signals) branch 
- Create ORM signal on [pre_save and pre_delete](https://github.com/t1m4/Aggregated-Usage-Models/blob/v1.0-django_signals/wingtel/usage/signals.py#L11#L32) for Data and Voice usage record models. This will allow to create new [table](https://github.com/t1m4/Aggregated-Usage-Models/blob/v1.0-django_signals/wingtel/usage/models.py#L25L37) 
where we store aggregated results from both tables  

## Solution using PostgeSQL trigger
- Solution in [feature/sql_triggers](https://github.com/t1m4/Aggregated-Usage-Models/releases/tag/v1.0-psql-triggers) branch
- [Create](https://github.com/t1m4/Aggregated-Usage-Models/blob/feature/sql_triggers/wingtel/usage/sql_functions/usage_triggers.sql) triggers, procedures and functions that will create UsageRecord instance on raw models CRUD operations. And SQL script to [Django migration system](https://github.com/t1m4/Aggregated-Usage-Models/blob/feature/sql_triggers/wingtel/usage/migrations/0003_add_sql_triggers.py).
## Solution using PostgreView
- Solution in [feature/sql_views](https://github.com/t1m4/Aggregated-Usage-Models/releases/tag/v1.0-psql-views) branch
- Create aggregated representation of two tables and connect Django model to it using [managed=False](https://github.com/t1m4/Aggregated-Usage-Models/blob/feature/sql_views/wingtel/usage/models.py#L40L53).


## Performance check.
Obviously PostgreSQL triggers, functions and views will work faster than Django signals. But it take more amount of time to write in SQL language properly, but it's worth it.

My opinion is the best solution depends on what are business requirements. Each solution has advantages and disadvantages. 
Statistic. 
1. 100 elements
    - ORM signal create = 5.8 seconds. ORM signal delete = 3.8 seconds
    - SQL trigger creat = 1.7 seconds. SQL trigge delete = 0.04 seconds
    - SQL view take 167-224 mc to load.
2. 1000 elements
    - ORM signal create = 55 seconds. ORM signal delete = 40 seconds
    - SQL trigger creat = 15 seconds. SQL trigge delete = 0.04 seconds
    - SQL view take 167-224 mc to load.
## WIP

1. Sql triggers. Write better solutions with small functions. Check performance. 
2. Another idea implementation on Django avoiding signal. Add process of aggregation in the views. It will be more clear to understand. Add more tests.
3. Write for bulk CRUD operations on Django ORM and SQL.
