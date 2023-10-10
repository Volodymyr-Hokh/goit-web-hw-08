import sys
import redis
from redis_lru import RedisLRU

import connect
from models import Author, Quote

client = redis.Redis(host="localhost", port=6379, password=None, db=0)
cache = RedisLRU(client)


@cache
def find_quotes(command):
    if command.startswith("name:"):
        author_name = command.split("name:")[1].strip()
        author = Author.objects(fullname=author_name).first()
        quotes = Quote.objects(author=author)
    elif command.startswith("tag:"):
        tag_name = command.split("tag:")[1].strip()
        quotes = Quote.objects(tags=tag_name)
    elif command.startswith("tags:"):
        tag_names = command.split("tags:")[1].strip().split(",")
        quotes = Quote.objects(tags__in=tag_names)
    elif command == "exit":
        sys.exit(0)
    else:
        quotes = []

    return list(quotes) 


if __name__ == '__main__':
    while True:
        user_input = input('Enter command: ')
        if user_input == 'exit':
            break

        quotes = find_quotes(user_input)
        
        for quote in quotes:
            author_fullname = quote.author.fullname
            quote_text = quote.quote
            print(author_fullname)
            print(quote_text, end='\n\n')
