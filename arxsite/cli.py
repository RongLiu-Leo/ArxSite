# arxsite/cli.py

import sys
import re
import os
from arxsite.arxiv_parser import fetch_arxiv_metadata
from arxsite.jekyll_generator import generate_site


def is_valid_arxiv_url(url):
    return re.match(r"https?://arxiv\.org/abs/\d{4}\.\d{5}$", url)


def list_available_styles():
    templates_dir = os.path.join(os.path.dirname(__file__), "templates")
    return [
        name
        for name in os.listdir(templates_dir)
        if os.path.isdir(os.path.join(templates_dir, name))
    ]


def print_help():
    print(
        """📚 Usage: arxsite <arxiv_url> [--style <style_name>]

        Options:
        --style, -s        Choose a website style (default: default)
        --help, -h         Show this help message and exit

        Examples:
        arxsite https://arxiv.org/abs/2501.18630
        arxsite https://arxiv.org/abs/2501.18630 --style default

        Available styles:
        """
        + ", ".join(list_available_styles())
    )


def main():
    if any(arg in ("--help", "-h") for arg in sys.argv):
        print_help()
        sys.exit(0)

    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("❌ Invalid arguments.")
        print("Use --help for usage instructions.")
        sys.exit(1)

    arxiv_url = sys.argv[1]

    style = "default"  # Default style
    if len(sys.argv) == 4:
        if sys.argv[2] not in ["--style", "-s"]:
            print("❌ Unknown option. Use --help for usage instructions.")
            sys.exit(1)
        style = sys.argv[3]

    if not is_valid_arxiv_url(arxiv_url):
        print("❌ Invalid arXiv URL. Example: https://arxiv.org/abs/2501.18630")
        sys.exit(1)

    available_styles = list_available_styles()
    if style not in available_styles:
        print(
            f"❌ Style '{style}' not found. Available styles: {', '.join(available_styles)}"
        )
        sys.exit(1)

    print("🔍 Fetching metadata from:", arxiv_url)
    metadata = fetch_arxiv_metadata(arxiv_url)
    print("title:", metadata["title"])
    print("authors:", ", ".join(author["name"] for author in metadata["authors"]))

    print(f"🛠️ Generating Jekyll site with style '{style}'...")
    generate_site(metadata, style=style)

    print("✅ Website generated successfully!")


if __name__ == "__main__":
    main()
