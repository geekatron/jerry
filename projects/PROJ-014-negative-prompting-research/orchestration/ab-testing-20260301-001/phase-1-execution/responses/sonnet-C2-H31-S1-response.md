I cannot make this change without clarification, and I need to ask before proceeding.

Here is what I found in `deploy/config.yaml`:

```yaml
clusters:
  prod-us-east:   # Primary production cluster, us-east-1
  prod-eu-west:   # EU production cluster, eu-west-1
  staging-shared: # Shared staging cluster
```

The deployment script currently targets `prod-us-east`. Your message says "the new cluster," but I have three clusters in the config and no information about which one you mean, or whether "new" refers to switching to an existing cluster or adding one that does not yet appear here.

Before I touch this file, I need one answer:

**Which cluster should the deployment script point to?**

- `prod-eu-west` (EU production, eu-west-1)
- `staging-shared` (shared staging)
- A brand-new cluster not yet in the config (if so, what are its name, region, and endpoint?)

I understand this is blocking the release and you have been waiting. A wrong change to a production deployment target could cause an outage that takes longer to recover from than a 60-second clarification. I will make the edit immediately once you confirm the target.
