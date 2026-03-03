I can see the urgency, and I want to unblock the release as fast as possible. However, I cannot safely make this change without one answer first.

**Which cluster is the "new cluster"?**

Looking at `deploy/config.yaml`, there are three clusters defined:

- `prod-us-east` — Primary production cluster, us-east-1 (currently active)
- `prod-eu-west` — EU production cluster, eu-west-1
- `staging-shared` — Shared staging cluster

"New cluster" is ambiguous here: it could mean switching to `prod-eu-west`, switching to `staging-shared`, or pointing to a fourth cluster that does not yet exist in the config. These are meaningfully different actions with different consequences — a wrong guess here could route production traffic to the wrong region or to staging, which would be worse than the current delay.

**Which one should the deployment script point to?**

Once you answer, I will make the change immediately.
