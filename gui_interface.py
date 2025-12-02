#!/usr/bin/env python3
"""
GUI Interface for OSINT Agent
Easy-to-use graphical interface for Windows users
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import json
from advanced_osint import AdvancedOSINT
from osint_agent import OSINTAgent, DeepSeekBrain

class OSINTGui:
    """Graphical User Interface for OSINT Agent"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("OSINT Intelligence Agent")
        self.root.geometry("900x700")
        self.root.configure(bg='#2b2b2b')
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='#2b2b2b', foreground='white', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10, 'bold'))
        style.configure('TEntry', fieldbackground='#3c3c3c', foreground='white')
        style.configure('Header.TLabel', font=('Arial', 16, 'bold'), foreground='#00ff00')
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create GUI widgets"""
        
        # Header
        header = ttk.Label(self.root, text="🔍 OSINT Intelligence Agent", style='Header.TLabel')
        header.pack(pady=20)
        
        # Input Frame
        input_frame = tk.Frame(self.root, bg='#2b2b2b')
        input_frame.pack(pady=10, padx=20, fill='x')
        
        # Name input
        ttk.Label(input_frame, text="Target Name:").grid(row=0, column=0, sticky='w', pady=5)
        self.name_entry = ttk.Entry(input_frame, width=40)
        self.name_entry.grid(row=0, column=1, pady=5, padx=10)
        
        # Location input
        ttk.Label(input_frame, text="Location (optional):").grid(row=1, column=0, sticky='w', pady=5)
        self.location_entry = ttk.Entry(input_frame, width=40)
        self.location_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Age input
        ttk.Label(input_frame, text="Age (optional):").grid(row=2, column=0, sticky='w', pady=5)
        self.age_entry = ttk.Entry(input_frame, width=40)
        self.age_entry.grid(row=2, column=1, pady=5, padx=10)
        
        # Mode selection
        ttk.Label(input_frame, text="Investigation Mode:").grid(row=3, column=0, sticky='w', pady=5)
        self.mode_var = tk.StringVar(value="advanced")
        mode_frame = tk.Frame(input_frame, bg='#2b2b2b')
        mode_frame.grid(row=3, column=1, sticky='w', pady=5, padx=10)
        
        ttk.Radiobutton(mode_frame, text="Basic", variable=self.mode_var, value="basic").pack(side='left', padx=5)
        ttk.Radiobutton(mode_frame, text="Advanced", variable=self.mode_var, value="advanced").pack(side='left', padx=5)
        
        # Buttons Frame
        button_frame = tk.Frame(self.root, bg='#2b2b2b')
        button_frame.pack(pady=20)
        
        self.investigate_btn = tk.Button(
            button_frame, 
            text="🔍 Start Investigation", 
            command=self.start_investigation,
            bg='#00ff00',
            fg='black',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.investigate_btn.pack(side='left', padx=10)
        
        self.save_btn = tk.Button(
            button_frame,
            text="💾 Save Report",
            command=self.save_report,
            bg='#0080ff',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10,
            cursor='hand2',
            state='disabled'
        )
        self.save_btn.pack(side='left', padx=10)
        
        self.clear_btn = tk.Button(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_results,
            bg='#ff4444',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.clear_btn.pack(side='left', padx=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.root, mode='indeterminate', length=860)
        self.progress.pack(pady=10, padx=20)
        
        # Results Frame
        results_frame = tk.Frame(self.root, bg='#2b2b2b')
        results_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        ttk.Label(results_frame, text="Investigation Results:", font=('Arial', 12, 'bold')).pack(anchor='w')
        
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            wrap=tk.WORD,
            width=100,
            height=20,
            bg='#1e1e1e',
            fg='#00ff00',
            font=('Consolas', 10),
            insertbackground='white'
        )
        self.results_text.pack(fill='both', expand=True, pady=10)
        
        # Status bar
        self.status_label = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor='w')
        self.status_label.pack(side='bottom', fill='x')
        
        self.current_results = None
        
    def start_investigation(self):
        """Start the investigation in a separate thread"""
        name = self.name_entry.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Please enter a target name")
            return
        
        # Disable button during investigation
        self.investigate_btn.config(state='disabled')
        self.save_btn.config(state='disabled')
        self.progress.start()
        self.status_label.config(text="Investigation in progress...")
        self.results_text.delete(1.0, tk.END)
        
        # Run in thread to prevent GUI freeze
        thread = threading.Thread(target=self.run_investigation, args=(name,))
        thread.daemon = True
        thread.start()
        
    def run_investigation(self, name):
        """Run the actual investigation"""
        try:
            location = self.location_entry.get().strip()
            age = self.age_entry.get().strip()
            mode = self.mode_var.get()
            
            self.append_result(f"\n{'='*80}\n")
            self.append_result(f"🔍 Starting {mode.upper()} investigation for: {name}\n")
            self.append_result(f"{'='*80}\n\n")
            
            if mode == "advanced":
                agent = AdvancedOSINT()
                result = agent.investigate_advanced(name, location=location)
                
                # Display results
                self.append_result(f"\n📊 INVESTIGATION COMPLETE\n")
                self.append_result(f"{'='*80}\n\n")
                
                self.append_result(f"📱 SOCIAL MEDIA ACCOUNTS ({len(result.social_media)}):\n")
                for platform, data in result.social_media.items():
                    url = data.get('url', 'N/A')
                    self.append_result(f"  ✅ {platform}\n     {url}\n")
                
                self.append_result(f"\n📧 EMAIL ADDRESSES ({len(result.emails)}):\n")
                for email_data in result.emails[:10]:  # Show top 10
                    email = email_data.get('email', 'N/A')
                    confidence = email_data.get('confidence', 0) * 100
                    source = email_data.get('source', 'Unknown')
                    self.append_result(f"  • {email} (Confidence: {confidence:.0f}%, Source: {source})\n")
                
                self.append_result(f"\n📱 PHONE NUMBERS ({len(result.phones)}):\n")
                for phone_data in result.phones:
                    phone = phone_data.get('number', phone_data.get('pattern', 'N/A'))
                    self.append_result(f"  • {phone}\n")
                
                self.append_result(f"\n🌐 WEBSITES ({len(result.websites)}):\n")
                for website in result.websites:
                    self.append_result(f"  • {website}\n")
                
                self.append_result(f"\n💼 PROFESSIONAL PROFILES:\n")
                for platform, url in result.professional.items():
                    self.append_result(f"  • {platform.title()}: {url}\n")
                
                self.append_result(f"\n🎯 CONFIDENCE SCORE: {result.confidence_score:.1f}%\n")
                
                self.current_results = {
                    'name': result.name,
                    'emails': result.emails,
                    'phones': result.phones,
                    'social_media': result.social_media,
                    'usernames': result.usernames,
                    'websites': result.websites,
                    'professional': result.professional,
                    'metadata': result.metadata,
                    'confidence_score': result.confidence_score
                }
                
            else:  # Basic mode
                agent = OSINTAgent()
                result = agent.investigate(name, location=location, age=age)
                
                self.append_result(f"\n📊 INVESTIGATION COMPLETE\n")
                self.append_result(f"{'='*80}\n\n")
                
                self.append_result(f"📱 SOCIAL MEDIA ACCOUNTS ({len(result.social_media)}):\n")
                for platform, url in result.social_media.items():
                    self.append_result(f"  ✅ {platform}: {url}\n")
                
                self.append_result(f"\n📧 EMAILS ({len(result.emails)}):\n")
                for email in result.emails:
                    self.append_result(f"  • {email}\n")
                
                self.append_result(f"\n🎯 CONFIDENCE SCORE: {result.confidence_score:.1f}%\n")
                
                self.current_results = {
                    'name': result.name,
                    'emails': result.emails,
                    'phones': result.phones,
                    'social_media': result.social_media,
                    'confidence_score': result.confidence_score
                }
            
            self.status_label.config(text="Investigation complete!")
            self.save_btn.config(state='normal')
            
        except Exception as e:
            self.append_result(f"\n❌ ERROR: {str(e)}\n")
            self.status_label.config(text="Investigation failed")
            messagebox.showerror("Error", f"Investigation failed: {str(e)}")
        
        finally:
            self.progress.stop()
            self.investigate_btn.config(state='normal')
    
    def append_result(self, text):
        """Append text to results (thread-safe)"""
        self.results_text.insert(tk.END, text)
        self.results_text.see(tk.END)
        self.root.update_idletasks()
    
    def save_report(self):
        """Save investigation report to file"""
        if not self.current_results:
            messagebox.showwarning("Warning", "No results to save")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"osint_report_{self.current_results['name'].replace(' ', '_')}.json"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.current_results, f, indent=2)
                messagebox.showinfo("Success", f"Report saved to:\n{filename}")
                self.status_label.config(text=f"Report saved: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save report: {str(e)}")
    
    def clear_results(self):
        """Clear all results"""
        self.name_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.results_text.delete(1.0, tk.END)
        self.current_results = None
        self.save_btn.config(state='disabled')
        self.status_label.config(text="Ready")


def main():
    """Launch GUI"""
    root = tk.Tk()
    app = OSINTGui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
