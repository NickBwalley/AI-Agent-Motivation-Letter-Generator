def synthesize(user_data, web_data, cv_text):
    parts = [
        f"# Title\n{user_data['title']}",
        f"# User Description\n{user_data['description']}",
        f"# Web Content\n{web_data}" if web_data else "",
        f"# CV Content\n{cv_text}" if cv_text else ""
    ]
    return "\n\n".join(p for p in parts if p)
