from constructs import Construct
from infra.constructs.b1.ses import B1EmailService
from infra.constructs.b2.dns import B2PublicHostedZones


class B2EmailServices(Construct):
    """Hosted Zone and Email Service"""

    def __init__(
        self,
        scope: Construct,
        id: str,
        hosted_zones: B2PublicHostedZones,
    ) -> None:
        super().__init__(scope, id)

        # Create an SES for mail.real-life-iac.com
        B1EmailService(
            scope=self,
            id="RealLifeIacEmailService",
            domain_name=hosted_zones.real_life_iac.hosted_zone.zone_name,
            mail_from_subdomain="mail",
            public_hosted_zone=hosted_zones.real_life_iac.hosted_zone,
            email_usernames=["support"],
            smtp_usernames=["auth0"],
        )
