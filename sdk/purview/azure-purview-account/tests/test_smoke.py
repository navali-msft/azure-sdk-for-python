# coding: utf-8
# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -------------------------------------------------------------------------
from testcase import PurviewAccountTest, PurviewAccountPowerShellPreparer
from _util import PurviewAccountRecordingProcessor, PurviewAccountCollectionsRecordingProcessor


class PurviewAccountSmokeTest(PurviewAccountTest):

    @PurviewAccountPowerShellPreparer()
    def test_basic_smoke_test(self, purviewaccount_endpoint):
        self.recording_processors.append(PurviewAccountRecordingProcessor())
        client = self.create_client(endpoint=purviewaccount_endpoint)
        response = client.accounts.get_access_keys()
        assert set(response.keys()) == set(['atlasKafkaPrimaryEndpoint', 'atlasKafkaSecondaryEndpoint'])

    @PurviewAccountPowerShellPreparer()
    def test_collections_list(self, purviewaccount_endpoint):
        self.recording_processors.append(PurviewAccountCollectionsRecordingProcessor())
        client = self.create_client(endpoint=purviewaccount_endpoint)
        response = client.collections.list_collections()
        result = [item for item in response]
        for item in result:
            assert set(item.keys()) == set(['name', 'friendlyName', 'description', 'systemData', 'collectionProvisioningState'])
