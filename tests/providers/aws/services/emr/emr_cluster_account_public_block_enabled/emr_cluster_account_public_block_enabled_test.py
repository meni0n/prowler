from unittest import mock

from prowler.providers.aws.services.emr.emr_service import (
    BlockPublicAccessConfiguration,
)
from tests.providers.aws.audit_info_utils import (
    AWS_ACCOUNT_NUMBER,
    AWS_REGION_EU_WEST_1,
)


class Test_emr_cluster_account_public_block_enabled:
    def test_account_public_block_enabled(self):
        emr_client = mock.MagicMock
        emr_client.audited_account = AWS_ACCOUNT_NUMBER
        emr_client.block_public_access_configuration = {
            AWS_REGION_EU_WEST_1: BlockPublicAccessConfiguration(
                block_public_security_group_rules=True
            )
        }
        with mock.patch(
            "prowler.providers.aws.services.emr.emr_service.EMR",
            new=emr_client,
        ):
            # Test Check
            from prowler.providers.aws.services.emr.emr_cluster_account_public_block_enabled.emr_cluster_account_public_block_enabled import (
                emr_cluster_account_public_block_enabled,
            )

            check = emr_cluster_account_public_block_enabled()
            result = check.execute()

            assert len(result) == 1
            assert result[0].region == AWS_REGION_EU_WEST_1
            assert result[0].resource_id == AWS_ACCOUNT_NUMBER
            assert result[0].status == "PASS"
            assert (
                result[0].status_extended
                == "EMR Account has Block Public Access enabled."
            )

    def test_account_public_block_disabled(self):
        emr_client = mock.MagicMock
        emr_client.audited_account = AWS_ACCOUNT_NUMBER
        emr_client.block_public_access_configuration = {
            AWS_REGION_EU_WEST_1: BlockPublicAccessConfiguration(
                block_public_security_group_rules=False
            )
        }
        with mock.patch(
            "prowler.providers.aws.services.emr.emr_service.EMR",
            new=emr_client,
        ):
            # Test Check
            from prowler.providers.aws.services.emr.emr_cluster_account_public_block_enabled.emr_cluster_account_public_block_enabled import (
                emr_cluster_account_public_block_enabled,
            )

            check = emr_cluster_account_public_block_enabled()
            result = check.execute()

            assert len(result) == 1
            assert result[0].region == AWS_REGION_EU_WEST_1
            assert result[0].resource_id == AWS_ACCOUNT_NUMBER
            assert result[0].status == "FAIL"
            assert (
                result[0].status_extended
                == "EMR Account has Block Public Access disabled."
            )
