# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
from azure.monitor.query import MetricsQueryClient
from azure.identity import DefaultAzureCredential

credential  = DefaultAzureCredential()

client = MetricsQueryClient(credential)

metrics_uri = os.environ['METRICS_RESOURCE_URI']
response = client.list_metric_definitions(metrics_uri, metric_namespace='microsoft.eventgrid/topics')

for item in response:
    print(item)
    for availability in item.metric_availabilities:
        print(availability.time_grain)
