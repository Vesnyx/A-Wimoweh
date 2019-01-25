# Shawn Schwartz

import trakt
from trakt.sync import search, search_by_id
from trakt.tv import TVShow

#PyTrakt validate search query
def invalid_search():
	functions = [search, search_by_id]
	for fn in functions:
		with pytest.raises(ValueError):
			fn('shouldfail', 'fake')

def search_show_by_id(id):
	result = search_by_id(id, id_type='imdb')
	return result
