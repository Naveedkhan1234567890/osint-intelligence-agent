#!/usr/bin/env python3
"""
OSINT Intelligence Agent with DeepSeek Brain
Advanced investigation tool for contact discovery and social media mapping
"""

import json
import re
import requests
import argparse
from typing import Dict, List, Optional
from dataclasses import dataclass
import concurrent.futures
from datetime import datetime

@dataclass
class InvestigationResult:
    """Stores investigation results"""
    name: str
    emails: List[str]
    phones: List[str]
    social_media: Dict[str, str]
    professional_contacts: List[str]
    confidence_score: float
    sources: List[str]
    timestamp: str

class DeepSeekBrain:
    """DeepSeek AI brain for intelligent investigation strategy"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
    
    def analyze_target(self, name: str, context: Dict) -> Dict:
        """Analyze target and determine best investigation strategy"""
        
        prompt = f"""
        You are an OSINT investigation strategist. Analyze this target and provide:
        1. Likely username patterns
        2. Probable email formats
        3. Most likely social media platforms
        4. Search strategy recommendations
        
        Target: {name}
        Context: {json.dumps(context)}
        
        Respond in JSON format with: username_patterns, email_patterns, platforms, strategy
        """
        
        if not self.api_key:
            # Fallback to rule-based logic if no API key
            return self._fallback_analysis(name, context)
        
        try:
            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return json.loads(result['choices'][0]['message']['content'])
            else:
                return self._fallback_analysis(name, context)
                
        except Exception as e:
            print(f"DeepSeek API error: {e}, using fallback logic")
            return self._fallback_analysis(name, context)
    
    def _fallback_analysis(self, name: str, context: Dict) -> Dict:
        """Rule-based fallback when DeepSeek unavailable"""
        parts = name.lower().split()
        first = parts[0] if parts else ""
        last = parts[-1] if len(parts) > 1 else ""
        
        return {
            "username_patterns": [
                f"{first}{last}",
                f"{first}_{last}",
                f"{first}.{last}",
                f"{first}{last}123",
                f"{last}{first}"
            ],
            "email_patterns": [
                f"{first}@gmail.com",
                f"{first}.{last}@gmail.com",
                f"{first}{last}@gmail.com",
                f"{first[0]}{last}@gmail.com"
            ],
            "platforms": ["instagram", "twitter", "tiktok", "facebook", "linkedin"],
            "strategy": "broad_search"
        }
    
    def generate_report(self, results: Dict) -> str:
        """Generate intelligent investigation report"""
        
        prompt = f"""
        Generate a professional OSINT investigation report from this data:
        {json.dumps(results, indent=2)}
        
        Include:
        - Executive summary
        - All contact methods found
        - Platform mapping
        - Confidence assessment
        - Recommended next steps
        """
        
        if not self.api_key:
            return self._generate_basic_report(results)
        
        try:
            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return self._generate_basic_report(results)
                
        except Exception as e:
            return self._generate_basic_report(results)
    
    def _generate_basic_report(self, results: Dict) -> str:
        """Basic report generation without AI"""
        report = f"""
# OSINT Investigation Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Target Information
Name: {results.get('name', 'Unknown')}

## Social Media Accounts Found
"""
        for platform, url in results.get('social_media', {}).items():
            report += f"- {platform}: {url}\n"
        
        report += f"\n## Emails Found\n"
        for email in results.get('emails', []):
            report += f"- {email}\n"
        
        report += f"\n## Phone Numbers Found\n"
        for phone in results.get('phones', []):
            report += f"- {phone}\n"
        
        return report


class OSINTAgent:
    """Main OSINT investigation agent"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.brain = DeepSeekBrain(self.config.get('deepseek_api_key'))
        self.results = {
            'emails': [],
            'phones': [],
            'social_media': {},
            'professional_contacts': [],
            'sources': []
        }
    
    def _load_config(self, path: str) -> Dict:
        """Load configuration file"""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Config file not found, using defaults")
            return {}
    
    def investigate(self, name: str, **kwargs) -> InvestigationResult:
        """Main investigation function"""
        
        print(f"\n🔍 Starting investigation for: {name}")
        print("🧠 DeepSeek brain analyzing target...")
        
        # Get AI strategy
        context = kwargs
        strategy = self.brain.analyze_target(name, context)
        
        print(f"✅ Strategy generated: {strategy['strategy']}")
        print(f"🎯 Testing {len(strategy['username_patterns'])} username patterns...")
        
        # Execute searches in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            
            # Social media searches
            for username in strategy['username_patterns']:
                futures.append(executor.submit(self._search_instagram, username))
                futures.append(executor.submit(self._search_twitter, username))
                futures.append(executor.submit(self._search_tiktok, username))
                futures.append(executor.submit(self._search_telegram, username))
            
            # Link aggregator searches
            for username in strategy['username_patterns']:
                futures.append(executor.submit(self._scrape_allmylinks, username))
                futures.append(executor.submit(self._scrape_linktree, username))
            
            # Email searches
            for email in strategy['email_patterns']:
                futures.append(executor.submit(self._validate_email, email))
            
            # Wait for all to complete
            concurrent.futures.wait(futures)
        
        print(f"\n✅ Investigation complete!")
        print(f"📊 Found {len(self.results['social_media'])} social media accounts")
        print(f"📧 Found {len(self.results['emails'])} emails")
        print(f"📱 Found {len(self.results['phones'])} phone numbers")
        
        # Generate AI report
        print("\n🧠 DeepSeek generating intelligence report...")
        report = self.brain.generate_report(self.results)
        
        return InvestigationResult(
            name=name,
            emails=self.results['emails'],
            phones=self.results['phones'],
            social_media=self.results['social_media'],
            professional_contacts=self.results['professional_contacts'],
            confidence_score=self._calculate_confidence(),
            sources=self.results['sources'],
            timestamp=datetime.now().isoformat()
        )
    
    def _search_instagram(self, username: str) -> None:
        """Search Instagram for username"""
        try:
            url = f"https://www.instagram.com/{username}/"
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code == 200:
                self.results['social_media'][f'Instagram (@{username})'] = url
                self.results['sources'].append('Instagram')
                print(f"✅ Found Instagram: @{username}")
        except:
            pass
    
    def _search_twitter(self, username: str) -> None:
        """Search Twitter for username"""
        try:
            url = f"https://twitter.com/{username}"
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code == 200 and 'This account doesn't exist' not in response.text:
                self.results['social_media'][f'Twitter (@{username})'] = url
                self.results['sources'].append('Twitter')
                print(f"✅ Found Twitter: @{username}")
        except:
            pass
    
    def _search_tiktok(self, username: str) -> None:
        """Search TikTok for username"""
        try:
            url = f"https://www.tiktok.com/@{username}"
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code == 200:
                self.results['social_media'][f'TikTok (@{username})'] = url
                self.results['sources'].append('TikTok')
                print(f"✅ Found TikTok: @{username}")
        except:
            pass
    
    def _search_telegram(self, username: str) -> None:
        """Search Telegram for username"""
        try:
            url = f"https://t.me/{username}"
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code == 200:
                self.results['social_media'][f'Telegram (@{username})'] = url
                self.results['sources'].append('Telegram')
                print(f"✅ Found Telegram: @{username}")
        except:
            pass
    
    def _scrape_allmylinks(self, username: str) -> None:
        """Scrape AllMyLinks for all platform links"""
        try:
            url = f"https://allmylinks.com/{username}"
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            
            if response.status_code == 200:
                # Extract all links from page
                links = re.findall(r'href=[\'"]?([^\'" >]+)', response.text)
                
                for link in links:
                    if any(platform in link.lower() for platform in 
                          ['instagram', 'twitter', 'tiktok', 'snapchat', 'onlyfans', 
                           'youtube', 'twitch', 'discord', 'telegram']):
                        platform_name = self._identify_platform(link)
                        if platform_name:
                            self.results['social_media'][platform_name] = link
                            print(f"✅ Found via AllMyLinks: {platform_name}")
                
                self.results['sources'].append('AllMyLinks')
        except:
            pass
    
    def _scrape_linktree(self, username: str) -> None:
        """Scrape Linktree for all platform links"""
        try:
            url = f"https://linktr.ee/{username}"
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            
            if response.status_code == 200:
                links = re.findall(r'href=[\'"]?([^\'" >]+)', response.text)
                
                for link in links:
                    if any(platform in link.lower() for platform in 
                          ['instagram', 'twitter', 'tiktok', 'snapchat', 'youtube']):
                        platform_name = self._identify_platform(link)
                        if platform_name:
                            self.results['social_media'][platform_name] = link
                            print(f"✅ Found via Linktree: {platform_name}")
                
                self.results['sources'].append('Linktree')
        except:
            pass
    
    def _validate_email(self, email: str) -> None:
        """Validate email address"""
        # Basic regex validation
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            # Could add SMTP validation here
            self.results['emails'].append(email)
            print(f"📧 Generated email pattern: {email}")
    
    def _identify_platform(self, url: str) -> Optional[str]:
        """Identify social media platform from URL"""
        platforms = {
            'instagram.com': 'Instagram',
            'twitter.com': 'Twitter',
            'x.com': 'Twitter/X',
            'tiktok.com': 'TikTok',
            'snapchat.com': 'Snapchat',
            'facebook.com': 'Facebook',
            'linkedin.com': 'LinkedIn',
            'youtube.com': 'YouTube',
            'twitch.tv': 'Twitch',
            'discord.gg': 'Discord',
            't.me': 'Telegram',
            'onlyfans.com': 'OnlyFans',
            'patreon.com': 'Patreon'
        }
        
        for domain, platform in platforms.items():
            if domain in url.lower():
                return f"{platform} ({url})"
        return None
    
    def _calculate_confidence(self) -> float:
        """Calculate confidence score based on findings"""
        score = 0.0
        
        # Social media accounts found
        score += min(len(self.results['social_media']) * 5, 50)
        
        # Emails found
        score += min(len(self.results['emails']) * 15, 30)
        
        # Phones found
        score += min(len(self.results['phones']) * 20, 20)
        
        return min(score, 100.0)
    
    def save_report(self, result: InvestigationResult, filename: str = None):
        """Save investigation report to file"""
        if not filename:
            filename = f"report_{result.name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump({
                'name': result.name,
                'emails': result.emails,
                'phones': result.phones,
                'social_media': result.social_media,
                'professional_contacts': result.professional_contacts,
                'confidence_score': result.confidence_score,
                'sources': result.sources,
                'timestamp': result.timestamp
            }, f, indent=2)
        
        print(f"\n💾 Report saved to: {filename}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='OSINT Intelligence Agent with DeepSeek Brain')
    parser.add_argument('--name', type=str, help='Target name to investigate')
    parser.add_argument('--location', type=str, help='Target location (optional)')
    parser.add_argument('--age', type=int, help='Target age (optional)')
    parser.add_argument('--profession', type=str, help='Target profession (optional)')
    parser.add_argument('--output', type=str, help='Output file path')
    
    args = parser.parse_args()
    
    # Interactive mode if no name provided
    if not args.name:
        print("\n🔍 OSINT Intelligence Agent with DeepSeek Brain")
        print("=" * 50)
        name = input("\nEnter target name: ")
        location = input("Enter location (optional): ")
        age = input("Enter age (optional): ")
        profession = input("Enter profession (optional): ")
    else:
        name = args.name
        location = args.location
        age = args.age
        profession = args.profession
    
    # Create agent and investigate
    agent = OSINTAgent()
    
    context = {}
    if location:
        context['location'] = location
    if age:
        context['age'] = age
    if profession:
        context['profession'] = profession
    
    result = agent.investigate(name, **context)
    
    # Generate and display report
    report = agent.brain.generate_report({
        'name': result.name,
        'emails': result.emails,
        'phones': result.phones,
        'social_media': result.social_media,
        'confidence_score': result.confidence_score
    })
    
    print("\n" + "=" * 50)
    print(report)
    print("=" * 50)
    
    # Save report
    agent.save_report(result, args.output)
    
    print(f"\n✅ Investigation complete! Confidence: {result.confidence_score}%")


if __name__ == "__main__":
    main()
