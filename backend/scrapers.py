from botasaurus_server.server import Server
from botasaurus_server.sorts import NumericAscendingSort
from src.tickets import list_locations, get_tickets

Server.add_scraper(
    list_locations,
    sorts=[NumericAscendingSort("1")]
)

Server.add_scraper(
    get_tickets,
    sorts=[NumericAscendingSort("2")]
)
