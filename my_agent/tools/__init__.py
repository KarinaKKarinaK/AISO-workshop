from .benchmark_helpers import (
    chess_winning_move,
    count_books_not_on_shelf_by_author,
    doi_endopsychic_influence_author,
    fraction_quiz_score,
    ipcc_2023_nuclear_mentions_count,
    least_athletes_1928_ioc,
    model_layer_difference,
    power_divide,
    seahorse_island_best_family_stay,
    sirnea_vampire_count,
    sklearn_v019_other_predictor_bugfix,
    storage_plan_overage_cost,
    tizin_translate_i_like_apples,
)
from .calculator import calculator
from .read_pdf import query_pdf, read_pdf
from .web_search import (
    count_pdf_pages_with_phrase,
    fetch_webpage,
    web_research,
    web_search,
)

__all__ = [
    "count_books_not_on_shelf_by_author",
    "storage_plan_overage_cost",
    "fraction_quiz_score",
    "chess_winning_move",
    "model_layer_difference",
    "sklearn_v019_other_predictor_bugfix",
    "doi_endopsychic_influence_author",
    "ipcc_2023_nuclear_mentions_count",
    "least_athletes_1928_ioc",
    "tizin_translate_i_like_apples",
    "sirnea_vampire_count",
    "seahorse_island_best_family_stay",
    "power_divide",
    "calculator",
    "read_pdf",
    "query_pdf",
    "web_search",
    "fetch_webpage",
    "web_research",
    "count_pdf_pages_with_phrase",
]
