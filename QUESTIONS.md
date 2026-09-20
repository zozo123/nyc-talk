# Skeptical Q&A

## Is this a sandbox escape?

No kernel escape is demonstrated. The title refers to task-policy violations through authority exposed to the worker: service credentials, writable mounts, a reachable recipient and a worker-influenced acceptance dependency. The Linux boundaries do what the chosen configuration allows. The acceptance example is a separate local fixture, not a proof that arbitrary hostile code is contained.

## Is there an original vendor vulnerability here?

No. The credential, mount, endpoint and verifier examples are controlled configurations in our code. Test tampering and artifact binding have prior art. The contribution is a reproducible boundary-testing method with explicit controls and an inspectable release path. The reference-API defect found during review belongs to this repository; no remote exploit route or commercial impact was established.

## Did a real model discover or execute these attacks?

No model attack-success rate was measured. Deterministic adversarial worker actions isolate the enforcement mechanism. A model experiment would need separately pinned model/version, prompts, tool policy, sampling configuration, repeated trials, denominators and failure classifications. Do not use these assertion totals as that experiment.

## Did HTTP really return 200, or did a program just print 200?

Both layers are explicit. The original handler was a command-line status model. The final `factory/http_demo.py` serves that same committed handler through a loopback HTTP wrapper and requests it with urllib. It then requests the actual released good file. HTTP responses are real. Credentials and authorization states are synthetic fixtures, not a production authentication stack.

## Was checker.py actually immutable?

The claim is narrower: no edit was needed. Its file bytes are measured before and after each execution and remain equal in the dependency attack. A separate regression deliberately edits the file to confirm that the hash is read from disk. We do not claim OS-enforced immutability of the checker in the local fixture. Even a read-only checker would still need trustworthy authoritative dependencies.

## Why isn't a second VM enough?

A second machine that evaluates the candidate against worker-chosen expected results would retain that trust error. Independence requires controller ownership of the criteria, dependencies and comparison, plus real separation from candidate execution. A fresh directory or the absence of a copied expectations file is not protection from code sharing controller privileges.

## Can the worker still propose tests?

Yes. Proposed tests are candidate material. They can inform review and be run as extra checks. They should not silently replace the authoritative release criteria. Changes to those criteria need an independently authorized review path. Treat imports, plugins, configurations, data files and launch context as part of the verifier's relevant dependencies.

## Does a short-lived credential solve the problem?

Lifetime limits time, not resource scope. The fixture tests task resource restrictions, audience and expiry separately. Real deployments need equivalent enforcement at their service or credential broker. No commercial identity provider or credential minting system was evaluated here.

## Does the broker solve data loss in general?

No. It closes one deliberate channel by removing the direct route and fixing operation, recipient and body. A free-text or arbitrary-file report can carry secrets and needs its own disclosure policy. Other routes, covert channels and timing channels are outside this experiment. The namespace observation specifically concerns reachability of the host-loopback fixture service.

## What does the approval authenticate?

The reference uses an HMAC with a controller-held ephemeral key. It binds task/run, artifact-manifest digest, verifier-source bundle and launch description, expected results, policy, environment-manifest description, decision and nonce. This is not a public digital signature, hardware attestation or proof that every described environment property was enforced. The local manifest explicitly says it is not OS/network isolated. Production needs a trustworthy executor and provenance of its actual environment.

## How do you know digest binding, rather than replay protection, rejected the swap?

Order. First use an unused approval with the wrong artifact: DENIED. Then use that same approval with the correct artifact: PUBLISHED. Finally reuse it: DENIED. A swap tested only after successful publication would confound digest binding and nonce consumption. The final tests correct that weakness in the original demonstration.

## What was wrong with your own Frozen object?

The baseline allowed controller-side code to mutate its payload while leaving its digest label unchanged. The old gate trusted that label and logged a publication without releasing a file. The probe required access to that trusted-side object; no sandbox-to-controller path was shown. The final implementation revalidates objects, rehashes the store and writes and tests actual released bytes. See the archived baseline probe and Appendix C.

## Is the gate production-ready?

No. It is a readable single-controller reference. Concurrent atomic nonce consumption, crash recovery, durable key management, access control and strong candidate isolation are deployment requirements. Ephemeral keys make old approvals invalid after restart. Unit tests establish specific behavior, not a proof of a concurrent protocol. Local fixture execution must not be used as an arbitrary-code service.

## Can the history itself be forged?

A hash chain detects the demonstrated rewrite only against an unchanged trusted head. A worker that controls both the log and its purported anchor can replace both. Authentic history can faithfully record a poor decision. Release must be enforced separately; logs are not an approval authority.

## What would falsify the advertised result?

A forbidden operation succeeding after the stated restriction, legitimate work failing under it, changed checker bytes in the dependency-only example, mismatched verified/authorized/released manifests, or an unused approval failing to distinguish the correct and swapped artifacts. Missing or malformed observations mean no evidence, not a successful defense.

## What should an engineer do tomorrow?

Choose one real task. Write one forbidden and one required operation for each of the four interfaces. Run them in the actual deployment, inspect the external effect and trace one accepted artifact to its released bytes. Record who owns each decision-changing input. Keep the reproducible result, source pin and scope next to the configuration rather than relying on the worker's completion message.
