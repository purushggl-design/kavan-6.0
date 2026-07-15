import os
import ast
import json
import glob

APPS_DIR = os.path.join("backend", "apps")
CONFIG_URLS = os.path.join("backend", "config", "urls.py")
TESTS_DIR = os.path.join("backend", "tests", "apps")

def get_models(app_path):
    models_file = os.path.join(app_path, "models.py")
    models_dir = os.path.join(app_path, "models")
    
    models = []
    
    def parse_file(fpath):
        if not os.path.exists(fpath):
            return
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        try:
            tree = ast.parse(content)
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    # Check if it inherits from Model
                    bases = [b.id for b in node.bases if isinstance(b, ast.Name)] + \
                            [b.attr for b in node.bases if isinstance(b, ast.Attribute)]
                    if any("Model" in b for b in bases):
                        fields = [n.targets[0].id for n in node.body if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', None)]
                        models.append({"name": node.name, "fields": fields[:3]})
        except Exception as e:
            pass
            
    if os.path.exists(models_file):
        parse_file(models_file)
    elif os.path.exists(models_dir):
        for f in glob.glob(os.path.join(models_dir, "*.py")):
            parse_file(f)
            
    return models

def check_file_substance(fpath):
    if not os.path.exists(fpath): return False
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    if len(content.strip()) < 20 or "pass" in content and "def " not in content:
        return False
    # Very rudimentary substance check: has logic lines
    return len(content.split('\n')) > 10

def check_dir_substance(dpath):
    if not os.path.exists(dpath): return False
    files = glob.glob(os.path.join(dpath, "**", "*.py"), recursive=True)
    for f in files:
        if "__init__" not in f and check_file_substance(f):
            return True
    return False

def check_tests(app_name):
    tpath = os.path.join(TESTS_DIR, f"test_{app_name}")
    tpath2 = os.path.join(TESTS_DIR, app_name)
    if os.path.exists(tpath):
        return True
    if os.path.exists(tpath2) and len(glob.glob(os.path.join(tpath2, "**", "*.py"), recursive=True)) > 0:
        return True
    return False

def get_wired_urls():
    if not os.path.exists(CONFIG_URLS): return []
    wired = []
    with open(CONFIG_URLS, "r", encoding="utf-8") as f:
        content = f.read()
        for line in content.split('\n'):
            if "path(" in line and "include(" in line:
                for app in os.listdir(APPS_DIR):
                    if f"apps.{app}.urls" in line:
                        wired.append(app)
    return wired

wired_urls = get_wired_urls()

results = {}
if os.path.exists(APPS_DIR):
    for app in os.listdir(APPS_DIR):
        app_path = os.path.join(APPS_DIR, app)
        if not os.path.isdir(app_path) or app == "__pycache__": continue
        
        models = get_models(app_path)
        
        api_exists = check_dir_substance(os.path.join(app_path, "api")) or check_dir_substance(os.path.join(app_path, "views")) or check_file_substance(os.path.join(app_path, "views.py"))
        serializers_exists = check_dir_substance(os.path.join(app_path, "serializers")) or check_file_substance(os.path.join(app_path, "serializers.py"))
        urls_exists = check_file_substance(os.path.join(app_path, "urls.py"))
        is_wired = app in wired_urls
        
        repos_exists = check_dir_substance(os.path.join(app_path, "repositories")) or check_file_substance(os.path.join(app_path, "repositories.py"))
        services_exists = check_dir_substance(os.path.join(app_path, "services")) or check_file_substance(os.path.join(app_path, "services.py"))
        signals_exists = check_file_substance(os.path.join(app_path, "signals.py"))
        tasks_exists = check_file_substance(os.path.join(app_path, "tasks.py"))
        
        has_tests = check_tests(app)
        
        status = "EMPTY"
        missing = []
        if models:
            if not api_exists and not serializers_exists and not urls_exists:
                status = "STUB"
                missing = ["API (serializers, views, urls)"]
            elif api_exists and serializers_exists and urls_exists and is_wired:
                if not repos_exists or not services_exists or not has_tests:
                    status = "PARTIAL"
                    if not repos_exists: missing.append("Repositories")
                    if not services_exists: missing.append("Services")
                    if not has_tests: missing.append("Tests")
                else:
                    status = "COMPLETE"
            else:
                status = "PARTIAL"
                if not api_exists: missing.append("Views/API")
                if not serializers_exists: missing.append("Serializers")
                if not urls_exists: missing.append("urls.py")
                if not is_wired: missing.append("URL wiring")
                
        results[app] = {
            "models": models,
            "api_exists": api_exists,
            "serializers_exists": serializers_exists,
            "urls_exists": urls_exists,
            "is_wired": is_wired,
            "repos_exists": repos_exists,
            "services_exists": services_exists,
            "signals_exists": signals_exists,
            "tasks_exists": tasks_exists,
            "has_tests": has_tests,
            "status": status,
            "missing": missing
        }

with open("apps_audit.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
