from logger.models import Sneaker, Collectibles, Media


def fetch_user_sneakers(user_id, session):
    return session.query(Sneaker).filter_by(user_id=user_id).all()


def fetch_user_collectibles(user_id, session):
    return session.query(Collectibles).filter_by(user_id=user_id).all()


def fetch_user_media(user_id, session):
    return session.query(Media).filter_by(user_id=user_id).all()
