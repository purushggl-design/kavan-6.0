import os
import sys
import django
import time

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.config.settings')
django.setup()

from backend.apps.tenants.models.tenant import Tenant

def benchmark_tenants(counts=[100, 500, 1000, 5000]):
    print("Starting Tenant Creation Benchmark...")
    for count in counts:
        start_time = time.time()
        tenants = []
        for i in range(count):
            tenants.append(Tenant(name=f"Benchmark {i}", subdomain=f"bench-{count}-{i}"))
        
        Tenant.objects.bulk_create(tenants)
        end_time = time.time()
        print(f"Created {count} tenants in {end_time - start_time:.4f} seconds.")

        # Benchmark query
        start_time = time.time()
        list(Tenant.objects.filter(name__startswith="Benchmark"))
        end_time = time.time()
        print(f"Queried {count} tenants in {end_time - start_time:.4f} seconds.")
        
        Tenant.objects.all().delete()
        print("-" * 40)

if __name__ == "__main__":
    benchmark_tenants()
