import aws_cdk as cdk

from constructs_package.constants import AwsAccountId
from constructs_package.constants import AwsRegion
from constructs_package.constants import AwsStage
from infra.stack import DomainEmailStack


app = cdk.App()

DomainEmailStack(
    scope=app,
    id=f"DomainEmail-{AwsStage.SANDBOX}",
    env=cdk.Environment(account=AwsAccountId.SANDBOX, region=AwsRegion.US_EAST_1),
)

DomainEmailStack(
    scope=app,
    id=f"DomainEmail-{AwsStage.STAGING}",
    env=cdk.Environment(account=AwsAccountId.STAGING, region=AwsRegion.US_EAST_1),
)

DomainEmailStack(
    scope=app,
    id=f"DomainEmail-{AwsStage.PRODUCTION}",
    env=cdk.Environment(account=AwsAccountId.PRODUCTION, region=AwsRegion.US_EAST_1),
    public_hosted_zone=True,
)

app.synth()
