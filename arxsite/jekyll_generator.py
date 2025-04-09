import os
import shutil
import importlib.resources
from jinja2 import Environment, FileSystemLoader


def generate_site(metadata, style):
    """Generate a Jekyll-compatible site using arXiv metadata."""

    output_dir = os.getcwd()

    root = importlib.resources.files("arxsite")

    env = Environment(loader=FileSystemLoader(root))

    # Make site folders
    os.makedirs(os.path.join(output_dir, "_layouts"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "assets/scripts"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "assets/images"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "assets/videos"), exist_ok=True)

    # Render templates
    _render_to_file(
        env, "_config.yml.j2", metadata, os.path.join(output_dir, "_config.yml")
    )

    # Copy
    shutil.copy(
        root / "icon.png",
        os.path.join(output_dir, "icon.png"),
    )
    shutil.copy(
        root / "teaser.png",
        os.path.join(output_dir, "teaser.png"),
    )
    shutil.copy(root / "index.md", os.path.join(output_dir, "index.md"))

    shutil.copy(
        root / "templates" / style / "default.html",
        os.path.join(output_dir, "_layouts/default.html"),
    )

    # Copy all other files from the templates/style directory to assets/scripts
    style_dir = root / "templates" / style
    for file in style_dir.iterdir():
        if file.name != "default.html" and file.is_file():
            shutil.copy(
                file,
                os.path.join(output_dir, "assets/scripts", file.name),
            )

    print(f"🌐 Jekyll site generated at: ./{output_dir}")


def _render_to_file(env, template_name, metadata, out_path):
    template = env.get_template(template_name)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(template.render(**metadata))
