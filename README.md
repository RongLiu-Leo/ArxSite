# ArxSite
![](arxsite/teaser.png)
## 1. Go to your Github project root folder
```
cd <Your Github Project Root>
```
## 2. Create and switch to a new empty branch called 'website'
```
git checkout --orphan website
git rm -rf .  # Remove all tracked files from index
```
## 3. Run arxsite with your desired arXiv URL (replace <url> accordingly)
```
arxsite <url>
```
## 4. Add all files, commit, and push the website branch
```
git add .
git commit -m "Initialize website from arxsite"
git push origin website
```
## 5. Use the created website branch to host Github Page
![](instruction.png)
## 6. Check your project website
The website could be found at
```
https://<Your Github User Name>.github.io/<Repo Name>/
```
One example is shown as [https://rongliu-leo.github.io/arxsite/](https://rongliu-leo.github.io/arxsite/) after running
```
arxsite https://arxiv.org/abs/2501.18630
```
