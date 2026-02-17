#!/usr/bin/env python3
"""
HTML to Image Converter using Playwright
Converts rendered Jinja2 HTML templates to PNG images
"""

import os
import asyncio
from playwright.async_api import async_playwright
import time

class HTMLToImageConverter:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        
    async def initialize(self):
        """Initialize Playwright browser"""
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=True,  # Run in headless mode
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--disable-gpu'
                ]
            )
            self.context = await self.browser.new_context(
                viewport={'width': 1200, 'height': 1400},  # Match your HTML template dimensions
                device_scale_factor=2  # Higher resolution
            )
            self.page = await self.context.new_page()
            return True
        except Exception as e:
            print(f"Error initializing Playwright: {e}")
            return False
    
    async def convert_html_to_image(self, html_file_path, output_image_path, wait_time=2):
        """Convert HTML file to PNG image"""
        try:
            if not os.path.exists(html_file_path):
                print(f"HTML file not found: {html_file_path}")
                return False
            
            # Convert file path to file URL
            file_url = f"file:///{html_file_path.replace(os.sep, '/')}"
            
            # Navigate to the HTML file
            await self.page.goto(file_url, wait_until='networkidle')
            
            # Wait for content to load and render
            await asyncio.sleep(wait_time)
            
            # Take screenshot
            await self.page.screenshot(
                path=output_image_path,
                full_page=True,
                type='png'
            )
            
            print(f"✅ Image saved to: {output_image_path}")
            return True
            
        except Exception as e:
            print(f"Error converting HTML to image: {e}")
            return False
    
    async def convert_html_string_to_image(self, html_content, output_image_path, wait_time=2):
        """Convert HTML string content to PNG image"""
        try:
            # Set HTML content directly
            await self.page.set_content(html_content, wait_until='networkidle')
            
            # Wait for content to load and render
            await asyncio.sleep(wait_time)
            
            # Take screenshot
            await self.page.screenshot(
                path=output_image_path,
                full_page=True,
                type='png'
            )
            
            print(f"✅ Image saved to: {output_image_path}")
            return True
            
        except Exception as e:
            print(f"Error converting HTML string to image: {e}")
            return False
    
    async def close(self):
        """Close browser and cleanup"""
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if hasattr(self, 'playwright'):
                await self.playwright.stop()
        except Exception as e:
            print(f"Error closing browser: {e}")


async def convert_html_file_to_image(html_file_path, output_image_path):
    """Convert a single HTML file to image"""
    converter = HTMLToImageConverter()
    
    try:
        # Initialize
        if not await converter.initialize():
            return False
        
        # Convert
        success = await converter.convert_html_to_image(html_file_path, output_image_path)
        
        return success
        
    finally:
        await converter.close()


async def convert_html_string_to_image(html_content, output_image_path):
    """Convert HTML string content to image"""
    converter = HTMLToImageConverter()
    
    try:
        # Initialize
        if not await converter.initialize():
            return False
        
        # Convert
        success = await converter.convert_html_string_to_image(html_content, output_image_path)
        
        return success
        
    finally:
        await converter.close()


def convert_html_file_to_image_sync(html_file_path, output_image_path):
    """Synchronous wrapper for HTML file conversion"""
    return asyncio.run(convert_html_file_to_image(html_file_path, output_image_path))


def convert_html_string_to_image_sync(html_content, output_image_path):
    """Synchronous wrapper for HTML string conversion"""
    return asyncio.run(convert_html_string_to_image(html_content, output_image_path))


# Example usage
async def main():
    """Example of how to use the HTML to Image converter"""
    
    # Example 1: Convert HTML file to image
    html_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'images', 'test_jinja2_output.html')
    output_image = html_file.replace('.html', '.png')
    
    if os.path.exists(html_file):
        print(f"Converting HTML file: {html_file}")
        success = await convert_html_file_to_image(html_file, output_image)
        
        if success:
            print(f"✅ Successfully converted to: {output_image}")
        else:
            print("❌ Conversion failed")
    else:
        print(f"HTML file not found: {html_file}")
    
    # Example 2: Convert HTML string to image
    sample_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
            }
            .container { 
                padding: 40px; 
                background: rgba(255,255,255,0.1); 
                border-radius: 20px;
                backdrop-filter: blur(10px);
            }
            h1 { font-size: 48px; margin-bottom: 20px; }
            p { font-size: 24px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎉 Jinja2 Template Success!</h1>
            <p>Your HTML template is working perfectly!</p>
            <p>Next: Convert to image and integrate with your MLB bot</p>
        </div>
    </body>
    </html>
    """
    
    string_output_image = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'images', 'sample_html_string.png')
    
    print(f"\nConverting HTML string to image...")
    success = await convert_html_string_to_image(sample_html, string_output_image)
    
    if success:
        print(f"✅ Successfully converted string to: {string_output_image}")
    else:
        print("❌ String conversion failed")


if __name__ == "__main__":
    print("🖼️  HTML to Image Converter")
    print("=" * 40)
    
    # Check if Playwright is installed
    try:
        import playwright
        print("✅ Playwright is installed")
    except ImportError:
        print("❌ Playwright is not installed")
        print("Install it with: pip install playwright")
        print("Then run: playwright install chromium")
        exit(1)
    
    # Run the example
    asyncio.run(main())
