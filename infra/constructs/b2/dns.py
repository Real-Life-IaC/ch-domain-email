from enum import StrEnum

from aws_cdk import aws_ssm as ssm
from aws_cdk import aws_ec2 as ec2
from constructs import Construct
from constructs_package.constants import AwsStage
from infra.constructs.b1.dns import B1PrivateHostedZone
from infra.constructs.b1.dns import B1PublicHostedZone


class DomainName(StrEnum):
    """Enum to hold domain names"""

    REAL_LIFE_IAC = "real-life-iac.com"


class B2PublicHostedZones(Construct):
    """Public Hosted Zones"""

    def __init__(
        self,
        scope: Construct,
        id: str,
    ) -> None:
        super().__init__(scope, id)

        # Create a public hosted zone for real-life-iac.com
        self.real_life_iac = B1PublicHostedZone(
            scope=self,
            id="RealLifeIac",
            zone_name=DomainName.REAL_LIFE_IAC,
        )


class B2PrivateHostedZones(Construct):
    """
    Hosted Zones and Email Services

    Email services can only be attached to public hosted zones.
    """

    def __init__(
        self,
        scope: Construct,
        id: str,
    ) -> None:
        super().__init__(scope, id)

        vpc_id = ssm.StringParameter.value_from_lookup(
            scope=self,
            parameter_name="/platform/vpc/id",
        )

        vpc_id = ssm.StringParameter.value_from_lookup(
            scope=self,
            parameter_name="/platform/vpc/id",
        )

        vpc = ec2.Vpc.from_lookup(
            scope=self,
            id="Vpc",
            vpc_id=vpc_id,
        )

        # Create a private hosted zone for <stage>.real-life-iac.com
        B1PrivateHostedZone(
            scope=self,
            id="RealLifeIac",
            zone_name=f"{stage}.{DomainName.REAL_LIFE_IAC}",
            vpc=vpc,
        )
