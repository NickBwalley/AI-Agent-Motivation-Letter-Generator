def validate(api_key, title, description, url, cv_file):
    if not api_key:
        return False, "API Key is required.", None
    if not description.strip():
        return False, "Job Description or key points are required.", None

    user_data = {
        "api_key": api_key,
        "title": "",  # Title is not used in the current version
        "description": description.strip(),
        "url": url.strip() if url else "",
        "cv_file": cv_file
    }
    return True, None, user_data
