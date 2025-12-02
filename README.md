# AutoPR Demo (ready-to-push)

This folder contains a minimal demo repository you can copy to GitHub to showcase AutoPR in action.


How to use
1. Create a new GitHub repository (for example: `autopr-demo`).
2. Copy the contents of `demo/demo-repo-ready` into your new repo or push directly using the included publish helpers.

## Push the demo quickly (example)
From your local machine, assuming you are inside the `demo/demo-repo-ready` folder:

```bash
# Using the helper script (Linux/macOS)
./publish_demo.sh git@github.com:<YOUR_USER>/autopr-demo.git main

# or on Windows PowerShell
./publish_demo.ps1 -RemoteUrl git@github.com:<YOUR_USER>/autopr-demo.git -Branch main
```

3. Edit `.github/workflows/auto-pr-demo.yml` in the remote repo and update the `pip install` line to point to the AutoPR repository you will publish (for example your fork):

```yaml
pip install git+https://github.com/<YOUR_USER>/AutoPR.git
```

4. Create a branch in the demo repo, change a single line (eg. edit README or a test), open a Pull Request — the workflow will run and post a demo comment back to the PR.

What the demo contains
- sample Python project with tests (src/sample.py + tests)
- GitHub Actions workflow to run tests and call AutoPR
- Example PR diff lives in demo/prs (for local demonstrations)
