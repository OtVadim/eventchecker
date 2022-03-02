from app import db
from app.models import Events, Place, EventImage
import requests
from datetime import datetime, date


def get_events(page, page_size):
  url = 'https://kudago.com/public-api/v1.4/events/'
  params = {
    'lang': 'ru',
    'location': 'msk',
    'page': page,
    'page_size': page_size,
    'fields': 'id,publication_date,title,place,slug,description,categories,tags,age_restriction,price,is_free,dates,location,images',
    'expand': 'dates,place',
    'text_format': 'html',
    'order_by': 'rank,id,publication_date,title',
    'actual_since': date.today(),
    'categories': 'concert,entertainment,party',
  }
  response = requests.get(url, params=params)
  data = response.json()
  if response.status_code == 200:
    return data['results']
  else:
    return None


def update_db():
    events_info = get_events(2, 100)
    for event_info in events_info: 
        location = event_info['location']['slug']
        if location == 'online':
            continue
        place_info = event_info['place']
        try:    
            slug_place = place_info['slug']
        except:
            slug_place = None
        slug_event = event_info['slug']
        place_db = Place.query.filter_by(slug = slug_place).first()
        event_db = Events.query.filter_by(slug = slug_event).first()
        if slug_place is None:
            place_id = None
        elif place_db is None:
            update_place = Place(
                title=place_info['title'],
                slug=place_info['slug'],
                address=place_info['address'],
                phone=place_info['phone'],
                latitude=place_info['coords']['lat'],
                longitude=place_info['coords']['lon'],
                )
            db.session.add(update_place)
            db.session.commit()
            place_id = update_place.id
        elif slug_place == place_db.slug:
            place_id = place_db.id
            print(place_db.slug)
        else:
            print('ERROR')

        if event_db is None:
            ts=int(event_info['publication_date'])
            publication_date=datetime.utcfromtimestamp(ts)
            update_event = Events(
            title=event_info['title'],
            publication_date=publication_date,
            place_id=place_id,
            slug=event_info['slug'],
            description=event_info['description'],
            location=event_info['location']['slug'],
            categories=event_info['categories'],
            tags=event_info['tags'],
            age_restriction=event_info['age_restriction'],
            price=event_info['price'],
            is_free=event_info['is_free'],
            start_date=event_info['dates'][-1]['start_date'],
            start_time=event_info['dates'][-1]['start_time'],
            end_date=event_info['dates'][-1]['end_date'],
            end_time=event_info['dates'][-1]['end_time'],
            is_continuous=event_info['dates'][-1]['is_continuous']
            )
            db.session.add(update_event)
            db.session.commit()
            event_id = update_event.id
            update_image = EventImage(
            event_id=event_id,
            url=event_info['images'][0]['image']
            )
            db.session.add(update_image)
            db.session.commit()
        else:
            print('Event already in DataBase')

update_db()
