# Bloodhound analyzer

Generate `.csv` reports from Neo4j database hosting BloodHound data.

## Description
`bloodhound-analyzer` executes Neo4j queries (Cypher queries) defined in an external file against a defined database. Neo4j does nto natively support exporting `csv` files with separate columns so the query output is parsed using `bloodhound_analyzer/analyzer.py` and converted to standard `csv` files.

## Configuration
Use [config.yaml.sample](config.yaml.sample) as basis for a new configuration file located either at `/etc/bloodhound-analyzer/config.yaml` or at the path defined in `BLOODHOUND_ANALYZER_CONFIG` environment variable.

```yaml
logging:
    version: 1
    disable_existing_loggers: false
    loggers:
        '':
            level: INFO
neo4j:
    address: neo4j://localhost:7687
    username: neo4j
    password: neo4j
bloodhound-analyzer:
    query_file: /etc/bloodhound-analyzer/cypher_queries.in
    output_dir: /etc/bloodhound-analyzer/csv_output
    tmp_dir: /tmp/bloodhound_analyzer
```
In the file above, change neo4j connection details as well as `bloodhound-analyzer` options. Notably:
* `query_file`: The file defining the queries to be executed as well as the output filename for each of the queries. 

    An example query configuration can be found at [cypher-queries.in.sample](cypher-queries.in.sample).

* `output_dir`: The directory under which final `csv` files will be stored. In order to discern consecutive executions, `csv` reports are stored under `output_dir/<EXECUTION_TIMESTAMP>.zip`.


## Usage
After defining the required configuration options as described in the previous section, execute:
```
bloodhound-analyzer
```

Keep in mind that `BLOODHOUND_ANALYZER_CONFIG` environment variable can be defined to override default configuration at `/etc/bloodhound-analyzer/config.yaml`