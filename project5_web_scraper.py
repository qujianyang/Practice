"""
Final Project 5: Web Scraper
A comprehensive web scraper with regex parsing, exception handling for network errors,
generators for efficient processing, and file I/O for storing results.

Note: This is a demonstration scraper that simulates web scraping without making actual
network requests to avoid dependencies and potential issues.
"""

import re
import json
import csv
import os
import time
import random
from datetime import datetime, timedelta
from typing import Generator, Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from functools import wraps
import hashlib
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('web_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ScraperError(Exception):
    """Base exception for scraper errors"""
    pass

class NetworkError(ScraperError):
    """Network-related errors"""
    pass

class ParsingError(ScraperError):
    """HTML/Data parsing errors"""
    pass

class RateLimitError(ScraperError):
    """Rate limiting errors"""
    pass

def retry_on_failure(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """Decorator to retry failed operations with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            current_delay = delay

            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except (NetworkError, RateLimitError) as e:
                    retries += 1
                    if retries >= max_retries:
                        logger.error(f"Max retries ({max_retries}) reached for {func.__name__}")
                        raise

                    logger.warning(f"Retry {retries}/{max_retries} for {func.__name__} after {current_delay}s")
                    time.sleep(current_delay)
                    current_delay *= backoff

            return None
        return wrapper
    return decorator

def rate_limit(requests_per_second: float = 1.0):
    """Decorator to rate limit function calls"""
    min_interval = 1.0 / requests_per_second
    last_called = {}

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = func.__name__
            current_time = time.time()

            if key in last_called:
                elapsed = current_time - last_called[key]
                if elapsed < min_interval:
                    sleep_time = min_interval - elapsed
                    logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f}s")
                    time.sleep(sleep_time)

            result = func(*args, **kwargs)
            last_called[key] = time.time()
            return result
        return wrapper
    return decorator

@dataclass
class ScrapedItem:
    """Represents a scraped item"""
    url: str
    title: str
    content: str
    metadata: Dict[str, Any]
    scraped_at: datetime
    hash_id: str = ""

    def __post_init__(self):
        if not self.hash_id:
            self.hash_id = self.generate_hash()

    def generate_hash(self) -> str:
        """Generate unique hash for the item"""
        content = f"{self.url}{self.title}{self.content}"
        return hashlib.md5(content.encode()).hexdigest()

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        data = asdict(self)
        data['scraped_at'] = self.scraped_at.isoformat()
        return data

class HTMLParser:
    """Parse HTML content using regex patterns"""

    PATTERNS = {
        'title': re.compile(r'<title[^>]*>(.*?)</title>', re.IGNORECASE | re.DOTALL),
        'meta_description': re.compile(r'<meta[^>]*name=["\'](description|Description)["\'][^>]*content=["\']([^"\']*)["\']', re.IGNORECASE),
        'links': re.compile(r'<a[^>]*href=["\']([^"\']*)["\']', re.IGNORECASE),
        'images': re.compile(r'<img[^>]*src=["\']([^"\']*)["\']', re.IGNORECASE),
        'headings': re.compile(r'<h([1-6])[^>]*>(.*?)</h\1>', re.IGNORECASE | re.DOTALL),
        'paragraphs': re.compile(r'<p[^>]*>(.*?)</p>', re.IGNORECASE | re.DOTALL),
        'emails': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
        'phones': re.compile(r'(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'),
        'prices': re.compile(r'\$\s*(\d+(?:,\d{3})*(?:\.\d{2})?)', re.IGNORECASE),
        'dates': re.compile(r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{2,4}\b', re.IGNORECASE),
        'script_tags': re.compile(r'<script[^>]*>.*?</script>', re.IGNORECASE | re.DOTALL),
        'style_tags': re.compile(r'<style[^>]*>.*?</style>', re.IGNORECASE | re.DOTALL),
        'html_tags': re.compile(r'<[^>]+>'),
        'whitespace': re.compile(r'\s+')
    }

    @classmethod
    def extract_title(cls, html: str) -> str:
        """Extract page title"""
        match = cls.PATTERNS['title'].search(html)
        if match:
            return cls.clean_text(match.group(1))
        return ""

    @classmethod
    def extract_meta_description(cls, html: str) -> str:
        """Extract meta description"""
        match = cls.PATTERNS['meta_description'].search(html)
        if match:
            return match.group(2)
        return ""

    @classmethod
    def extract_links(cls, html: str, base_url: str = "") -> List[str]:
        """Extract all links from HTML"""
        links = cls.PATTERNS['links'].findall(html)

        # Normalize links
        normalized = []
        for link in links:
            if link.startswith('http'):
                normalized.append(link)
            elif link.startswith('//'):
                normalized.append('https:' + link)
            elif link.startswith('/') and base_url:
                normalized.append(base_url.rstrip('/') + link)
            elif base_url:
                normalized.append(base_url.rstrip('/') + '/' + link)

        return list(set(normalized))  # Remove duplicates

    @classmethod
    def extract_images(cls, html: str) -> List[str]:
        """Extract image URLs"""
        return cls.PATTERNS['images'].findall(html)

    @classmethod
    def extract_text_content(cls, html: str) -> str:
        """Extract clean text content from HTML"""
        # Remove script and style tags
        html = cls.PATTERNS['script_tags'].sub('', html)
        html = cls.PATTERNS['style_tags'].sub('', html)

        # Remove HTML tags
        text = cls.PATTERNS['html_tags'].sub(' ', html)

        # Clean whitespace
        text = cls.PATTERNS['whitespace'].sub(' ', text)

        return text.strip()

    @classmethod
    def extract_structured_data(cls, html: str) -> Dict:
        """Extract structured data from HTML"""
        return {
            'title': cls.extract_title(html),
            'meta_description': cls.extract_meta_description(html),
            'headings': cls.extract_headings(html),
            'paragraphs': cls.extract_paragraphs(html),
            'emails': cls.PATTERNS['emails'].findall(html),
            'phones': cls.PATTERNS['phones'].findall(html),
            'prices': cls.PATTERNS['prices'].findall(html),
            'dates': cls.PATTERNS['dates'].findall(html)
        }

    @classmethod
    def extract_headings(cls, html: str) -> List[Tuple[int, str]]:
        """Extract headings with their levels"""
        headings = []
        for match in cls.PATTERNS['headings'].finditer(html):
            level = int(match.group(1))
            text = cls.clean_text(match.group(2))
            if text:
                headings.append((level, text))
        return headings

    @classmethod
    def extract_paragraphs(cls, html: str) -> List[str]:
        """Extract paragraph text"""
        paragraphs = []
        for match in cls.PATTERNS['paragraphs'].finditer(html):
            text = cls.clean_text(match.group(1))
            if text and len(text) > 20:  # Filter out very short paragraphs
                paragraphs.append(text)
        return paragraphs

    @classmethod
    def clean_text(cls, text: str) -> str:
        """Clean extracted text"""
        # Remove HTML entities
        text = re.sub(r'&[a-zA-Z]+;', ' ', text)
        text = re.sub(r'&#\d+;', ' ', text)

        # Remove extra whitespace
        text = cls.PATTERNS['whitespace'].sub(' ', text)

        return text.strip()

class URLValidator:
    """Validate and filter URLs"""

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if URL is valid"""
        url_pattern = re.compile(
            r'^https?://'  # Protocol
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # Domain
            r'localhost|'  # Localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
            r'(?::\d+)?'  # Optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE
        )
        return bool(url_pattern.match(url))

    @staticmethod
    def should_scrape(url: str, allowed_domains: List[str] = None,
                      blocked_patterns: List[str] = None) -> bool:
        """Check if URL should be scraped"""
        if not URLValidator.is_valid_url(url):
            return False

        # Check allowed domains
        if allowed_domains:
            domain_match = any(domain in url for domain in allowed_domains)
            if not domain_match:
                return False

        # Check blocked patterns
        if blocked_patterns:
            for pattern in blocked_patterns:
                if re.search(pattern, url):
                    return False

        # Skip common non-content URLs
        skip_extensions = ['.pdf', '.jpg', '.png', '.gif', '.zip', '.exe', '.mp4', '.mp3']
        for ext in skip_extensions:
            if url.lower().endswith(ext):
                return False

        return True

class WebScraper:
    """Main web scraper engine"""

    def __init__(self, base_url: str = "", max_depth: int = 2,
                 max_pages: int = 100, delay: float = 1.0):
        self.base_url = base_url
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.delay = delay
        self.visited_urls = set()
        self.scraped_items: List[ScrapedItem] = []
        self.errors: List[Dict] = []
        self.session_stats = {
            'pages_scraped': 0,
            'errors': 0,
            'start_time': None,
            'end_time': None
        }

    def simulate_html_content(self, url: str) -> str:
        """Simulate HTML content for demonstration"""
        # Generate realistic HTML content
        templates = [
            """
            <html>
            <head>
                <title>Sample Product Page - Electronics Store</title>
                <meta name="description" content="High-quality electronics at great prices">
            </head>
            <body>
                <h1>Premium Wireless Headphones</h1>
                <p>Experience crystal-clear audio with our premium wireless headphones.
                   Features include noise cancellation, 30-hour battery life, and premium comfort.</p>
                <p>Price: $299.99</p>
                <p>Contact: sales@electronics-store.com</p>
                <p>Phone: (555) 123-4567</p>
                <h2>Product Features</h2>
                <p>Advanced noise cancellation technology eliminates background noise for immersive listening.</p>
                <a href="/products/speakers">View Speakers</a>
                <a href="/products/earbuds">View Earbuds</a>
                <img src="/images/headphones.jpg" alt="Headphones">
            </body>
            </html>
            """,
            """
            <html>
            <head>
                <title>Tech News - Latest Updates</title>
                <meta name="description" content="Stay updated with the latest technology news">
            </head>
            <body>
                <h1>Breaking: New AI Breakthrough Announced</h1>
                <p>Published on Jan 15, 2024</p>
                <p>Researchers have announced a major breakthrough in artificial intelligence
                   that could revolutionize how we interact with technology.</p>
                <h2>Key Highlights</h2>
                <p>The new system demonstrates unprecedented capabilities in natural language understanding.</p>
                <p>For inquiries: press@technews.com</p>
                <a href="/news/archive">News Archive</a>
                <a href="/news/subscribe">Subscribe</a>
            </body>
            </html>
            """,
            """
            <html>
            <head>
                <title>Online Course Platform</title>
                <meta name="description" content="Learn new skills with expert instructors">
            </head>
            <body>
                <h1>Python Programming Masterclass</h1>
                <p>Complete Python course from beginner to advanced. Learn at your own pace with
                   hands-on projects and real-world applications.</p>
                <p>Course Price: $89.99</p>
                <p>Duration: 40 hours</p>
                <p>Start Date: Feb 1, 2024</p>
                <h2>Course Content</h2>
                <p>Module 1: Python Basics</p>
                <p>Module 2: Object-Oriented Programming</p>
                <p>Module 3: Web Development with Python</p>
                <p>Instructor email: instructor@courses.com</p>
                <a href="/courses/java">Java Programming</a>
                <a href="/courses/javascript">JavaScript Essentials</a>
            </body>
            </html>
            """
        ]

        # Return a random template with some variation
        html = random.choice(templates)

        # Add some random elements for variety
        if random.random() > 0.5:
            html = html.replace("</body>",
                f"<p>Special offer expires: {datetime.now() + timedelta(days=7)}</p></body>")

        return html

    @retry_on_failure(max_retries=3)
    @rate_limit(requests_per_second=1)
    def fetch_page(self, url: str) -> str:
        """Fetch page content (simulated)"""
        logger.info(f"Fetching: {url}")

        # Simulate network delays and errors
        if random.random() < 0.1:  # 10% chance of network error
            raise NetworkError(f"Connection timeout for {url}")

        if random.random() < 0.05:  # 5% chance of rate limit
            raise RateLimitError("Rate limit exceeded")

        # Simulate fetching delay
        time.sleep(self.delay * random.uniform(0.5, 1.5))

        # Return simulated content
        return self.simulate_html_content(url)

    def scrape_page(self, url: str) -> Optional[ScrapedItem]:
        """Scrape a single page"""
        try:
            # Check if already visited
            if url in self.visited_urls:
                logger.debug(f"Skipping already visited URL: {url}")
                return None

            # Validate URL
            if not URLValidator.should_scrape(url):
                logger.debug(f"Skipping invalid/blocked URL: {url}")
                return None

            # Fetch page content
            html = self.fetch_page(url)

            # Parse content
            structured_data = HTMLParser.extract_structured_data(html)
            text_content = HTMLParser.extract_text_content(html)

            # Create scraped item
            item = ScrapedItem(
                url=url,
                title=structured_data['title'],
                content=text_content,
                metadata=structured_data,
                scraped_at=datetime.now()
            )

            # Mark as visited
            self.visited_urls.add(url)
            self.scraped_items.append(item)
            self.session_stats['pages_scraped'] += 1

            logger.info(f"Successfully scraped: {url}")
            return item

        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            self.errors.append({
                'url': url,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            self.session_stats['errors'] += 1
            return None

    def crawl(self, start_urls: List[str]) -> Generator[ScrapedItem, None, None]:
        """Crawl websites starting from given URLs"""
        self.session_stats['start_time'] = datetime.now()
        logger.info(f"Starting crawl with {len(start_urls)} seed URLs")

        url_queue = [(url, 0) for url in start_urls]  # (url, depth)
        processed = 0

        while url_queue and processed < self.max_pages:
            url, depth = url_queue.pop(0)

            # Skip if max depth reached
            if depth > self.max_depth:
                continue

            # Scrape page
            item = self.scrape_page(url)
            if item:
                processed += 1
                yield item

                # Extract and queue new links if not at max depth
                if depth < self.max_depth:
                    html = self.fetch_page(url)
                    links = HTMLParser.extract_links(html, self.base_url)

                    for link in links[:10]:  # Limit links per page
                        if link not in self.visited_urls:
                            url_queue.append((link, depth + 1))

        self.session_stats['end_time'] = datetime.now()
        logger.info(f"Crawl completed. Scraped {processed} pages")

    def save_results(self, output_dir: str = "scraper_output"):
        """Save scraped data to files"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save as JSON
        json_file = os.path.join(output_dir, f"scraped_data_{timestamp}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            data = {
                'session_stats': self.session_stats,
                'items': [item.to_dict() for item in self.scraped_items],
                'errors': self.errors
            }
            json.dump(data, f, indent=2, default=str)
        logger.info(f"Saved JSON data to {json_file}")

        # Save as CSV
        if self.scraped_items:
            csv_file = os.path.join(output_dir, f"scraped_data_{timestamp}.csv")
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['url', 'title', 'content', 'scraped_at', 'hash_id']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

                for item in self.scraped_items:
                    writer.writerow({
                        'url': item.url,
                        'title': item.title,
                        'content': item.content[:500],  # Truncate content
                        'scraped_at': item.scraped_at.isoformat(),
                        'hash_id': item.hash_id
                    })
            logger.info(f"Saved CSV data to {csv_file}")

        # Save errors log
        if self.errors:
            error_file = os.path.join(output_dir, f"errors_{timestamp}.json")
            with open(error_file, 'w', encoding='utf-8') as f:
                json.dump(self.errors, f, indent=2)
            logger.info(f"Saved error log to {error_file}")

    def generate_report(self) -> str:
        """Generate scraping report"""
        duration = 0
        if self.session_stats['start_time'] and self.session_stats['end_time']:
            duration = (self.session_stats['end_time'] - self.session_stats['start_time']).total_seconds()

        report = [
            "="*60,
            "WEB SCRAPING REPORT",
            "="*60,
            f"Start Time: {self.session_stats['start_time']}",
            f"End Time: {self.session_stats['end_time']}",
            f"Duration: {duration:.2f} seconds",
            f"",
            f"Pages Scraped: {self.session_stats['pages_scraped']}",
            f"Errors: {self.session_stats['errors']}",
            f"Success Rate: {(1 - self.session_stats['errors'] / max(1, self.session_stats['pages_scraped'] + self.session_stats['errors'])) * 100:.1f}%",
            f"",
            "Top Extracted Data:",
        ]

        # Analyze extracted data
        if self.scraped_items:
            total_emails = sum(len(item.metadata.get('emails', [])) for item in self.scraped_items)
            total_phones = sum(len(item.metadata.get('phones', [])) for item in self.scraped_items)
            total_prices = sum(len(item.metadata.get('prices', [])) for item in self.scraped_items)

            report.extend([
                f"  Total Emails Found: {total_emails}",
                f"  Total Phone Numbers: {total_phones}",
                f"  Total Prices: {total_prices}",
                f"",
                "Sample Scraped Pages:"
            ])

            for item in self.scraped_items[:5]:  # Show first 5
                report.append(f"  - {item.title or 'Untitled'} ({item.url})")

        return "\n".join(report)

class DataExtractor:
    """Extract specific data patterns from scraped content"""

    @staticmethod
    def extract_products(items: List[ScrapedItem]) -> List[Dict]:
        """Extract product information"""
        products = []

        for item in items:
            # Look for product patterns
            prices = item.metadata.get('prices', [])
            if prices:
                product = {
                    'url': item.url,
                    'title': item.title,
                    'price': prices[0] if prices else None,
                    'description': item.content[:200]
                }
                products.append(product)

        return products

    @staticmethod
    def extract_contacts(items: List[ScrapedItem]) -> Dict[str, List]:
        """Extract contact information"""
        contacts = {
            'emails': set(),
            'phones': set()
        }

        for item in items:
            emails = item.metadata.get('emails', [])
            phones = item.metadata.get('phones', [])

            contacts['emails'].update(emails)
            contacts['phones'].update(phones)

        return {
            'emails': list(contacts['emails']),
            'phones': list(contacts['phones'])
        }

    @staticmethod
    def extract_articles(items: List[ScrapedItem]) -> List[Dict]:
        """Extract article/blog post information"""
        articles = []

        for item in items:
            # Check if likely an article (has date and substantial content)
            dates = item.metadata.get('dates', [])
            paragraphs = item.metadata.get('paragraphs', [])

            if dates and paragraphs and len(item.content) > 500:
                article = {
                    'url': item.url,
                    'title': item.title,
                    'date': dates[0] if dates else None,
                    'content_preview': ' '.join(paragraphs[:2])[:300],
                    'word_count': len(item.content.split())
                }
                articles.append(article)

        return articles

class WebScraperCLI:
    """Command-line interface for web scraper"""

    def __init__(self):
        self.scraper = None
        self.running = True

    def run(self):
        """Run the CLI application"""
        print("\n" + "="*60)
        print("WEB SCRAPER")
        print("="*60)

        while self.running:
            self.show_menu()
            choice = input("\nEnter your choice: ").strip()
            self.handle_choice(choice)

    def show_menu(self):
        """Display main menu"""
        print("\n--- Main Menu ---")
        print("1. Configure Scraper")
        print("2. Start Scraping")
        print("3. View Results")
        print("4. Extract Data")
        print("5. Generate Report")
        print("6. Save Results")
        print("7. Exit")

    def handle_choice(self, choice):
        """Handle menu choice"""
        try:
            if choice == "1":
                self.configure_scraper()
            elif choice == "2":
                self.start_scraping()
            elif choice == "3":
                self.view_results()
            elif choice == "4":
                self.extract_data()
            elif choice == "5":
                self.generate_report()
            elif choice == "6":
                self.save_results()
            elif choice == "7":
                print("Goodbye!")
                self.running = False
            else:
                print("Invalid choice")

        except Exception as e:
            print(f"Error: {e}")
            logger.error(f"Error in menu: {e}")

    def configure_scraper(self):
        """Configure scraper settings"""
        print("\n--- Configure Scraper ---")

        base_url = input("Base URL (or empty): ").strip()
        max_depth = int(input("Max crawl depth (default 2): ") or "2")
        max_pages = int(input("Max pages to scrape (default 100): ") or "100")
        delay = float(input("Delay between requests in seconds (default 1): ") or "1")

        self.scraper = WebScraper(
            base_url=base_url,
            max_depth=max_depth,
            max_pages=max_pages,
            delay=delay
        )

        print(f"Scraper configured successfully")

    def start_scraping(self):
        """Start web scraping"""
        if not self.scraper:
            print("Please configure scraper first")
            return

        print("\n--- Start Scraping ---")
        print("Enter URLs to scrape (one per line, empty line to finish):")

        urls = []
        while True:
            url = input().strip()
            if not url:
                break
            urls.append(url)

        if not urls:
            # Use demo URLs for testing
            print("Using demo URLs for testing...")
            urls = [
                "https://example-store.com/products",
                "https://tech-news.com/latest",
                "https://learning-platform.com/courses"
            ]

        print(f"\nStarting scrape of {len(urls)} URLs...")

        # Scrape pages
        for item in self.scraper.crawl(urls):
            print(f"  Scraped: {item.title or 'Untitled'} - {item.url}")

        print(f"\nScraping completed!")
        print(f"Pages scraped: {self.scraper.session_stats['pages_scraped']}")
        print(f"Errors: {self.scraper.session_stats['errors']}")

    def view_results(self):
        """View scraped results"""
        if not self.scraper or not self.scraper.scraped_items:
            print("No scraped data available")
            return

        print(f"\n--- Scraped Results ({len(self.scraper.scraped_items)} items) ---")

        for i, item in enumerate(self.scraper.scraped_items[:10], 1):  # Show first 10
            print(f"\n{i}. {item.title or 'Untitled'}")
            print(f"   URL: {item.url}")
            print(f"   Content: {item.content[:200]}...")
            print(f"   Scraped: {item.scraped_at.strftime('%Y-%m-%d %H:%M:%S')}")

    def extract_data(self):
        """Extract specific data from scraped content"""
        if not self.scraper or not self.scraper.scraped_items:
            print("No scraped data available")
            return

        print("\n--- Extract Data ---")
        print("1. Extract Products")
        print("2. Extract Contacts")
        print("3. Extract Articles")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            products = DataExtractor.extract_products(self.scraper.scraped_items)
            print(f"\nFound {len(products)} products:")
            for product in products[:5]:  # Show first 5
                print(f"  - {product['title']}: ${product['price']}")

        elif choice == "2":
            contacts = DataExtractor.extract_contacts(self.scraper.scraped_items)
            print(f"\nExtracted Contacts:")
            print(f"  Emails: {len(contacts['emails'])}")
            for email in contacts['emails'][:5]:
                print(f"    - {email}")
            print(f"  Phones: {len(contacts['phones'])}")
            for phone in contacts['phones'][:5]:
                print(f"    - {phone}")

        elif choice == "3":
            articles = DataExtractor.extract_articles(self.scraper.scraped_items)
            print(f"\nFound {len(articles)} articles:")
            for article in articles[:5]:
                print(f"  - {article['title']}")
                print(f"    Date: {article['date']}")
                print(f"    Words: {article['word_count']}")

    def generate_report(self):
        """Generate and display report"""
        if not self.scraper:
            print("No scraper session available")
            return

        report = self.scraper.generate_report()
        print("\n" + report)

    def save_results(self):
        """Save scraping results"""
        if not self.scraper or not self.scraper.scraped_items:
            print("No data to save")
            return

        output_dir = input("Output directory (default: scraper_output): ").strip() or "scraper_output"
        self.scraper.save_results(output_dir)
        print(f"Results saved to {output_dir}")

def demo_mode():
    """Run demo scraping session"""
    print("\n" + "="*60)
    print("WEB SCRAPER - DEMO MODE")
    print("="*60)

    # Create scraper
    scraper = WebScraper(
        base_url="https://demo-site.com",
        max_depth=1,
        max_pages=10,
        delay=0.5
    )

    # Demo URLs
    demo_urls = [
        "https://demo-store.com/electronics",
        "https://demo-news.com/technology",
        "https://demo-blog.com/tutorials"
    ]

    print(f"\nStarting demo scrape of {len(demo_urls)} URLs...")

    # Perform scraping
    scraped_count = 0
    for item in scraper.crawl(demo_urls):
        scraped_count += 1
        print(f"  [{scraped_count}] Scraped: {item.title}")

        # Show extracted data
        if item.metadata.get('emails'):
            print(f"      Emails: {', '.join(item.metadata['emails'])}")
        if item.metadata.get('prices'):
            print(f"      Prices: {', '.join(item.metadata['prices'])}")

    # Generate and display report
    print("\n" + scraper.generate_report())

    # Extract specific data
    print("\n=== Extracted Data ===")

    products = DataExtractor.extract_products(scraper.scraped_items)
    if products:
        print(f"\nProducts Found ({len(products)}):")
        for product in products[:3]:
            print(f"  - {product['title']}: ${product['price']}")

    contacts = DataExtractor.extract_contacts(scraper.scraped_items)
    if contacts['emails'] or contacts['phones']:
        print(f"\nContacts Found:")
        print(f"  Emails: {len(contacts['emails'])}")
        print(f"  Phones: {len(contacts['phones'])}")

    # Save results
    scraper.save_results("demo_output")
    print(f"\nDemo results saved to demo_output/")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_mode()
    else:
        cli = WebScraperCLI()
        cli.run()