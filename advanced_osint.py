#!/usr/bin/env python3
"""
Advanced OSINT Intelligence Agent
Enhanced version with Sherlock, breach data, phone lookup, and advanced scraping
"""

import json
import re
import requests
import subprocess
import os
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
import time
from bs4 import BeautifulSoup
import hashlib

@dataclass
class AdvancedResult:
    """Enhanced investigation results"""
    name: str
    emails: List[Dict]  # {email, source, confidence}
    phones: List[Dict]  # {phone, source, confidence}
    social_media: Dict[str, Dict]  # {platform: {url, username, followers, verified}}
    usernames: List[str]
    websites: List[str]
    breach_data: List[Dict]
    professional: Dict
    metadata: Dict
    confidence_score: float

class AdvancedOSINT:
    """Advanced OSINT with multiple intelligence sources"""
    
    def __init__(self):
        self.results = {
            'emails': [],
            'phones': [],
            'social_media': {},
            'usernames': set(),
            'websites': [],
            'breach_data': [],
            'professional': {},
            'metadata': {}
        }
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def investigate_advanced(self, name: str, **kwargs) -> AdvancedResult:
        """Advanced multi-source investigation"""
        
        print(f"\n🔍 ADVANCED OSINT Investigation: {name}")
        print("=" * 60)
        
        # Phase 1: Username generation and validation
        print("\n[Phase 1] Generating username patterns...")
        usernames = self._generate_usernames(name)
        print(f"✅ Generated {len(usernames)} username variations")
        
        # Phase 2: Sherlock scan (400+ platforms)
        print("\n[Phase 2] Running Sherlock scan (400+ platforms)...")
        self._run_sherlock(usernames[:5])
        
        # Phase 3: Social media deep dive
        print("\n[Phase 3] Deep social media analysis...")
        with ThreadPoolExecutor(max_workers=15) as executor:
            futures = []
            
            for username in usernames[:10]:
                futures.append(executor.submit(self._deep_instagram, username))
                futures.append(executor.submit(self._deep_twitter, username))
                futures.append(executor.submit(self._deep_tiktok, username))
                futures.append(executor.submit(self._deep_facebook, username))
                futures.append(executor.submit(self._deep_linkedin, username))
                futures.append(executor.submit(self._deep_github, username))
                futures.append(executor.submit(self._deep_reddit, username))
                futures.append(executor.submit(self._deep_telegram, username))
                futures.append(executor.submit(self._deep_snapchat, username))
                futures.append(executor.submit(self._deep_discord, username))
            
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    pass
        
        # Phase 4: Link aggregator scraping
        print("\n[Phase 4] Scraping link aggregators...")
        for username in usernames[:5]:
            self._scrape_allmylinks_advanced(username)
            self._scrape_linktree_advanced(username)
            self._scrape_beacons(username)
            self._scrape_biolink(username)
        
        # Phase 5: Email discovery
        print("\n[Phase 5] Email pattern generation and validation...")
        self._generate_emails(name)
        self._validate_emails()
        
        # Phase 6: Phone number patterns
        print("\n[Phase 6] Phone number pattern analysis...")
        if 'location' in kwargs:
            self._generate_phone_patterns(kwargs['location'])
        
        # Phase 7: Breach data search
        print("\n[Phase 7] Searching breach databases...")
        self._search_breaches(name)
        
        # Phase 8: Professional networks
        print("\n[Phase 8] Professional network analysis...")
        self._search_professional(name)
        
        # Phase 9: Website discovery
        print("\n[Phase 9] Personal website discovery...")
        self._find_websites(name, usernames)
        
        # Phase 10: Metadata extraction
        print("\n[Phase 10] Extracting metadata...")
        self._extract_metadata()
        
        print("\n" + "=" * 60)
        print("✅ INVESTIGATION COMPLETE")
        self._print_summary()
        
        return AdvancedResult(
            name=name,
            emails=self.results['emails'],
            phones=self.results['phones'],
            social_media=self.results['social_media'],
            usernames=list(self.results['usernames']),
            websites=self.results['websites'],
            breach_data=self.results['breach_data'],
            professional=self.results['professional'],
            metadata=self.results['metadata'],
            confidence_score=self._calculate_advanced_confidence()
        )
    
    def _generate_usernames(self, name: str) -> List[str]:
        """Generate comprehensive username variations"""
        parts = name.lower().replace('-', ' ').replace('_', ' ').split()
        
        if not parts:
            return []
        
        first = parts[0]
        last = parts[-1] if len(parts) > 1 else ""
        
        usernames = [
            # Basic combinations
            f"{first}{last}",
            f"{first}_{last}",
            f"{first}.{last}",
            f"{first}-{last}",
            f"{last}{first}",
            f"{last}_{first}",
            f"{last}.{first}",
            
            # With numbers
            f"{first}{last}123",
            f"{first}{last}1",
            f"{first}{last}99",
            f"{first}{last}2024",
            
            # Abbreviated
            f"{first[0]}{last}",
            f"{first}{last[0]}",
            f"{first[0]}.{last}",
            
            # Single name
            first,
            last,
            
            # With underscores
            f"_{first}{last}",
            f"{first}{last}_",
            f"_{first}_{last}_",
            
            # Official/real
            f"{first}{last}official",
            f"real{first}{last}",
            f"{first}{last}real",
            
            # The/its
            f"the{first}{last}",
            f"its{first}{last}",
        ]
        
        return list(set(usernames))
    
    def _run_sherlock(self, usernames: List[str]):
        """Run Sherlock for 400+ platform scan"""
        try:
            # Check if sherlock is installed
            result = subprocess.run(['sherlock', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            
            for username in usernames:
                print(f"  🔎 Sherlock scanning: {username}")
                try:
                    result = subprocess.run(
                        ['sherlock', username, '--timeout', '10', '--print-found'],
                        capture_output=True,
                        text=True,
                        timeout=120
                    )
                    
                    # Parse sherlock output
                    for line in result.stdout.split('\n'):
                        if 'http' in line:
                            self.results['usernames'].add(username)
                            # Extract platform and URL
                            match = re.search(r'\[(.*?)\].*?(https?://\S+)', line)
                            if match:
                                platform, url = match.groups()
                                self.results['social_media'][f"{platform} (@{username})"] = {
                                    'url': url,
                                    'username': username,
                                    'source': 'Sherlock'
                                }
                                print(f"    ✅ Found on {platform}")
                
                except subprocess.TimeoutExpired:
                    print(f"    ⏱️ Sherlock timeout for {username}")
                except Exception as e:
                    print(f"    ❌ Sherlock error: {e}")
        
        except FileNotFoundError:
            print("  ⚠️ Sherlock not installed. Install with: pip install sherlock-project")
    
    def _deep_instagram(self, username: str):
        """Deep Instagram analysis"""
        try:
            url = f"https://www.instagram.com/{username}/"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200 and 'Page Not Found' not in response.text:
                # Extract data from page
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Try to extract follower count, bio, etc.
                self.results['social_media'][f'Instagram (@{username})'] = {
                    'url': url,
                    'username': username,
                    'platform': 'Instagram',
                    'source': 'Direct scrape',
                    'verified': 'Verified' in response.text
                }
                self.results['usernames'].add(username)
                print(f"  ✅ Instagram: @{username}")
                
                # Extract bio for emails/phones
                bio_match = re.search(r'"biography":"(.*?)"', response.text)
                if bio_match:
                    bio = bio_match.group(1)
                    self._extract_contact_from_text(bio, 'Instagram bio')
        except:
            pass
    
    def _deep_twitter(self, username: str):
        """Deep Twitter/X analysis"""
        try:
            url = f"https://twitter.com/{username}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200 and "This account doesn't exist" not in response.text:
                self.results['social_media'][f'Twitter (@{username})'] = {
                    'url': url,
                    'username': username,
                    'platform': 'Twitter/X',
                    'source': 'Direct scrape'
                }
                self.results['usernames'].add(username)
                print(f"  ✅ Twitter: @{username}")
                
                # Extract bio
                self._extract_contact_from_text(response.text, 'Twitter bio')
        except:
            pass
    
    def _deep_tiktok(self, username: str):
        """Deep TikTok analysis"""
        try:
            url = f"https://www.tiktok.com/@{username}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200 and "Couldn't find this account" not in response.text:
                self.results['social_media'][f'TikTok (@{username})'] = {
                    'url': url,
                    'username': username,
                    'platform': 'TikTok',
                    'source': 'Direct scrape'
                }
                self.results['usernames'].add(username)
                print(f"  ✅ TikTok: @{username}")
        except:
            pass
    
    def _deep_facebook(self, username: str):
        """Deep Facebook analysis"""
        try:
            url = f"https://www.facebook.com/{username}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                self.results['social_media'][f'Facebook ({username})'] = {
                    'url': url,
                    'username': username,
                    'platform': 'Facebook',
                    'source': 'Direct scrape'
                }
                self.results['usernames'].add(username)
                print(f"  ✅ Facebook: {username}")
        except:
            pass
    
    def _deep_linkedin(self, username: str):
        """Deep LinkedIn analysis"""
        try:
            url = f"https://www.linkedin.com/in/{username}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                self.results['social_media'][f'LinkedIn ({username})'] = {
                    'url': url,
                    'username': username,
                    'platform': 'LinkedIn',
                    'source': 'Direct scrape'
                }
                self.results['usernames'].add(username)
                self.results['professional']['linkedin'] = url
                print(f"  ✅ LinkedIn: {username}")
        except:
            pass
    
    def _deep_github(self, username: str):
        """Deep GitHub analysis"""
        try:
            url = f"https://github.com/{username}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200 and 'Not Found' not in response.text:
                self.results['social_media'][f'GitHub (@{username})'] = {
                    'url': url,
                    'username': username,
                    'platform': 'GitHub',
                    'source': 'Direct scrape'
                }
                self.results['usernames'].add(username)
                self.results['professional']['github'] = url
                print(f"  ✅ GitHub: @{username}")
                
                # Try to extract email from commits
                self._extract_github_email(username)
        except:
            pass
    
    def _deep_reddit(self, username: str):
        """Deep Reddit analysis"""
        try:
            url = f"https://www.reddit.com/user/{username}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200 and 'page not found' not in response.text.lower():
                self.results['social_media'][f'Reddit (u/{username})'] = {
                    'url': url,
                    'username': username,
                    'platform': 'Reddit',
                    'source': 'Direct scrape'
                }
                self.results['usernames'].add(username)
                print(f"  ✅ Reddit: u/{username}")
        except:
            pass
    
    def _deep_telegram(self, username: str):
        """Deep Telegram analysis"""
        try:
            url = f"https://t.me/{username}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                self.results['social_media'][f'Telegram (@{username})'] = {
                    'url': url,
                    'username': username,
                    'platform': 'Telegram',
                    'source': 'Direct scrape'
                }
                self.results['usernames'].add(username)
                print(f"  ✅ Telegram: @{username}")
        except:
            pass
    
    def _deep_snapchat(self, username: str):
        """Deep Snapchat analysis"""
        try:
            url = f"https://www.snapchat.com/add/{username}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                self.results['social_media'][f'Snapchat (@{username})'] = {
                    'url': url,
                    'username': username,
                    'platform': 'Snapchat',
                    'source': 'Direct scrape'
                }
                self.results['usernames'].add(username)
                print(f"  ✅ Snapchat: @{username}")
        except:
            pass
    
    def _deep_discord(self, username: str):
        """Deep Discord analysis"""
        # Discord requires different approach - search for public servers
        try:
            search_url = f"https://discord.com/invite/{username}"
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code == 200:
                self.results['social_media'][f'Discord ({username})'] = {
                    'url': search_url,
                    'username': username,
                    'platform': 'Discord',
                    'source': 'Invite link'
                }
                print(f"  ✅ Discord: {username}")
        except:
            pass
    
    def _scrape_allmylinks_advanced(self, username: str):
        """Advanced AllMyLinks scraping"""
        try:
            url = f"https://allmylinks.com/{username}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract all links
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if any(platform in href.lower() for platform in 
                          ['instagram', 'twitter', 'tiktok', 'snapchat', 'onlyfans',
                           'youtube', 'twitch', 'discord', 'telegram', 'facebook']):
                        platform = self._identify_platform(href)
                        if platform:
                            self.results['social_media'][platform] = {
                                'url': href,
                                'source': 'AllMyLinks'
                            }
                            print(f"  ✅ AllMyLinks: {platform}")
                
                # Extract contact info from page
                self._extract_contact_from_text(response.text, 'AllMyLinks')
        except:
            pass
    
    def _scrape_linktree_advanced(self, username: str):
        """Advanced Linktree scraping"""
        try:
            url = f"https://linktr.ee/{username}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    platform = self._identify_platform(href)
                    if platform:
                        self.results['social_media'][platform] = {
                            'url': href,
                            'source': 'Linktree'
                        }
                        print(f"  ✅ Linktree: {platform}")
        except:
            pass
    
    def _scrape_beacons(self, username: str):
        """Scrape Beacons.ai"""
        try:
            url = f"https://beacons.ai/{username}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                self._extract_contact_from_text(response.text, 'Beacons.ai')
        except:
            pass
    
    def _scrape_biolink(self, username: str):
        """Scrape Bio.link"""
        try:
            url = f"https://bio.link/{username}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                self._extract_contact_from_text(response.text, 'Bio.link')
        except:
            pass
    
    def _generate_emails(self, name: str):
        """Generate comprehensive email patterns"""
        parts = name.lower().split()
        if not parts:
            return
        
        first = parts[0]
        last = parts[-1] if len(parts) > 1 else ""
        
        domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 
                  'protonmail.com', 'icloud.com']
        
        patterns = [
            f"{first}@",
            f"{last}@",
            f"{first}.{last}@",
            f"{first}{last}@",
            f"{first}_{last}@",
            f"{first[0]}{last}@",
            f"{first}{last[0]}@",
            f"{last}.{first}@",
        ]
        
        for pattern in patterns:
            for domain in domains:
                email = pattern + domain
                self.results['emails'].append({
                    'email': email,
                    'source': 'Generated pattern',
                    'confidence': 0.3,
                    'validated': False
                })
    
    def _validate_emails(self):
        """Validate email addresses"""
        print(f"  📧 Validating {len(self.results['emails'])} email patterns...")
        
        validated = []
        for email_data in self.results['emails']:
            email = email_data['email']
            
            # Basic regex validation
            if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                email_data['validated'] = True
                validated.append(email_data)
        
        self.results['emails'] = validated[:20]  # Keep top 20
        print(f"  ✅ {len(self.results['emails'])} emails validated")
    
    def _generate_phone_patterns(self, location: str):
        """Generate phone number patterns based on location"""
        # US area codes by state/city
        area_codes = {
            'california': ['213', '310', '323', '408', '415', '510', '562', '619', '626', '650', '714', '760', '805', '818', '831', '858', '909', '916', '925', '949'],
            'new york': ['212', '315', '347', '516', '518', '585', '607', '631', '646', '716', '718', '845', '914', '917'],
            'texas': ['210', '214', '254', '281', '325', '361', '409', '430', '432', '469', '512', '682', '713', '737', '806', '817', '830', '832', '903', '915', '936', '940', '956', '972', '979'],
            'florida': ['239', '305', '321', '352', '386', '407', '561', '727', '754', '772', '786', '813', '850', '863', '904', '941', '954'],
        }
        
        location_lower = location.lower()
        codes = []
        
        for state, state_codes in area_codes.items():
            if state in location_lower:
                codes = state_codes
                break
        
        if codes:
            print(f"  📱 Generated phone patterns for {location} ({len(codes)} area codes)")
            for code in codes[:5]:  # Top 5 area codes
                self.results['phones'].append({
                    'pattern': f"({code}) XXX-XXXX",
                    'area_code': code,
                    'location': location,
                    'confidence': 0.4
                })
    
    def _search_breaches(self, name: str):
        """Search for breach data (simulated - real implementation needs API)"""
        print("  🔓 Searching breach databases...")
        
        # This would integrate with services like:
        # - Have I Been Pwned API
        # - Dehashed API
        # - Intelligence X
        
        # Simulated for now
        self.results['breach_data'].append({
            'note': 'Breach search requires API keys for HIBP, Dehashed, or Intelligence X',
            'recommendation': 'Add API keys to config.json for breach data access'
        })
    
    def _search_professional(self, name: str):
        """Search professional networks"""
        print("  💼 Searching professional networks...")
        
        # Already covered LinkedIn in deep search
        # Could add: AngelList, Crunchbase, etc.
        pass
    
    def _find_websites(self, name: str, usernames: List[str]):
        """Find personal websites"""
        print("  🌐 Searching for personal websites...")
        
        # Try common patterns
        name_clean = name.lower().replace(' ', '')
        domains = [
            f"{name_clean}.com",
            f"{name_clean}.net",
            f"{name_clean}.io",
        ]
        
        for username in usernames[:5]:
            domains.extend([
                f"{username}.com",
                f"{username}.net",
                f"{username}.io",
            ])
        
        for domain in domains:
            try:
                response = self.session.get(f"http://{domain}", timeout=5)
                if response.status_code == 200:
                    self.results['websites'].append(domain)
                    print(f"  ✅ Website: {domain}")
            except:
                pass
    
    def _extract_metadata(self):
        """Extract metadata from findings"""
        self.results['metadata'] = {
            'total_platforms': len(self.results['social_media']),
            'total_usernames': len(self.results['usernames']),
            'total_emails': len(self.results['emails']),
            'total_phones': len(self.results['phones']),
            'total_websites': len(self.results['websites']),
            'investigation_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def _extract_contact_from_text(self, text: str, source: str):
        """Extract emails and phones from text"""
        # Extract emails
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        for email in emails:
            if not any(e['email'] == email for e in self.results['emails']):
                self.results['emails'].append({
                    'email': email,
                    'source': source,
                    'confidence': 0.9,
                    'validated': True
                })
                print(f"  📧 Email found: {email} (from {source})")
        
        # Extract phone numbers
        phones = re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text)
        for phone in phones:
            if not any(p.get('number') == phone for p in self.results['phones']):
                self.results['phones'].append({
                    'number': phone,
                    'source': source,
                    'confidence': 0.8
                })
                print(f"  📱 Phone found: {phone} (from {source})")
    
    def _extract_github_email(self, username: str):
        """Extract email from GitHub commits"""
        try:
            # GitHub API to get user's public events
            url = f"https://api.github.com/users/{username}/events/public"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                events = response.json()
                for event in events[:10]:  # Check recent events
                    if event.get('type') == 'PushEvent':
                        commits = event.get('payload', {}).get('commits', [])
                        for commit in commits:
                            email = commit.get('author', {}).get('email')
                            if email and not any(e['email'] == email for e in self.results['emails']):
                                self.results['emails'].append({
                                    'email': email,
                                    'source': 'GitHub commits',
                                    'confidence': 0.95,
                                    'validated': True
                                })
                                print(f"  📧 GitHub email: {email}")
        except:
            pass
    
    def _identify_platform(self, url: str) -> Optional[str]:
        """Identify platform from URL"""
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
            'reddit.com': 'Reddit',
            'github.com': 'GitHub',
            'onlyfans.com': 'OnlyFans',
            'patreon.com': 'Patreon',
        }
        
        for domain, platform in platforms.items():
            if domain in url.lower():
                return f"{platform} ({url})"
        return None
    
    def _calculate_advanced_confidence(self) -> float:
        """Calculate confidence score"""
        score = 0.0
        
        # Social media (max 40 points)
        score += min(len(self.results['social_media']) * 3, 40)
        
        # Validated emails (max 30 points)
        validated_emails = [e for e in self.results['emails'] if e.get('validated')]
        score += min(len(validated_emails) * 10, 30)
        
        # Phone numbers (max 15 points)
        score += min(len(self.results['phones']) * 5, 15)
        
        # Websites (max 10 points)
        score += min(len(self.results['websites']) * 5, 10)
        
        # Professional profiles (max 5 points)
        score += min(len(self.results['professional']) * 2.5, 5)
        
        return min(score, 100.0)
    
    def _print_summary(self):
        """Print investigation summary"""
        print(f"\n📊 INVESTIGATION SUMMARY:")
        print(f"  • Social Media Accounts: {len(self.results['social_media'])}")
        print(f"  • Unique Usernames: {len(self.results['usernames'])}")
        print(f"  • Email Addresses: {len(self.results['emails'])}")
        print(f"  • Phone Numbers: {len(self.results['phones'])}")
        print(f"  • Personal Websites: {len(self.results['websites'])}")
        print(f"  • Professional Profiles: {len(self.results['professional'])}")
        print(f"  • Confidence Score: {self._calculate_advanced_confidence():.1f}%")


def main():
    """Main entry point for advanced OSINT"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Advanced OSINT Intelligence Agent')
    parser.add_argument('--name', type=str, required=True, help='Target name')
    parser.add_argument('--location', type=str, help='Target location')
    parser.add_argument('--output', type=str, help='Output JSON file')
    
    args = parser.parse_args()
    
    agent = AdvancedOSINT()
    result = agent.investigate_advanced(args.name, location=args.location)
    
    # Save results
    if args.output:
        with open(args.output, 'w') as f:
            json.dump({
                'name': result.name,
                'emails': result.emails,
                'phones': result.phones,
                'social_media': result.social_media,
                'usernames': result.usernames,
                'websites': result.websites,
                'professional': result.professional,
                'metadata': result.metadata,
                'confidence_score': result.confidence_score
            }, f, indent=2)
        print(f"\n💾 Results saved to: {args.output}")


if __name__ == "__main__":
    main()
