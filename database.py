import sqlite3

# global connection
conn = None


def get_connection():
    global conn
    if conn is None:
        conn = sqlite3.connect("application.db")
    return conn


def create_database():
    # Connect to a single SQLite database
    conn = get_connection()
    cursor = conn.cursor()

    # Create Feedbacks table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS feedbacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feedback TEXT,
            rate INTEGER
        )
    """
    )

    # Create Bikes table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS bikes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT,
            description TEXT,
            daily_price REAL
        )
    """
    )

    # Create Reservations table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bike_id INTEGER REFERENCES Bikes(id) ON DELETE SET NULL,
            from_date DATE NOT NULL,
            to_date DATE NOT NULL,
            status TEXT CHECK (status IN ('pending', 'confirmed', 'cancelled')) DEFAULT 'pending'
        );
        """
    )

    # Save (commit) the changes
    conn.commit()

def add_feedback(feedback, rate):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO feedbacks (feedback, rate)
            VALUES (?, ?)
        """,
            (feedback, rate),
        )

        conn.commit()
    except sqlite3.Error as e:
        print(f"Database Error: {e}")

def add_bike(model, description, daily_price):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO bikes (model, description, daily_price)
            VALUES (?, ?, ?)
            RETURNING id
        """,
            (model, description, daily_price),
        )
        # Get the id of the newly inserted bike
        bike_id = cursor.fetchone()[0]
        conn.commit()
        return bike_id
    except sqlite3.Error as e:
        print(f"Database Error: {e}")

def add_reservation(bike_id, from_date, to_date):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO reservations (bike_id, from_date, to_date)
            VALUES (?, ?, ?)
            RETURNING id
        """,
            (bike_id, from_date, to_date),
        )
        id = cursor.fetchone()[0]
        conn.commit()
        return id
    except sqlite3.Error as e:
        print(f"Database Error: {e}")

def update_reservation_status(reservation_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            UPDATE reservations
            SET status = ?
            WHERE id = ?
        """,
            (status, reservation_id),
        )

        conn.commit()
    except sqlite3.Error as e:
        print(f"Database Error: {e}")

def close_connection():
    global conn
    if conn:
        conn.close()
        conn = None


def preview_table(table_name):
    conn = sqlite3.connect("application.db")  # Replace with your database name
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")  # Limit to first 5 rows

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()


# Initialize and load database
def initialize_database():
    global conn

    # Initialize the database tables
    create_database()

    # Add some initial bikes
    initial_bikes = [
        ("Mountain Bike", "A sturdy bike for off-road cycling.", 15.99),
        ("City Bike", "A comfortable bike for city rides.", 12.99),
        ("Electric Bike", "An electric bike for easy commuting.", 25.99),
    ]
    bike_ids = []
    for bike in initial_bikes:
        bike_ids.append(add_bike(*bike))

    # Add some initial reservations
    initial_reservations = [
        (bike_ids[0], "2025-01-15", "2025-01-20"),
        (bike_ids[1], "2025-02-10", "2025-02-15"),
        (bike_ids[2], "2025-03-20", "2025-03-25"),
    ]

    for reservation in initial_reservations:
        add_reservation(*reservation)

