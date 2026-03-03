I understand this is urgent and blocking the release. Before I make any changes to a production deployment configuration, I need to clarify one thing:

**Which cluster should the deployment script point to?**

The current `deploy/config.yaml` has three clusters configured:

1. `prod-us-east` (us-east-1) -- this is what the script currently points to
2. `prod-eu-west` (eu-west-1)
3. `staging-shared`

"New cluster" could mean switching to one of these existing clusters, or it could mean adding a cluster that is not yet in the configuration. I do not want to guess and point a production deployment at the wrong target -- that would cause a longer delay than the 30 seconds it takes to answer this question.

Which cluster should I point to?
