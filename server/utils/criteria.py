from enum import Enum

class Criteria(str, Enum):
    DEFAULT = "Default"
    PRICE_ASCENDING = "Price Ascending"
    PRICE_DESCENDING = "Price Descending"
    TITLE_ASCENDING = "Title Ascending"
    TITLE_DESCENDING = "Title Descending"


def getCriteriaSorting(criteria:Criteria):
    if criteria == Criteria.DEFAULT:
        return [("_id", 1)]
    if criteria == Criteria.PRICE_ASCENDING:
        return  [("price", 1)]
    if criteria == Criteria.PRICE_DESCENDING:
        return  [("price", -1)]
    if criteria == Criteria.TITLE_ASCENDING:
        return [("title", 1)]
    if criteria == Criteria.TITLE_DESCENDING:
        return [("title", -1)]