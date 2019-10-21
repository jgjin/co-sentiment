"""Get and analyze tweets about company."""

import itertools
import json
import os
from threading import Thread

from twitter.api import Api

from analyze import get_sentences, analyze_sentences
from auth import get_twitter_credentials
from utils import chunks


def get_twitter_api(
):
    """Convenience function to get Api object."""
    credentials = get_twitter_credentials()
    return Api(
        credentials["consumer_key"],
        credentials["consumer_secret"],
        credentials["access_token"],
        credentials["access_token_secret"],
    )


def get_company_stream(
        company_keywords,
):
    """Get stream filtering on company_keywords."""
    return get_twitter_api().GetStreamFilter(
        track=company_keywords,
        languages=["en"],
    )


def process_tweet(
        tweet,
):
    """Process individual tweet."""
    text = tweet["text"]
    if "extended_tweet" in tweet:
        text = tweet["extended_tweet"]["full_text"]
    return {
        "id": tweet["id"],
        "text": text,
    }


def group_into_full_texts(
        tweets_chunk,
        char_limit=10000,
):
    """Group tweets into full texts of at most char_limit characters."""
    full_texts = []

    full_text = ""
    while tweets_chunk:
        while tweets_chunk and \
              len(full_text) + len(tweets_chunk[-1]["text"]) < char_limit:
            full_text = f"{full_text}{tweets_chunk.pop()['text']}\n"
        full_texts.append(full_text)
        full_text = ""

    return full_texts


def company_thread(
        company_metadata,
        chunk_size=144,
        chunks_limit=144,
):
    """Get chunks of tweets from stream filtering on company_keywords."""
    name = company_metadata["name"]
    os.makedirs(name, exist_ok=True)

    tweets_stream = get_company_stream(company_metadata["keywords"])
    for chunk, chunk_index in zip(
            chunks(tweets_stream, chunk_size),
            range(chunks_limit),
    ):
        tweets_chunk = list(map(
            process_tweet,
            chunk,
        ))

        print(f"Writing chunk {chunk_index}")
        with open(
                f"{name}/data_{chunk_index}.json",
                "w",
                encoding="utf-8",
        ) as output:
            json.dump({
                "tweets": tweets_chunk,
            }, output, ensure_ascii=False)

        print(f"Analyzing chunk {chunk_index}")
        full_texts = group_into_full_texts(tweets_chunk)

        for subchunk_index, sentences_chunk in enumerate(chunks(
                itertools.chain(*list(map(
                    get_sentences,
                    full_texts,
                ))),
                96,
        )):
            with open(
                    f"{name}/analysis_{chunk_index}_{subchunk_index}.json",
                    "w",
                    encoding="utf-8",
            ) as output:
                json.dump(
                    analyze_sentences(sentences_chunk),
                    output,
                    ensure_ascii=False,
                )


def main(
):
    """Get and analyze tweets about company."""
    # threads = []
    for company_name in [
            "Uber",
            # "Lyft",
    ]:
        company_metadata = {
            "name": company_name,
            "keywords": [
                company_name.lower(),
                f"#{company_name.lower()}",
            ],
        }
        company_thread(company_metadata)
        # thread = Thread(
        #     target=company_thread,
        #     args=(company_metadata,),
        # )
        # threads.append(thread)
        # thread.start()

    # for thread in threads:
    #     thread.join()


if __name__ == "__main__":
    main()
