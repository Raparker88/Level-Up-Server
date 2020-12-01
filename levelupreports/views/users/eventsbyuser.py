"""Module for generating events by user report"""
import sqlite3
from django.shortcuts import render
from levelupapi.models import Event
from levelupreports.views import Connection


def userevent_list(request):
    """Function to build an HTML report of events by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related user info.
            db_cursor.execute("""
                SELECT 
                    e.id,
                    e.day,
                    e.time,
                    g.title,
                    u.first_name || " " || u.last_name full_name,
                    eg.gamer_id

                    FROM levelupapi_event e
                    JOIN levelupapi_game g ON e.game_id = g.id
                    JOIN levelupapi_eventgamer eg ON eg.event_id = e.id
                    JOIN levelupapi_gamer gr ON eg.gamer_id = gr.id
                    JOIN auth_user u ON u.id = gr.user_id;    
            """)

            dataset = db_cursor.fetchall()

            # Take the flat data from the database, and build the
            # following data structure for each user.
            #
            # {
            #     1: {
            #         "gamer_id": 1,
            #         "full_name": "Molly Ringwald",
            #         "events": [
            #             {
            #                 "id": 5,
            #                 "day": "2020-12-23",
            #                 "time": "19:00",
            #                 "game_name": "Fortress America"
            #             }
            #         ]
            #     }
            # }

            events_by_user = {}

            for row in dataset:
                # Create an Event instance and set its properties
                event = Event()
                event.day = row["day"]
                event.time = row["time"]
                event.game_name = row["title"]
            
                # Store the user's id
                gid = row["gamer_id"]

                # If the gamer's id is already a key in the dictionary...
                if gid in events_by_user:

                    # Add the current game to the `games` list for it
                    events_by_user[gid]['events'].append(event)

                else:
                    # Otherwise, create the key and dictionary value
                    events_by_user[gid] = {}
                    events_by_user[gid]["gamer_id"] = gid
                    events_by_user[gid]["full_name"] = row["full_name"]
                    events_by_user[gid]["events"] = [event]

        # Get only the values from the dictionary and create a list from them
        list_of_users_with_events = events_by_user.values()

        # Specify the Django template and provide data context
        template = 'users/list_with_events.html'
        context = {
            'userevent_list': list_of_users_with_events
        }

        return render(request, template, context)