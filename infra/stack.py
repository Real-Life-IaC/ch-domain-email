import aws_cdk as cdk

from constructs import Construct
from infra.constructs.b2.dns import B2PrivateHostedZones
from infra.constructs.b2.dns import B2PublicHostedZones
from infra.constructs.b2.email import B2EmailServices


class DomainEmailStack(cdk.Stack):
    """Create the AWS foundational resources for the Production stage"""

    def __init__(
        self,
        scope: Construct,
        id: str,
        public_hosted_zone: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        B2PrivateHostedZones(
            scope=self,
            id="PrivateHostedZone",
        )

        if public_hosted_zone:
            public_hosted_zones = B2PublicHostedZones(
                scope=self,
                id="PublicHostedZone",
            )

            B2EmailServices(
                scope=self,
                id="EmailService",
                hosted_zones=public_hosted_zones,
            )

        # Add tags to everything in this stack
        cdk.Tags.of(self).add(key="owner", value="Platform")
        cdk.Tags.of(self).add(key="repo", value="ch-domain-email")
        cdk.Tags.of(self).add(key="stack", value=self.stack_name)
