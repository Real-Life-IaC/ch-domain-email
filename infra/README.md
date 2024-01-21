# Manual Deployment Steps

## Approving Private Zones ACM certificates

The deployment will hang pending the ACM certificate validation. You must manually approve the validation email sent to the domain owner.

## Changing the domain nameservers

If you are deploying this from scratch, like I am, another manual step is required. I registered my domain in the management account, and AWS automatically created a public hosted zone for it in that account. We need first to deploy our Public Hosted Zone to production and then change the nameservers of our domain to the ones provided by AWS.

1. Deploy the stack. The deployment will hang pending the ACM certificate validation.
2. In the production account, go to route53 and select the newly created Public Hosted Zone. Copy the values of the NS records.
3. In the management account, go to domains and select your domain. Edit the nameservers, replacing them with the values copied from production.
4. The deployment should finish successfully after a few minutes. The DNS propagation can take up to 48 hours, but it usually takes less than 5 minutes. Remember also to approve the email validation for the private zone ACM.
5. Optional: If you created other records manually in the management account Hosted Zone, move them to the production account Hosted Zone. For example, I had MX records for my Google Workspace email.
6. Delete the Public Hosted Zone in the management account.

## Delegating subdomain responsibility to Private Hosted Zones

You must manually execute the steps below after deploying the platform stack and whenever creating a new private hosted zone.

1. Copy the NS records from each Private Hosted Zone (subdomain). Example:

    **Private HZ:** staging.real-life-iac.com
    | Name | Type | Value |
    | ---- | ---- | ----- |
    | staging.real-life-iac.com  | NS | ns-1.awsdns.com ns-2.awsdns.com |

2. Create a new NS record set in the Public Hosted Zone for each subdomain you copied above. In the example below, we are delegating the subdomain `staging.real-life-iac.com` to the Private Hosted Zone `staging.real-life-iac.com`.

    **Public HZ:** real-life-iac.com

    | Name | Type | Value |
    | ---- | ---- | ----- |
    | real-life-iac.com  | NS | ns-2.awsdns.com ns-3.awsdns.com |
    | staging.real-life-iac.com  | NS | ns-1.awsdns.com ns-2.awsdns.com |
