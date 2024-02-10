from elasticsearch_dsl import (
    Document,
    SearchAsYouType,
    analyzer,
    token_filter,
    Text,
)

# custom analyzer for names
ascii_fold = analyzer(
    "ascii_fold",
    # we don't want to split O'Brian or Toulouse-Lautrec
    tokenizer="whitespace",
    filter=["lowercase", token_filter("ascii_fold", "asciifolding")],
)
ascii_fold_1 = analyzer(
    "ascii_fold",
    tokenizer="whitespace",
    filter=["lowercase", "asciifolding"],
)

class Person(Document):
    name = SearchAsYouType(max_shingle_size=3)
    # author = SearchAsYouType(max_shingle_size=3)

    class Index:
        name = "test-search-as-you-type"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}


class CompositionElastic(Document):
    name = SearchAsYouType(max_shingle_size=3, analyzer=ascii_fold_1)
    author = SearchAsYouType(max_shingle_size=3)
    genre = SearchAsYouType(max_shingle_size=3)
    description = SearchAsYouType(max_shingle_size=3)
    
    class Index:
        name = "composition"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}
        