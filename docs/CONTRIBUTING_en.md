# 🎉 Contributing to CMDB 🥳

First of all, thank you very much for considering contributing to our project! We welcome any kind of contribution, whether it's proposing new functional features, improving code, fixing bugs, or improving documentation.

This guide will provide all the relevant information to help you get started working on this project. Please take a few minutes to read it, it will help us collaborate better and create a better project together.

## ❖ Submit Issue

Before jumping into a PR be sure to search [existing PRs](https://github.com/veops/cmdb/pulls) or [issues](https://github.com/veops/cmdb/issues) for an open or closed item that relates to your submission.

If it's a bug fix, please raise it in an Issue first.

For new feature additions, please first contact us directly via the contact information we provide.

## ❖ Pull Requests Steps

1. Fork this project's repo on Github
2. Create a new branch on your local copy to develop new features, fix bugs, or make other contributions, `git checkout -b feat/xxxx`
3. Submit your changes: `git commit -am 'feat: add xxxxx'`
4. Push your branch: `git push origin feat/xxxx`
5. To submit a `Pull Request`, make sure your source branch is the one you just pushed, and your target branch is the `master` branch of the CMDB project.
6. After submitting, watch out for emails and notifications associated with the Pull request. Once it's approved, we'll merge it into the `master` branch as planned. Doing a new round of releases

## ❖ Development Environment
- Python >= 3.8
- node >= 14.17.6
- docker

## ❖ Code Style

**API**: Please follow the [Python Style](https://google.github.io/styleguide/pyguide.html)

**UI**: Please follow the [node-style-guide](https://github.com/felixge/node-style-guide)

## ❖ Commit Messages

+ Please follow the [Angular](https://github.com/conventional-changelog/conventional-changelog/tree/master/packages/conventional-changelog-angular)

+ Commit with different scopes
  - API: `feat(api): xxx`
  - UI: `feat(ui): xxx`

+ Please keep the commit message in English for better understanding by all developers.

  - `feat` Add new features
  - `fix` Fix the problem/BUG
  - `style` The code style is related and does not affect the running result
  - `perf` Optimization/performance improvement
  - `refactor` Refactor
  - `revert` Undo edit
  - `test` Test related
  - `docs` Documentation/notes
  - `chore` Dependency update/scaffolding configuration modification etc.
  - `workflow` Workflow improvements
  - `ci` Continuous integration
  - `types` Type definition file changes
  - `wip` In development

## ❖ Code Content

Please keep the code comments and code content in English for better understanding by all developers.