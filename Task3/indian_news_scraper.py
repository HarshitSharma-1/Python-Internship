import requests
from bs4 import BeautifulSoup
import datetime
import time

class IndianNewsScraper:
    """
    Web scraper for various Indian news channels
    """
    
    # Dictionary of Indian news channels and their URLs
    NEWS_CHANNELS = {
        'timesofindia': {
            'name': 'Times of India',
            'url': 'https://timesofindia.indiatimes.com/',
            'selectors': ['h2', 'h3', '.heading', '.title']
        },
        'ndtv': {
            'name': 'NDTV',
            'url': 'https://www.ndtv.com/latest',
            'selectors': ['h2', 'h3', '.newsHdng', '.nstory_header']
        },
        'hindustantimes': {
            'name': 'Hindustan Times',
            'url': 'https://www.hindustantimes.com/latest-news',
            'selectors': ['h2', 'h3', '.hdg3', '.heading']
        },
        'indiatoday': {
            'name': 'India Today',
            'url': 'https://www.indiatoday.in/news.html',
            'selectors': ['h2', 'h3', '.story__title', '.heading']
        },
        'thehindu': {
            'name': 'The Hindu',
            'url': 'https://www.thehindu.com/latest-news/',
            'selectors': ['h2', 'h3', '.title', '.story-title']
        },
        'indianexpress': {
            'name': 'The Indian Express',
            'url': 'https://indianexpress.com/latest-news/',
            'selectors': ['h2', 'h3', '.title', '.headline']
        },
        'republicworld': {
            'name': 'Republic World',
            'url': 'https://www.republicworld.com/',
            'selectors': ['h2', 'h3', '.heading', '.news-title']
        },
        'aajtak': {
            'name': 'Aaj Tak',
            'url': 'https://www.aajtak.in/latest-news',
            'selectors': ['h2', 'h3', '.widget-title', '.story-heading']
        },
        'abplive': {
            'name': 'ABP Live',
            'url': 'https://news.abplive.com/latest-news',
            'selectors': ['h2', 'h3', '.title', '.headline']
        },
        'zeenews': {
            'name': 'Zee News',
            'url': 'https://zeenews.india.com/latest-news',
            'selectors': ['h2', 'h3', '.news-title', '.heading']
        }
    }

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }

    def scrape_channel(self, channel_key, max_headlines=15):
        """
        Scrape headlines from a specific news channel
        """
        if channel_key not in self.NEWS_CHANNELS:
            print(f"Channel '{channel_key}' not found. Available channels: {list(self.NEWS_CHANNELS.keys())}")
            return []
        
        channel = self.NEWS_CHANNELS[channel_key]
        print(f"Scraping headlines from {channel['name']}...")
        
        try:
            response = requests.get(channel['url'], headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            headlines = []
            
            # Try different selectors to find headlines
            for selector in channel['selectors']:
                elements = soup.select(selector)
                for element in elements:
                    text = element.get_text().strip()
                    if self.is_valid_headline(text):
                        headlines.append(text)
            
            # Remove duplicates while preserving order
            unique_headlines = []
            seen = set()
            for headline in headlines:
                if headline not in seen:
                    seen.add(headline)
                    unique_headlines.append(headline)
            
            return unique_headlines[:max_headlines]
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {channel['name']}: {e}")
            return []
        except Exception as e:
            print(f"Error parsing {channel['name']}: {e}")
            return []

    def is_valid_headline(self, text):
        """
        Validate if the text is a proper headline
        """
        # Filter out short texts, navigation items, etc.
        if len(text) < 20 or len(text) > 200:
            return False
        
        # Common words to exclude (navigation, footer links, etc.)
        exclude_words = ['home', 'about', 'contact', 'login', 'sign up', 'menu', 'search', 'follow us']
        text_lower = text.lower()
        
        if any(word in text_lower for word in exclude_words):
            return False
            
        return True

    def list_channels(self):
        """
        Display available news channels
        """
        print("Available Indian News Channels:")
        print("=" * 50)
        for key, channel in self.NEWS_CHANNELS.items():
            print(f"{key:15} - {channel['name']}")
        print()

    def scrape_multiple_channels(self, channel_keys, max_per_channel=10):
        """
        Scrape headlines from multiple channels
        """
        all_headlines = {}
        
        for channel_key in channel_keys:
            if channel_key in self.NEWS_CHANNELS:
                headlines = self.scrape_channel(channel_key, max_per_channel)
                all_headlines[channel_key] = headlines
                time.sleep(2)  # Be polite - delay between requests
            
        return all_headlines

def save_headlines(headlines_data, filename=None):
    """
    Save headlines to a text file
    """
    if not filename:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"indian_news_headlines_{timestamp}.txt"
    
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("INDIAN NEWS CHANNELS - TOP HEADLINES\n")
            file.write("=" * 60 + "\n")
            file.write(f"Scraped on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("=" * 60 + "\n\n")
            
            for channel_key, headlines in headlines_data.items():
                channel_name = scraper.NEWS_CHANNELS[channel_key]['name']
                file.write(f"{channel_name.upper()}\n")
                file.write("-" * 40 + "\n")
                
                if headlines:
                    for i, headline in enumerate(headlines, 1):
                        file.write(f"{i:2d}. {headline}\n")
                else:
                    file.write("No headlines found (website structure may have changed)\n")
                
                file.write("\n")
        
        print(f"Headlines saved to: {filename}")
        return filename
        
    except Exception as e:
        print(f"Error saving to file: {e}")
        return None

def display_headlines(headlines_data):
    """
    Display headlines in console
    """
    print("\n" + "="*70)
    print("INDIAN NEWS CHANNELS - TOP HEADLINES")
    print("="*70)
    
    for channel_key, headlines in headlines_data.items():
        channel_name = scraper.NEWS_CHANNELS[channel_key]['name']
        print(f"\n{channel_name.upper()}")
        print("-" * 60)
        
        if headlines:
            for i, headline in enumerate(headlines, 1):
                print(f"{i:2d}. {headline}")
        else:
            print("No headlines found (website structure may have changed)")
        
        print()

def main():
    """
    Main function to run the Indian news scraper
    """
    global scraper
    scraper = IndianNewsScraper()
    
    print("INDIAN NEWS CHANNELS SCRAPER")
    print("=" * 40)
    
    # Display available channels
    scraper.list_channels()
    
    # Let user choose channels or use default
    available_channels = list(scraper.NEWS_CHANNELS.keys())
    
    print("Choose channels to scrape (comma-separated):")
    print("Example: timesofindia,ndtv,hindustantimes")
    print("Press Enter for default selection (first 3 channels)")
    
    user_input = input("Your choice: ").strip()
    
    if user_input:
        selected_channels = [chan.strip() for chan in user_input.split(',')]
        # Validate channels
        valid_channels = [chan for chan in selected_channels if chan in available_channels]
        if not valid_channels:
            print("No valid channels selected. Using default.")
            valid_channels = available_channels[:3]
    else:
        valid_channels = available_channels[:3]  # Default to first 3
    
    print(f"\nScraping from: {', '.join(valid_channels)}")
    print("Please wait...\n")
    
    # Scrape headlines
    headlines_data = scraper.scrape_multiple_channels(valid_channels, max_per_channel=10)
    
    # Display results
    display_headlines(headlines_data)
    
    # Save to file
    filename = save_headlines(headlines_data)
    
    if filename:
        total_headlines = sum(len(headlines) for headlines in headlines_data.values())
        print(f"\nSuccessfully extracted {total_headlines} headlines from {len(valid_channels)} channels!")
        print(f"Results saved to: {filename}")
    else:
        print("Failed to save headlines to file.")

if __name__ == "__main__":
    main()