from swarm import Agent
import database

def add_feedback(feedback, rate):
    """Add feedback to the database."""
    database.add_feedback(feedback, rate)
    return "Feedback added!"

def get_reservation(reservation_id):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM reservations WHERE id = ?
    """,
        (reservation_id,),
    )
    reservation = cursor.fetchone()
    return reservation

def get_bikes():
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM bikes
    """
    )
    bikes = cursor.fetchall()
    return bikes

def get_available_bikes(from_date, to_date):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM bikes
        WHERE id NOT IN (
            SELECT bike_id FROM reservations
            WHERE from_date < ? AND to_date > ?
            AND status IS NOT 'cancelled'
        )
    """,
        (to_date, from_date),
    )
    bikes = cursor.fetchall()
    return bikes

def reserve_bike(bike_id, from_date, to_date):
    id = database.add_reservation(bike_id, from_date, to_date)
    return f"Reservation added with id: {id}"

def update_reservation(reservation_id, bike_id=None, from_date=None, to_date=None, status=None):
    """Update a reservation in the database."""
    conn = database.get_connection()
    cursor = conn.cursor()
    update_values = {}
    if bike_id:
        update_values["bike_id"] = bike_id
    if from_date:
        update_values["from_date"] = from_date
    if to_date:
        update_values["to_date"] = to_date
    if status:
        update_values["status"] = status
    update_values_keys = ", ".join([f"{key} = ?" for key in update_values.keys()])
    cursor.execute(
        f"""
        UPDATE reservations
        SET {update_values_keys}
        WHERE id = ?
    """,
        (*update_values.values(), reservation_id),
    )
    conn.commit()
    return "Reservation updated!"

triage_agent = Agent(
    name="Triage Agent",
    instructions=f"""You are to triage a users request, and call a tool to transfer to the right intent.
    Once you are ready to transfer to the right intent, call the tool to transfer to the right intent.
    You dont need to know specifics, just the topic of the request.
    If the user request is about making a feedback, transfer to the User Feedback Agent.
    If the user request is about making, updating or cancelling a reservation, transfer to the Reservation Agent.
    If the user request is about getting information about bikes, prices, or available bikes, transfer to the Welcome Agent.
    When you need more information to triage the request to an agent, ask a direct question without explaining why you're asking it.
    Do not share your thought process with the user! Do not make unreasonable assumptions on behalf of user.""",
)
welcome_agent = Agent(
    name="Welcome Agent",
    instructions="Provide information about prices, bikes models, available bikes.",
    functions=[get_bikes, get_available_bikes],
)
reservation_agent = Agent(
    name="Reservation Agent",
    instructions="Handle reservation status, modification, and cancellation requests. When a user wants to cancel a reservation, you should set the reservation status to 'cancelled'.",
    functions=[get_reservation, reserve_bike, update_reservation],
)
user_feedback_agent = Agent(
    name='User Feedback Agent',
    instructions="Handle user feedback. Ask users if they want to provide a rating from 1 to 5 with and/or a feedback.",
    functions=[add_feedback],
)

def transfer_back_to_triage():
    """Call this function if a user is asking about a topic that is not handled by the current agent."""
    return triage_agent

def transfer_to_welcome():
    return welcome_agent

def transfer_to_user_feedback():
    return user_feedback_agent

def transfer_to_reservation():
    return reservation_agent

triage_agent.functions = [transfer_to_welcome, transfer_to_user_feedback, transfer_to_reservation]
welcome_agent.functions.append(transfer_back_to_triage)
user_feedback_agent.functions.append(transfer_back_to_triage)
reservation_agent.functions.append(transfer_back_to_triage)
