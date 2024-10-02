# server/models.py

# server/models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Set up metadata with naming convention
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Specify max length
    hire_date = db.Column(db.Date, nullable=False)

    # Relationship mapping the employee to related reviews
    reviews = db.relationship(
        'Review', back_populates="employee", cascade='all, delete-orphan'
    )

    # Relationship mapping employee to related onboarding
    onboarding = db.relationship(
        'Onboarding', uselist=False, back_populates='employee', cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Employee {self.id}, {self.name}, {self.hire_date}>'


class Onboarding(db.Model):
    __tablename__ = 'onboardings'

    id = db.Column(db.Integer, primary_key=True)
    orientation = db.Column(db.DateTime, nullable=False)
    forms_complete = db.Column(db.Boolean, default=False, nullable=False)

    # Foreign key to store the employee id
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)

    # Relationship mapping onboarding to related employee
    employee = db.relationship('Employee', back_populates='onboarding')

    def __repr__(self):
        return f'<Onboarding {self.id}, {self.orientation}, {self.forms_complete}>'


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    summary = db.Column(db.String(255), nullable=True)  # Set max length

    # Foreign key to store the employee id
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)

    # Relationship mapping the review to related employee
    employee = db.relationship('Employee', back_populates="reviews")

    def __repr__(self):
        return f'<Review {self.id}, {self.year}, {self.summary}>'

# Function to safely retrieve a review by ID
def get_review_by_id(review_id):
    review = Review.query.filter_by(id=review_id).first()  # Attempt to retrieve the review by ID
    if review is None:
        print(f"No review found with ID: {review_id}")
    return review
