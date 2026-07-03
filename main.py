from pyboxen import boxen
from fastapi import FastAPI, HTTPException
from scrape import parse
from fastapi.responses import PlainTextResponse

app = FastAPI()

def star_maker(rating):
    rating = float(rating)
    star = "★"
    half = "½"

    if not rating.is_integer():
        rating -= 0.5

        result = star * int(rating)
        return f"{result}{half}"
    else:
        result = star * int(rating)
        return result

@app.get("/{username}")
def fetch(username: str, page: int = 1, amount_per_page: int = 5):
    try:
        activities = parse(username, page, amount_per_page)
    except KeyError:
        raise HTTPException(status_code=500, detail="something bad might happen :(")

    for activity in activities:
        (
            link,
            watched_date,
            film_title,
            film_year,
            member_rating,
            member_like,
            member_rewatch,
            tmdb_movieid,
            review,
        ) = activity.values()
        return PlainTextResponse(
            boxen(
                f"{review}",
                title=f"{film_title} - [yellow bold]{star_maker(member_rating)}[/] {"[red bold]:heart:[/]" if member_like else ""}",
                # subtitle="Cool subtitle goes here",
                # subtitle_alignment="center",
                color="#eeeeee",
                padding=1,
            )
        )
