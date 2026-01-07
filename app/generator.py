import json
import os
import time
import random
from datetime import datetime
from faker import Faker

fake = Faker()
INPUT_PATH = "data/input"

if not os.path.exists(INPUT_PATH):
    os.makedirs(INPUT_PATH)

print("🚀 Iniciando geração de logs de cliques...")

while True:
    data = {
        "user_id": random.randint(1000, 9999),
        "event_type": random.choice(["click", "view", "scroll", "purchase"]),
        "page_id": random.choice(["home", "products", "cart", "checkout"]),
        "timestamp": datetime.now().isoformat(),
        "ip_address": fake.ipv4()
    }
    
    file_name = f"event_{int(time.time() * 1000)}.json"
    with open(os.path.join(INPUT_PATH, file_name), 'w') as f:
        json.dump(data, f)
    
    print(f"✅ Evento gerado: {data['event_type']} em {data['page_id']}")
    time.sleep(random.uniform(0.5, 2.0)) # Simula tráfego irregular
