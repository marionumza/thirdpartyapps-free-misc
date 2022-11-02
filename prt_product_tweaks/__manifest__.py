{
    "name": "Product Tweaks. Multiple Internal Reference Product Code SKU",
    "version": "15.0.1.0.1",
    "author": "Cetmix",
    "category": "Stock",
    "license": "GPL-3",
    "website": "https://cetmix.com",
    "live_test_url": "https://demo.cetmix.com",
    "summary": """Multiple internal references for products """,
    "description": """
    Multiple Internal References SKU Product Codes
""",
    "depends": ["product", "stock"],
    "images": ["static/description/banner.png"],
    "demo": ["data/demo.xml"],
    "data": [
        "security/ir.model.access.csv",
        "views/product.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
