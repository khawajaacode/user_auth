from app.models.feed import Feed


MOCK_FEEDS = [
    {
        "title": "Workout of the Day (WOD)",
        "description": "Quick sets or circuits showing daily workout routines. Regular workouts strengthen your heart, muscles, and bones. It reduces the risk of chronic diseases like heart disease, diabetes, and high blood pressure.",
        "category": "Fitness",
        "image_url": "https://via.placeholder.com/400x300"
    },
    {
        "title": "Trainer Tips",
        "description": "Short videos from personal trainers giving workout or nutrition advice. Learn the best techniques to maximize your gym sessions and avoid common mistakes.",
        "category": "Gym",
        "image_url": "https://via.placeholder.com/400x300"
    },
    {
        "title": "Healthy and nutritious food",
        "description": "Before and after photos with short testimonials. Eating healthy food helps fuel your workouts and supports muscle recovery.",
        "category": "Nutrition",
        "image_url": "https://via.placeholder.com/400x300"
    },
    {
        "title": "5 advantages of gym exercise",
        "description": "Regular workouts strengthen your heart, muscles, and bones. It reduces the risk of chronic diseases like heart disease, diabetes, and high blood pressure. Exercise releases endorphins which are natural mood boosters. It helps reduce stress, anxiety, and symptoms of depression, while improving sleep and self-esteem.",
        "category": "Gym",
        "image_url": "https://via.placeholder.com/400x300"
    },
    {
        "title": "Benefits of yoga with a partner",
        "description": "Yoga with a partner builds trust, improves flexibility, and deepens your practice. Partner yoga also improves communication and connection between people.",
        "category": "Health",
        "image_url": "https://via.placeholder.com/400x300"
    },
    {
        "title": "Best foods for muscle gain",
        "description": "Protein-rich foods like eggs, chicken, and legumes are essential for muscle growth. Combined with proper training, nutrition plays a key role in achieving your fitness goals.",
        "category": "Nutrition",
        "image_url": "https://via.placeholder.com/400x300"
    }
]


async def seed_feeds():
    count = await Feed.count()
    if count == 0:
        for data in MOCK_FEEDS:
            feed = Feed(**data)
            await feed.insert()
        print("✅ Feed data seeded successfully")
    else:
        print("ℹ️ Feed data already exists, skipping seed")