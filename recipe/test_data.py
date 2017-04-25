from recipe import models
from decimal import Decimal
r = models.Recipe(title='Tacos', description="Tacos muy ricos", cost=Decimal('100.00'), images={}, ingredients={}, steps={}, portions=8)
r.save()

