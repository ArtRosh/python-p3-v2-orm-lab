# lib/department.py
from __init__ import CURSOR, CONN


class Department:
    """
    ORM mapping for the departments table.
    """

    # Cache of objects persisted to the DB: {id: Department(...)}
    all = {}

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name        # validated by @property
        self.location = location  # validated by @property

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"

    # -------- properties (validation) --------
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError("Name must be a non-empty string")

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        if isinstance(location, str) and len(location):
            self._location = location
        else:
            raise ValueError("Location must be a non-empty string")

    # -------- schema management --------
    @classmethod
    def create_table(cls):
        """Create the departments table if it doesn't exist."""
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY,
                name TEXT,
                location TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drop the departments table."""
        sql = "DROP TABLE IF EXISTS departments;"
        CURSOR.execute(sql)
        CONN.commit()

    # -------- persistence (CRUD) --------
    def save(self):
        """
        Insert a new row for this Department (name, location).
        Set self.id from the new row's primary key and cache the object.
        """
        sql = "INSERT INTO departments (name, location) VALUES (?, ?)"
        CURSOR.execute(sql, (self.name, self.location))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, location):
        """Initialize, save, and return a new Department."""
        dept = cls(name, location)
        dept.save()
        return dept

    def update(self):
        """Update this Department's row in the DB."""
        sql = """
            UPDATE departments
            SET name = ?, location = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    def delete(self):
        """
        Delete this Department's row, remove from cache, and clear id.
        """
        sql = "DELETE FROM departments WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        del type(self).all[self.id]
        self.id = None

    # -------- retrieval helpers --------
    @classmethod
    def instance_from_db(cls, row):
        """
        Return a Department object for a given table row tuple: (id, name, location).
        Reuse the cached instance if present; otherwise create and cache it.
        """
        if not row:
            return None

        dept = cls.all.get(row[0])
        if dept:
            dept.name = row[1]
            dept.location = row[2]
        else:
            dept = cls(row[1], row[2], id=row[0])
            cls.all[dept.id] = dept
        return dept

    @classmethod
    def get_all(cls):
        """Return a list of all Department objects in the table."""
        rows = CURSOR.execute("SELECT * FROM departments").fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Return the Department with the given primary key (or None)."""
        row = CURSOR.execute(
            "SELECT * FROM departments WHERE id = ?",
            (id,)
        ).fetchone()
        return cls.instance_from_db(row)

    @classmethod
    def find_by_name(cls, name):
        """Return the first Department whose name matches (or None)."""
        row = CURSOR.execute(
            "SELECT * FROM departments WHERE name = ?",
            (name,)
        ).fetchone()
        return cls.instance_from_db(row)

    # -------- relationship (one-to-many) --------
    def employees(self):
        """
        Return a list of Employee objects that reference this department via department_id.
        Import inside method to avoid circular imports.
        """
        from employee import Employee
        CURSOR.execute(
            "SELECT * FROM employees WHERE department_id = ?",
            (self.id,)
        )
        rows = CURSOR.fetchall()
        return [Employee.instance_from_db(row) for row in rows]