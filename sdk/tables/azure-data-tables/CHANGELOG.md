# Release History

## 12.0.0b3 (Unreleased)
* Add support for transactional batching of entity operations.
* Fix deserialization bug in `list_tables` and `query_tables` where `TableItem.table_name` was an object instead of a string.

## 12.0.0b2 (2020-10-07)
* Adds support for Enumerable types by converting the Enum to a string before sending to the service

## 12.0.0b1 (2020-09-08)
This is the first beta of the `azure-data-tables` client library. The Azure Tables client library can seamlessly target either Azure Table storage or Azure Cosmos DB table service endpoints with no code changes.


