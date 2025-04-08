import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
import re
from nltk.corpus import stopwords

import nltk

nltk.download("stopwords", quiet=True)
STOPWORDS = set(stopwords.words("english"))


def slugify_title(title, max_words=4):
    words = re.sub(r"[^\w\s]", "", title).lower().split()
    filtered = [word for word in words if word not in STOPWORDS]
    return "".join(filtered[:max_words])


def fetch_arxiv_metadata(arxiv_url):
    """Fetch metadata from arXiv and generate a BibTeX entry using official-style keys."""

    paper_id = urlparse(arxiv_url).path.split("/")[-1]
    api_url = f"http://export.arxiv.org/api/query?id_list={paper_id}"

    response = requests.get(api_url)
    if response.status_code != 200:
        raise RuntimeError(
            f"Failed to fetch arXiv metadata (status code {response.status_code})"
        )

    root = ET.fromstring(response.content)
    entry = root.find("{http://www.w3.org/2005/Atom}entry")
    if entry is None:
        raise ValueError("No entry found for the given arXiv ID")

    title = (
        entry.find("{http://www.w3.org/2005/Atom}title").text.strip().replace("\n", " ")
    )
    summary = entry.find("{http://www.w3.org/2005/Atom}summary").text.strip()
    authors_list = [
        author.find("{http://www.w3.org/2005/Atom}name").text
        for author in entry.findall("{http://www.w3.org/2005/Atom}author")
    ]
    published = entry.find("{http://www.w3.org/2005/Atom}published").text

    first_author_lastname = authors_list[0].split()[-1].lower()
    year = published[:4]
    title_slug = slugify_title(title)

    bib_key = f"{first_author_lastname}{year}{title_slug}"

    bibtex = f"""@misc{{{bib_key},
        title={{ {title} }},
        author={{ {' and '.join(authors_list)} }},
        year={{ {year} }},
        eprint={{ {paper_id} }},
        archivePrefix={{arXiv}},
        primaryClass={{cs.CV}},
        url={{ {arxiv_url} }}
    }}"""

    metadata = {
        "title": title,
        "abstract": summary,
        "authors": [{"name": name} for name in authors_list],
        "arxiv_url": arxiv_url,
        "pdf_url": f"https://arxiv.org/pdf/{paper_id}.pdf",
        "bibtex": bibtex,
    }

    return metadata
