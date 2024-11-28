from typing import List

import bigbox
from bigbox import Box
from catalog import Catalog, Item
from recommendation import RecommendationService, UserData


def main():
    # print("Cargando el Catalogo")
    # catalog = Catalog()
    # catalog.load_catalog()
    #
    # recommended_items: List[Box] = RecommendationService(catalog).recommend(UserData("18-30", "10.000-15.000", "Noviazgo", "Aventura", "Aniversario"))
    # print(recommended_items)
    # https://www.bigbox.com.ar/experiencias/casa-nera-xp-suelta/
    box = bigbox.fetch_activity("casa-nera-xp-suelta")

if __name__ == '__main__':
    main()
