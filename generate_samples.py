#!/usr/bin/env python3
"""
Sample Data Generator Script
Creates sample JSON data for testing your API
"""

import json
from datetime import datetime

def create_sample_data():
    """Create sample product data"""
    
    sample_products = [
        {
            "name": "Premium Coffee Beans",
            "hs_code": "0901.11.00",
            "quantity": "1000",
            "unit": "kg",
            "fcl_type": "20ft",
            "packaging": "Vacuum sealed bags",
            "quantity_per_fcl": "20000",
            "description": [
                "Premium Arabica coffee beans sourced from Colombia",
                "Medium roast with rich flavor profile",
                "Perfect for espresso and filter coffee",
                "Certified organic and fair trade"
            ],
            "specifications": [
                "Origin: Colombia",
                "Roast Level: Medium",
                "Bean Size: Screen 17-18",
                "Moisture Content: <12%",
                "Packaging: Vacuum sealed",
                "Shelf Life: 24 months"
            ],
            "images": [
                {"path": "coffee1.jpg", "w": 200, "h": 150},
                {"path": "coffee2.jpg", "w": 200, "h": 150}
            ],
            "client_name": "Coffee Importers Ltd",
            "rate": "$15.50 per kg",
            "expiry_date": "2025-12-31",
            "company": {
                "name": "Premium Coffee Co",
                "website": "https://premiumcoffee.com",
                "address": "123 Coffee Street, Bean City, BC 12345",
                "phone": "+1-555-0123",
                "email": "info@premiumcoffee.com"
            }
        },
        {
            "name": "Organic Tea Leaves",
            "hs_code": "0902.30.00",
            "quantity": "500",
            "unit": "kg",
            "fcl_type": "20ft",
            "packaging": "Paper bags",
            "quantity_per_fcl": "10000",
            "description": [
                "High-quality organic green tea leaves",
                "Hand-picked from mountain gardens",
                "Rich in antioxidants and natural flavor",
                "Perfect for daily consumption"
            ],
            "specifications": [
                "Origin: Darjeeling, India",
                "Type: Green Tea",
                "Grade: Premium",
                "Caffeine Content: Low",
                "Packaging: Eco-friendly",
                "Shelf Life: 18 months"
            ],
            "images": [
                {"path": "tea1.jpg", "w": 200, "h": 150}
            ],
            "client_name": "Tea Distributors Inc",
            "rate": "$8.75 per kg",
            "expiry_date": "2025-06-30",
            "company": {
                "name": "Mountain Tea Co",
                "website": "https://mountaintea.com",
                "address": "456 Tea Garden Road, Darjeeling, India",
                "phone": "+91-9876543210",
                "email": "sales@mountaintea.com"
            }
        },
        {
            "name": "Spices Mix",
            "hs_code": "0910.99.00",
            "quantity": "200",
            "unit": "kg",
            "fcl_type": "20ft",
            "packaging": "Plastic containers",
            "quantity_per_fcl": "4000",
            "description": [
                "Premium blend of Indian spices",
                "Authentic taste and aroma",
                "Perfect for Indian cuisine",
                "No artificial preservatives"
            ],
            "specifications": [
                "Origin: India",
                "Mix: Turmeric, Cumin, Coriander, Cardamom",
                "Processing: Sun-dried",
                "Color: Natural",
                "Packaging: Food-grade plastic",
                "Shelf Life: 12 months"
            ],
            "images": [
                {"path": "spices1.jpg", "w": 200, "h": 150},
                {"path": "spices2.jpg", "w": 200, "h": 150}
            ],
            "client_name": "Spice Traders LLC",
            "rate": "$12.00 per kg",
            "expiry_date": "2024-12-31",
            "company": {
                "name": "Indian Spice Co",
                "website": "https://indianspice.com",
                "address": "789 Spice Market, Mumbai, India",
                "phone": "+91-9876543211",
                "email": "export@indianspice.com"
            }
        }
    ]
    
    return sample_products

def save_sample_data():
    """Save sample data to JSON files"""
    products = create_sample_data()
    
    for i, product in enumerate(products, 1):
        filename = f"sample_product_{i}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(product, f, indent=2, ensure_ascii=False)
        print(f"✅ Created: {filename}")
    
    # Create a combined file
    with open("all_sample_products.json", 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    print("✅ Created: all_sample_products.json")
    
    # Create minimal test data
    minimal_data = {
        "name": "Test Product",
        "description": ["Simple test product"],
        "specifications": ["Basic specification"],
        "company": {
            "name": "Test Company",
            "website": "https://test.com"
        }
    }
    
    with open("minimal_test.json", 'w', encoding='utf-8') as f:
        json.dump(minimal_data, f, indent=2, ensure_ascii=False)
    print("✅ Created: minimal_test.json")

if __name__ == "__main__":
    print("📄 Sample Data Generator")
    print("=" * 40)
    print("Creating sample JSON files for API testing...")
    
    save_sample_data()
    
    print("\n" + "=" * 40)
    print("Sample files created:")
    print("- sample_product_1.json (Coffee)")
    print("- sample_product_2.json (Tea)")
    print("- sample_product_3.json (Spices)")
    print("- all_sample_products.json (All products)")
    print("- minimal_test.json (Simple test data)")
    print("\nUse these files to test your API endpoints!")
