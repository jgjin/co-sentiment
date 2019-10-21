"""Pick most extreme example of each tone."""

from collections import defaultdict
from glob import glob
import json

import matplotlib.pyplot as plt


def main(
):
    """Pick most extreme example of each tone."""
    tones_agg = defaultdict(list)
    for analysis_file in glob("Uber/*analysis*"):
        data = json.load(open(analysis_file))
        for sentence in data["sentences_tone"]:
            for tone in sentence["tones"]:
                tone_name = tone["tone_name"]
                tones_agg[tone_name].append((tone["score"], sentence["text"]))

    for tone_name, tone_scores in tones_agg.items():
        print(tone_name)
        print(max(tone_scores))


if __name__ == "__main__":
    main()
