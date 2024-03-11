from typing import Dict, Optional, Callable
from recipe_scrapers import scrape_me

def safe_access(callable_attr: Callable[[], str]) -> Optional[str]:
    try:
        return callable_attr()
    except Exception:
        return None

def scrape_recipe(url: str) -> Dict[str, Optional[str]]:
    try:
        scraper = scrape_me(url)
        return {
            "title": safe_access(scraper.title),
            "author": safe_access(scraper.author),
            "prep_time": safe_access(scraper.prep_time),
            "cook_time": safe_access(scraper.cook_time),
            "total_time": safe_access(scraper.total_time),
            "yields": safe_access(scraper.yields),
            "ingredients": safe_access(scraper.ingredients),
            "instructions": safe_access(lambda: scraper.instructions().split('\n')),
            "equipment": safe_access(scraper.equipment) if hasattr(scraper, 'equipment') else None,
            "image": safe_access(scraper.image),
            "description": safe_access(scraper.description),
            "canonical_url": safe_access(scraper.canonical_url),
            "category": safe_access(scraper.category),
            "site_name": safe_access(scraper.site_name)
        }
    except Exception as e:
        return {"error": str(e)}

KEY_ALIASES = {
    "name": "title",
    "author": "source",
    "total_time": "duration",
    "yields": "servings",
    "ingredients": "ingredients",
    "directions": "instructions",
    "equipment": "equipment",
    "image": "picture"
}
