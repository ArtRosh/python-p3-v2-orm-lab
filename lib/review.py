from __init__ import CURSOR, CONN
from department import Department
from employee import Employee


class Review:

    # Dictionary for mapping a table row to a persisted class instance.
    all = {}

    def __init__(self, year, summary, employee_id, id=None):
        self.id = id
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    def __repr__(self):
        return (
            f"<Review {self.id}: {self.year}, {self.summary}, "
            + f"Employee: {self.employee_id}>"
        )

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, year):
        if isinstance(year, int) and year >= 2000:
            self._year = year
        else:
            raise ValueError(
                "year must be an integer >= 2000"
            )

    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, summary):
        if isinstance(summary, str) and len(summary) > 0:
            self._summary = summary
        else:
            raise ValueError(
                "summary must be a non-empty string"
            )

    @property
    def employee_id(self):
        return self._employee_id

    @employee_id.setter
    def employee_id(self, employee_id):
        if Employee.find_by_id(employee_id):
            self._employee_id = employee_id
        else:
            raise ValueError(
                "employee_id must reference an employee in the database")

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            year INT,
            summary TEXT,
            employee_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employee(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Review class instances """
        sql = """
            DROP TABLE IF EXISTS reviews;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the year, summary, and employee id values of the current Review object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        pass

    @classmethod
    def create(cls, year, summary, employee_id):
        """ Initialize a new Review object and save the object to the database """
        pass

    def update(self):
        """Update the table row corresponding to the current Review object."""
        pass

    def delete(self):
        """Delete the row corresponding to the current Review object"""
        pass

    @classmethod
    def instance_from_db(cls, row):
        """Return an Review object having the attribute values from the table row."""
        pass

    @classmethod
    def get_all(cls):
        """Return a list containing one Review object per table row"""
        pass

    @classmethod
    def find_by_id(cls, id):
        """Return Review object corresponding to the table row matching the specified primary key"""
        pass
