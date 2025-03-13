from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Text
from sqlalchemy import SmallInteger
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


# 创建对象的基类:
Base = declarative_base()


# 多对多的关系表定义
ArtworkTag = Table(
    'illust_tag', Base.metadata,
    Column('tagid', Integer, ForeignKey("tag.tagid"), primary_key=True, nullable=False),
    Column('illustid', Integer, ForeignKey("illust.illustid"), primary_key=True, nullable=False)
)

ArtworkPixivision = Table(
    'illust_pixivision', Base.metadata,
    Column('aid', Integer, ForeignKey("pixivision.aid"), primary_key=True, nullable=False),
    Column('illustid', Integer, ForeignKey("illust.illustid"), primary_key=True, nullable=False)
)


class User(Base):
    __tablename__ = 'user'

    def __repr__(self):
        return f'User(userid={self.user_id}, username="{self.user_name}")'

    user_id = Column("userid", Integer, primary_key=True, nullable=False)
    user_name = Column("username", String(64), nullable=False)

    sql_create_time = Column(TIMESTAMP, nullable=False, default=func.current_timestamp())
    sql_update_time = Column(TIMESTAMP, nullable=False, default=func.current_timestamp(),
                             onupdate=func.current_timestamp())

    artworks = relationship('Artwork', viewonly=True)


class Tag(Base):
    __tablename__ = 'tag'

    def __repr__(self):
        return f'Tag(id={self.tag_id}, name="{self.name}", trans_name="{self.trans_name}")'

    tag_id = Column("tagid", Integer, primary_key=True, autoincrement=True)
    name = Column("tagname", String(128), nullable=False, index=True)
    trans_name = Column("tagtransname", String(128))

    sql_create_time = Column(TIMESTAMP, nullable=False, default=func.current_timestamp())
    sql_update_time = Column(TIMESTAMP, nullable=False, default=func.current_timestamp(),
                             onupdate=func.current_timestamp())

    artworks = relationship('Artwork', secondary=ArtworkTag, viewonly=True)


class Pixivision(Base):
    __tablename__ = 'pixivision'

    def __repr__(self):
        return f'Pixivision(' \
               f'aid={self.aid}, title="{self.title}", type="{self.type}", ' \
               f'description="{self.description[:10]}...")'

    aid = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(128), nullable=False)
    type = Column(String(16), nullable=False)
    description = Column(String(1024), nullable=False, default="")

    sql_create_time = Column(TIMESTAMP, nullable=False, default=func.current_timestamp())
    sql_update_time = Column(TIMESTAMP, nullable=False, default=func.current_timestamp(),
                             onupdate=func.current_timestamp())

    artworks = relationship('Artwork', secondary=ArtworkPixivision, viewonly=True)


class Artwork(Base):
    __tablename__ = 'illust'

    def __repr__(self):
        return str({
            'artwork_id': self.artwork_id,
            'user': self.user
        })

    artwork_id = Column("illustid", Integer, primary_key=True, nullable=False)
    user_id = Column("userid", Integer, ForeignKey("user.userid"), nullable=False, index=True)

    artwork_type = Column("illust_type", SmallInteger, nullable=False, index=True)
    title = Column(String(40), nullable=False)
    nums = Column(SmallInteger, nullable=False, index=True)
    restrict = Column(SmallInteger, nullable=False, index=True)
    description = Column(Text)

    bookmark_cnt = Column(Integer, nullable=False, index=True)
    like_cnt = Column(Integer, nullable=False, index=True)
    comment_cnt = Column(Integer, nullable=False, index=True)
    view_cnt = Column(Integer, nullable=False, index=True)

    create_time = Column(TIMESTAMP, nullable=False)
    upload_time = Column(TIMESTAMP, nullable=False)

    sql_create_time = Column(TIMESTAMP, nullable=False, default=func.current_timestamp())
    sql_update_time = Column(TIMESTAMP, nullable=False, default=func.current_timestamp(),
                             onupdate=func.current_timestamp())

    user = relationship("User")
    tags = relationship('Tag', secondary=ArtworkTag)
    images = relationship('Image', back_populates='artwork', cascade="all, delete-orphan")
    pixivisions = relationship('Pixivision', secondary=ArtworkPixivision)


class Image(Base):
    __tablename__ = 'image'

    image_id = Column("imageid", Integer, primary_key=True, autoincrement=True)
    artwork_id = Column("illustid", Integer, ForeignKey("illust.illustid"), nullable=False)

    idx = Column("idx", SmallInteger, nullable=True)

    height = Column("height", Integer, nullable=False)
    width = Column("width", Integer, nullable=False)
    file_size = Column("filesize", Integer, nullable=False)

    sql_create_time = Column(TIMESTAMP, nullable=False, default=func.current_timestamp())
    sql_update_time = Column(TIMESTAMP, nullable=False, default=func.current_timestamp(),
                             onupdate=func.current_timestamp())

    artwork = relationship('Artwork', back_populates='images')

    def __repr__(self):
        return f'Image(id={self.image_id}, artwork_id={self.artwork_id}), idx={self.idx}'


def new_session(session_url: str):
    sql_engine = create_engine(session_url)
    Base.metadata.create_all(sql_engine)
    return sessionmaker(sql_engine)
