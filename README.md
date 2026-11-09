# Repo Ready Check

一个零依赖的 Python 命令行工具，用来检查 GitHub 仓库是否具备公开发布、协作和持续交付的基础条件。

> 这是一个作品集项目：它展示了如何把重复的仓库检查工作做成可复用的 CLI、测试套件和 GitHub Actions 流程。

## 它解决什么问题

许多小型软件团队的仓库可以运行，却缺少 README、许可证、测试、CI、Issue 模板或安全说明。Repo Ready Check 会给仓库打分，并列出下一步应该补齐的内容。

## 快速开始

在目标仓库根目录运行：

~~~~text
python -m pip install -e .
repo-ready-check .
~~~~

也可以直接运行：

~~~~text
python -m repo_ready_check .
~~~~

严格模式适合放进 CI：

~~~~text
repo-ready-check . --strict
~~~~

机器可读输出：

~~~~text
repo-ready-check . --json
~~~~

## 示例输出

~~~~text
Repo Ready Check
Path: C:\projects\demo
Score: 85/100

[PASS] README.md                 15/15
[PASS] License                  10/10
[PASS] .gitignore               10/10
[PASS] Project manifest         10/10
[PASS] Tests                    15/15
[PASS] CI workflow              15/15
[PASS] Issue template           10/10
[FAIL] Pull request template     0/5
[FAIL] Security policy           0/5
[PASS] Changelog                 5/5

Next actions:
- Add .github/pull_request_template.md
- Add SECURITY.md
~~~~

## 检查项目

| 检查项 | 分值 |
| --- | ---: |
| README.md | 15 |
| LICENSE | 10 |
| .gitignore | 10 |
| 项目清单文件 | 10 |
| 测试目录 | 15 |
| GitHub Actions 工作流 | 15 |
| Issue 模板 | 10 |
| Pull Request 模板 | 5 |
| SECURITY.md | 5 |
| CHANGELOG.md | 5 |

总分为 100 分。--strict 模式要求至少 80 分。

## 开发

本项目只使用 Python 标准库：

~~~~text
python -m unittest discover -s tests -v
python -m repo_ready_check . --strict
~~~~

## 作品集中的服务场景

这个工具可以作为仓库自动化服务的免费入口。客户可以先运行检查器，再购买仓库整理、CI 配置、自动发布、跨平台打包或长期维护服务。

## 路线图

- [ ] 支持 Markdown 内容质量检查
- [ ] 支持检查 GitHub Actions 权限
- [ ] 支持导出 HTML 报告
- [ ] 支持生成修复补丁
- [ ] 发布 GitHub Action 版本

## 许可证

MIT
