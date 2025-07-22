def construct_multimodal_prompt(images, user_prompt, style, tone, length):
    """
    Constructs a prompt for multimodal blog generation for OpenAI GPT-4o Vision.
    Images: list of PIL.Image
    user_prompt: topic or focus text
    style: blog style
    tone: blog tone
    length: desired length
    """
    prompt = "You are a blog writing assistant. Analyze the uploaded images and generate a blog post."
    prompt += f"\n\nBlog Style: {style}\nTone: {tone}\nLength: {length}\n"
    if user_prompt:
        prompt += f"Focus/Topic: {user_prompt}\n"
    prompt += "\nInstructions:\n"
    prompt += "- Integrate visual elements and context from images.\n"
    prompt += "- Write a catchy title (use #)."
    prompt += "\n- Add relevant tags at the end (format: Tags: tag1, tag2)."
    prompt += "\n- Generate readable, engaging blog body suitable for publishing."
    prompt += "\n- Output in Markdown format."
    return prompt
