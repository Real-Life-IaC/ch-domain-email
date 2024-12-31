from aws_cdk import aws_iam as iam
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_ses as ses
from constructs import Construct


class B1EmailService(Construct):
    """
    Create Simple Email Service resources

    - Email identities are used to send emails from SES.
    - SMTP users are used to send emails from external services.

    For SMTP users, after deployment, find the user in the
    AWS IAM Console and generate the Access Key and Secret Key.
    """

    def __init__(
        self,
        scope: Construct,
        id: str,
        domain_name: str,
        mail_from_subdomain: str,
        public_hosted_zone: route53.PublicHostedZone,
        email_usernames: list[str],
        smtp_usernames: list[str],
    ) -> None:
        super().__init__(scope, id)

        # Create the SES configuration set
        configuration_set = ses.ConfigurationSet(
            scope=self,
            id="ConfigurationSet",
            reputation_metrics=True,
            sending_enabled=True,
            suppression_reasons=ses.SuppressionReasons.BOUNCES_AND_COMPLAINTS,
            tls_policy=ses.ConfigurationSetTlsPolicy.REQUIRE,
        )

        # Create the SES Email Identity
        domain_identity = ses.EmailIdentity(
            scope=self,
            id="DomainIdentity",
            identity=ses.Identity.public_hosted_zone(hosted_zone=public_hosted_zone),
            configuration_set=configuration_set,
            dkim_identity=ses.DkimIdentity.easy_dkim(
                signing_key_length=ses.EasyDkimSigningKeyLength.RSA_2048_BIT
            ),
            dkim_signing=True,
            feedback_forwarding=True,
            mail_from_behavior_on_mx_failure=ses.MailFromBehaviorOnMxFailure.REJECT_MESSAGE,
            mail_from_domain=f"{mail_from_subdomain}.{domain_name}",
        )

        # Email Identities
        for username in email_usernames:
            email_identity = ses.EmailIdentity(
                scope=self,
                id=f"{username}AT{domain_name}EmailIdentity",
                identity=ses.Identity.email(email=f"{username}@{domain_name}"),
                configuration_set=configuration_set,
                dkim_identity=ses.DkimIdentity.easy_dkim(
                    signing_key_length=ses.EasyDkimSigningKeyLength.RSA_2048_BIT
                ),
                dkim_signing=True,
                feedback_forwarding=True,
                mail_from_behavior_on_mx_failure=ses.MailFromBehaviorOnMxFailure.REJECT_MESSAGE,
                mail_from_domain=f"{mail_from_subdomain}.{domain_name}",
            )
            email_identity.node.add_dependency(domain_identity)

        # Create SMTP IAM users
        for username in smtp_usernames:
            smtp_user = iam.User(
                scope=self,
                id=f"{domain_name}AT{domain_name}SmtpUser",
                user_name=f"SES-SMTP-{username}-{domain_name}",
            )
            smtp_user.add_to_policy(
                statement=iam.PolicyStatement(
                    actions=["ses:SendRawEmail"],
                    resources=["*"],
                    effect=iam.Effect.ALLOW,
                )
            )
