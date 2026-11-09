# 发布到 GitHub

本项目已经在本地提交。远程仓库地址预设为：

https://github.com/chengyangguang47-cloud/repo-ready-check

## 第一步：创建空仓库

登录 GitHub 后打开新建仓库页面：

https://github.com/new

填写：

- Repository name：`repo-ready-check`
- Description：`Audit a repository for release and collaboration readiness.`
- Visibility：Public
- 不要勾选 README、.gitignore 或 License

点击 Create repository。

## 第二步：推送本地项目

在项目目录运行：

~~~~powershell
git push -u origin main
~~~~

如果 GitHub 要求登录，请在浏览器完成登录或按 Git Credential Manager 的提示操作，不要把密码写进命令行。

## 第三步：检查结果

打开仓库首页，确认能看到 README、Actions、Issues 和 LICENSE。进入 Actions 页面，等待 CI 工作流完成。
