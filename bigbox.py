import string

import requests


class Box:
    def __init__(self,
                 slug: str = "",
                 name: str = "",
                 rating: str = "",
                 description: str = "",
                 participants: str = "",
                 price: str = "",
                 product_image_url: str = "",
                 product_url: str = ""):
        self.slug = slug
        self.name = name
        self.rating = rating
        self.description = description
        self.participants = participants
        self.price = price
        self.product_image_url = product_image_url
        self.product_url = product_url

def fetch_activity(slug: string) -> Box:
    query = """
    query Activity($slug: String!) {
      activity(slug: $slug) {
        id
        name
        rating
        description
        short_description
        price
        participants
        product_image_url
        product_url
        __typename
      }
    }
    """
    variables = {
        "slug": slug
    }

    payload = {
        "query": query,
        "variables": variables
    }

    graphql_url = "https://www.qa-e.bigbox.com.ar/graphql"
    url = f"{graphql_url}/?operationName=Activity"

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    activity = data.get('data').get('activity')
    box = Box(slug=activity.get('slug'),
        name=activity.get('name'),
        rating=activity.get('rating', "5"),
        description=activity.get('description'),
        participants=activity.get('participants'),
        price=activity.get('price'),
        product_image_url=activity.get('product_image_url'),
        product_url=activity.get('product_url'))

    return box

def fetch_box(slug: string) -> Box:
    query = """
    query Box($box_slug: String) {
      box(box_slug: $box_slug) {
        id
        name
        category {
          id
          color
          image_cover
          name
          keywords
          __typename
        }
        slug
        rating
        description
        expiration_date
        discount
        participants
        price
        available
        product_image_url
        product_url
        digital_images {
          image
          __typename
        }
        physical_images {
          image
          __typename
        }
        __typename
      }
    }
    """
    variables = {
        "box_slug": slug
    }

    payload = {
        "query": query,
        "variables": variables
    }

    graphql_url = "https://www.qa-e.bigbox.com.ar/graphql"
    url = f"{graphql_url}/?operationName=Box"

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    box = Box(slug=data.get('data').get('box').get('slug'),
        name=data.get('data').get('box').get('name'),
        rating=data.get('data').get('box').get('rating'),
        description=data.get('data').get('box').get('description'),
        participants=data.get('data').get('box').get('participants'),
        price=data.get('data').get('box').get('price'),
        product_image_url=data.get('data').get('box').get('product_image_url'),
        product_url=data.get('data').get('box').get('product_url'))

    return box
