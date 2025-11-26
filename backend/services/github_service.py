import requests
import base64
import logging

logger = logging.getLogger(__name__)

class GitHubService:
    def __init__(self):
        self.base_url = "https://api.github.com/repos"

    def _get_default_branch(self, owner, repo):
        try:
            url = f"{self.base_url}/{owner}/{repo}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json().get("default_branch", "main")
            return "main"
        except Exception:
            return "main"

    def get_repo_content(self, repo_url):
        """
        Fetch README and file structure from GitHub repo.
        repo_url: https://github.com/owner/repo
        """
        try:
            # Parse owner/repo from URL
            parts = repo_url.rstrip("/").split("/")
            if len(parts) < 2:
                raise ValueError("Invalid GitHub URL")
            
            owner = parts[-2]
            repo = parts[-1]
            
            # Get default branch
            branch = self._get_default_branch(owner, repo)
            
            # 1. Fetch README
            readme_content = ""
            readme_url = f"{self.base_url}/{owner}/{repo}/readme"
            response = requests.get(readme_url)
            
            if response.status_code == 200:
                data = response.json()
                # Content is base64 encoded
                readme_content = base64.b64decode(data["content"]).decode("utf-8")
            else:
                logger.warning(f"README not found for {owner}/{repo}")

            # 2. Fetch File Structure (root level)
            files_list = []
            contents_url = f"{self.base_url}/{owner}/{repo}/contents"
            response = requests.get(contents_url)
            
            if response.status_code == 200:
                items = response.json()
                for item in items:
                    files_list.append(f"{item['type']}: {item['name']}")
                    
                    # If it's a package.json or requirements.txt, fetch content
                    if item["name"] in ["package.json", "requirements.txt", "pyproject.toml"]:
                        file_res = requests.get(item["download_url"])
                        if file_res.status_code == 200:
                            files_list.append(f"--- Content of {item['name']} ---\n{file_res.text}\n--- End of {item['name']} ---")

            # Combine context
            context = f"Repository: {owner}/{repo}\n"
            context += f"Branch: {branch}\n\n"
            context += "=== FILE STRUCTURE ===\n"
            context += "\n".join(files_list)
            context += "\n\n=== README ===\n"
            context += readme_content
            
            return context

        except Exception as e:
            logger.error(f"Error fetching GitHub content: {str(e)}")
            raise e
