select *
from (
    values
        ('childcare', 'Approved childcare places', 'places'),
        ('youth_welfare', 'Youth welfare places (Hilfen)', 'places'),
        ('hospital', 'Hospital beds (annual average)', 'beds')
) as t(sector_key, sector_description, benchmark_unit)
