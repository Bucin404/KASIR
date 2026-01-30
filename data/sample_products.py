# Sample product data
FOOD_MENU = [
    # Makanan
    {
        "id": 1, 
        "name": "Nasi Goreng Spesial", 
        "price": 25000, 
        "category": "Makanan", 
        "image": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=300&h=200&fit=crop&auto=format",
        "description": "Nasi goreng dengan telur, ayam, dan sayuran segar",
        "popular": True
    },
    {
        "id": 2, 
        "name": "Mie Ayam Bakso", 
        "price": 20000, 
        "category": "Makanan", 
        "image": "https://images.unsplash.com/photo-1612874742237-6526221588e3?w=300&h=200&fit=crop&auto=format",
        "description": "Mie ayam dengan bakso sapi pilihan",
        "popular": True
    },
    {
        "id": 3, 
        "name": "Ayam Goreng Crispy", 
        "price": 18000, 
        "category": "Makanan", 
        "image": "https://images.unsplash.com/photo-1626645738196-c2a7c87a8f58?w=300&h=200&fit=crop&auto=format",
        "description": "Ayam goreng crispy dengan bumbu rempah",
        "popular": False
    },
    {
        "id": 4, 
        "name": "Sate Ayam (10 tusuk)", 
        "price": 22000, 
        "category": "Makanan", 
        "image": "https://images.unsplash.com/photo-1594041680534-e8c8cdebd659?w=300&h=200&fit=crop&auto=format",
        "description": "Sate ayam dengan bumbu kacang spesial",
        "popular": True
    },
    {
        "id": 5, 
        "name": "Nasi Campur Komplit", 
        "price": 22000, 
        "category": "Makanan", 
        "image": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=300&h=200&fit=crop&auto=format",
        "description": "Nasi dengan lauk lengkap dan sayuran",
        "popular": False
    },
    {
        "id": 6, 
        "name": "Rendang Daging Sapi", 
        "price": 30000, 
        "category": "Makanan", 
        "image": "https://images.unsplash.com/photo-1555939614-8674f6df1389?w=300&h=200&fit=crop&auto=format",
        "description": "Rendang daging sapi dengan bumbu rempah pilihan",
        "popular": True
    },
    {
        "id": 7, 
        "name": "Soto Ayam Lamongan", 
        "price": 22000, 
        "category": "Makanan", 
        "image": "https://images.unsplash.com/photo-1553909489-cd47e0907980?w=300&h=200&fit=crop&auto=format",
        "description": "Soto ayam dengan bumbu koya dan sambal",
        "popular": True
    },
    {
        "id": 8, 
        "name": "Gado-gado", 
        "price": 18000, 
        "category": "Makanan", 
        "image": "https://images.unsplash.com/photo-1559054663-e8d23213f55c?w=300&h=200&fit=crop&auto=format",
        "description": "Sayuran segar dengan bumbu kacang khas",
        "popular": False
    },
    # Minuman
    {
        "id": 9, 
        "name": "Es Teh Manis", 
        "price": 5000, 
        "category": "Minuman", 
        "image": "https://images.unsplash.com/photo-1597481499753-6e63aca6d3f3?w=300&h=200&fit=crop&auto=format",
        "description": "Es teh manis dengan gula aren",
        "popular": True
    },
    {
        "id": 10, 
        "name": "Jus Alpukat", 
        "price": 15000, 
        "category": "Minuman", 
        "image": "https://images.unsplash.com/photo-1623063878630-7c10b5f6d0c9?w=300&h=200&fit=crop&auto=format",
        "description": "Jus alpukat segar dengan susu kental",
        "popular": True
    },
    {
        "id": 11, 
        "name": "Kopi Latte", 
        "price": 18000, 
        "category": "Minuman", 
        "image": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=300&h=200&fit=crop&auto=format",
        "description": "Kopi latte dengan susu segar",
        "popular": True
    },
    {
        "id": 12, 
        "name": "Air Mineral", 
        "price": 4000, 
        "category": "Minuman", 
        "image": "https://images.unsplash.com/photo-1523362628745-0c100150b504?w=300&h=200&fit=crop&auto=format",
        "description": "Air mineral botolan 600ml",
        "popular": False
    },
    {
        "id": 13, 
        "name": "Es Jeruk Segar", 
        "price": 8000, 
        "category": "Minuman", 
        "image": "https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?w=300&h=200&fit=crop&auto=format",
        "description": "Es jeruk peras tanpa biji",
        "popular": True
    },
    {
        "id": 14, 
        "name": "Milkshake Coklat", 
        "price": 20000, 
        "category": "Minuman", 
        "image": "https://images.unsplash.com/photo-1579954115545-a95591f28bfc?w=300&h=200&fit=crop&auto=format",
        "description": "Milkshake coklat dengan topping whipped cream",
        "popular": True
    },
    {
        "id": 15, 
        "name": "Matcha Latte", 
        "price": 22000, 
        "category": "Minuman", 
        "image": "https://images.unsplash.com/photo-1561047029-3000c68339ca?w=300&h=200&fit=crop&auto=format",
        "description": "Matcha latte dengan susu oat",
        "popular": False
    },
    {
        "id": 16, 
        "name": "Boba Milk Tea", 
        "price": 18000, 
        "category": "Minuman", 
        "image": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=300&h=200&fit=crop&auto=format",
        "description": "Milk tea dengan bubble boba",
        "popular": True
    },
    # Dessert
    {
        "id": 17, 
        "name": "Brownies Coklat", 
        "price": 12000, 
        "category": "Dessert", 
        "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=300&h=200&fit=crop&auto=format",
        "description": "Brownies coklat premium dengan kacang",
        "popular": True
    },
    {
        "id": 18, 
        "name": "Pisang Goreng", 
        "price": 8000, 
        "category": "Dessert", 
        "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=300&h=200&fit=crop&auto=format",
        "description": "Pisang goreng dengan keju parut",
        "popular": False
    },
    {
        "id": 19, 
        "name": "Donat Gula", 
        "price": 7000, 
        "category": "Dessert", 
        "image": "https://images.unsplash.com/photo-1551106652-a5bcf4b29ab6?w=300&h=200&fit=crop&auto=format",
        "description": "Donat lembut dengan taburan gula",
        "popular": True
    },
    {
        "id": 20, 
        "name": "Puding Coklat", 
        "price": 10000, 
        "category": "Dessert", 
        "image": "https://images.unsplash.com/photo-1623334044303-241021148842?w=300&h=200&fit=crop&auto=format",
        "description": "Puding coklat dengan saus karamel",
        "popular": False
    },
    {
        "id": 21, 
        "name": "Es Krim Vanilla", 
        "price": 15000, 
        "category": "Dessert", 
        "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=300&h=200&fit=crop&auto=format",
        "description": "Es krim vanilla dengan topping coklat",
        "popular": True
    },
    {
        "id": 22, 
        "name": "Cheesecake Berry", 
        "price": 25000, 
        "category": "Dessert", 
        "image": "https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?w=300&h=200&fit=crop&auto=format",
        "description": "Cheesecake dengan saus berry segar",
        "popular": True
    },
    {
        "id": 23, 
        "name": "Tiramisu", 
        "price": 22000, 
        "category": "Dessert", 
        "image": "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=300&h=200&fit=crop&auto=format",
        "description": "Tiramisu klasik Italia",
        "popular": True
    },
    {
        "id": 24, 
        "name": "Waffle Madu", 
        "price": 18000, 
        "category": "Dessert", 
        "image": "https://images.unsplash.com/photo-1562376552-0d160a2f238d?w=300&h=200&fit=crop&auto=format",
        "description": "Waffle renyah dengan madu dan buah",
        "popular": False
    },
]
