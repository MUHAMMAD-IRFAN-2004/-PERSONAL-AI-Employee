import os

base_path = r"D:\PIAIC AI\-PERSONAL-AI-Employee\.agents\skills"

dirs_to_create = [
    "whatsapp-monitor",
    "approval-workflow",
    "social-media-poster"
]

for dir_name in dirs_to_create:
    full_path = os.path.join(base_path, dir_name)
    os.makedirs(full_path, exist_ok=True)
    print(f"✓ Created: {dir_name}")

print("\n✅ All skill directories created successfully!")

# List created directories
print("\nCreated skills:")
for item in os.listdir(base_path):
    item_path = os.path.join(base_path, item)
    if os.path.isdir(item_path):
        print(f"  - {item}")
