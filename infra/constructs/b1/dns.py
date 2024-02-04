from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_ssm as ssm
from constructs import Construct


class B1PublicHostedZone(Construct):
    """
    Route53 Public Hosted Zone

    Use this construct to create a hosted zone,
    an ACM certificate, and SSM parameters.
    """

    def __init__(
        self,
        scope: Construct,
        id: str,
        domain_name: str,
    ) -> None:
        super().__init__(scope, id)

        zone_name = domain_name

        self.hosted_zone = route53.PublicHostedZone(
            scope=self,
            id="HostedZone",
            zone_name=zone_name,
            caa_amazon=False,
            comment=f"{zone_name} Public Hosted Zone",
        )

        # Create the SSL certificate for the hosted zone
        # It will automatically validate by adding a
        # CNAME record to the public hosted zone
        self.certificate = acm.Certificate(
            scope=self,
            id="Certificate",
            domain_name=f"*.{zone_name}",
            validation=acm.CertificateValidation.from_dns(
                hosted_zone=self.hosted_zone
            ),
        )

        # Create a SSM parameter for the private hosted zone id
        ssm.StringParameter(
            scope=self,
            id="HostedZoneId",
            string_value=self.hosted_zone.hosted_zone_id,
            description=f"{zone_name} Public Hosted Zone Id",
            parameter_name=f"/platform/dns/{zone_name}/public-hosted-zone/id",
        )

        # Create a SSM parameter for the private hosted zone name
        ssm.StringParameter(
            scope=self,
            id="HostedZoneName",
            string_value=self.hosted_zone.zone_name,
            description=f"{domain_name} Public Hosted Zone Name",
            parameter_name=f"/platform/dns/{domain_name}/public-hosted-zone/name",
        )

        # Create a SSM parameter for the private hosted zone certificate arn
        ssm.StringParameter(
            scope=self,
            id="CertificateArn",
            string_value=self.certificate.certificate_arn,
            description=f"{domain_name} Public Certificate Arn",
            parameter_name=f"/platform/dns/{domain_name}/public-hosted-zone/certificate/arn",
        )


class B1PrivateHostedZone(Construct):
    """
    Route53 Private Hosted Zone

    Use this construct to create a hosted zone,
    an ACM certificate, and SSM parameters.
    """

    def __init__(
        self,
        scope: Construct,
        id: str,
        domain_name: str,
        vpc: ec2.IVpc,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        stage = ssm.StringParameter.value_from_lookup(
            scope=self,
            parameter_name="/platform/stage",
        )

        zone_name = f"{stage}.{domain_name}"
        # Create the private hosted zone
        self.hosted_zone = route53.HostedZone(
            scope=self,
            id="HostedZone",
            vpcs=[vpc],
            zone_name=zone_name,
            comment=f"{zone_name} Private Hosted Zone",
        )

        # Create the SSL certificate for the hosted zone
        # Private hosted zones are not accessible from the internet
        # so we need to use email validation instead of DNS
        self.certificate = acm.Certificate(
            scope=self,
            id="Certificate",
            domain_name=f"*.{zone_name}",
            validation=acm.CertificateValidation.from_email(),
        )

        # Create a SSM parameter for the private hosted zone id
        ssm.StringParameter(
            scope=self,
            id="HostedZoneId",
            string_value=self.hosted_zone.hosted_zone_id,
            description=f"{domain_name} Private Hosted Zone Id",
            parameter_name=f"/platform/dns/{domain_name}/private-hosted-zone/id",
        )

        # Create a SSM parameter for the private hosted zone name
        ssm.StringParameter(
            scope=self,
            id="HostedZoneName",
            string_value=self.hosted_zone.zone_name,
            description=f"{domain_name} Private Hosted Zone Name",
            parameter_name=f"/platform/dns/{domain_name}/private-hosted-zone/name",
        )

        # Create a SSM parameter for the private hosted zone certificate arn
        ssm.StringParameter(
            scope=self,
            id="CertificateArn",
            string_value=self.certificate.certificate_arn,
            description=f"{domain_name} Private Certificate Arn",
            parameter_name=f"/platform/dns/{domain_name}/private-hosted-zone/certificate/arn",
        )
