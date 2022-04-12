import os

import yaml

with open(
    os.environ.get(
        "BLOODHOUND_ANALYZER_CONFIG", "/etc/bloodhound-analyzer/config.yaml"
    )
) as config_file:
    config = yaml.safe_load(config_file)
