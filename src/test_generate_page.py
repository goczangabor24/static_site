import unittest
import generate_page

class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        matches = generate_page.extract_title(
            """
# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien

## Blog posts

- [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
- [Why Tom Bombadil Was a Mistake](/blog/tom)
- [The Unparalleled Majesty of "The Lord of the Rings"](/blog/majesty)
"""
        )
        self.assertEqual(
            "Tolkien Fan Club", matches
        )