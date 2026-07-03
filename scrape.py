import feedparser
import re


def parse(username: str, page: int, amount_per_page: int):
    start = (page - 1) * amount_per_page
    end = start + amount_per_page

    feed = feedparser.parse(f"https://letterboxd.com/{username}/rss/")

    entry = feed.entries[start:end]

    clean_entry = []
    for e in entry:
        summary = re.sub(r"<.*?>", "", e.summary).strip()  # type: ignore
        clean_entry.append(
            {
                "link": e.get("link"),
                "watched_date": e.get("letterboxd_watcheddate"),
                "film_title": e.get("letterboxd_filmtitle"),
                "film_year": e.get("letterboxd_filmyear"),
                "member_rating": e.get("letterboxd_memberrating"),
                "member_like": True if e.get("letterboxd_watcheddate") == "Yes" else False,
                "member_rewatch": True if e.get("letterboxd_rewatch") == "Yes" else False,
                "tmbd_movieid": e.get("tmdb_movieid"),
                "review": summary,
            }
        )

    return clean_entry

