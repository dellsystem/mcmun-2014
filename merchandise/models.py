from django.db import models


class PriceField(models.DecimalField):
    description = 'Exactly what it says on the tin'

    def __init__(self, *args, **kwargs):
        kwargs['decimal_places'] = 2
        kwargs['max_digits'] = 5
        models.DecimalField.__init__(self, *args, **kwargs)


class Item(models.Model):
    name = models.CharField(max_length=50)
    online_price = PriceField()
    retail_price = PriceField()
    description = models.TextField()
    slug = models.SlugField()
    is_limited = models.BooleanField()

    def __unicode__(self):
        return self.name


class Bundle(models.Model):
    """A collection of items."""
    name = models.CharField(max_length=50)
    online_price = PriceField()
    retail_price = PriceField()
    description = models.TextField()
    slug = models.SlugField()
    items = models.ManyToManyField(Item)

    def __unicode__(self):
        return self.name

    def get_amount_saved(self):
        """I could have just made this a field whose value must be input by the
        user, but where's the fun in that?"""
        expected_price = sum(item.online_price for item in self.items.all())
        return expected_price - self.online_price
