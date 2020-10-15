from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class User(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String, nullable=False)
    dob_year = DB.Column(DB.BigInteger, nullable=False)
    hobby = DB.Column(DB.String, nullable=False)
    location = DB.Column(DB.String, nullable=False)

    def __repr__(self):
        return "<User: {} - Born: {} - Hobby: {} - Located: {}>".format(
            self.name, self.dob_year, self.hobby, self.location
            )

class Tweet(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))

    user_id = DB.Column(DB.BigInteger, DB.ForeignKey("user.id"), nullable=False)
    user = DB.relationship("User", backref=DB.backref("tweets", lazy=True))

    def __repr__(self):
        return "<Tweet: {}>".format(
            self.text
        )

def tweet_stat():
    name_1 = User(id=101, name="Papi Lester", dob_year=1994, 
                  hobby="Pool", location="New York")
    DB.session.add(name_1)

    name_2 = User(id=102, name="Chef Lester", dob_year=1994, 
                  hobby="Cooking", location="New York")
    DB.session.add(name_2)

    tweet_uno = Tweet(id=1, text="se va a acabar el mundo", user=name_1)
    tweet_dos = Tweet(id=2, text="manana se bebe", user=name_1)
    tweet_tres = Tweet(id=3, text="dime ave manin", user=name_1)
    tweet_cuatro = Tweet(id=4, text="I played pool two days ago", user=name_2)
    tweet_sinco = Tweet(id=5, text="I got 1 billion dollars in my bank", user=name_2)
    tweet_seis = Tweet(id=6, text="Dam my track team is still MIA", user=name_2)
    
    DB.session.add(tweet_uno)
    DB.session.add(tweet_dos)
    DB.session.add(tweet_tres)
    DB.session.add(tweet_cuatro)
    DB.session.add(tweet_sinco)
    DB.session.add(tweet_seis)

    DB.session.commit()