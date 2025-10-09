import requests

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    ),
    "Accept": "application/vnd.github.v3+json",
}


def _fetch_readme_via_api(username, repository):
    url = f"https://api.github.com/repos/{username}/{repository}/readme"
    response = requests.get(url, headers=_HEADERS)
    if response.status_code == 404:
        return None, None
    if response.status_code != 200:
        print(
            "Failed to retrieve README via API "
            f"(status code: {response.status_code})."
        )
        return None, None
    data = response.json()
    download_url = data.get("download_url")
    html_url = data.get("html_url")
    if not download_url:
        print("README response missing download URL; unable to fetch content.")
        return None, None
    download_response = requests.get(
        download_url,
        headers={"User-Agent": _HEADERS["User-Agent"]},
    )
    if download_response.status_code != 200:
        print(
            "Failed to download README content "
            f"(status code: {download_response.status_code})."
        )
        return None, None
    branch = None
    if html_url and "/blob/" in html_url:
        try:
            branch = html_url.split("/blob/")[1].split("/", 1)[0]
        except (IndexError, ValueError):
            branch = None
    return branch, download_response.text


def _fetch_readme_from_branch(username, repository, branch):
    candidate_filenames = [
        "README.md",
        "README.MD",
        "README",
        "README.txt",
        "README.rst",
    ]
    for filename in candidate_filenames:
        url = (
            f"https://raw.githubusercontent.com/{username}/{repository}/"
            f"{branch}/{filename}"
        )
        response = requests.get(
            url,
            headers={"User-Agent": _HEADERS["User-Agent"]},
        )
        if response.status_code == 200:
            return response.text
        if response.status_code not in (403, 404):
            print(
                f"Attempt to fetch {filename} from branch '{branch}' "
                f"failed (status code: {response.status_code})."
            )
            break
    return None


def scrape_readme(username, repository):
    branch, readme_content = _fetch_readme_via_api(username, repository)
    if readme_content:
        return branch or "default", readme_content
    for fallback_branch in ["main", "master"]:
        print(f"Trying branch: {fallback_branch}")
        content = _fetch_readme_from_branch(username, repository, fallback_branch)
        if content:
            return fallback_branch, content
    print("No README could be fetched via API or fallback branches.")
    return None, None


