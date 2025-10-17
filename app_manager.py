"""
NLP 100 Apps Manager
Interactive CLI tool to browse, search, and launch apps
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class AppManager:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.apps = self.load_apps()
    
    def load_apps(self):
        """Load all app information"""
        apps = []
        for folder in sorted(self.base_dir.glob("app_*")):
            if folder.is_dir():
                app_id = folder.name.split("_")[1]
                app_name = "_".join(folder.name.split("_")[2:])
                
                # Read README for description
                readme_path = folder / "README.md"
                description = ""
                if readme_path.exists():
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        for line in lines:
                            if line.startswith("**Real-world Use Case**"):
                                description = line.split(":", 1)[1].strip() if ":" in line else ""
                                break
                
                apps.append({
                    'id': int(app_id),
                    'name': app_name.replace("_", " ").title(),
                    'folder': folder.name,
                    'path': folder,
                    'description': description
                })
        
        return apps
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*70)
        print("🔤 NLP 100 Applications Manager")
        print("="*70)
        print("\nOptions:")
        print("  1. List all apps")
        print("  2. Search apps")
        print("  3. Launch app")
        print("  4. Install app dependencies")
        print("  5. View app details")
        print("  6. Browse by category")
        print("  7. Quick launch (by ID)")
        print("  8. Check system requirements")
        print("  9. Exit")
        print("\n" + "="*70)
    
    def list_apps(self, apps=None, show_description=False):
        """List all apps"""
        if apps is None:
            apps = self.apps
        
        print(f"\n📚 Found {len(apps)} applications:\n")
        
        for app in apps:
            if show_description and app['description']:
                print(f"  {app['id']:03d}. {app['name']}")
                print(f"       └─ {app['description']}")
            else:
                print(f"  {app['id']:03d}. {app['name']}")
        
        print()
    
    def search_apps(self, query):
        """Search apps by name or description"""
        query = query.lower()
        results = [
            app for app in self.apps
            if query in app['name'].lower() or query in app['description'].lower()
        ]
        return results
    
    def get_app_by_id(self, app_id):
        """Get app by ID"""
        for app in self.apps:
            if app['id'] == app_id:
                return app
        return None
    
    def launch_app(self, app):
        """Launch an app"""
        app_path = app['path'] / "app.py"
        
        if not app_path.exists():
            print(f"❌ Error: app.py not found in {app['folder']}")
            return False
        
        print(f"\n🚀 Launching {app['name']}...")
        print(f"📂 Location: {app['path']}")
        print(f"🌐 Opening in browser at http://localhost:8501")
        print("\nPress Ctrl+C to stop the app\n")
        
        try:
            subprocess.run(
                ["streamlit", "run", str(app_path)],
                cwd=str(app['path'])
            )
        except KeyboardInterrupt:
            print("\n\n✅ App stopped")
        except FileNotFoundError:
            print("❌ Error: Streamlit not installed. Install with: pip install streamlit")
        
        return True
    
    def install_dependencies(self, app):
        """Install app dependencies"""
        req_path = app['path'] / "requirements.txt"
        
        if not req_path.exists():
            print(f"❌ Error: requirements.txt not found in {app['folder']}")
            return False
        
        print(f"\n📦 Installing dependencies for {app['name']}...")
        print(f"📂 Location: {app['path']}\n")
        
        try:
            subprocess.run(
                ["pip", "install", "-r", "requirements.txt"],
                cwd=str(app['path'])
            )
            print(f"\n✅ Dependencies installed successfully!")
        except Exception as e:
            print(f"❌ Error installing dependencies: {e}")
            return False
        
        return True
    
    def view_details(self, app):
        """View app details"""
        print("\n" + "="*70)
        print(f"📋 App Details: {app['name']}")
        print("="*70)
        print(f"\n  ID: {app['id']:03d}")
        print(f"  Name: {app['name']}")
        print(f"  Folder: {app['folder']}")
        print(f"  Path: {app['path']}")
        
        if app['description']:
            print(f"\n  Description:")
            print(f"  {app['description']}")
        
        # Check for files
        print(f"\n  Files:")
        files = ['app.py', 'requirements.txt', 'README.md']
        for file in files:
            file_path = app['path'] / file
            status = "✅" if file_path.exists() else "❌"
            print(f"    {status} {file}")
        
        # Read README if exists
        readme_path = app['path'] / "README.md"
        if readme_path.exists():
            print(f"\n  README Preview:")
            with open(readme_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:10]
                for line in lines:
                    print(f"    {line.rstrip()}")
        
        print("\n" + "="*70)
    
    def browse_by_category(self):
        """Browse apps by category"""
        categories = {
            "1": ("Text Analysis & Classification", range(1, 21)),
            "2": ("Information Extraction & NER", range(21, 41)),
            "3": ("Generation & Transformation", range(41, 61)),
            "4": ("Semantic Analysis & Search", range(61, 81)),
            "5": ("Advanced & Domain-Specific", range(81, 101))
        }
        
        print("\n📂 Categories:")
        for key, (name, _) in categories.items():
            print(f"  {key}. {name}")
        
        choice = input("\nSelect category (1-5): ").strip()
        
        if choice in categories:
            cat_name, app_range = categories[choice]
            cat_apps = [app for app in self.apps if app['id'] in app_range]
            
            print(f"\n📂 {cat_name}")
            self.list_apps(cat_apps, show_description=True)
        else:
            print("❌ Invalid category")
    
    def check_requirements(self):
        """Check system requirements"""
        print("\n🔍 Checking System Requirements...\n")
        
        # Check Python version
        python_version = sys.version.split()[0]
        print(f"  Python Version: {python_version}")
        
        # Check installed packages
        packages = [
            'streamlit', 'pandas', 'numpy', 'plotly',
            'nltk', 'spacy', 'transformers', 'scikit-learn'
        ]
        
        print("\n  Key Packages:")
        for package in packages:
            try:
                __import__(package)
                print(f"    ✅ {package}")
            except ImportError:
                print(f"    ❌ {package} (not installed)")
        
        print("\n  System Info:")
        print(f"    OS: {os.name}")
        print(f"    Working Directory: {os.getcwd()}")
        print(f"    Total Apps: {len(self.apps)}")
        
        print("\n" + "="*70)
    
    def run(self):
        """Run the interactive manager"""
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-9): ").strip()
            
            if choice == '1':
                self.list_apps(show_description=True)
                input("\nPress Enter to continue...")
            
            elif choice == '2':
                query = input("\nEnter search query: ").strip()
                results = self.search_apps(query)
                if results:
                    print(f"\n🔍 Found {len(results)} matching apps:")
                    self.list_apps(results, show_description=True)
                else:
                    print("\n❌ No apps found matching your query")
                input("\nPress Enter to continue...")
            
            elif choice == '3':
                app_id = input("\nEnter app ID to launch: ").strip()
                try:
                    app = self.get_app_by_id(int(app_id))
                    if app:
                        self.launch_app(app)
                    else:
                        print(f"❌ App {app_id} not found")
                except ValueError:
                    print("❌ Invalid app ID")
                input("\nPress Enter to continue...")
            
            elif choice == '4':
                app_id = input("\nEnter app ID to install dependencies: ").strip()
                try:
                    app = self.get_app_by_id(int(app_id))
                    if app:
                        self.install_dependencies(app)
                    else:
                        print(f"❌ App {app_id} not found")
                except ValueError:
                    print("❌ Invalid app ID")
                input("\nPress Enter to continue...")
            
            elif choice == '5':
                app_id = input("\nEnter app ID to view details: ").strip()
                try:
                    app = self.get_app_by_id(int(app_id))
                    if app:
                        self.view_details(app)
                    else:
                        print(f"❌ App {app_id} not found")
                except ValueError:
                    print("❌ Invalid app ID")
                input("\nPress Enter to continue...")
            
            elif choice == '6':
                self.browse_by_category()
                input("\nPress Enter to continue...")
            
            elif choice == '7':
                app_id = input("\nEnter app ID for quick launch: ").strip()
                try:
                    app = self.get_app_by_id(int(app_id))
                    if app:
                        self.launch_app(app)
                    else:
                        print(f"❌ App {app_id} not found")
                except ValueError:
                    print("❌ Invalid app ID")
            
            elif choice == '8':
                self.check_requirements()
                input("\nPress Enter to continue...")
            
            elif choice == '9':
                print("\n👋 Thank you for using NLP 100 Apps Manager!")
                print("="*70 + "\n")
                break
            
            else:
                print("\n❌ Invalid choice. Please select 1-9.")
                input("\nPress Enter to continue...")

def main():
    """Main entry point"""
    manager = AppManager()
    
    # Check if command line arguments provided
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'list':
            manager.list_apps(show_description=True)
        
        elif command == 'search' and len(sys.argv) > 2:
            query = ' '.join(sys.argv[2:])
            results = manager.search_apps(query)
            if results:
                manager.list_apps(results, show_description=True)
            else:
                print(f"No apps found matching '{query}'")
        
        elif command == 'launch' and len(sys.argv) > 2:
            try:
                app_id = int(sys.argv[2])
                app = manager.get_app_by_id(app_id)
                if app:
                    manager.launch_app(app)
                else:
                    print(f"App {app_id} not found")
            except ValueError:
                print("Invalid app ID")
        
        elif command == 'install' and len(sys.argv) > 2:
            try:
                app_id = int(sys.argv[2])
                app = manager.get_app_by_id(app_id)
                if app:
                    manager.install_dependencies(app)
                else:
                    print(f"App {app_id} not found")
            except ValueError:
                print("Invalid app ID")
        
        elif command == 'help':
            print("\nNLP 100 Apps Manager - Command Line Usage\n")
            print("  python app_manager.py              - Interactive mode")
            print("  python app_manager.py list         - List all apps")
            print("  python app_manager.py search <query> - Search apps")
            print("  python app_manager.py launch <id>  - Launch app by ID")
            print("  python app_manager.py install <id> - Install dependencies")
            print("  python app_manager.py help         - Show this help\n")
        
        else:
            print("Invalid command. Use 'python app_manager.py help' for usage.")
    
    else:
        # Interactive mode
        manager.run()

if __name__ == "__main__":
    main()
