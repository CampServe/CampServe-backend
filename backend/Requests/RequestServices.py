from flask import jsonify, Blueprint, request
from flask_socketio import SocketIO, emit, join_room
from flask_cors import CORS
from Requests.RequestsModel import Requests
from Providers.ProviderModel import Providers
from Users.UserModel import User
from Requests.RequestsModel import Requests

request_services_route = Blueprint("request_services_route", __name__)
CORS(request_services_route)




@request_services_route.route('/book_services', methods=['POST'])
def book_services():
    from app import session
    from app import socketio


    data = request.get_json()

    provider_id = data['provider_id']
    user_id = data['user_id']
    location = data['location']
    payment_mode = data['paymentMode']
    agreed_price = data['price']
    scheduled_datetime = data['scheduledDateTime']
    subcategory = data['subcategory']

    try:
        new_request = Requests(
            provider_id=provider_id,
            user_id=user_id,
            location=location,
            payment_mode=payment_mode,
            agreed_price=agreed_price,
            scheduled_datetime=scheduled_datetime,
            subcategory=subcategory,
            status_comp_inco="no action",
            status_acc_dec="no action"
        )

        # Add the new_request to the session and commit to the database
        session.add(new_request)
        session.commit()

         # Emit an event to notify the provider of the new request
        provider_id = provider_id  # Replace with the actual provider ID
        room = f'provider_{provider_id}'
        socketio.emit('new_request', room=room, namespace='/requests')
        

        return jsonify({'message': 'Request added successfully'})

    except Exception as e:
        return jsonify({'error': str(e)})



@request_services_route.route('/get_service_status', methods=['POST'])
def get_service_status():
    from app import session
    data = request.get_json()
    user_id = data['user_id']
    subcategory = data['subcategory']
    provider_id = data['provider_id']

    recent_booking = session.query(Requests).filter(
        Requests.user_id == user_id,
        Requests.subcategory == subcategory,
        Requests.provider_id == provider_id,
    ).order_by(Requests.request_id.desc()).first()

    if recent_booking:
        status_acc_dec = recent_booking.status_acc_dec
        status_comp_inco = recent_booking.status_comp_inco

        if status_acc_dec == "no action":
            return jsonify({'status': 'request pending'})
        elif status_acc_dec == "declined":
            return jsonify({'status': 'request declined'})
        elif status_acc_dec == "accepted" and status_comp_inco == "complete":
            return jsonify({'status': 'request complete'})
        elif status_acc_dec == "accepted" and status_comp_inco == "incomplete":
            return jsonify({'status': 'request in progress'})
        else:
            return jsonify({'status': 'service not booked'})
    else:
        return jsonify({'status': 'service not booked'})



# for shwoing the requests for a particular user when they log in to their account
@request_services_route.route('/get_all_user_requests', methods=['POST'])
def get_all_user_requests():
    from app import session

    data = request.get_json()
    user_id = data['user_id']

    try:
        user_request = session.query(Requests,Providers).join(
           Providers, Requests.provider_id == Providers.provider_id).filter(
                Requests.user_id == user_id).all()

        if not user_request:
            return jsonify({'message': 'No requests found.'})
        
        all_requests = []
        for requestt,provider in user_request:
            all_requests.append({
                'request_id': requestt.request_id,
                'agreed_price': requestt.agreed_price,
                'location': requestt.location,
                'payment_mode': requestt.payment_mode,
                'datetime': requestt.scheduled_datetime,
                'status_acc_dec': requestt.status_acc_dec,
                'status_comp_inco': requestt.status_comp_inco,
                'subcategory': requestt.subcategory,
                'business_name': provider.business_name
            })    

        return jsonify({
            'all_requests': all_requests
        })

    except Exception as e:
        return jsonify({'error': str(e)})


# for shwoing the requests for a provider user when they log in to their account
@request_services_route.route('/get_all_provider_requests', methods=['POST'])
def get_all_provider_requests():
    from app import session
    from app import socketio


    data = request.get_json()
    provider_id = data['provider_id']

    try:
        provider_requests = session.query(Requests).filter_by(provider_id=provider_id).all()

        if not provider_requests:
            return jsonify({'message': 'No requests found.'})

        # Emit an event to the provider's room to establish a connection
        socketio.emit('join_room', room=provider_id, namespace='/')
   
        #i want to include a count for all their requests tht shows on the ui
        all_requests = []
        for req in provider_requests:
            user_id = req.user_id

            # Query the users table to obtain the first and last name of the user
            user = session.query(User).filter_by(user_id=user_id).first()

            request_data = {
                'request_id': req.request_id,
                'agreed_price': req.agreed_price,
                'location': req.location,
                'payment_mode': req.payment_mode,
                'datetime': req.scheduled_datetime,
                'status_acc_dec': req.status_acc_dec,
                'status_comp_inco': req.status_comp_inco,
                'subcategory': req.subcategory,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
            all_requests.append(request_data)

        return jsonify({'all_requests': all_requests})

    except Exception as e:
        return jsonify({'error': str(e)})

#for all buttons associated with canceling,accepting, declining and completing a request.
@request_services_route.route('/change_request_status', methods=['POST'])
def change_request_status():
    from app import session
    from app import socketio
    
    data = request.get_json()
    action_type = data['action_type']
    request_id = data['request_id']

    req = session.query(Requests).filter_by(request_id=request_id).first()


    try:
        if action_type == 'accept':
            req.status_acc_dec = 'accepted'
            req.status_comp_inco = 'incomplete'

        elif action_type == 'decline':
            req.status_acc_dec = 'declined'

        elif action_type == 'cancel':
            # Delete the request with the provided request_id
            session.query(Requests).filter_by(request_id=request_id).delete()

        elif action_type == 'mark_complete':
            # Update the request with the provided request_id
            req.status_comp_inco = 'complete'

        session.commit()

        # socketio.emit('request_status_updated', room='relevant_room', namespace='/requests')

        return jsonify({'message': 'Request status updated successfully.'})
        
    except Exception:
        return jsonify({'error': 'An error occurred while updating the request status.'})
    finally:
        session.close()

