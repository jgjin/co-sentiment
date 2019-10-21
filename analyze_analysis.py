"""Analyze and plot sentiment analysis."""

from collections import defaultdict
from glob import glob
import json

import matplotlib.pyplot as plt


def main(
):
    """Analyze and plot sentiment analysis."""
    tones_agg = defaultdict(list)
    for analysis_file in glob("Uber/*analysis*"):
        data = json.load(open(analysis_file))
        for sentence in data["sentences_tone"]:
            for tone in sentence["tones"]:
                tone_name = tone["tone_name"]
                tones_agg[tone_name].append(tone["score"])

    tone_name_agg = []
    tone_num_agg = []
    for tone_name, tone_scores in sorted(
            tones_agg.items(),
            key=lambda key_val: len(key_val[1]),
    ):
        tone_name_agg.append(tone_name)
        tone_num_agg.append(len(tone_scores))

    plt.bar(tone_name_agg, tone_num_agg)
    plt.title("4320 Tweets about #Uber Collected by Yo Boi Jason", fontname="Roboto", fontsize=16)
    plt.xlabel("Tone", fontname="Roboto", fontsize=12)
    plt.xticks(fontname="Roboto", fontsize=10)
    plt.ylabel("Number of Sentences", fontname="Roboto", fontsize=12)
    plt.yticks(fontname="Roboto", fontsize=10)

    axes = plt.axes()
    for bar, label in zip(axes.patches, tone_num_agg):
        axes.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 2,
            label,
            ha="center",
            va="bottom",
            fontname="Roboto",
            fontsize=10,
        )

    plt.savefig(f"tone.png", dpi=300)


if __name__ == "__main__":
    main()
