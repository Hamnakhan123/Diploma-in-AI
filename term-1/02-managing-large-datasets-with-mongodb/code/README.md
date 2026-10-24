# 💻 Code · Module 2: Managing Large Datasets with MongoDB

> Prepared by **Hamna Zahid Khan**, Junior Lecturer

Every file below is complete and runnable on its own. Each one is used by a session page, which shows the real output it produced.

[⬅ Back to the module](../README.md)

## ⚙️ Setup

Python 3.10+ and these packages:

```bash
pip install bson mongomock pandas pymongo store_db
```

Notebooks (`.ipynb`) open directly in Google Colab from the badge at the top of each session page, or locally with `jupyter notebook`.

JavaScript files run with Node.js 18+: `node file.js`.

Run every command from inside this `code/` folder so relative data paths resolve.

## 📂 Files

### [Session 1: Introduction to MongoDB](../session-01-introduction-to-mongodb.md)

| File | What it does | How to run |
|---|---|---|
| [`session-01-introduction-to-mongodb.ipynb`](session-01-introduction-to-mongodb.ipynb) | Executed notebook with every Python example of the session | `jupyter notebook session-01-introduction-to-mongodb.ipynb` (or the Colab badge on the session page) |
| [`session-01_first_look.py`](session-01_first_look.py) | Example 1: Databases, collections and a flexible schema | `python session-01_first_look.py` |
| [`session-01_relational_vs_document.py`](session-01_relational_vs_document.py) | Example 2: One order, two designs | `python session-01_relational_vs_document.py` |

### [Session 2: Working with MongoDB Databases (CRUD)](../session-02-working-with-mongodb-databases.md)

| File | What it does | How to run |
|---|---|---|
| [`session-02-working-with-mongodb-databases.ipynb`](session-02-working-with-mongodb-databases.ipynb) | Executed notebook with every Python example of the session | `jupyter notebook session-02-working-with-mongodb-databases.ipynb` (or the Colab badge on the session page) |
| [`session-02_bulk_write.py`](session-02_bulk_write.py) | Example 3: Bulk writes and duplicate keys | `python session-02_bulk_write.py` |
| [`session-02_create_read.py`](session-02_create_read.py) | Example 1: Create and read | `python session-02_create_read.py` |
| [`session-02_update_delete.py`](session-02_update_delete.py) | Example 2: Update and delete | `python session-02_update_delete.py` |
| [`store_db.py`](store_db.py) | Session 2: Working with MongoDB Databases (CRUD) | `python store_db.py` |

### [Session 3: MongoDB Operators](../session-03-mongodb-operators.md)

| File | What it does | How to run |
|---|---|---|
| [`session-03-mongodb-operators.ipynb`](session-03-mongodb-operators.ipynb) | Executed notebook with every Python example of the session | `jupyter notebook session-03-mongodb-operators.ipynb` (or the Colab badge on the session page) |
| [`session-03_array_operators.py`](session-03_array_operators.py) | Example 2: Array operators | `python session-03_array_operators.py` |
| [`session-03_query_operators.py`](session-03_query_operators.py) | Example 1: Query operators | `python session-03_query_operators.py` |

### [Session 4: The Aggregation Pipeline](../session-04-aggregation-pipeline.md)

| File | What it does | How to run |
|---|---|---|
| [`session-04-aggregation-pipeline.ipynb`](session-04-aggregation-pipeline.ipynb) | Executed notebook with every Python example of the session | `jupyter notebook session-04-aggregation-pipeline.ipynb` (or the Colab badge on the session page) |
| [`session-04_pipeline_basics.py`](session-04_pipeline_basics.py) | Example 1: Pipeline basics | `python session-04_pipeline_basics.py` |
| [`session-04_reports.py`](session-04_reports.py) | Example 3: Reporting stages | `python session-04_reports.py` |
| [`session-04_unwind_lookup.py`](session-04_unwind_lookup.py) | Example 2: `$unwind` and `$lookup` | `python session-04_unwind_lookup.py` |

### [Session 5: Database Commands](../session-05-database-commands.md)

| File | What it does | How to run |
|---|---|---|
| [`session-05-database-commands.ipynb`](session-05-database-commands.ipynb) | Executed notebook with every Python example of the session | `jupyter notebook session-05-database-commands.ipynb` (or the Colab badge on the session page) |
| [`session-05_admin_helpers.py`](session-05_admin_helpers.py) | Example 1: Administrative helpers and a home-made `collStats` | `python session-05_admin_helpers.py` |
| [`session-05_run_command.py`](session-05_run_command.py) | Example 2: Command documents and their replies | `python session-05_run_command.py` |

### [Session 6: MongoDB Shell Methods](../session-06-mongodb-shell-methods.md)

| File | What it does | How to run |
|---|---|---|
| [`session-06-mongodb-shell-methods.ipynb`](session-06-mongodb-shell-methods.ipynb) | Executed notebook with every Python example of the session | `jupyter notebook session-06-mongodb-shell-methods.ipynb` (or the Colab badge on the session page) |
| [`session-06_collection_methods.py`](session-06_collection_methods.py) | Example 2: Collection methods | `python session-06_collection_methods.py` |
| [`session-06_cursor_methods.py`](session-06_cursor_methods.py) | Example 1: Cursor methods | `python session-06_cursor_methods.py` |
| [`session-06_restock.js`](session-06_restock.js) | Example 3: A shell script and its Python twin | `node session-06_restock.js` |
| [`session-06_restock.py`](session-06_restock.py) | Example 3: A shell script and its Python twin | `python session-06_restock.py` |

### [Session 7: MongoDB Indexing](../session-07-mongodb-indexing.md)

| File | What it does | How to run |
|---|---|---|
| [`session-07-mongodb-indexing.ipynb`](session-07-mongodb-indexing.ipynb) | Executed notebook with every Python example of the session | `jupyter notebook session-07-mongodb-indexing.ipynb` (or the Colab badge on the session page) |
| [`session-07_index_types.py`](session-07_index_types.py) | Example 1: Creating index types | `python session-07_index_types.py` |
| [`session-07_scan_vs_index.py`](session-07_scan_vs_index.py) | Example 2: Collection scan versus index scan | `python session-07_scan_vs_index.py` |

### [Session 8: Replication and Sharding](../session-08-replication-and-sharding.md)

| File | What it does | How to run |
|---|---|---|
| [`session-08-replication-and-sharding.ipynb`](session-08-replication-and-sharding.ipynb) | Executed notebook with every Python example of the session | `jupyter notebook session-08-replication-and-sharding.ipynb` (or the Colab badge on the session page) |
| [`session-08_replica_set_sim.py`](session-08_replica_set_sim.py) | Example 1: A replica set in miniature | `python session-08_replica_set_sim.py` |
| [`session-08_sharding_sim.py`](session-08_sharding_sim.py) | Example 2: Ranged versus hashed shard keys | `python session-08_sharding_sim.py` |

### [Session 9: Transaction Management](../session-09-transaction-management.md)

| File | What it does | How to run |
|---|---|---|
| [`session-09-transaction-management.ipynb`](session-09-transaction-management.ipynb) | Executed notebook with every Python example of the session | `jupyter notebook session-09-transaction-management.ipynb` (or the Colab badge on the session page) |
| [`session-09_single_doc_atomicity.py`](session-09_single_doc_atomicity.py) | Example 1: Single-document atomicity, and what goes wrong without a transaction | `python session-09_single_doc_atomicity.py` |
| [`session-09_transaction_real.py`](session-09_transaction_real.py) | Example 3: The real PyMongo code (run it against Atlas or a replica set) | `python session-09_transaction_real.py` |
| [`session-09_transaction_sim.py`](session-09_transaction_sim.py) | Example 2: All-or-nothing with a transaction | `python session-09_transaction_sim.py` |

### [Session 10: MongoDB Tools: Compass and BI Connector](../session-10-mongodb-tools.md)

| File | What it does | How to run |
|---|---|---|
| [`session-10-mongodb-tools.ipynb`](session-10-mongodb-tools.ipynb) | Executed notebook with every Python example of the session | `jupyter notebook session-10-mongodb-tools.ipynb` (or the Colab badge on the session page) |
| [`session-10_bi_sql.py`](session-10_bi_sql.py) | Example 3: What the BI Connector does | `python session-10_bi_sql.py` |
| [`session-10_import_export.py`](session-10_import_export.py) | Example 1: Import and export from Python | `python session-10_import_export.py` |
| [`session-10_schema_analysis.py`](session-10_schema_analysis.py) | Example 2: The Compass Schema tab, by hand | `python session-10_schema_analysis.py` |

### [Session 11: MongoDB in the Cloud with Atlas](../session-11-mongodb-cloud-atlas.md)

| File | What it does | How to run |
|---|---|---|
| [`session-11-mongodb-cloud-atlas.ipynb`](session-11-mongodb-cloud-atlas.ipynb) | Executed notebook with every Python example of the session | `jupyter notebook session-11-mongodb-cloud-atlas.ipynb` (or the Colab badge on the session page) |
| [`session-11_atlas_client.py`](session-11_atlas_client.py) | Example 2: One client factory for laptop, Colab and Atlas | `python session-11_atlas_client.py` |
| [`session-11_connection_strings.py`](session-11_connection_strings.py) | Example 1: Building and reading a connection string | `python session-11_connection_strings.py` |
| [`session-11_vector_search_demo.py`](session-11_vector_search_demo.py) | Example 3: The idea behind Atlas Vector Search | `python session-11_vector_search_demo.py` |

### [Session 12: Connecting Python to MongoDB with PyMongo](../session-12-python-connectivity-pymongo.md)

| File | What it does | How to run |
|---|---|---|
| [`session-12-python-connectivity-pymongo.ipynb`](session-12-python-connectivity-pymongo.ipynb) | Executed notebook with every Python example of the session | `jupyter notebook session-12-python-connectivity-pymongo.ipynb` (or the Colab badge on the session page) |
| [`session-12_etl_batch.py`](session-12_etl_batch.py) | Example 3: A batched, idempotent ETL job | `python session-12_etl_batch.py` |
| [`session-12_repository.py`](session-12_repository.py) | Example 1: A repository class with error handling | `python session-12_repository.py` |
| [`session-12_to_pandas.py`](session-12_to_pandas.py) | Example 2: MongoDB → pandas → MongoDB | `python session-12_to_pandas.py` |

---

<sub>Prepared by **Hamna Zahid Khan**, Junior Lecturer</sub>
