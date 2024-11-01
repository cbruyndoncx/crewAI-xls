from langchain.tools import tool
import os, requests, re, mdpdf, subprocess
from openai import OpenAI

class BookPublishingTools():

    @tool('generate an illustration for a childrens book')
    def generateimage(chapter_content_and_character_details: str) -> str:
        """
        Generates an image for a given chapter number, chapter content, detailed location details and character details.
        Using the OpenAI image generation API,
        saves it in the current folder, and returns the image path.
        """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.images.generate(
            model="dall-e-3",
            prompt=f"Image is about: {chapter_content_and_character_details}. Style: Illustration. Create an illustration incorporating a vivid palette with an emphasis on shades of azure and emerald, augmented by splashes of gold for contrast and visual interest. The style should evoke the intricate detail and whimsy of early 20th-century storybook illustrations, blending realism with fantastical elements to create a sense of wonder and enchantment. The composition should be rich in texture, with a soft, luminous lighting that enhances the magical atmosphere. Attention to the interplay of light and shadow will add depth and dimensionality, inviting the viewer to delve into the scene. DON'T include ANY text in this image. DON'T include colour palettes in this image.",
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        words = chapter_content_and_character_details.split()[:5] 
        safe_words = [re.sub(r'[^a-zA-Z0-9_]', '', word) for word in words]  
        filename = "_".join(safe_words).lower() + ".png"
        filepath = os.path.join(os.getcwd(), filename)

        # Download the image from the URL
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            with open(filepath, 'wb') as file:
                file.write(image_response.content)
        else:
            print("Failed to download the image.")
            return ""

        return filepath

    @tool
    def convermarkdowntopdf(markdownfile_name: str) -> str:
        """
        Converts a Markdown file to a PDF document using the mdpdf command line application.

        Args:
            markdownfile_name (str): Path to the input Markdown file.

        Returns:
            str: Path to the generated PDF file.
        """
        output_file = os.path.splitext(markdownfile_name)[0] + '.pdf'
        
        # Command to convert markdown to PDF using mdpdf
        cmd = ['mdpdf', '--output', output_file, markdownfile_name]
        
        # Execute the command
        subprocess.run(cmd, check=True)
        
        return output_file