from PIL import Image
import io

class ImageProcessor:
    def validate(self, image: Image.Image):
        if image.format not in ["JPEG", "JPG", "PNG"]:
            return False, "Unsupported file format."
        if image.size[0] < 100 or image.size[1] < 100:
            return False, "Image dimensions too small."
        return True, "OK"

    def preprocess(self, image: Image.Image):
        max_dim = 1024
        if max(image.size) > max_dim:
            ratio = max_dim / float(max(image.size))
            new_size = tuple([int(x * ratio) for x in image.size])
        
            resample_filter = getattr(Image, 'Resampling', Image).LANCZOS
            image = image.resize(new_size, resample_filter)

        if image.mode != "RGB":
            image = image.convert("RGB")
        return image


class BlogFormatter:
    def format(self, ai_output, images):
        title = self.extract_title(ai_output)
        tags = self.extract_tags(ai_output)
        body = self.extract_body(ai_output)
        return {
            "title": title,
            "body": body,
            "images": images,
            "tags": tags
        }

    def extract_title(self, ai_output):
        lines = ai_output.splitlines()
        for line in lines:
            if line.strip().startswith("# "):
                return line.strip()[2:]
        return lines[0] if lines else "AI Blog Post"

    def extract_tags(self, ai_output):
        if "Tags:" in ai_output:
            tagline = ai_output.split("Tags:")[-1]
            tags = [t.strip() for t in tagline.split(",")]
            return tags
        return []

    def extract_body(self, ai_output):
        lines = ai_output.splitlines()
        body_lines = []
        for line in lines:
            if line.strip().startswith("# ") or line.strip().startswith("Tags:"):
                continue
            body_lines.append(line)
        return "\n".join(body_lines)

    def to_markdown(self, blog_post):
        md = f"# {blog_post['title']}\n\n"
        for i, img in enumerate(blog_post.get("images", [])):
            md += f"![Image{i+1}](image_placeholder_{i})\n"
        md += blog_post["body"] + "\n\n"
        if blog_post.get("tags"):
            md += "Tags: " + ", ".join(blog_post["tags"])
        return md

    def to_html(self, blog_post):
        html = f"<h1>{blog_post['title']}</h1>\n"
        for i, img in enumerate(blog_post.get("images", [])):
            html += f"<img src='image_placeholder_{i}' alt='Blog Image {i+1}'/><br>"
        html += f"<div>{blog_post['body']}</div>"
        if blog_post.get("tags"):
            html += "<p><b>Tags:</b> " + ", ".join(blog_post["tags"]) + "</p>"
        return html
